#!/usr/bin/env python3
"""
Ping the given hosts, print the hostnames and the milliseconds response
time.  Negative numbers indicate an error occurred.

Error codes:
    -1 no response before the timeout
"""
import logging
import argparse
import asyncio
import re

logger = logging.getLogger(__name__)


async def ping(host, timeout=1):
    pat = re.compile(r"^.*time=([\d\.]+) ms")
    cmd = ["ping", "-o", "-t", str(timeout), host]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    lines = stdout.decode().split("\n")
    matches = [pat.match(line) for line in lines]
    for mo in matches:
        if mo:
            return (host, mo.group(1))

    # no result in the timeout
    return (host, "-1")


async def main(event_loop, parser: argparse.ArgumentParser, args: argparse.Namespace):
    tasks = [asyncio.create_task(ping(host, args.timeout)) for host in args.hosts]
    results = await asyncio.gather(*tasks)
    for host, rtt in results:
        print(f"{host} {rtt}")


def parse_args():
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        required=False,
        default=1,
        help="Response timeout in seconds",
    )
    parser.add_argument("-D", "--debug", action="store_true", help="Log debug messages")
    parser.add_argument("hosts", nargs="*", default=[], help="The hosts to ping")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=format)
    return parser, args


if __name__ == "__main__":
    parser, args = parse_args()
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop, parser, args))
    finally:
        event_loop.close()
