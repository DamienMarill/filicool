"""
🍭 Fililico - UI Application
Point d'entrée de l'application avec Eel
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import eel
from core import WatermarkEngine

# Initialize Eel with web folder
WEB_FOLDER = Path(__file__).parent.parent.parent / "web"
eel.init(str(WEB_FOLDER))

# Global engine instance
engine = WatermarkEngine()


@eel.expose
def process_file(
    file_path: str,
    watermark_text: str = "CONFIDENTIEL",
    opacity: float = 0.5,
    output_folder: str = None,
) -> dict:
    """
    Traite un fichier (image ou PDF) avec un filigrane.

    Args:
        file_path: Chemin du fichier à traiter
        watermark_text: Texte du filigrane
        opacity: Opacité (0.0 à 1.0)
        output_folder: Dossier de sortie optionnel

    Returns:
        Dictionnaire avec le résultat du traitement
    """
    try:
        # Update engine settings
        engine.text = watermark_text
        engine.opacity = opacity

        # Calculate output path
        input_path = Path(file_path)
        if output_folder:
            output_path = Path(output_folder) / f"{input_path.stem}_watermarked{input_path.suffix}"
        else:
            output_path = None

        # Process
        result = engine.process(input_path, output_path)

        if result.success:
            return {
                "success": True,
                "input": str(result.input_path.name),
                "output": str(result.output_path.name),
                "output_path": str(result.output_path),
            }
        else:
            return {
                "success": False,
                "input": str(result.input_path.name),
                "error": result.error,
            }

    except Exception as e:
        return {
            "success": False,
            "input": Path(file_path).name if file_path else "unknown",
            "error": str(e),
        }


@eel.expose
def generate_preview(file_path: str, watermark_text: str, opacity: float) -> dict:
    """
    Génère un aperçu du filigrane.

    Args:
        file_path: Chemin du fichier
        watermark_text: Texte du filigrane
        opacity: Opacité

    Returns:
        Dictionnaire avec l'image en base64
    """
    try:
        engine.text = watermark_text
        engine.opacity = opacity

        preview = engine.generate_preview(file_path)

        if preview:
            return {
                "success": True,
                "preview": preview,
            }
        else:
            return {
                "success": False,
                "error": "Format non supporté pour la prévisualisation",
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@eel.expose
def get_supported_formats() -> list:
    """Retourne la liste des formats supportés."""
    return list(engine.get_supported_extensions())


@eel.expose
def check_file_supported(file_path: str) -> bool:
    """Vérifie si un fichier est supporté."""
    return engine.is_supported(Path(file_path))


def start_app():
    """Démarre l'application Eel."""
    print("🍭 Fililico - Démarrage...")

    try:
        # Start Eel with default browser
        eel.start(
            "index.html",
            size=(1200, 800),
            position=(100, 100),
            mode="chrome",  # or 'edge', 'default'
        )
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    except Exception as e:
        print(f"❌ Erreur: {e}")
        # Fallback to default browser
        eel.start("index.html", mode="default")


if __name__ == "__main__":
    start_app()
