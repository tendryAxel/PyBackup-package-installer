import subprocess
import re
import sys
from typing import List, Tuple, Optional, Callable

from pybackup.type import Increment, parse_increments


class RdiffBackupManager:
    def __init__(self, rdiff_path: str = "rdiff-backup"):
        """
        Initialise le gestionnaire de sauvegarde.

        Args:
            rdiff_path: Chemin vers l'exécutable rdiff-backup
        """
        self.rdiff_path = rdiff_path

    def _run_command(
        self,
        args: List[str],
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> Tuple[bool, str]:
        """
        Exécute une commande rdiff-backup avec capture de la progression.

        Args:
            args: Arguments à passer à rdiff-backup
            progress_callback: Fonction de rappel pour la progression

        Returns:
            Tuple (succès, sortie)
        """
        process = subprocess.Popen(
            [self.rdiff_path] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        output = []
        while True:
            line = process.stdout.readline()
            if line == "" and process.poll() is not None:
                break
            if line:
                output.append(line)
                if progress_callback:
                    progress = self._parse_progress(line)
                    if progress is not None:
                        progress_callback(progress, line.strip())

        return process.returncode == 0, "".join(output)

    @staticmethod
    def _parse_progress(line: str) -> Optional[float]:
        """
        Extrait la progression d'une ligne de sortie.
        """
        match = re.search(r"(\d+\.\d+)%", line)
        return float(match.group(1)) if match else None

    def backup(
        self,
        source: str,
        dest: str,
        exclude: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        force: bool = False,
        verbosity: int = 3,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> Tuple[bool, str]:
        """
        Effectue une sauvegarde incrémentielle.

        Args:
            source: Chemin source
            dest: Chemin destination
            exclude: Listes d'exclusions
            include: Listes d'inclusions
            force: Forcer l'opération
            verbosity: Niveau de verbosité (0-9)
            progress_callback: Callback pour la progression

        Returns:
            Tuple (succès, sortie)
        """
        args = []

        if force:
            args.append("--force")

        if exclude:
            for pattern in exclude:
                args.extend(["--exclude", pattern])

        if include:
            for pattern in include:
                args.extend(["--include", pattern])

        args.extend(["--verbosity", str(verbosity), source, dest])

        return self._run_command(args, progress_callback)

    def restore(
        self,
        backup_path: str,
        dest: str,
        restore_time: str = "now",
        force: bool = False,
        verbosity: int = 3,
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> Tuple[bool, str]:
        """
        Restaure une sauvegarde.

        Args:
            backup_path: Chemin de la sauvegarde
            dest: Chemin de destination
            restore_time: Moment de restauration (format rdiff-backup)
            force: Forcer l'opération
            verbosity: Niveau de verbosité (0-9)
            progress_callback: Callback pour la progression

        Returns:
            Tuple (succès, sortie)
        """
        args = ["--restore-as-of", restore_time, "--verbosity", str(verbosity)]

        if force:
            args.append("--force")

        args.extend([backup_path, dest])

        return self._run_command(args, progress_callback)

    def list_increments(self, backup_path: str) -> Tuple[bool, List[Increment]]:
        """
        Liste les points de restauration disponibles.

        Args:
            backup_path: Chemin de la sauvegarde
            verbosity: Niveau de verbosité

        Returns:
            Increments
        """
        success, output = self._run_command(
            ["list", "increments", "--size", backup_path]
        )

        if not success:
            return False, []

        return True, parse_increments(output)


# Exemple d'utilisation
if __name__ == "__main__":

    def print_progress(progress: float, message: str):
        sys.stdout.write(f"\rProgression: {progress:.1f}% - {message}")
        sys.stdout.flush()
        if progress >= 100:
            print()

    manager = RdiffBackupManager()

    # Exemple de sauvegarde
    print("Début de la sauvegarde...")
    success, output = manager.backup(
        source="/chemin/vers/source",
        dest="/chemin/vers/backup",
        exclude=["*.tmp", "/chemin/vers/source/logs"],
        progress_callback=print_progress,
    )

    if success:
        print("\nSauvegarde réussie!")
    else:
        print("\nÉchec de la sauvegarde:")
        print(output)

    # Exemple de liste des incréments
    print("\nListe des points de restauration:")
    success, increments = manager.list_increments("/chemin/vers/backup")
    if success:
        for increments in increments:
            print(f"{increments}")

    # Exemple de restauration
    print("\nDébut de la restauration...")
    success, output = manager.restore(
        backup_path="/chemin/vers/backup",
        dest="/chemin/vers/restauration",
        restore_time="3D",  # Il y a 3 jours
        progress_callback=print_progress,
    )

    if success:
        print("\nRestauration réussie!")
    else:
        print("\nÉchec de la restauration:")
        print(output)
