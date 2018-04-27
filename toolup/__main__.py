from argparse import ArgumentParser
from itertools import zip_longest
from pathlib import Path

from toolup import Dependency


DEFAULT_CONFIG_PATH = Path.home() / ".toolup.toml"


def main(args=None):
    parser = ArgumentParser(prog="toolup")
    parser.add_argument("-c", "--config", help="Path to config TOML file")
    parser.add_argument(
        "-n", "--name", action="append", default=[], help="Name to install"
    )
    parser.add_argument(
        "-i",
        "--install_args",
        action="append",
        default=[],
        help="Arguments to pass to pip",
    )
    parser.add_argument(
        "-e", "--entry_points", action="append", default=[], help="Entry points to copy"
    )
    parser.add_argument("-t", "--target", help="Where to link executables")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Whether to delete existing executables",
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.config:
        Dependency.install_from_config(parsed_args.config, parsed_args.force)

    install_tuples = zip_longest(
        parsed_args.name, parsed_args.install_args, parsed_args.entry_points
    )

    for name, install_args, entry_points in install_tuples:
        Dependency(name, install_args, entry_points).install(
            parsed_args.target, parsed_args.force
        )

    if not any(
        [
            parsed_args.config,
            parsed_args.name,
            parsed_args.install_args,
            parsed_args.entry_points,
        ]
    ):
        Dependency.install_from_config(DEFAULT_CONFIG_PATH, parsed_args.force)


if __name__ == "__main__":
    main()
