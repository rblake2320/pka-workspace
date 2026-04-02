#!/usr/bin/env python
from __future__ import annotations

import sys

from pka_lib import sync_control_files


def main() -> int:
    sync_control_files()
    print("PKA sync: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
