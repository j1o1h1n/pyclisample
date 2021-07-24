#!/usr/bin/env python3
"""
Do a thing that needs to be done
"""
import logging
import argparse

logger = logging.getLogger(__name__)


def func() -> int:
    return 3


def main(parser: argparse.ArgumentParser, args: argparse.Namespace):
    if args.wabe > 1:
        print(" ".join(['wabe'] * args.wabe))
    for g in args.gyre:
        print(f"gimble, {g}")
    if not args.wabe and not args.gyre:
        parser.error("no wabe, no gyre and therefore no gimble")


def parse_args():
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("-w", "--wabe", type=int, required=False, default=0,
                        help="The amount of wabe")
    parser.add_argument("-D", "--debug", action="store_true",
                        help="Log debug messages")
    parser.add_argument("gyre", nargs='*', default=[],
                        help="The gyres")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=format)
    return parser, args


if __name__ == "__main__":
    parser, args = parse_args()
    main(parser, args)

