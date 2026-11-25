"""Copy the rendered front-page PNG to /output/entry.png."""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    os.umask(0o022)
    src = os.path.join(HERE, "entry.png")
    dst = "/output/entry.png"
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
