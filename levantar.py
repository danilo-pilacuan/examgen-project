#!/usr/bin/env python3
"""Root launcher: full bring-up + cloudflared exposure in one command.

Delegates to scripts/bring-up.py (single source of truth, see RECIPE.md).
Accepts the same flags as that script and prints the public trycloudflare
URL at the end (a new random URL is assigned on every run).

Usage:
    python levantar.py
    python levantar.py --no-tunnel
"""

import os
import runpy
import sys

_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "scripts", "bring-up.py")

if __name__ == "__main__":
    if not os.path.isfile(_SCRIPT):
        sys.exit("ERROR: %s not found (run this from the repo root)" % _SCRIPT)
    runpy.run_path(_SCRIPT, run_name="__main__")
