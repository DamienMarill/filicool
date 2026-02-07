#!/usr/bin/env python3
"""
🍭 Fililico - Linux Context Menu Integration
Scripts pour Nautilus (GNOME) et Dolphin (KDE)
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional


class LinuxContextMenuInstaller:
    """
    Gère l'installation du menu contextuel Linux pour Fililico.
    Supporte Nautilus (GNOME) et Dolphin (KDE).
    """

    def __init__(self):
        """Initialise l'installateur."""
        self.home = Path.home()
        self.app_path = self._get_app_path()
        self.desktop_env = self._detect_desktop_environment()

    def _get_app_path(self) -> Path:
        """Retourne le chemin de l'exécutable/script."""
        # En développement
        quick_mode = Path(__file__).parent.parent / "ui" / "quick_mode.py"
        if quick_mode.exists():
            return quick_mode

        # En production (après installation)
        for path in ["/usr/local/bin/fililico", "/opt/fililico/fililico"]:
            if Path(path).exists():
                return Path(path)

        return quick_mode

    def _detect_desktop_environment(self) -> str:
        """Détecte l'environnement de bureau."""
        de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        session = os.environ.get("DESKTOP_SESSION", "").lower()

        if "gnome" in de or "gnome" in session:
            return "gnome"
        elif "kde" in de or "plasma" in de or "kde" in session:
            return "kde"
        elif "xfce" in de:
            return "xfce"
        else:
            return "unknown"

    def _get_nautilus_scripts_dir(self) -> Path:
        """Retourne le dossier des scripts Nautilus."""
        # Priorité au chemin XDG
        xdg_data = os.environ.get("XDG_DATA_HOME", self.home / ".local/share")
        nautilus_dir = Path(xdg_data) / "nautilus" / "scripts"

        # Fallback vers l'ancien chemin
        if not nautilus_dir.parent.exists():
            nautilus_dir = self.home / ".gnome2" / "nautilus-scripts"

        return nautilus_dir

    def _get_dolphin_service_dir(self) -> Path:
        """Retourne le dossier des services Dolphin."""
        xdg_data = os.environ.get("XDG_DATA_HOME", self.home / ".local/share")
        return Path(xdg_data) / "kservices5" / "ServiceMenus"

    def install_nautilus(self) -> bool:
        """
        Installe le script pour Nautilus (GNOME).

        Returns:
            True si l'installation a réussi
        """
        scripts_dir = self._get_nautilus_scripts_dir()
        scripts_dir.mkdir(parents=True, exist_ok=True)

        script_path = scripts_dir / "🍭 Fililico - Ajouter un filigrane"

        script_content = f'''#!/bin/bash
# 🍭 Fililico - Script Nautilus
# Ajoute un filigrane aux fichiers sélectionnés

# Récupérer les fichiers sélectionnés
IFS=$'\\n'
for file in $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS; do
    if [[ -f "$file" ]]; then
        python3 "{self.app_path}" "$file"
    fi
done
'''

        try:
            script_path.write_text(script_content)
            os.chmod(script_path, 0o755)
            print(f"✅ Script Nautilus installé : {script_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur installation Nautilus : {e}")
            return False

    def install_dolphin(self) -> bool:
        """
        Installe le service pour Dolphin (KDE).

        Returns:
            True si l'installation a réussi
        """
        service_dir = self._get_dolphin_service_dir()
        service_dir.mkdir(parents=True, exist_ok=True)

        desktop_path = service_dir / "fililico.desktop"

        desktop_content = f'''[Desktop Entry]
Type=Service
ServiceTypes=KonqPopupMenu/Plugin
MimeType=image/png;image/jpeg;image/bmp;image/gif;application/pdf;
Actions=watermark

[Desktop Action watermark]
Name=🍭 Ajouter un filigrane (Fililico)
Icon=applications-graphics
Exec=python3 "{self.app_path}" %f
'''

        try:
            desktop_path.write_text(desktop_content)
            print(f"✅ Service Dolphin installé : {desktop_path}")

            # Rafraîchir le cache
            subprocess.run(["kbuildsycoca5"], capture_output=True)
            return True
        except Exception as e:
            print(f"❌ Erreur installation Dolphin : {e}")
            return False

    def install_desktop_entry(self) -> bool:
        """
        Installe l'entrée .desktop pour l'application complète.

        Returns:
            True si l'installation a réussi
        """
        xdg_data = os.environ.get("XDG_DATA_HOME", self.home / ".local/share")
        apps_dir = Path(xdg_data) / "applications"
        apps_dir.mkdir(parents=True, exist_ok=True)

        desktop_path = apps_dir / "fililico.desktop"
        icon_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"

        desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Fililico
GenericName=Watermark Tool
Comment=🍭 Application de filigranage kawaii
Exec=python3 "{self.app_path.parent.parent / "main.py"}"
Icon={icon_path if icon_path.exists() else "applications-graphics"}
Terminal=false
Categories=Graphics;Utility;
MimeType=image/png;image/jpeg;image/bmp;image/gif;application/pdf;
Keywords=watermark;filigrane;image;pdf;
'''

        try:
            desktop_path.write_text(desktop_content)
            os.chmod(desktop_path, 0o755)
            print(f"✅ Entrée desktop installée : {desktop_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur installation desktop entry : {e}")
            return False

    def install(self) -> bool:
        """
        Installe l'intégration système selon l'environnement détecté.

        Returns:
            True si au moins une installation a réussi
        """
        success = False

        print(f"🔍 Environnement détecté : {self.desktop_env}")

        # Toujours installer l'entrée desktop
        if self.install_desktop_entry():
            success = True

        # Installer selon l'environnement
        if self.desktop_env == "gnome":
            if self.install_nautilus():
                success = True
        elif self.desktop_env == "kde":
            if self.install_dolphin():
                success = True
        else:
            # Installer les deux par défaut
            print("⚠️  Environnement non détecté, installation des deux...")
            self.install_nautilus()
            self.install_dolphin()
            success = True

        return success

    def uninstall(self) -> bool:
        """
        Désinstalle l'intégration système.

        Returns:
            True si la désinstallation a réussi
        """
        files_to_remove = [
            self._get_nautilus_scripts_dir() / "🍭 Fililico - Ajouter un filigrane",
            self._get_dolphin_service_dir() / "fililico.desktop",
            Path(os.environ.get("XDG_DATA_HOME", self.home / ".local/share"))
            / "applications"
            / "fililico.desktop",
        ]

        for file_path in files_to_remove:
            if file_path.exists():
                file_path.unlink()
                print(f"🗑️  Supprimé : {file_path}")

        print("✅ Intégration système désinstallée")
        return True


def main():
    """Point d'entrée."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🍭 Fililico - Intégration Linux"
    )
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "status"],
        help="Action à effectuer",
    )
    args = parser.parse_args()

    installer = LinuxContextMenuInstaller()

    if args.action == "install":
        installer.install()
    elif args.action == "uninstall":
        installer.uninstall()
    elif args.action == "status":
        print(f"🔍 Environnement : {installer.desktop_env}")
        print(f"📁 Scripts Nautilus : {installer._get_nautilus_scripts_dir()}")
        print(f"📁 Services Dolphin : {installer._get_dolphin_service_dir()}")


if __name__ == "__main__":
    main()
