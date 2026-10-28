import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ChecksumTests(unittest.TestCase):
    def test_download_checksum_detects_firmware_changes(self):
        spec = importlib.util.spec_from_file_location("checksum", ROOT / "tools/checksum.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "corne_rev1_qeth.hex"
            image.write_bytes(b":00000001FF\n")
            receipt = module.checksum(image)
            self.assertEqual(receipt, image.with_suffix(".hex.sha256"))
            self.assertEqual(receipt.read_text(encoding="ascii"), "9e2df0a1190a1205c098889c455e5b76c4df18b5ccac2b7605da1575f05b64c5  corne_rev1_qeth.hex\n")
            self.assertEqual(module.checksum(image, check=True), receipt)
            image.write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "differs"):
                module.checksum(image, check=True)

    def test_cli_verifies_and_fails_without_replacing_the_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "download.hex"
            image.write_bytes(b":00000001FF\n")
            command = [sys.executable, str(ROOT / "tools/checksum.py"), str(image)]
            subprocess.run(command, check=True, capture_output=True)
            receipt = image.with_suffix(".hex.sha256")
            expected = receipt.read_bytes()
            subprocess.run(command + ["--check"], check=True, capture_output=True)
            image.write_bytes(b"changed")
            result = subprocess.run(command + ["--check"], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn(b"differs", result.stderr)
            self.assertEqual(receipt.read_bytes(), expected)

    def test_missing_empty_or_unsafe_firmware_names_are_rejected(self):
        spec = importlib.util.spec_from_file_location("checksum", ROOT / "tools/checksum.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "missing.hex"
            with self.assertRaises(OSError):
                module.checksum(image)
            image.write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "empty"):
                module.checksum(image)
            unsafe = Path(directory) / "bad\nname.hex"
            # Rejection occurs before I/O; Windows cannot create this name.
            with self.assertRaisesRegex(ValueError, "name"):
                module.checksum(unsafe)
