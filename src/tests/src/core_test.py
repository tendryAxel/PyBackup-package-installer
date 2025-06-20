import os

import pytest

from pybackup.core import RdiffBackupManager
from pybackup.exceptions import EmptyBackupTargetException
from tests.utils import create_folder, TestContext


def test_backup_success():
    with TestContext() as context:
        source_folder = create_folder(f"{context.TMP_FOLDER}/source")
        txt_file = "/test.txt"
        open(source_folder + txt_file, "w").close()
        destination_folder = create_folder(f"{context.TMP_FOLDER}/destination")

        RdiffBackupManager().backup(source_folder, destination_folder)

        assert os.path.exists(destination_folder + txt_file) is True


def test_restore_after_backup_success():
    with TestContext() as context:
        manager = RdiffBackupManager()
        source_folder = create_folder(f"{context.TMP_FOLDER}/source")
        txt_file = "/test.txt"
        open(source_folder + txt_file, "w").close()
        destination_folder = create_folder(f"{context.TMP_FOLDER}/destination")

        # Backup file
        manager.backup(source_folder, destination_folder)

        # Destroy source folder
        os.remove(source_folder + txt_file)

        # Restore source folder
        manager.restore(destination_folder, source_folder)

        assert os.path.exists(source_folder + txt_file) is True


def test_list_backup_of_not_empty_backup_folder_fail():
    with TestContext() as context:
        manager = RdiffBackupManager()
        source_folder = create_folder(f"{context.TMP_FOLDER}/source")
        txt_file = "/test.txt"
        open(source_folder + txt_file, "w").close()

        with pytest.raises(EmptyBackupTargetException):
            manager.list_increments(source_folder)


def test_list_backup_of_empty_backup_folder_success():
    with TestContext() as context:
        manager = RdiffBackupManager()
        source_folder = create_folder(f"{context.TMP_FOLDER}/source")
        txt_file = "/test.txt"
        open(source_folder + txt_file, "w").close()
        destination_folder = create_folder(f"{context.TMP_FOLDER}/destination")

        work, increments = manager.list_increments(destination_folder)

        assert work
        assert increments == []
