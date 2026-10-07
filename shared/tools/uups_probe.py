#!/usr/bin/env python3
"""Read-only UUPS UUID reconnaissance; Python standard library only."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

# Read only this submitted sibling module; it supplies bounded, direct RPC.
from . import proxy_route as route
UUID_SELECTOR = '0x52d1902d'
LEGACY_SLOT = '0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7'
IMPLEMENTATION_SLOT = route.SLOTS['implementation']
CALLER = '0x0000000000000000000000000000000000000001'
LIMITATIONS = ('A UUID response is an untrusted compatibility claim, not proof of dispatch, '
               'upgrade authorization, storage-layout safety or future upgradeability. '
               'A revert, empty slot or different UUID does not prove immutability. '
               'Custom routers, beacon targets and clone chains are not resolved. '
               'Calls run directly on candidate implementations, not through the proxy. '
               'Provider honesty and block-hash recheck races remain.')


def classify_uuid(value, expected):
    raw = route.hex_bytes(value)
    if len(raw) != 32:
        return {'status': 'malformed_return', 'raw': value,
                'reason': 'Expected exactly one ABI bytes32 word'}
    normalized = '0x' + raw.hex()
    return {'status': 'matching_uuid' if normalized == expected else 'different_uuid',
            'raw': value, 'uuid': normalized, 'expected_uuid': expected}


def inspect(endpoint, address, rpc=None):
    read = rpc or (lambda method, params: route.rpc(endpoint, method, params))
    if not re.fullmatch(r'0x[0-9a-fA-F]{40}', address):
        raise ValueError('address must be 20-byte hexadecimal')
    address = address.lower()
    if read('eth_chainId', []) != '0x1':
        raise ValueError('Expected Ethereum mainnet chainId 1')
    block, block_hash = route.block_ref(read('eth_getBlockByNumber', ['latest', False]))
    code = route.hex_bytes(read('eth_getCode', [address, block]))
    candidates, slots = [], {}
    for kind, slot in [('eip1967', IMPLEMENTATION_SLOT), ('erc1822_original', LEGACY_SLOT)]:
        word = read('eth_getStorageAt', [address, slot, block])
        target = route.slot_address(word)
        slots[kind] = word
        if target is None:
            continue
        target_code = route.hex_bytes(read('eth_getCode', [target, block]))
        item = {'slot_kind': kind, 'address': target, 'code_bytes': len(target_code)}
        if not target_code:
            item['probe'] = {'status': 'empty_target_code'}
        else:
            # Read-only simulation, bounded gas, fixed simulation caller, no value.
            try:
                value = read('eth_call', [{'to': target, 'from': CALLER,
                              'data': UUID_SELECTOR, 'gas': '0x186a0'}, block])
            except (ValueError, OSError) as exc:
                item['probe'] = {'status': 'unresolved_call', 'error': str(exc)[:500]}
            else:
                # Malformed transport data is fatal; ABI shape is an observation.
                item['probe'] = classify_uuid(value, slot)
        candidates.append(item)
    end_block, end_hash = route.block_ref(read('eth_getBlockByNumber', [block, False]))
    if (end_block, end_hash) != (block, block_hash):
        raise ValueError('Block changed during read; retry')
    return {'chain_id': 1, 'address': address, 'block_number': int(block, 16),
            'block_hash': block_hash, 'code_bytes': len(code), 'raw_slots': slots,
            'candidates': candidates,
            'assessment': ('implementation candidates probed' if candidates else
                           'no implementation in either recognized slot; no UUID call made'),
            'limitations': LIMITATIONS}


def self_test():
    target = '0x' + '22' * 20
    zero = '0x' + '00' * 32
    word = '0x' + '00' * 12 + target[2:]
    good_hash = '0x' + 'ab' * 32
    calls = []

    def run(slot=IMPLEMENTATION_SLOT, value=IMPLEMENTATION_SLOT, code='0x6000',
            reorg=False, error=False, populated=True):
        calls.clear()
        def fake(method, params):
            calls.append((method, params))
            if method == 'eth_chainId':
                return '0x1'
            if method == 'eth_getBlockByNumber':
                return {'number': '0x10', 'hash': ('0x' + 'cd' * 32)
                        if reorg and params[0] != 'latest' else good_hash}
            assert params[-1] == '0x10', 'Read was not pinned'
            if method == 'eth_getStorageAt':
                assert params[0] == route.ZTO, 'Wrong storage context'
                return word if populated and params[1] == slot else zero
            if method == 'eth_getCode':
                return code if params[0] == target else '0x6000'
            if method == 'eth_call':
                assert params[0] == {'to': target, 'from': CALLER,
                                    'data': UUID_SELECTOR, 'gas': '0x186a0'}
                if error:
                    raise ValueError('execution reverted')
                return value
            raise AssertionError('Unexpected method ' + method)
        return inspect('', route.ZTO, fake)

    assert run()['candidates'][0]['probe']['status'] == 'matching_uuid'
    assert run(LEGACY_SLOT, LEGACY_SLOT)['candidates'][0]['probe']['status'] == 'matching_uuid'
    assert run(value=LEGACY_SLOT)['candidates'][0]['probe']['status'] == 'different_uuid'
    for value in ['0x', '0x01', IMPLEMENTATION_SLOT + '00']:
        assert run(value=value)['candidates'][0]['probe']['status'] == 'malformed_return'
    assert run(error=True)['candidates'][0]['probe']['status'] == 'unresolved_call'
    assert run(code='0x')['candidates'][0]['probe']['status'] == 'empty_target_code'
    assert not any(m == 'eth_call' for m, _ in calls)
    assert not run(populated=False)['candidates']
    assert not any(m == 'eth_call' for m, _ in calls)
    for kwargs in [{'reorg': True}, {'value': '0xzz'}]:
        try:
            run(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid evidence accepted')
    print('PASS: modern/legacy UUID, mismatch, malformed ABI, failed call, empty target, '
          'absent slots, direct bounded pinned calls, reorg and invalid hex rejection')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--address', default=route.ZTO)
    parser.add_argument('--rpc', default='https://ethereum-rpc.publicnode.com')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.rpc.startswith('https://'):
        parser.error('RPC endpoint must use HTTPS')
    try:
        print(json.dumps(inspect(args.rpc, args.address), indent=2))
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print('uups-probe: ' + str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
