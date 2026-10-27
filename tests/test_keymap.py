import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import generate
ROOT=Path(__file__).resolve().parents[1]
class KeymapTests(unittest.TestCase):
    def setUp(self):self.source=json.loads((ROOT/'keymap.json').read_text())
    def test_all_layers_match_the_physical_matrix(self):
        data=generate.validate(self.source)
        self.assertEqual([len(layer['keys']) for layer in data['layers']],[42]*4)
        self.assertEqual(len({tuple(key['matrix']) for key in generate.layout()}),42)
    def test_thumb_layer_keys_can_always_be_released(self):
        generate.validate(self.source)
        for layer_index in range(1,4):
            for index in (37,40):
                bad=copy.deepcopy(self.source);bad['layers'][layer_index]['keys'][index]='KC_A'
                with self.assertRaises(ValueError):generate.validate(bad)
    def test_code_injection_unknown_codes_and_wrong_counts_are_rejected(self):
        for code in ['KC_A); system("x")','MO(4)','KC_FAKE']:
            bad=copy.deepcopy(self.source);bad['layers'][0]['keys'][0]=code
            with self.assertRaises(ValueError):generate.validate(bad)
        bad=copy.deepcopy(self.source);bad['layers'][0]['keys'].pop()
        with self.assertRaises(ValueError):generate.validate(bad)
    def test_base_has_letters_and_no_boot_or_transparency(self):
        for code in ('QK_BOOT','KC_TRNS'):
            bad=copy.deepcopy(self.source);bad['layers'][0]['keys'][0]=code
            with self.assertRaises(ValueError):generate.validate(bad)
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':self.assertIn('KC_'+letter,self.source['layers'][0]['keys'])
    def test_official_reference_and_generation_are_exact(self):
        generate.layout()
        subprocess.run([sys.executable,str(ROOT/'tools/generate.py'),'--check'],check=True)
if __name__=='__main__':unittest.main()
