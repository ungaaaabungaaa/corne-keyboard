// SPDX-License-Identifier: GPL-2.0-or-later
// Generated from keymap.json. Edit that source, then run tools/generate.py.
#include QMK_KEYBOARD_H
enum layers { BASE, NAV, SYMBOL, ADJUST };
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [BASE] = LAYOUT_split_3x6_3(
        KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_BSPC,
        KC_LCTL, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN, KC_QUOT,
        KC_LSFT, KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, KC_ESC,
        KC_LGUI, MO(1), KC_SPC, KC_ENT, MO(2), KC_RALT
    ),
    [NAV] = LAYOUT_split_3x6_3(
        KC_TRNS, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_TRNS,
        KC_TRNS, KC_HOME, KC_PGDN, KC_PGUP, KC_END, KC_NO, KC_LEFT, KC_DOWN, KC_UP, KC_RGHT, KC_DEL, KC_INS,
        KC_TRNS, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS
    ),
    [SYMBOL] = LAYOUT_split_3x6_3(
        KC_TRNS, KC_EXLM, KC_AT, KC_HASH, KC_DLR, KC_PERC, KC_CIRC, KC_AMPR, KC_ASTR, KC_LPRN, KC_RPRN, KC_TRNS,
        KC_TRNS, KC_GRV, KC_MINS, KC_EQL, KC_LBRC, KC_RBRC, KC_LCBR, KC_RCBR, KC_BSLS, KC_SCLN, KC_QUOT, KC_TRNS,
        KC_TRNS, KC_TILD, KC_UNDS, KC_PLUS, KC_PIPE, KC_NO, KC_NO, KC_NO, KC_COMM, KC_DOT, KC_SLSH, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS
    ),
    [ADJUST] = LAYOUT_split_3x6_3(
        QK_BOOT, KC_F11, KC_F12, KC_TRNS, KC_TRNS, KC_TRNS, KC_MPRV, KC_MPLY, KC_MNXT, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_VOLD, KC_VOLU, KC_MUTE, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS
    ),
};

layer_state_t layer_state_set_user(layer_state_t state) {
    return update_tri_layer_state(state, NAV, SYMBOL, ADJUST);
}
