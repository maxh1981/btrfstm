import unittest

from btrfstm.cli import get_argparser


class TestGetArgparser(unittest.TestCase):
    def setUp(self):
        self.argparser = get_argparser()

    def test_ShouldPass(self):
        # arrange
        argv = [
            "--working-dir=/storage/data",
            "--name=dropbox",
            "--snapshot-prefix=daily"
        ]

        # act
        args = self.argparser.parse_args(argv)

        # assert
        self.assertEqual("/storage/data", args.working_dir)
        self.assertEqual("dropbox", args.name)
        self.assertEqual("daily", args.snapshot_prefix)

    def test_WithCount_ShouldPass(self):
        # arrange
        argv = [
            "--working-dir=/storage/data",
            "--name=dropbox",
            "--snapshot-prefix=daily",
            "--count=31"
        ]

        # act
        args = self.argparser.parse_args(argv)

        # assert
        self.assertEqual(31, args.count)
