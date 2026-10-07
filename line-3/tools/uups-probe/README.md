# UUPS Probe

Read-only reconnaissance for workers deciding whether a deployed Ethereum interface may point at replaceable code. Looks in the EIP-1967 and original ERC-1822 implementation slots, checks target code, then calls `proxiableUUID()` directly on each nonempty candidate with a fixed caller and 100,000 gas. Compares the exact bytes32 return to the slot used to discover that candidate. Each response is an untrusted compatibility claim, never proof of upgrade authority or safety.

Python standard library only. Keep the sibling `proxy-route` folder with this tool: its submitted module supplies bounded direct JSON-RPC, address parsing and block validation. No packages, keys or configuration needed. One network-free command from the repository root:

```sh
python3 -B line-3/tools/uups-probe/uups_probe.py --self-test
```

For a read-only mainnet ZTO scan:

```sh
python3 -B line-3/tools/uups-probe/uups_probe.py
```

Choose another contract with `--address 0x...`, or the alternative endpoint with `--rpc https://eth.drpc.org`. All storage, code and simulated calls use the same block number, followed by a block-hash recheck. HTTP uses the sibling reader's dedicated User-Agent, 30-second timeout, 1 MiB response cap and disabled environment proxy discovery. No wallet, environment variable, credential, signing or transaction-submission access.

## What happened when tried

Offline checks passed for modern and original UUID matches, a different UUID, empty/short/oversized ABI returns, failed calls, empty target code, absent slots, malformed hex and a changed ending block hash. Mock RPC assertions enforce the original storage context, direct implementation calls, fixed gas/caller and block pinning. No-slot and empty-target cases make no calls.

Live PublicNode scan on 2026-10-07: ZTO at block **26137121**, hash `0x2680196439b836b6ac2fb0aad73d9e6bc9e27c88bdcce2a1c32c732931ee0bbf`, had 1287 code bytes and zero values in both recognized implementation slots. The ending hash matched. No UUID call was made. A live positive UUPS implementation was not exercised; positive cases are synthetic tests.

## Interpretation and limits

`matching_uuid` records the expected bytes32 response; `different_uuid` records another valid word. `malformed_return` reports incorrect ABI length. `unresolved_call` covers revert, network or RPC errors without treating them as evidence against upgradeability. `empty_target_code` prevents an empty account from becoming a claimed implementation. Malformed storage, malformed hex, failed essential reads and detected reorganizations stop the scan.

The original [ERC-1822 example](https://eips.ethereum.org/EIPS/eip-1822) uses the PROXIABLE slot. [OpenZeppelin UUPSUpgradeable](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/utils/UUPSUpgradeable.sol) uses the EIP-1967 implementation slot and rejects delegated UUID calls, which is why this tool probes a candidate directly. It does not try an upgrade or test an upgrade permission.

A contract may spoof the getter, ignore a populated slot, require a different caller, or exceed the gas cap. Beacon implementations, custom routers, diamonds and clone chains are not resolved here. Empty slots, reverts and mismatches do not prove immutability. Matching UUIDs do not establish storage-layout compatibility, dispatch, authorization, or future behavior. Provider honesty and block-hash recheck races remain.
