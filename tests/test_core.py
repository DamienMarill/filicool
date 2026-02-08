"""
🍭 Fillico - Tests Unitaires
Tests pour le Core Engine (watermark_engine, image_processor, pdf_processor)
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core import WatermarkEngine, ImageProcessor, PDFProcessor
from core.watermark_engine import FileType, ProcessingResult


class TestImageProcessor:
    """Tests pour ImageProcessor."""

    def test_supported_formats(self):
        """Vérifie les formats supportés."""
        processor = ImageProcessor()

        assert processor.is_supported(Path("test.png"))
        assert processor.is_supported(Path("test.jpg"))
        assert processor.is_supported(Path("test.jpeg"))
        assert processor.is_supported(Path("test.bmp"))
        assert processor.is_supported(Path("test.gif"))
        assert not processor.is_supported(Path("test.txt"))
        assert not processor.is_supported(Path("test.pdf"))

    def test_init_with_defaults(self):
        """Vérifie l'initialisation avec les valeurs par défaut."""
        processor = ImageProcessor()

        assert processor.text == "CONFIDENTIEL"
        assert processor.opacity == 0.5

    def test_init_with_custom_values(self):
        """Vérifie l'initialisation avec des valeurs personnalisées."""
        processor = ImageProcessor(text="TEST", opacity=0.8)

        assert processor.text == "TEST"
        assert processor.opacity == 0.8

    def test_opacity_clamping(self):
        """Vérifie que l'opacité est limitée entre 0 et 1."""
        processor = ImageProcessor(opacity=1.5)
        assert processor.opacity == 1.0

        processor = ImageProcessor(opacity=-0.5)
        assert processor.opacity == 0.0

    def test_process_file_not_found(self):
        """Vérifie la gestion des fichiers inexistants."""
        processor = ImageProcessor()

        with pytest.raises(FileNotFoundError):
            processor.process(Path("fichier_inexistant.png"))

    def test_process_unsupported_format(self):
        """Vérifie la gestion des formats non supportés."""
        processor = ImageProcessor()

        # Créer un fichier temporaire avec extension non supportée
        test_file = Path(__file__).parent / "temp_test.txt"
        test_file.write_text("test")

        try:
            with pytest.raises(ValueError):
                processor.process(test_file)
        finally:
            test_file.unlink()


class TestPDFProcessor:
    """Tests pour PDFProcessor."""

    def test_supported_formats(self):
        """Vérifie les formats supportés."""
        processor = PDFProcessor()

        assert processor.is_supported(Path("test.pdf"))
        assert not processor.is_supported(Path("test.png"))
        assert not processor.is_supported(Path("test.txt"))

    def test_init_with_defaults(self):
        """Vérifie l'initialisation avec les valeurs par défaut."""
        processor = PDFProcessor()

        assert processor.text == "CONFIDENTIEL"
        assert processor.opacity == 0.3

    def test_process_file_not_found(self):
        """Vérifie la gestion des fichiers inexistants."""
        processor = PDFProcessor()

        with pytest.raises(FileNotFoundError):
            processor.process(Path("fichier_inexistant.pdf"))


class TestWatermarkEngine:
    """Tests pour WatermarkEngine."""

    def test_init_with_defaults(self):
        """Vérifie l'initialisation avec les valeurs par défaut."""
        engine = WatermarkEngine()

        assert engine.text == "CONFIDENTIEL"
        assert engine.opacity == 0.5

    def test_init_with_custom_values(self):
        """Vérifie l'initialisation avec des valeurs personnalisées."""
        engine = WatermarkEngine(text="CUSTOM", opacity=0.7)

        assert engine.text == "CUSTOM"
        assert engine.opacity == 0.7

    def test_get_file_type_image(self):
        """Vérifie la détection des types d'images."""
        engine = WatermarkEngine()

        assert engine.get_file_type(Path("test.png")) == FileType.IMAGE
        assert engine.get_file_type(Path("test.jpg")) == FileType.IMAGE
        assert engine.get_file_type(Path("test.jpeg")) == FileType.IMAGE
        assert engine.get_file_type(Path("test.bmp")) == FileType.IMAGE
        assert engine.get_file_type(Path("test.gif")) == FileType.IMAGE

    def test_get_file_type_pdf(self):
        """Vérifie la détection des PDF."""
        engine = WatermarkEngine()

        assert engine.get_file_type(Path("test.pdf")) == FileType.PDF

    def test_get_file_type_unknown(self):
        """Vérifie la détection des types inconnus."""
        engine = WatermarkEngine()

        assert engine.get_file_type(Path("test.txt")) == FileType.UNKNOWN
        assert engine.get_file_type(Path("test.doc")) == FileType.UNKNOWN

    def test_is_supported(self):
        """Vérifie la vérification de support."""
        engine = WatermarkEngine()

        assert engine.is_supported(Path("test.png"))
        assert engine.is_supported(Path("test.pdf"))
        assert not engine.is_supported(Path("test.txt"))

    def test_get_supported_extensions(self):
        """Vérifie la liste des extensions supportées."""
        engine = WatermarkEngine()
        extensions = engine.get_supported_extensions()

        assert ".png" in extensions
        assert ".jpg" in extensions
        assert ".pdf" in extensions
        assert ".txt" not in extensions

    def test_text_property_updates_processors(self):
        """Vérifie que modifier le texte met à jour les processeurs."""
        engine = WatermarkEngine(text="INITIAL")
        assert engine.text == "INITIAL"

        engine.text = "UPDATED"
        assert engine.text == "UPDATED"
        assert engine._image_processor.text == "UPDATED"
        assert engine._pdf_processor.text == "UPDATED"

    def test_opacity_property_updates_processors(self):
        """Vérifie que modifier l'opacité met à jour les processeurs."""
        engine = WatermarkEngine(opacity=0.5)
        assert engine.opacity == 0.5

        engine.opacity = 0.8
        assert engine.opacity == 0.8
        assert engine._image_processor.opacity == 0.8
        assert engine._pdf_processor.opacity == 0.8

    def test_process_unsupported_file(self):
        """Vérifie le traitement d'un fichier non supporté."""
        engine = WatermarkEngine()
        result = engine.process(Path("test.txt"))

        assert isinstance(result, ProcessingResult)
        assert result.success is False
        assert result.error is not None
        assert result.file_type == FileType.UNKNOWN


class TestProcessingResult:
    """Tests pour ProcessingResult."""

    def test_success_result(self):
        """Vérifie la création d'un résultat de succès."""
        result = ProcessingResult(
            input_path=Path("input.png"),
            output_path=Path("output.png"),
            success=True,
            file_type=FileType.IMAGE,
        )

        assert result.success
        assert result.error is None
        assert result.input_path == Path("input.png")
        assert result.output_path == Path("output.png")

    def test_error_result(self):
        """Vérifie la création d'un résultat d'erreur."""
        result = ProcessingResult(
            input_path=Path("input.png"),
            output_path=None,
            success=False,
            error="Test error",
            file_type=FileType.IMAGE,
        )

        assert not result.success
        assert result.error == "Test error"
        assert result.output_path is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
