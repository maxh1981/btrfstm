import re
import sh

from pathlib import Path
from time import gmtime, strftime


class BtrfstmError(Exception):
    def __init__(
            self,
            msg):
        self._msg = msg


def _get_snapshot_regex(
        name,
        snapshot_prefix):
    return re.compile(
        r"^_" + name + r"_" + snapshot_prefix
        + r"_snapshot_"
        + r"@([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9]{2}:[0-9]{2}:[0-9]{2})Z$")


class Profile(object):
    def __init__(
            self,
            working_dir,
            name,
            snapshot_prefix):
        """
        Args:
            working_dir
                should be an instance of pathlib.Path
            name
                should be an instance of str
            snapshot_prefix
                should be an instance of str
        """
        self._working_dir = working_dir
        self._name = name
        self._snapshot_prefix = snapshot_prefix

        self._snapshot_regex = _get_snapshot_regex(
            name,
            snapshot_prefix)

        self._btrfs = sh.btrfs

    def list_all(self):
        """
        Return:
            list of pathlib.Path
        """
        if not self._working_dir.is_dir():
            raise BtrfstmError("directory not exist: " + str(self._working_dir))

        rtn = list()
        for p in self._working_dir.iterdir():
            match = self._snapshot_regex.match(p.name)
            if not match:
                continue

            rtn += [p]

        return sorted(rtn)

    def create(self):
        """
        Return:
            pathlib.Path
                as created subvolume path
        """
        new_subvolume = self._working_dir / Path(
            "_" + self._name + "_" + self._snapshot_prefix + "_snapshot_@" + strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()))
        try:
            self._btrfs.subvolume.snapshot(self._working_dir / self._name, new_subvolume)
            return new_subvolume

        except sh.ErrorReturnCode as erc:
            raise BtrfstmError("btrfs command line error")

    def delete(
            self,
            snapshot):
        snapshot_list = self.list_all()

        if snapshot not in snapshot_list:
            raise BtrfstmError("not exist")

        try:
            self._btrfs.subvolume.delete(snapshot)

        except sh.ErrorReturnCode as erc:
            raise BtrfstmError("btrfs command line error")
