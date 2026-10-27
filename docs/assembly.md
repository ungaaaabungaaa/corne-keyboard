# Assembly and physical acceptance — pending

This project targets the original wired42-key Corne classic board and two ProMicro ATmega32U4 controllers. It does not target a wireless nice!nano, RP2040 converter, newer integrated-controller board, or an arbitrary kit sold under the Corne name. The QMK revision alone does not identify every physical kit. Read the exact PCB marking and controller part before choosing firmware.

Reference hardware owner: foostan's [Corne repository](https://github.com/foostan/crkbd/tree/63366fb7f51cf2a796462fdd90527e99dd126055). Use its [classic build guide](https://github.com/foostan/crkbd/blob/63366fb7f51cf2a796462fdd90527e99dd126055/docs/corne-classic/buildguide_en.md) for component footprints, diode orientation, controller position and soldering order. Other Corne variants have different requirements. The design references retain their upstream licenses; this project does not publish new PCB manufacturing files.

## Parts to verify against that board

| Part | Quantity | Check |
| --- | --- | --- |
| Matched left/right classic PCBs | 1 pair | Exact board revision and switch footprint |
| ProMicro ATmega32U4 controllers | 2 | Voltage, pinout, connector and bootloader |
| Compatible switches | 42 | Plate and PCB compatibility |
| Switch diodes | 42 | Package, footprint and polarity |
| Keycaps | 42 |40×1u plus2×1.5u in the referenced guide; verify thumb geometry |
| Compatible TRRS sockets | 2 | Match footprint and contacts |
| TRRS cable | 1 | Continuity and wiring |
| Reset switches | 2 | Match PCB footprint |
| Controller headers/sockets | 2 sets | Correct height and orientation |
| Matching plates, spacers, screws, feet | 1 set | Board-specific mechanical dimensions |
| USB data cable | 1 | Match controller connector |

OLED and RGB parts are intentionally omitted from this firmware build. Hot-swap sockets are not assumed for the classic soldered-switch board. Stock, prices, replacement fit and procurement have not been verified; no parts were bought.

## Unpowered inspection

Disconnect USB before adding/removing the inter-half cable or changing any component. Inspect solder joints under magnification. Check controller and diode polarity against the board guide. Measure continuity for ground, power and split signal. Check for a power-to-ground short and verify switch/diode connections. Inspect both halves separately. A printed guide or generated cover does not prove any of these checks passed.

## Manual firmware and switch checks

The real QMK build targets `crkbd/rev1:qeth`, with MASTER_LEFT and no OLED/RGB. USB is expected on the left half. BOOTMAGIC is disabled; the explicit ADJUST-layer BOOT action and the physical reset mechanism remain. Firmware is compiled in CI; no device has been flashed here. The build result is not evidence of electrical compatibility.

After inspecting the actual controller/bootloader, follow the official [QMK flashing guide](https://docs.qmk.fm/newbs_flashing). Flash both halves using the procedure for that exact controller. This repository does not invoke a flash command or expose USB devices in CI. Do not select a bootloader from the generated cover image.

Then record these tests with actual hardware and OS layout:

1. Verify every one of42 switch positions separately. Confirm no stuck or repeated key and both halves' handedness.
2. Hold NAV, press/release a navigation key, then release NAV. Confirm BASE returns.
3. Repeat for SYMBOL. Hold both, test an ADJUST media key, then release thumbs in both orders. Confirm no layer remains active.
4. Confirm left/right modifiers, Space/Enter, USB reconnect and idle behaviour.
5. Test BOOT only when you intend to enter the bootloader and can recover manually. Confirm subsequent boot is normal.

These physical, split-transport, debounce, USB, rollover and ergonomic tests are pending. The browser guide previews labels only.
