import sys
from argparse import ArgumentParser
from btrfstm import Profile
from pathlib import Path


def main():
    argparser = get_argparser()
    args = argparser.parse_args()

    profile = Profile(
        Path(args.working_dir),
        args.name,
        args.snapshot_prefix)

    if args.count > 0:
        # remove old snapshots
        snapshot_list = profile.list_all()
        while len(snapshot_list) >= args.count:
            profile.delete(snapshot_list[0])

            snapshot_list = profile.list_all()

    snapshot = profile.create()
    print(snapshot)


def get_argparser():
    parser = ArgumentParser(description="btrfs time machine")
    parser.add_argument(
        "--working-dir",
        metavar="PATH",
        type=str,
        required=True)

    parser.add_argument(
        "--name",
        metavar="NAME",
        type=str,
        required=True)

    parser.add_argument(
        "--snapshot-prefix",
        metavar="PREFIX",
        type=str,
        required=True)

    parser.add_argument(
        "--count",
        metavar="COUNT",
        type=int,
        default=0)

    return parser


if __name__ == "__main__":
    main()
