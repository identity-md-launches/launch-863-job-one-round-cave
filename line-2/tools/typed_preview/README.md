# Typed call preview

`typed_preview.py` accepts a canonical Solidity function signature and typed argument values, constructs ABI calldata, previews the unsigned call with `eth_call`, and decodes declared return values. It supports `address`, `bool`, explicitly sized integers (`int8`–`int256` and `uint8`–`uint256` in multiples of eight), `bytes1`–`bytes32`, `bytes`, and `string`. Unsized `int` and `uint` aliases are rejected: use `int256` and `uint256`. A revert is named using the existing error catalog when its selector is known. It uses only Python's standard library, sends no transaction, and reads no keys or environment variables.

From the repository root, run this live ZTO balance preview:

```sh
python3 -B line-2/tools/typed_preview/typed_preview.py --demo
```

For a custom call, pass `--to 0x... --signature 'balanceOf(address)' --arg 0x... --returns uint256`. Repeat `--arg` in signature order. `--from`, `--value-wei`, `--gas`, `--block`, and `--rpc` use the same conventions as call preview. For dynamic `bytes`, supply even-length `0x` hex; for `bool`, use `true`, `false`, `1`, or `0`. Integers accept decimal or `0x` hex. The signature must contain canonical ABI types without names or spaces.

Tried against `https://ethereum-rpc.publicnode.com`: the `--demo` ZTO `balanceOf(0x...01)` call succeeded and decoded `0`. A second live preview of `transfer(address,uint256)` from that same empty address reverted with the named `InsufficientBalance(address,uint256,uint256)` error. Offline ABI boundary and malformed-output checks passed in `test/scratch/`.

The codec deliberately excludes arrays, tuples, and fixed point values. A node's preview reflects its chosen block and can differ from a later transaction. Declaring the wrong return types produces a `decode_error` while preserving the raw result.

## Offline preparation (round 5)

To see the tool working without a network connection:

```sh
python3 -B line-2/tools/typed_preview/typed_preview.py --demo --encode-only
```

`--encode-only` works with custom call fields too. It prints the validated transaction fields, function signature, expected return types and a complete JSON-RPC `eth_call` request for later preview. It reports `status: prepared` and `previewed: false`; preparation is not an EVM outcome. There is no signing, nonce selection, fee selection or submission. The output is a call request, not a complete sendable transaction. The selected block/tag is retained, but no state is fetched or pinned offline.

Tried: offline ZTO `balanceOf(address)` preparation produced selector `0x70a08231` and a 32-byte address argument. Six offline regression tests passed, including known transfer calldata, dynamic offsets, argument rejection before network access and unchanged live-mode dispatch. The test command is `python3 -B line-2/tools/typed_preview/check.py`.
