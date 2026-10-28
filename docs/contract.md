# Keymap build contract

Source keymap.json contains schema1, keyboard crkbd/rev1, layout LAYOUT_split_3x6_3 and exactly four named layers of42 QMK keycode strings. Each keycode must belong to the explicit supported set; only MO(1) and MO(2) are allowed as momentary functions. Thumb positions37/40 are MO(1)/MO(2) on BASE and KC_TRNS on every overlay. BASE contains no KC_TRNS, boot, reset, dynamic macro or EEPROM key. Only ADJUST can contain QK_BOOT.

Generator validates before writing; --check compares generated artifacts without modifying them. Outputs: firmware/keymap.c, docs/generated/layers.svg, site/index.html/style.css/app.js/keymap.json, docs/generated/layout.json. Official upstream42-position matrix/coordinates are SHA-pinned. Native test compiles the actual generated layer_state_set_user hook against a small deterministic QMK API stand-in; it does not claim USB, matrix, split transport or QMK runtime verification. CI separately compiles crkbd/rev1:qeth with the real pinned QMK source/toolchain. No automatic flash command.

Browser is a read-only layer guide from generated JSON. It labels physical positions and QMK actions; selecting a layer changes the displayed keycodes only. No remote API, HID access, keystroke capture, macros, downloads of personal data or firmware writes. Serve only generated site on loopback.

Original artwork is not reused. New source GPL-2.0-or-later to match QMK integration; upstream hardware references keep their own licenses. Physical part fit, polarity, hot-swap option, controller orientation, soldering, bootloader and all42 switch/split/USB tests remain pending.

Optional `--variant colemak --out NEW_DIR` exports nine files to a new destination only. It changes the 30 BASE letter/punctuation positions to the attributed standard Colemak arrangement, preserving the modifiers, layer thumbs and all overlays. `--check` compares that variant export without writes. The variant and output flags must be supplied together. Default generation/check remains unchanged. The exported config.h/rules.mk use the same wired controller assumptions as the default build.
