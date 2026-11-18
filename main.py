"""Publish the committed front page for the make.fun grader."""

import os
from pathlib import Path
from shutil import copyfile


def main():
    source = Path(__file__).resolve().with_name("entry.png")
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    if output.resolve() == source.parent:
        raise ValueError("The output directory must be separate from the source directory")
    output.mkdir(parents=True, exist_ok=True)
    for item in output.iterdir():
        if item.is_symlink() or item.is_file():
            item.unlink()
    copyfile(source, output / "entry.png")


if __name__ == "__main__":
    main()
