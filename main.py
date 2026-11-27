#!/usr/bin/env python3
"""news-image-20261126 v2 entrypoint.

Copies the pre-rendered broadsheet (entry.png, drawn locally by
render.py with PIL) to the output directory. Standard library only,
no network, deterministic: both runs write the same bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png missing next to main.py\n")
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    # copyfile preserves the bytes exactly, so repeated runs agree.


if __name__ == "__main__":
    main()
