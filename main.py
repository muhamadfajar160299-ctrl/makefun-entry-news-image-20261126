"""Entry point for the make.fun news-image-20261126 entry.

Standard library only. The image is pre-rendered by render.py and shipped
in this repository as entry.png; this program only copies it to the output
directory the grader names (MAKEFUN_OUTPUT_DIR, default /output).
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
