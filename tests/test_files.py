"""Tests for gdrive_utils.files."""

import os
from pathlib import Path

import pytest

from gdrive_utils.exceptions import FileOperationError
from gdrive_utils.files import move_file


class TestMoveFile:
    """move_file() disk-level tests using a temporary directory."""

    def test_move_success(self, tmp_path: Path) -> None:
        src = tmp_path / "source.txt"
        src.write_text("hello")
        dest = move_file(str(src), "renamed.txt")
        assert os.path.exists(dest)
        assert Path(dest).read_text() == "hello"
        assert not src.exists()

    def test_creates_processed_dir(self, tmp_path: Path) -> None:
        src = tmp_path / "file.txt"
        src.write_text("data")
        dest = move_file(str(src), "file.txt", processed_dir="archived")
        assert os.path.exists(tmp_path / "archived" / "file.txt")
        assert dest == str(tmp_path / "archived" / "file.txt")

    def test_source_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileOperationError, match="not found"):
            move_file(str(tmp_path / "missing.txt"), "x.txt")

    def test_destination_is_directory(self, tmp_path: Path) -> None:
        src = tmp_path / "file.txt"
        src.write_text("data")
        # Create a directory with the same name as the target file
        (tmp_path / "ot_procesados").mkdir()
        (tmp_path / "ot_procesados" / "collision.txt").mkdir()

        with pytest.raises(FileOperationError, match="directory"):
            move_file(str(src), "collision.txt")
