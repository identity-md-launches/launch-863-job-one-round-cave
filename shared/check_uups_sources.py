"""Offline composition checks: no network and no source extraction."""
from uups_sources import inspect


def check():
    original, implementation, empty = ['0x' + c * 40 for c in '123']
    calls = []
    evidence = {'address': original, 'block_number': 16, 'block_hash': '0x' + 'ab' * 32,
                'candidates': [{'address': implementation, 'code_bytes': 2},
                               {'address': implementation.upper().replace('0X', '0x'), 'code_bytes': 2},
                               {'address': empty, 'code_bytes': 0}]}
    def scan(endpoint, address):
        assert (endpoint, address) == ('fixture', original)
        return evidence
    def fetch(address):
        calls.append(address)
        if address == implementation:
            raise OSError('source unavailable')
        return {'status': 'source_available', 'sources': {'../untrusted.sol': 'data only'}}
    result = inspect('fixture', original, scan=scan, fetch=fetch)
    assert calls == [original, implementation], calls
    assert result['uups'] is evidence
    assert result['source_reviews'][0]['bundle']['sources']['../untrusted.sol'] == 'data only'
    assert result['source_reviews'][1]['lookup'] == 'failed'
    assert result['sent'] is False
    calls.clear()
    def failed_scan(*args):
        raise ValueError('block changed')
    try:
        inspect('fixture', original, scan=failed_scan, fetch=fetch)
    except ValueError:
        pass
    else:
        raise AssertionError('scan failure hidden')
    assert not calls
    result = inspect('fixture', original,
                     scan=lambda *a: dict(evidence, candidates=[]), fetch=fetch)
    assert calls == [original] and len(result['source_reviews']) == 1
    print('PASS: candidate deduplication, empty-code exclusion, preserved evidence, '
          'source failure isolation, no extraction, failed scan stops lookup, absent slots')


if __name__ == '__main__':
    check()
