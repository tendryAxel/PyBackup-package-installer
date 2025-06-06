from rdiff_backup import Main as RdiffMain
from pathlib import Path
from typing import Optional
import sys

def _run_rdiff(args: list[str]):
    old_argv = sys.argv
    sys.argv = args
    try:
        RdiffMain.Main(args)
    finally:
        sys.argv = old_argv


def backup(source: str, backup_dir: str):
    """
    Sauvegarde incrémentale avec rdiff-backup.
    Le répertoire `backup_dir` contiendra les données actuelles + incréments.
    """
    source = str(Path(source).resolve())
    backup_dir = str(Path(backup_dir).resolve())

    _run_rdiff(["rdiff-backup", source, backup_dir])


def restore(backup_dir: str, restore_path: str, time: Optional[str] = None):
    """
    Restaure depuis un backup rdiff-backup. Si `time` est donné, utilise un snapshot précis.
    Le paramètre `time` peut être une durée ("3D", "1h", "30m"), ou une date exacte.
    """
    backup_dir = str(Path(backup_dir).resolve())
    restore_path = str(Path(restore_path).resolve())

    args = ["rdiff-backup"]
    if time:
        args += ["--restore-as-of", time]
    else:
        args += ["-r", "now"]
    args += [backup_dir, restore_path]

    _run_rdiff(args)
