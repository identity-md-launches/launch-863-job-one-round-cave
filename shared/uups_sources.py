"""Attach public source-review leads to block-pinned UUPS observations."""
import argparse
import json
from tools import uups_probe, source_check


def inspect(endpoint, address, scan=None, fetch=None):
    scan = scan or uups_probe.inspect
    fetch = fetch or source_check.fetch
    observation = scan(endpoint, address)
    # The original contract's source can describe routing; implementations'
    # sources can explain UUID responses. Neither is an authorization proof.
    addresses = [observation['address']]
    addresses += [item['address'] for item in observation['candidates']
                  if item['code_bytes'] > 0]
    sources = []
    for target in dict.fromkeys(a.lower() for a in addresses):
        try:
            bundle = fetch(target)
            sources.append({'address': target, 'lookup': 'completed', 'bundle': bundle})
        except (ValueError, OSError) as exc:
            sources.append({'address': target, 'lookup': 'failed', 'error': str(exc)[:500]})
    return {'uups': observation, 'source_reviews': sources, 'sent': False,
            'limitations': 'Source responses are current provider reports, not pinned to the '
            'UUPS block and not independently compiled. A UUID match is an untrusted '
            'compatibility claim. Empty slots, absent source, and lookup failures do not '
            'prove immutability or safety. No source files are extracted or executed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--address', default=uups_probe.route.ZTO)
    parser.add_argument('--rpc', default='https://ethereum-rpc.publicnode.com')
    args = parser.parse_args()
    from urllib.parse import urlsplit
    url = urlsplit(args.rpc)
    if (url.scheme != 'https' or not url.hostname or url.username is not None
            or url.password is not None or url.query or url.fragment):
        parser.error('require a public HTTPS RPC without credentials, query or fragment')
    try:
        result = inspect(args.rpc, args.address)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'scan_failed', 'error': str(exc), 'sent': False}))
        return 1
    print(json.dumps(result, indent=2))
    return 1 if any(s['lookup'] == 'failed' for s in result['source_reviews']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
