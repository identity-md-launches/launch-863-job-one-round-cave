"""Observe Ethereum RPC head movement over a bounded sampling window."""
import argparse
import importlib.util
import json
from pathlib import Path

from . import rpc_sampling as sampling


def summarize(observations):
    """Analyze ordered health samples; gaps do not count as consecutive repeats."""
    events, seen = [], {}
    previous = None
    valid = errors = stale = advances = repeats = 0
    longest_run = run = 0
    for index, item in enumerate(observations, 1):
        if item['status'] == 'error':
            errors += 1
            previous = None
            run = 0
            continue
        if item['status'] not in ('fresh', 'stale'):
            raise ValueError('unknown health status')
        height, block_hash = item['block_number'], item['block_hash'].lower()
        if type(height) is not int or height < 0:
            raise ValueError('invalid block height')
        if len(block_hash) != 66 or not block_hash.startswith('0x') or any(
                c not in '0123456789abcdef' for c in block_hash[2:]):
            raise ValueError('invalid block hash')
        valid += 1
        stale += item['status'] == 'stale'
        if height in seen and seen[height] != block_hash:
            events.append({'sample': index, 'kind': 'hash_changed', 'height': height,
                           'earlier_hash': seen[height], 'observed_hash': block_hash})
        seen[height] = block_hash
        if previous is not None:
            old_height, old_hash = previous
            if height < old_height:
                events.append({'sample': index, 'kind': 'height_regressed',
                               'from_height': old_height, 'to_height': height})
            elif height > old_height:
                advances += 1
            if (height, block_hash) == previous:
                repeats += 1
                run += 1
            else:
                run = 1
        else:
            run = 1
        longest_run = max(longest_run, run)
        previous = height, block_hash
    status = ('anomalies_observed' if events else 'inconclusive' if errors or stale or valid < 2
              else 'advance_observed' if advances else 'no_advance_observed')
    return {'status': status, 'valid_samples': valid, 'error_samples': errors,
            'stale_samples': stale, 'advancing_transitions': advances,
            'identical_consecutive_transitions': repeats,
            'longest_identical_run_samples': longest_run, 'events': events}


def demo():
    def row(n, h='ab', status='fresh'):
        return {'status': status, 'block_number': n, 'block_hash': '0x' + h * 32}
    a, b = row(10), row(11, 'cd')
    checks = 0
    cases = [([], 'inconclusive'), ([a], 'inconclusive'),
             ([a, a], 'no_advance_observed'), ([a, b], 'advance_observed'),
             ([b, a], 'anomalies_observed'), ([a, row(10, 'cd')], 'anomalies_observed'),
             ([a, {'status': 'error'}, b], 'inconclusive'),
             ([a, row(11, status='stale')], 'inconclusive')]
    for rows, expected in cases:
        assert summarize(rows)['status'] == expected
        checks += 1
    result = summarize([a, a, {'status': 'error'}, a, a, a])
    assert result['longest_identical_run_samples'] == 3
    assert result['identical_consecutive_transitions'] == 3
    assert summarize([a, row(10, 'AB')])['events'] == []
    result = summarize([a, b, row(10, 'ef')])
    assert {e['kind'] for e in result['events']} == {'hash_changed', 'height_regressed'}
    assert summarize([a, {'status': 'error'}, row(10, 'ef')])['events'][0]['kind'] == 'hash_changed'
    counts = {}
    def probe(endpoint, *args):
        counts[endpoint] = counts.get(endpoint, 0) + 1
        return {**row(counts[endpoint]), 'latency_ms': 1}
    sampled = sampling.sample(['fixture'], rounds=3, interval=0, probe=probe)
    assert summarize(sampled['reports'][0]['observations'])['advancing_transitions'] == 2
    print(json.dumps({'demo': 'passed', 'checks': checks + 5,
                      'covers': 'repeats, progress, regressions, hash changes, gaps, stale data, case normalization, sampler integration'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--endpoint', action='append')
    parser.add_argument('--rounds', type=int, default=3)
    parser.add_argument('--interval', type=float, default=13)
    parser.add_argument('--timeout', type=float, default=12)
    parser.add_argument('--max-age', type=float, default=120)
    args = parser.parse_args()
    if args.demo:
        demo()
        return 0
    endpoints = args.endpoint or sampling.health.DEFAULTS
    if any(not e.startswith('https://') for e in endpoints):
        parser.error('require public HTTPS endpoints without credentials')
    # Explicitly reject credential-bearing URLs before transport.
    from urllib.parse import urlsplit
    if any(urlsplit(e).username is not None or urlsplit(e).password is not None
           or urlsplit(e).query or urlsplit(e).fragment for e in endpoints):
        parser.error('credentials, query strings and fragments are not supported')
    try:
        result = sampling.sample(endpoints, args.rounds, args.interval, args.timeout, args.max_age)
    except ValueError as exc:
        parser.error(str(exc))
    for report in result['reports']:
        report['progress'] = summarize(report['observations'])
    result['status'] = ('advance_observed' if all(
        r['progress']['status'] == 'advance_observed' for r in result['reports'])
        else 'review_observations')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'advance_observed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
