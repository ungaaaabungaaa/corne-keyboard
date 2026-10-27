# SPDX-License-Identifier: GPL-2.0-or-later
"""Compile the actual generated hook against a narrow QMK API stand-in."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
compiler=shutil.which('cc')
if compiler is None:raise SystemExit('A native C compiler is required for this separate check.')
keys=sorted({key for layer in json.loads((ROOT/'keymap.json').read_text())['layers'] for key in layer['keys'] if not key.startswith('MO(')})
with tempfile.TemporaryDirectory() as directory:
    temp=Path(directory)
    (temp/'mock_qmk.h').write_text('''#include <stdint.h>
#define PROGMEM
#define MATRIX_ROWS 1
#define MATRIX_COLS 42
#define LAYOUT_split_3x6_3(...) {{__VA_ARGS__}}
#define MO(n) (0x5000+(n))
typedef uint32_t layer_state_t;
static layer_state_t update_tri_layer_state(layer_state_t state, unsigned lower, unsigned upper, unsigned adjust) {
    const layer_state_t both=(1u<<lower)|(1u<<upper);
    return (state&both)==both ? state|(1u<<adjust) : state&~(1u<<adjust);
}
enum keycodes {'''+','.join(keys)+'''};
''')
    (temp/'main.c').write_text('#include <assert.h>\n#include "'+str(ROOT/'firmware/keymap.c')+'"\n'+'''int main(void){
        for(uint32_t state=0;state<256;state++){
            uint32_t result=layer_state_set_user(state);
            uint32_t expected=(state&6)==6 ? state|8 : state&~8u;
            assert(result==expected);
            assert((result&~8u)==(state&~8u));
        }
        assert(sizeof(keymaps)/sizeof(keymaps[0])==4);
        return 0;
    }
''')
    executable=temp/'native'
    subprocess.run([compiler,'-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-fno-omit-frame-pointer','-DQMK_KEYBOARD_H="mock_qmk.h"','-I',str(temp),str(temp/'main.c'),'-o',str(executable)],check=True)
    subprocess.run([str(executable)],check=True)
print('Actual generated hook: 256 state combinations passed under ASan/UBSan. QMK API is a stand-in; real AVR compilation is separate.')
