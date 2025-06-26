import unittest
import os
import subprocess

import paige as pg
from paige.const import PAIGE_DIR_NAME
from unittest.mock import patch


class TestPathFunctions(unittest.TestCase):
    def setUp(self):
        self.test_git_root = "/tmp/test_git_root"
        os.makedirs(self.test_git_root, exist_ok=True)

    def tearDown(self):
        pass

    def test_from_work_dir(self):
        cwd = os.getcwd()
        self.assertEqual(pg.path.from_work_dir(), cwd)
        test_subdir_file = ("subdir", "file.txt")
        expected_path = os.path.join(cwd, *test_subdir_file)
        self.assertEqual(pg.path.from_work_dir(*test_subdir_file), expected_path)

    @patch("subprocess.check_output")
    def test_from_git_root_success(self, mock_check_output):
        mock_check_output.return_value = self.test_git_root.encode("utf-8")
        test_subdir_file = ("subdir", "file.txt")
        expected_path = os.path.join(self.test_git_root, *test_subdir_file)
        self.assertEqual(pg.path.from_git_root(*test_subdir_file), expected_path)
        mock_check_output.assert_called_once_with(
            ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
        )

    @patch("subprocess.check_output")
    def test_from_git_root_failure(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["git", "rev-parse", "--show-toplevel"]
        )
        with self.assertRaisesRegex(
            Exception, "Not in a git repository or git command failed."
        ):
            pg.path.from_git_root()

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_ensure_parent_dir_not_exists(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        test_path = "/tmp/test_dir/test_file.txt"
        pg.path.ensure_parent_dir(test_path)
        mock_makedirs.assert_called_once_with("/tmp/test_dir", exist_ok=True)

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_ensure_parent_dir_exists(self, mock_exists, mock_makedirs):
        mock_exists.return_value = True
        test_path = "/tmp/test_dir/test_file.txt"
        pg.path.ensure_parent_dir(test_path)
        mock_makedirs.assert_not_called()

    @patch("paige.path.from_git_root")
    def test_from_paige_dir(self, mock_from_git_root):
        mock_from_git_root.side_effect = lambda *args: os.path.join(
            "/test/paige/git/root", *args
        )
        expected_paige_dir = os.path.join("/test/paige/git/root", PAIGE_DIR_NAME)
        self.assertEqual(pg.path.from_paige_dir(), expected_paige_dir)
        test_subdir_file = ("subdir", "file.txt")
        expected_path = os.path.join(expected_paige_dir, *test_subdir_file)
        self.assertEqual(pg.path.from_paige_dir(*test_subdir_file), expected_path)
        mock_from_git_root.assert_any_call(PAIGE_DIR_NAME)


if __name__ == "__main__":
    unittest.main()
