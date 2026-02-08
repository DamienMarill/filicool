"""
Fillico - Image Processor
Gère le filigranage des fichiers images (PNG, JPG, JPEG, BMP, GIF)
"""

from pathlib import Path
from typing import Optional, Tuple
import base64
import io

from PIL import Image

from .watermark_renderer import WatermarkRenderer


class ImageProcessor:
    """Processeur de filigrane pour les images."""

    SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    def __init__(
        self,
        text: str = "CONFIDENTIEL",
        opacity: float = 0.3,
        font_size_ratio: float = 0.08,
        min_font_size: int = 16,
        max_font_size: int = 120,
        pattern: str = "tiled",
        rotation: int = -45,
        spacing: float = 1.8,
        outline: bool = True,
        text_color: Tuple[int, int, int] = (0, 0, 0),
        outline_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        """Initialise le processeur d'images avec le renderer partagé."""
        self.renderer = WatermarkRenderer(
            text=text,
            opacity=opacity,
            font_size_ratio=font_size_ratio,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            pattern=pattern,
            rotation=rotation,
            spacing=spacing,
            outline=outline,
            text_color=text_color,
            outline_color=outline_color,
        )

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        """Vérifie si le format de fichier est supporté."""
        return file_path.suffix.lower() in cls.SUPPORTED_FORMATS

    def process(
        self, input_path: Path, output_path: Optional[Path] = None
    ) -> Path:
        """
        Applique le filigrane sur une image.

        Args:
            input_path: Chemin du fichier source
            output_path: Chemin de sortie (optionnel)

        Returns:
            Chemin du fichier créé
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {input_path}")

        if not self.is_supported(input_path):
            raise ValueError(
                f"Format non supporté: {input_path.suffix}. "
                f"Formats supportés: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_watermarked{input_path.suffix}"

        with Image.open(input_path) as img:
            # Appliquer le filigrane
            result = self.renderer.apply_watermark(img)

            # Convertir en RGB si le format ne supporte pas la transparence
            if input_path.suffix.lower() in {".jpg", ".jpeg", ".bmp"}:
                result = result.convert("RGB")

            result.save(output_path)

        return output_path

    def generate_preview(
        self, input_path: Path, max_size: Tuple[int, int] = (800, 600)
    ) -> str:
        """Génère une preview en base64 de l'image avec filigrane."""
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {input_path}")

        with Image.open(input_path) as img:
            preview = img.copy()
            preview.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Appliquer le filigrane
            result = self.renderer.apply_watermark(preview)
            result = result.convert("RGB")

            buffer = io.BytesIO()
            result.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)

            return base64.b64encode(buffer.read()).decode("utf-8")
