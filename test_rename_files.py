#!/usr/bin/env python3
"""Tests for rename_files.py"""

import io
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rename_files import (
    move_files,
    rename_lowercase,
    rename_regex,
    rename_remove_spaces,
    rename_replace,
    rename_sequential,
)


def make_files(folder, *names):
    for name in names:
        open(os.path.join(folder, name), "w").close()


def ls(folder):
    return sorted(os.listdir(folder))


class TestRenameSequential(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_dry_run_leaves_files_unchanged(self):
        make_files(self.tmp, "b.txt", "a.txt")
        rename_sequential(self.tmp, dry_run=True)
        self.assertEqual(ls(self.tmp), ["a.txt", "b.txt"])

    def test_dry_run_output_contains_marker(self):
        make_files(self.tmp, "a.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_sequential(self.tmp, dry_run=True)
        self.assertIn("[DRY RUN]", out.getvalue())

    def test_execute_renames_in_lexicographic_order(self):
        make_files(self.tmp, "c.txt", "a.txt", "b.txt")
        rename_sequential(self.tmp, prefix="file", dry_run=False)
        # lexicographic sort: a→1, b→2, c→3
        self.assertEqual(ls(self.tmp), ["file_1.txt", "file_2.txt", "file_3.txt"])

    def test_execute_custom_prefix(self):
        make_files(self.tmp, "x.jpg", "y.jpg")
        rename_sequential(self.tmp, prefix="photo", dry_run=False)
        self.assertEqual(ls(self.tmp), ["photo_1.jpg", "photo_2.jpg"])

    def test_execute_preserves_original_extension(self):
        make_files(self.tmp, "a.png", "b.jpg")
        rename_sequential(self.tmp, prefix="img", dry_run=False)
        result = ls(self.tmp)
        extensions = {os.path.splitext(f)[1] for f in result}
        self.assertIn(".png", extensions)
        self.assertIn(".jpg", extensions)

    def test_execute_forced_extension_overrides_original(self):
        make_files(self.tmp, "a.txt", "b.txt")
        rename_sequential(self.tmp, prefix="img", extension=".jpg", dry_run=False)
        self.assertEqual(ls(self.tmp), ["img_1.jpg", "img_2.jpg"])

    def test_empty_folder_prints_message(self):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_sequential(self.tmp, dry_run=False)
        self.assertIn("No files found", out.getvalue())

    def test_empty_folder_makes_no_changes(self):
        rename_sequential(self.tmp, dry_run=False)
        self.assertEqual(ls(self.tmp), [])


class TestRenameReplace(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_dry_run_leaves_files_unchanged(self):
        make_files(self.tmp, "old_file.txt")
        rename_replace(self.tmp, "old", "new", dry_run=True)
        self.assertEqual(ls(self.tmp), ["old_file.txt"])

    def test_dry_run_output_contains_marker(self):
        make_files(self.tmp, "old_file.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_replace(self.tmp, "old", "new", dry_run=True)
        self.assertIn("[DRY RUN]", out.getvalue())

    def test_execute_replaces_all_matching_files(self):
        make_files(self.tmp, "old_a.txt", "old_b.jpg", "keep.txt")
        rename_replace(self.tmp, "old_", "", dry_run=False)
        self.assertIn("a.txt", ls(self.tmp))
        self.assertIn("b.jpg", ls(self.tmp))
        self.assertIn("keep.txt", ls(self.tmp))

    def test_execute_replaces_only_matching_substring(self):
        make_files(self.tmp, "foo_bar.txt", "no_match.txt")
        rename_replace(self.tmp, "foo", "baz", dry_run=False)
        self.assertIn("baz_bar.txt", ls(self.tmp))
        self.assertIn("no_match.txt", ls(self.tmp))

    def test_no_matches_prints_message(self):
        make_files(self.tmp, "file.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_replace(self.tmp, "xyz", "abc", dry_run=False)
        self.assertIn("xyz", out.getvalue())
        self.assertEqual(ls(self.tmp), ["file.txt"])

    def test_empty_folder_prints_message(self):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_replace(self.tmp, "a", "b", dry_run=False)
        self.assertIn("No files found", out.getvalue())


class TestRenameRegex(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_dry_run_leaves_files_unchanged(self):
        make_files(self.tmp, "photo123.jpg")
        rename_regex(self.tmp, r"\d+", "NUM", dry_run=True)
        self.assertEqual(ls(self.tmp), ["photo123.jpg"])

    def test_dry_run_output_contains_marker(self):
        make_files(self.tmp, "photo123.jpg")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_regex(self.tmp, r"\d+", "NUM", dry_run=True)
        self.assertIn("[DRY RUN]", out.getvalue())

    def test_execute_applies_substitution(self):
        make_files(self.tmp, "photo123.jpg", "img456.png")
        rename_regex(self.tmp, r"(\d+)", r"_\1_", dry_run=False)
        self.assertIn("photo_123_.jpg", ls(self.tmp))
        self.assertIn("img_456_.png", ls(self.tmp))

    def test_execute_strips_digits(self):
        make_files(self.tmp, "file001.txt", "doc2024.pdf")
        rename_regex(self.tmp, r"\d+", "", dry_run=False)
        self.assertIn("file.txt", ls(self.tmp))
        self.assertIn("doc.pdf", ls(self.tmp))

    def test_regex_applies_to_extension_too(self):
        make_files(self.tmp, "file.TXT")
        rename_regex(self.tmp, r"\.TXT$", ".txt", dry_run=False)
        self.assertIn("file.txt", ls(self.tmp))

    def test_no_matches_prints_message(self):
        make_files(self.tmp, "abc.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_regex(self.tmp, r"\d+", "", dry_run=False)
        self.assertIn("No files matched", out.getvalue())
        self.assertEqual(ls(self.tmp), ["abc.txt"])

    def test_empty_folder_prints_message(self):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_regex(self.tmp, r".*", "", dry_run=False)
        self.assertIn("No files found", out.getvalue())


class TestRenameLowercase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_dry_run_leaves_files_unchanged(self):
        make_files(self.tmp, "UPPER.TXT")
        rename_lowercase(self.tmp, dry_run=True)
        self.assertIn("UPPER.TXT", ls(self.tmp))

    def test_dry_run_output_contains_marker(self):
        make_files(self.tmp, "UPPER.TXT")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_lowercase(self.tmp, dry_run=True)
        self.assertIn("[DRY RUN]", out.getvalue())

    def test_execute_lowercases_name_and_extension(self):
        make_files(self.tmp, "README.MD", "Script.PY")
        rename_lowercase(self.tmp, dry_run=False)
        result = ls(self.tmp)
        self.assertIn("readme.md", result)
        self.assertIn("script.py", result)

    def test_already_lowercase_prints_no_op_message(self):
        make_files(self.tmp, "already.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_lowercase(self.tmp, dry_run=False)
        self.assertIn("No files needed renaming", out.getvalue())

    def test_already_lowercase_makes_no_changes(self):
        make_files(self.tmp, "already.txt")
        rename_lowercase(self.tmp, dry_run=False)
        self.assertEqual(ls(self.tmp), ["already.txt"])

    def test_empty_folder_prints_message(self):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_lowercase(self.tmp, dry_run=False)
        self.assertIn("No files found", out.getvalue())


class TestRenameRemoveSpaces(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_dry_run_leaves_files_unchanged(self):
        make_files(self.tmp, "hello world.txt")
        rename_remove_spaces(self.tmp, dry_run=True)
        self.assertIn("hello world.txt", ls(self.tmp))

    def test_dry_run_output_contains_marker(self):
        make_files(self.tmp, "hello world.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_remove_spaces(self.tmp, dry_run=True)
        self.assertIn("[DRY RUN]", out.getvalue())

    def test_execute_replaces_spaces_with_default_separator(self):
        make_files(self.tmp, "hello world.txt", "my file.jpg")
        rename_remove_spaces(self.tmp, dry_run=False)
        result = ls(self.tmp)
        self.assertIn("hello_world.txt", result)
        self.assertIn("my_file.jpg", result)

    def test_execute_custom_separator(self):
        make_files(self.tmp, "hello world.txt")
        rename_remove_spaces(self.tmp, separator="-", dry_run=False)
        self.assertIn("hello-world.txt", ls(self.tmp))

    def test_multiple_spaces_all_replaced(self):
        make_files(self.tmp, "a b c.txt")
        rename_remove_spaces(self.tmp, dry_run=False)
        self.assertIn("a_b_c.txt", ls(self.tmp))

    def test_no_spaces_prints_no_op_message(self):
        make_files(self.tmp, "nospaces.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_remove_spaces(self.tmp, dry_run=False)
        self.assertIn("No files with spaces found", out.getvalue())

    def test_empty_folder_prints_message(self):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            rename_remove_spaces(self.tmp, dry_run=False)
        self.assertIn("No files found", out.getvalue())


class TestMoveFiles(unittest.TestCase):
    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.dst = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.src, ignore_errors=True)
        shutil.rmtree(self.dst, ignore_errors=True)

    def test_dry_run_leaves_source_unchanged(self):
        make_files(self.src, "a.txt", "b.jpg")
        move_files(self.src, self.dst, dry_run=True)
        self.assertEqual(ls(self.src), ["a.txt", "b.jpg"])

    def test_dry_run_leaves_destination_empty(self):
        make_files(self.src, "a.txt")
        move_files(self.src, self.dst, dry_run=True)
        self.assertEqual(ls(self.dst), [])

    def test_dry_run_output_contains_marker(self):
        make_files(self.src, "a.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            move_files(self.src, self.dst, dry_run=True)
        self.assertIn("[DRY RUN]", out.getvalue())

    def test_execute_moves_all_files(self):
        make_files(self.src, "a.txt", "b.jpg")
        move_files(self.src, self.dst, dry_run=False)
        self.assertEqual(ls(self.src), [])
        self.assertEqual(ls(self.dst), ["a.txt", "b.jpg"])

    def test_execute_with_glob_moves_only_matches(self):
        make_files(self.src, "a.txt", "b.jpg", "c.txt")
        move_files(self.src, self.dst, pattern="*.txt", dry_run=False)
        self.assertEqual(ls(self.src), ["b.jpg"])
        self.assertIn("a.txt", ls(self.dst))
        self.assertIn("c.txt", ls(self.dst))
        self.assertNotIn("b.jpg", ls(self.dst))

    def test_glob_case_sensitive(self):
        # macOS APFS is case-insensitive, so use distinct base names
        make_files(self.src, "upper.JPG", "lower.jpg")
        move_files(self.src, self.dst, pattern="*.jpg", dry_run=False)
        self.assertIn("lower.jpg", ls(self.dst))
        self.assertIn("upper.JPG", ls(self.src))

    def test_collision_skips_file_leaves_it_in_source(self):
        make_files(self.src, "a.txt")
        make_files(self.dst, "a.txt")
        move_files(self.src, self.dst, dry_run=False)
        self.assertIn("a.txt", ls(self.src))

    def test_collision_prints_skipped_marker(self):
        make_files(self.src, "a.txt")
        make_files(self.dst, "a.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            move_files(self.src, self.dst, dry_run=False)
        self.assertIn("[SKIPPED]", out.getvalue())

    def test_partial_collision_moves_non_colliding_files(self):
        make_files(self.src, "a.txt", "b.txt")
        make_files(self.dst, "a.txt")
        move_files(self.src, self.dst, dry_run=False)
        self.assertNotIn("b.txt", ls(self.src))
        self.assertIn("b.txt", ls(self.dst))

    def test_summary_counts_moved_and_skipped(self):
        make_files(self.src, "a.txt", "b.txt")
        make_files(self.dst, "a.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            move_files(self.src, self.dst, dry_run=False)
        output = out.getvalue()
        self.assertIn("1 file(s) moved", output)
        self.assertIn("1 skipped (collision)", output)

    def test_execute_creates_new_destination_directory(self):
        new_dst = os.path.join(self.dst, "subdir")
        make_files(self.src, "a.txt")
        move_files(self.src, new_dst, dry_run=False)
        self.assertTrue(os.path.isdir(new_dst))
        self.assertIn("a.txt", os.listdir(new_dst))

    def test_dry_run_does_not_create_new_destination(self):
        new_dst = os.path.join(self.dst, "subdir")
        make_files(self.src, "a.txt")
        move_files(self.src, new_dst, dry_run=True)
        self.assertFalse(os.path.exists(new_dst))

    def test_dry_run_announces_new_destination_creation(self):
        new_dst = os.path.join(self.dst, "subdir")
        make_files(self.src, "a.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            move_files(self.src, new_dst, dry_run=True)
        self.assertIn("Would create directory", out.getvalue())

    def test_empty_source_prints_message(self):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            move_files(self.src, self.dst, dry_run=False)
        self.assertIn("No files found", out.getvalue())

    def test_no_pattern_matches_prints_message(self):
        make_files(self.src, "a.txt", "b.txt")
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            move_files(self.src, self.dst, pattern="*.jpg", dry_run=False)
        self.assertIn("No files matched", out.getvalue())
        self.assertEqual(ls(self.src), ["a.txt", "b.txt"])

    def test_no_pattern_matches_leaves_source_unchanged(self):
        make_files(self.src, "a.txt")
        move_files(self.src, self.dst, pattern="*.jpg", dry_run=False)
        self.assertEqual(ls(self.src), ["a.txt"])
        self.assertEqual(ls(self.dst), [])

    def test_subdirectories_in_source_are_ignored(self):
        make_files(self.src, "a.txt")
        os.mkdir(os.path.join(self.src, "subdir"))
        move_files(self.src, self.dst, dry_run=False)
        self.assertIn("subdir", ls(self.src))
        self.assertNotIn("subdir", ls(self.dst))


if __name__ == "__main__":
    unittest.main(verbosity=2)
