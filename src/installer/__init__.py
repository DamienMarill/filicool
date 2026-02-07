"""
Fililico - Installer Package
Scripts d'installation pour les différentes plateformes
"""

from pathlib import Path
import platform

__all__ = []

# Import conditionnel selon la plateforme
system = platform.system()

if system == "Windows":
    from .windows_context_menu import WindowsContextMenuInstaller
    __all__.append("WindowsContextMenuInstaller")
