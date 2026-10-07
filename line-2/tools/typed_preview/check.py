#!/usr/bin/env python3
"""Offline preparation regression checks; no network, keys or environment reads."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('typed', Path(__file__).with_name('typed_preview.py'))
typed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(typed)


class Checks(unittest.TestCase):
    def run_cli(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = typed.main(args)
        self.assertEqual(code, 0)
        return json.loads(output.getvalue())

    def test_demo_offline(self):
        with patch.object(typed.preview, 'rpc_call', side_effect=AssertionError('network forbidden')):
            report = self.run_cli(['--demo', '--encode-only'])
        self.assertEqual(report['transaction']['to'], typed.preview.ZTO)
        self.assertEqual(report['transaction']['data'], '0x70a08231' + '0' * 63 + '1')
        self.assertEqual(report['status'], 'prepared')
        self.assertIs(report['previewed'], False)
        self.assertIs(report['sent'], False)
        self.assertEqual(report['request']['method'], 'eth_call')
        self.assertNotIn('decoded_return', report)

    def test_transfer_fields(self):
        with patch.object(typed.preview, 'rpc_call', side_effect=AssertionError('network forbidden')):
            report = self.run_cli(['--encode-only', '--to', typed.preview.ZTO,
                '--signature', 'transfer(address,uint256)', '--arg', typed.preview.POOL_MANAGER,
                '--arg', '1', '--from', typed.preview.DEMO_FROM, '--value-wei', '0',
                '--gas', '50000', '--block', '123', '--returns', 'bool'])
        tx = report['transaction']
        self.assertEqual(tx['data'], '0xa9059cbb' + typed.preview.POOL_MANAGER[2:].rjust(64, '0') + '0' * 63 + '1')
        self.assertEqual(tx['gas'], '0xc350')
        self.assertEqual(tx['from'], typed.preview.DEMO_FROM)
        self.assertEqual(report['request']['params'], [tx, '0x7b'])

    def test_dynamic_offsets(self):
        raw = typed.encode_args(['string', 'bytes'], ['seed', '0x1234'])
        self.assertEqual(int.from_bytes(raw[:32], 'big'), 64)
        self.assertEqual(int.from_bytes(raw[32:64], 'big'), 128)
        self.assertEqual(raw[96:100], b'seed')
        self.assertEqual(raw[160:162], b'\x12\x34')
        self.assertEqual(len(raw), 192)

    def test_invalid_input_never_calls(self):
        for signature, arg in [('f(uint)', '1'), ('f(int)', '1'), ('f(uint8)', '256'), ('f(bool)', 'yes')]:
            with self.subTest(signature=signature), patch.object(typed.preview, 'rpc_call') as rpc:
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                    typed.main(['--encode-only', '--to', typed.preview.ZTO, '--signature', signature, '--arg', arg])
                self.assertEqual(exc.exception.code, 2)
                rpc.assert_not_called()

    def test_live_dispatch_unchanged(self):
        with patch.object(typed.preview, 'rpc_call', return_value={'result': '0x' + '00' * 32}) as rpc:
            report = self.run_cli(['--demo'])
        rpc.assert_called_once()
        self.assertEqual(report['status'], 'succeeded')
        self.assertEqual(report['decoded_return'], ['0'])
        self.assertNotIn('request', report)

    def test_named_revert_unchanged(self):
        payload = '0xdb42144d' + '0' * 63 + '1' + '00' * 32 + '0' * 63 + '1'
        with patch.object(typed.preview, 'rpc_call', return_value={'error': {
                'code': 3, 'message': 'execution reverted', 'data': payload}}):
            report = self.run_cli(['--demo'])
        self.assertEqual(report['status'], 'reverted')
        self.assertEqual(report['error']['named']['matches'][0]['signature'], 'InsufficientBalance(address,uint256,uint256)')


if __name__ == '__main__':
    unittest.main(verbosity=2)
