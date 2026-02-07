#!/usr/bin/env python3
"""
🍭 Fililico - macOS Context Menu Integration
Quick Action pour Finder Services
"""

import os
import plistlib
import subprocess
from pathlib import Path
from typing import Optional


class MacOSContextMenuInstaller:
    """
    Gère l'installation du Quick Action macOS pour Fililico.
    Crée un workflow Automator pour le menu contextuel Finder.
    """

    # Extensions supportées
    SUPPORTED_TYPES = [
        "public.png",
        "public.jpeg",
        "com.compuserve.gif",
        "public.bmp",
        "com.adobe.pdf",
    ]

    def __init__(self):
        """Initialise l'installateur."""
        self.home = Path.home()
        self.app_path = self._get_app_path()
        self.services_dir = self.home / "Library" / "Services"

    def _get_app_path(self) -> Path:
        """Retourne le chemin de l'exécutable/script."""
        # En développement
        quick_mode = Path(__file__).parent.parent / "ui" / "quick_mode.py"
        if quick_mode.exists():
            return quick_mode

        # En production
        app_locations = [
            "/Applications/Fililico.app/Contents/MacOS/Fililico",
            self.home / "Applications" / "Fililico.app" / "Contents" / "MacOS" / "Fililico",
        ]
        for loc in app_locations:
            if Path(loc).exists():
                return Path(loc)

        return quick_mode

    def _create_workflow_structure(self, workflow_path: Path) -> bool:
        """
        Crée la structure du workflow Automator.

        Args:
            workflow_path: Chemin du .workflow

        Returns:
            True si réussi
        """
        # Structure du workflow
        contents_dir = workflow_path / "Contents"
        contents_dir.mkdir(parents=True, exist_ok=True)

        # Info.plist
        info_plist = {
            "CFBundleIdentifier": "dev.marill.fililico.quickaction",
            "CFBundleName": "🍭 Ajouter un filigrane",
            "CFBundleShortVersionString": "1.0",
            "CFBundleVersion": "1",
            "NSServices": [
                {
                    "NSMenuItem": {"default": "🍭 Ajouter un filigrane (Fililico)"},
                    "NSMessage": "runWorkflowAsService",
                    "NSSendFileTypes": self.SUPPORTED_TYPES,
                }
            ],
        }

        with open(contents_dir / "Info.plist", "wb") as f:
            plistlib.dump(info_plist, f)

        # document.wflow (le workflow Automator)
        workflow_content = {
            "AMApplicationBuild": "523",
            "AMApplicationVersion": "2.10",
            "AMDocumentVersion": "2",
            "actions": [
                {
                    "action": {
                        "AMActionVersion": "1.0.2",
                        "AMApplication": ["Automator"],
                        "AMAttributes": {
                            "AMAccepts": {
                                "Container": "List",
                                "Optional": True,
                                "Types": ["com.apple.cocoa.path"],
                            },
                            "AMCanShowWhenRun": False,
                            "AMCategory": "Utilities",
                            "AMProvides": {
                                "Container": "List",
                                "Types": ["com.apple.cocoa.string"],
                            },
                        },
                        "AMBundleIdentifier": "com.apple.Automator.RunShellScript",
                        "AMRequiredResources": [],
                    },
                    "class": "AMBundleAction",
                    "name": "Run Shell Script",
                    "parameters": {
                        "COMMAND_STRING": f'''for f in "$@"
do
    python3 "{self.app_path}" "$f"
done''',
                        "CheckedForUserDefaultShell": True,
                        "inputMethod": 1,
                        "shell": "/bin/bash",
                        "source": "",
                    },
                }
            ],
            "connectors": {},
            "workflowMetaData": {
                "applicationBundleID": "com.apple.finder",
                "applicationBundleIDsByPath": {
                    "/System/Library/CoreServices/Finder.app": "com.apple.finder"
                },
                "applicationPath": "/System/Library/CoreServices/Finder.app",
                "inputTypeIdentifier": "com.apple.Automator.fileSystemObject",
                "outputTypeIdentifier": "com.apple.Automator.nothing",
                "serviceInputTypeIdentifier": "com.apple.Automator.fileSystemObject",
                "serviceOutputTypeIdentifier": "com.apple.Automator.nothing",
                "workflowTypeIdentifier": "com.apple.Automator.servicesMenu",
            },
        }

        with open(contents_dir / "document.wflow", "wb") as f:
            plistlib.dump(workflow_content, f)

        return True

    def install(self) -> bool:
        """
        Installe le Quick Action macOS.

        Returns:
            True si l'installation a réussi
        """
        self.services_dir.mkdir(parents=True, exist_ok=True)

        workflow_path = self.services_dir / "Fililico - Ajouter un filigrane.workflow"

        # Supprimer l'ancien si existant
        if workflow_path.exists():
            import shutil
            shutil.rmtree(workflow_path)

        try:
            self._create_workflow_structure(workflow_path)

            # Rafraîchir les services
            subprocess.run(
                ["/System/Library/CoreServices/pbs", "-update"],
                capture_output=True,
            )

            print(f"✅ Quick Action installé : {workflow_path}")
            print("💡 Redémarrez le Finder pour voir le nouveau service")
            return True

        except Exception as e:
            print(f"❌ Erreur installation : {e}")
            return False

    def uninstall(self) -> bool:
        """
        Désinstalle le Quick Action macOS.

        Returns:
            True si la désinstallation a réussi
        """
        workflow_path = self.services_dir / "Fililico - Ajouter un filigrane.workflow"

        if workflow_path.exists():
            import shutil
            shutil.rmtree(workflow_path)
            print(f"🗑️  Supprimé : {workflow_path}")

        # Rafraîchir
        subprocess.run(
            ["/System/Library/CoreServices/pbs", "-update"],
            capture_output=True,
        )

        print("✅ Quick Action désinstallé")
        return True

    def is_installed(self) -> bool:
        """Vérifie si le Quick Action est installé."""
        workflow_path = self.services_dir / "Fililico - Ajouter un filigrane.workflow"
        return workflow_path.exists()


def main():
    """Point d'entrée."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🍭 Fililico - Intégration macOS"
    )
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "status"],
        help="Action à effectuer",
    )
    args = parser.parse_args()

    installer = MacOSContextMenuInstaller()

    if args.action == "install":
        installer.install()
    elif args.action == "uninstall":
        installer.uninstall()
    elif args.action == "status":
        if installer.is_installed():
            print("✅ Quick Action Fililico est installé")
        else:
            print("❌ Quick Action Fililico n'est pas installé")


if __name__ == "__main__":
    main()
