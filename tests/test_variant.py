import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import generate

ROOT = Path(__file__).resolve().parents[1]


class VariantTests(unittest.TestCase):
    def test_colemak_keeps_every_letter_once_and_preserves_overlay_thumb_keys(self):
        default = generate.artifacts()
        variant = generate.artifacts("colemak")
        original = json.loads(default["site/keymap.json"])
        data = json.loads(variant["site/keymap.json"])
        keys = data["layers"][0]["keys"]
        self.assertEqual(keys[1:11], ["KC_" + x for x in "QWFPGJLUY"] + ["KC_SCLN"])
        self.assertEqual(keys[13:23], ["KC_" + x for x in "ARSTDHNEIO"])
        self.assertEqual(keys[25:35], ["KC_" + x for x in "ZXCVBKM"] + ["KC_COMM", "KC_DOT", "KC_SLSH"])
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.assertEqual(keys.count("KC_" + letter), 1)
        self.assertEqual(data["layers"][1:], original["layers"][1:])
        self.assertEqual(keys[36:], original["layers"][0]["keys"][36:])
        generate.validate({key: value for key, value in data.items() if key != "positions"})
        self.assertEqual(generate.artifacts(), default)

    def test_export_is_separate_reproducible_and_refuses_overwrite(self):
        command = [sys.executable, str(ROOT / "tools/generate.py"), "--variant", "colemak"]
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "colemak"
            subprocess.run(command + ["--out", str(dest)], check=True, capture_output=True)
            subprocess.run(command + ["--out", str(dest), "--check"], check=True, capture_output=True)
            self.assertEqual((dest / "firmware/config.h").read_bytes(), (ROOT / "firmware/config.h").read_bytes())
            first = (dest / "firmware/keymap.c").read_bytes()
            result = subprocess.run(command + ["--out", str(dest)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((dest / "firmware/keymap.c").read_bytes(), first)
            (dest / "firmware/keymap.c").write_bytes(b"changed")
            self.assertNotEqual(subprocess.run(command + ["--out", str(dest), "--check"], capture_output=True).returncode, 0)
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
