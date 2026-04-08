from __future__ import annotations

import argparse
from os import fspath
from typing import Sequence


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="just-player",
        description="Minimal Windows video player on Python + libmpv",
    )
    parser.add_argument("paths", nargs="*", help="Files to open immediately")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    startup_paths = [fspath(path) for path in args.paths]

    from .app import JustPlayerApp

    app = JustPlayerApp(startup_paths=startup_paths)
    app.run()
    return 0
