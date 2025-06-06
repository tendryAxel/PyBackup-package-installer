import os

from pybackup.core import RdiffBackupManager
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
