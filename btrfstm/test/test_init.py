import os
import unittest
from pathlib import Path
from shutil import rmtree

from btrfstm import _get_snapshot_regex, Profile


class TestGetSnapshotRegex(unittest.TestCase):
    def setUp(self):
        self.regex = _get_snapshot_regex(
            "dropbox",
            "daily")

    def test_ShouldPass(self):
        # arrange
        SUT = "_dropbox_daily_snapshot_@2016-06-11T11:45:21Z"

        # act
        match = self.regex.match(SUT)

        # assert
        self.assertTrue(match)

    def test_WithIllegalName_ShouldFail(self):
        # arrange
        SUT = "dropbox"

        # act
        should_not_match = self.regex.match(SUT)

        # assert
        self.assertFalse(should_not_match)


class TestProfile(unittest.TestCase):
    def setUp(self):
        self._test_root = Path("/dev/shm/btrfstm-test")
        if self._test_root.exists():
            rmtree(str(self._test_root))

        self.working_dir = self._test_root / Path("working-dir")

        os.makedirs(str(self.working_dir))

        os.mkdir(str(self.working_dir / Path("dropbox")))

        os.mkdir(str(self.working_dir / Path("_dropbox_daily_snapshot_@2016-06-10T02:00:00Z")))
        os.mkdir(str(self.working_dir / Path("_dropbox_daily_snapshot_@2016-06-11T02:00:00Z")))

        self.profile = Profile(
            self.working_dir,
            "dropbox",
            "daily")

    def tearDown(self):
        rmtree(str(self._test_root))

    def test_ListAll_ShouldPass(self):
        # arrange

        # act
        snapshot_list = self.profile.list_all()

        # assert
        self.assertEqual(2, len(snapshot_list))

        snapshot_list = [str(x) for x in snapshot_list]
        self.assertIn("/dev/shm/btrfstm-test/working-dir/_dropbox_daily_snapshot_@2016-06-10T02:00:00Z", snapshot_list)
        self.assertIn("/dev/shm/btrfstm-test/working-dir/_dropbox_daily_snapshot_@2016-06-11T02:00:00Z", snapshot_list)
