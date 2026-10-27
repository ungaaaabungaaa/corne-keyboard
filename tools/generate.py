# SPDX-License-Identifier: GPL-2.0-or-later
"""Generate firmware and guides from one validated keymap; never flash hardware."""
import argparse
import hashlib
import html
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOWED=set(('KC_'+letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))|set('KC_TAB KC_BSPC KC_LCTL KC_SCLN KC_QUOT KC_LSFT KC_COMM KC_DOT KC_SLSH KC_ESC KC_LGUI KC_SPC KC_ENT KC_RALT KC_TRNS KC_NO KC_HOME KC_PGDN KC_PGUP KC_END KC_LEFT KC_DOWN KC_UP KC_RGHT KC_DEL KC_INS KC_EXLM KC_AT KC_HASH KC_DLR KC_PERC KC_CIRC KC_AMPR KC_ASTR KC_LPRN KC_RPRN KC_GRV KC_MINS KC_EQL KC_LBRC KC_RBRC KC_LCBR KC_RCBR KC_BSLS KC_TILD KC_UNDS KC_PLUS KC_PIPE KC_MPRV KC_MPLY KC_MNXT KC_VOLD KC_VOLU KC_MUTE QK_BOOT MO(1) MO(2)'.split())|set(f'KC_{i}' for i in range(10))|set(f'KC_F{i}' for i in range(1,13))

def validate(data):
 if not isinstance(data,dict) or set(data)!={'schema_version','keyboard','layout','layers'} or type(data['schema_version']) is not int or data['schema_version']!=1 or data['keyboard']!='crkbd/rev1' or data['layout']!='LAYOUT_split_3x6_3':raise ValueError('Unsupported board, layout or schema.')
 if not isinstance(data['layers'],list) or len(data['layers'])!=4:raise ValueError('Exactly four layers required.')
 for i,(layer,name) in enumerate(zip(data['layers'],['BASE','NAV','SYMBOL','ADJUST'])):
  if not isinstance(layer,dict) or set(layer)!={'name','keys'} or layer['name']!=name or not isinstance(layer['keys'],list) or len(layer['keys'])!=42 or any(not isinstance(key,str) or key not in ALLOWED for key in layer['keys']):raise ValueError('Invalid layer or unsupported QMK keycode.')
  if i==0 and any(key in ('KC_TRNS','QK_BOOT') for key in layer['keys']):raise ValueError('Base must type directly and must not boot.')
  if i<3 and 'QK_BOOT' in layer['keys']:raise ValueError('Boot is confined to ADJUST.')
  if [layer['keys'][j] for j in (37,40)] != (['MO(1)','MO(2)'] if i==0 else ['KC_TRNS','KC_TRNS']):raise ValueError('Thumb layers must fall through on all overlays.')
 return data

def layout():
 pins=json.loads((ROOT/'references/UPSTREAM.json').read_text())
 for name,digest in pins['files'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Pinned upstream reference changed.')
 keys=json.loads((ROOT/'references/qmk-crkbd-info.json').read_text())['layouts']['LAYOUT_split_3x6_3']['layout']
 if len(keys)!=42 or len({tuple(key['matrix']) for key in keys})!=42:raise ValueError('Official layout is not the expected 42-position matrix.')
 return keys

def artifacts():
 data=validate(json.loads((ROOT/'keymap.json').read_text()));positions=layout()
 c='// SPDX-License-Identifier: GPL-2.0-or-later\n// Generated from keymap.json. Edit that source, then run tools/generate.py.\n#include QMK_KEYBOARD_H\nenum layers { BASE, NAV, SYMBOL, ADJUST };\nconst uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {\n'
 for layer in data['layers']:
  c+='    ['+layer['name']+'] = LAYOUT_split_3x6_3(\n'
  for start,end in [(0,12),(12,24),(24,36),(36,42)]:c+='        '+', '.join(layer['keys'][start:end])+(',' if end<42 else '')+'\n'
  c+='    ),\n'
 c+='};\n\nlayer_state_t layer_state_set_user(layer_state_t state) {\n    return update_tri_layer_state(state, NAV, SYMBOL, ADJUST);\n}\n'
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1530" viewBox="0 0 1200 1530"><rect width="1200" height="1530" fill="#f4f3ec"/><style>text{font-family:monospace;fill:#243c35}.key{fill:white;stroke:#b1bcb1}</style><text x="35" y="40" font-size="24">CORNE / Four-layer guide — QMK crkbd/rev1</text>']
 for index,layer in enumerate(data['layers']):
  offset=80+index*360;svg.append(f'<text x="35" y="{offset}" font-size="20">{layer["name"]}</text>')
  for key,position in zip(layer['keys'],positions):
   x=35+position['x']*74;y=offset+20+position['y']*60;label=key.replace('KC_','')
   svg.append(f'<rect class="key" x="{x}" y="{y}" width="68" height="52" rx="4"/><text x="{x+34}" y="{y+30}" text-anchor="middle" font-size="12">{html.escape(label)}</text>')
 svg.append('<text x="35" y="1510" font-size="14">Hold NAV + SYMBOL for ADJUST. Guide only; physical keyboard tests remain pending.</text></svg>')
 rendered={'firmware/keymap.c':c,'docs/generated/layers.svg':''.join(svg)+'\n','docs/generated/layout.json':json.dumps({'keyboard':data['keyboard'],'positions':positions},indent=2)+'\n','site/keymap.json':json.dumps({**data,'positions':positions},indent=2)+'\n'}
 for name in ['index.html','style.css','app.js']:rendered['site/'+name]=(ROOT/'web'/name).read_text()
 return rendered

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
 try:
  output=artifacts()
  if args.check:
   for name,value in output.items():
    if (ROOT/name).read_text()!=value:raise ValueError('Generated artifact differs: '+name)
   print(f'{len(output)} generated artifacts match exactly.')
  else:
   for name,value in output.items():(ROOT/name).write_text(value,encoding='utf-8',newline='\n')
   print(f'Generated {len(output)} artifacts. No board was connected or flashed.')
  return 0
 except (OSError,ValueError,KeyError,TypeError) as error:print(str(error));return 1
if __name__=='__main__':raise SystemExit(main())
