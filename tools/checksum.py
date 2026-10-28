# SPDX-License-Identifier: GPL-2.0-or-later
"""Write or verify a portable SHA-256 receipt for a firmware download."""

import argparse
import hashlib
from pathlib import Path
import re


def checksum(image, check=False):
    image = Path(image)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", image.name):
        raise ValueError("Firmware name must use letters, digits, dot, dash or underscore.")
    content = image.read_bytes()
    if not content:
        raise ValueError("Firmware image is empty.")
    receipt = image.with_suffix(image.suffix + ".sha256")
    expected = hashlib.sha256(content).hexdigest() + "  " + image.name + "\n"
    if check:
        if receipt.read_bytes() != expected.encode("ascii"):
            raise ValueError("Firmware checksum differs from its download receipt.")
    else:
        receipt.write_text(expected, encoding="ascii", newline="\n")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        receipt = checksum(args.image, args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
    print(("Verified " if args.check else "Wrote ") + str(receipt))


if __name__ == "__main__":
    main()
