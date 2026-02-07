"""
Fililico - Image Processor
Gère le filigranage des fichiers images (PNG, JPG, JPEG, BMP, GIF)
"""

from pathlib import Path
from typing import Optional, Tuple
import base64
import io

from PIL import Image, ImageDraw, ImageFont


class ImageProcessor:
    """Processeur de filigrane pour les images."""

    SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    def __init__(
        self,
        text: str = "CONFIDENTIEL",
        opacity: float = 0.5,
        font_size_ratio: float = 0.10,
        min_font_size: int = 20,
        max_font_size: int = 200,
    ):
        """
        Initialise le processeur d'images.

        Args:
            text: Texte du filigrane
            opacity: Opacité du filigrane (0.0 à 1.0)
            font_size_ratio: Ratio de la taille de police par rapport à l'image
            min_font_size: Taille minimale de la police
            max_font_size: Taille maximale de la police
        """
        self.text = text
        self.opacity = max(0.0, min(1.0, opacity))
        self.font_size_ratio = font_size_ratio
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        """Vérifie si le format de fichier est supporté."""
        return file_path.suffix.lower() in cls.SUPPORTED_FORMATS

    def _calculate_font_size(self, image_size: Tuple[int, int]) -> int:
        """Calcule la taille de police optimale basée sur les dimensions de l'image."""
        min_dimension = min(image_size)
        calculated_size = int(min_dimension * self.font_size_ratio)
        return max(self.min_font_size, min(self.max_font_size, calculated_size))

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Charge une police avec fallback sur la police par défaut."""
        font_names = [
            "arial.ttf",
            "Arial.ttf",
            "DejaVuSans.ttf",
            "FreeSans.ttf",
            "NotoSans-Regular.ttf",
        ]

        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except (IOError, OSError):
                continue

        # Fallback sur la police par défaut de Pillow
        return ImageFont.load_default()

    def _create_watermark_layer(
        self, size: Tuple[int, int], font: ImageFont.FreeTypeFont
    ) -> Image.Image:
        """Crée un layer transparent avec le texte du filigrane."""
        # Créer un layer RGBA transparent
        watermark = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Calculer les dimensions du texte
        bbox = draw.textbbox((0, 0), self.text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Positionner au centre
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2

        # Calculer l'opacité (0-255)
        alpha = int(255 * self.opacity)

        # Dessiner le texte en blanc semi-transparent
        draw.text((x, y), self.text, font=font, fill=(255, 255, 255, alpha))

        return watermark

    def process(
        self, input_path: Path, output_path: Optional[Path] = None
    ) -> Path:
        """
        Applique le filigrane sur une image.

        Args:
            input_path: Chemin du fichier source
            output_path: Chemin de sortie (optionnel, génère automatiquement si None)

        Returns:
            Chemin du fichier créé

        Raises:
            FileNotFoundError: Si le fichier source n'existe pas
            ValueError: Si le format n'est pas supporté
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {input_path}")

        if not self.is_supported(input_path):
            raise ValueError(
                f"Format non supporté: {input_path.suffix}. "
                f"Formats supportés: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # Générer le chemin de sortie si non spécifié
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_watermarked{input_path.suffix}"

        # Ouvrir l'image et convertir en RGBA
        with Image.open(input_path) as img:
            # Conserver le format original
            original_format = img.format
            original_mode = img.mode

            # Convertir en RGBA pour la composition
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            # Calculer la taille de police et obtenir la police
            font_size = self._calculate_font_size(img.size)
            font = self._get_font(font_size)

            # Créer le layer de filigrane
            watermark = self._create_watermark_layer(img.size, font)

            # Composer l'image finale
            result = Image.alpha_composite(img, watermark)

            # Convertir en RGB si le format original ne supporte pas la transparence
            if input_path.suffix.lower() in {".jpg", ".jpeg", ".bmp"}:
                result = result.convert("RGB")

            # Sauvegarder
            result.save(output_path)

        return output_path

    def generate_preview(
        self, input_path: Path, max_size: Tuple[int, int] = (800, 600)
    ) -> str:
        """
        Génère une preview en base64 de l'image avec filigrane.

        Args:
            input_path: Chemin du fichier source
            max_size: Dimensions maximales de la preview

        Returns:
            Chaîne base64 de l'image preview
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {input_path}")

        with Image.open(input_path) as img:
            # Créer une copie pour ne pas modifier l'original
            preview = img.copy()

            # Redimensionner pour la preview
            preview.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Convertir en RGBA
            if preview.mode != "RGBA":
                preview = preview.convert("RGBA")

            # Calculer la taille de police et obtenir la police
            font_size = self._calculate_font_size(preview.size)
            font = self._get_font(font_size)

            # Créer le layer de filigrane
            watermark = self._create_watermark_layer(preview.size, font)

            # Composer
            result = Image.alpha_composite(preview, watermark)

            # Convertir en RGB pour le format JPEG
            result = result.convert("RGB")

            # Encoder en base64
            buffer = io.BytesIO()
            result.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)

            return base64.b64encode(buffer.read()).decode("utf-8")
