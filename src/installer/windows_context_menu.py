"""
🍭 Fililico - Windows Context Menu Integration
Script d'installation/désinstallation du menu contextuel Windows
"""

import sys
import winreg
from pathlib import Path
from typing import List


class WindowsContextMenuInstaller:
    """
    Gère l'installation du menu contextuel Windows pour Fililico.
    Ajoute "Ajouter un filigrane" au clic droit sur les fichiers supportés.
    """

    # Extensions supportées
    SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".pdf"]

    # Clé de registre pour le shell
    SHELL_KEY = r"*\shell\Fililico"
    COMMAND_KEY = r"*\shell\Fililico\command"

    def __init__(self):
        """Initialise l'installateur."""
        self.app_path = self._get_app_path()

    def _get_app_path(self) -> Path:
        """Retourne le chemin de l'exécutable/script."""
        # En développement, utiliser le script Python
        quick_mode_path = Path(__file__).parent / "quick_mode.py"
        if quick_mode_path.exists():
            return quick_mode_path

        # En production, chercher l'exécutable
        exe_path = Path(sys.executable).parent / "fililico.exe"
        if exe_path.exists():
            return exe_path

        return quick_mode_path

    def _get_python_path(self) -> str:
        """Retourne le chemin de Python."""
        return sys.executable

    def install(self) -> bool:
        """
        Installe le menu contextuel Windows.

        Returns:
            True si l'installation a réussi
        """
        try:
            # Créer la clé principale du shell
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, self.SHELL_KEY) as key:
                # Nom affiché dans le menu contextuel
                winreg.SetValue(key, "", winreg.REG_SZ, "🍭 Ajouter un filigrane")

                # Icône (utiliser l'icône de l'app si disponible)
                icon_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.ico"
                if icon_path.exists():
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, str(icon_path))

            # Créer la commande
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, self.COMMAND_KEY) as key:
                if self.app_path.suffix == ".py":
                    # Mode développement - utiliser Python
                    command = f'"{self._get_python_path()}" "{self.app_path}" "%1"'
                else:
                    # Mode production - exécutable direct
                    command = f'"{self.app_path}" "%1"'

                winreg.SetValue(key, "", winreg.REG_SZ, command)

            print("✅ Menu contextuel installé avec succès!")
            print(f"   Commande: {command}")
            return True

        except PermissionError:
            print("❌ Erreur: Exécutez ce script en tant qu'administrateur!")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de l'installation: {e}")
            return False

    def uninstall(self) -> bool:
        """
        Désinstalle le menu contextuel Windows.

        Returns:
            True si la désinstallation a réussi
        """
        try:
            # Supprimer la clé command d'abord
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, self.COMMAND_KEY)
            except FileNotFoundError:
                pass

            # Puis la clé principale
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, self.SHELL_KEY)
            except FileNotFoundError:
                pass

            print("✅ Menu contextuel désinstallé avec succès!")
            return True

        except PermissionError:
            print("❌ Erreur: Exécutez ce script en tant qu'administrateur!")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la désinstallation: {e}")
            return False

    def is_installed(self) -> bool:
        """
        Vérifie si le menu contextuel est installé.

        Returns:
            True si installé
        """
        try:
            winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, self.SHELL_KEY)
            return True
        except FileNotFoundError:
            return False


def main():
    """Point d'entrée pour l'installation/désinstallation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🍭 Fililico - Gestionnaire du menu contextuel Windows"
    )
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "status"],
        help="Action à effectuer",
    )
    args = parser.parse_args()

    installer = WindowsContextMenuInstaller()

    if args.action == "install":
        installer.install()
    elif args.action == "uninstall":
        installer.uninstall()
    elif args.action == "status":
        if installer.is_installed():
            print("✅ Le menu contextuel Fililico est installé")
        else:
            print("❌ Le menu contextuel Fililico n'est pas installé")


if __name__ == "__main__":
    main()
