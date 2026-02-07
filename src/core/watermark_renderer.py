"""
Fililico - Watermark Renderer
Logique de rendu du filigrane partagée entre images et PDFs
"""

from typing import Tuple
import math

from PIL import Image, ImageDraw, ImageFont


class WatermarkRenderer:
    """Classe utilitaire pour créer des filigranes sur des images PIL."""

    def __init__(
        self,
        text: str = "CONFIDENTIEL",
        opacity: float = 0.3,
        font_size_ratio: float = 0.08,
        min_font_size: int = 16,
        max_font_size: int = 120,
        pattern: str = "tiled",  # "single" ou "tiled"
        rotation: int = -45,  # Angle en degrés
        spacing: float = 1.8,  # Espacement entre répétitions
        outline: bool = True,  # Contour du texte
        text_color: Tuple[int, int, int] = (0, 0, 0),  # Noir
        outline_color: Tuple[int, int, int] = (255, 255, 255),  # Blanc
    ):
        """
        Initialise le renderer de filigrane.

        Args:
            text: Texte du filigrane
            opacity: Opacité du filigrane (0.0 à 1.0)
            font_size_ratio: Ratio de la taille de police par rapport à l'image
            min_font_size: Taille minimale de la police
            max_font_size: Taille maximale de la police
            pattern: Mode de rendu ("single" centré ou "tiled" répété)
            rotation: Angle de rotation en degrés
            spacing: Multiplicateur d'espacement entre répétitions
            outline: Ajouter un contour au texte
            text_color: Couleur du texte (RGB)
            outline_color: Couleur du contour (RGB)
        """
        self.text = text
        self.opacity = max(0.0, min(1.0, opacity))
        self.font_size_ratio = font_size_ratio
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size
        self.pattern = pattern
        self.rotation = rotation
        self.spacing = spacing
        self.outline = outline
        self.text_color = text_color
        self.outline_color = outline_color

    def calculate_font_size(self, image_size: Tuple[int, int]) -> int:
        """Calcule la taille de police optimale basée sur les dimensions de l'image."""
        min_dimension = min(image_size)
        calculated_size = int(min_dimension * self.font_size_ratio)
        return max(self.min_font_size, min(self.max_font_size, calculated_size))

    def get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Charge une police avec fallback sur la police par défaut."""
        font_names = [
            "Lato-Bold.ttf",
            "Lato-Black.ttf",
            "arialbd.ttf",
            "Arial Bold.ttf",
            "DejaVuSans-Bold.ttf",
            "FreeSansBold.ttf",
            "NotoSans-Bold.ttf",
            "arial.ttf",
            "DejaVuSans.ttf",
        ]

        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except (IOError, OSError):
                continue

        return ImageFont.load_default()

    def _draw_text_with_outline(
        self,
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        alpha: int,
        outline_width: int = 2,
    ):
        """Dessine du texte avec un contour."""
        x, y = position
        text_rgba = (*self.text_color, alpha)
        outline_rgba = (*self.outline_color, alpha)

        if self.outline:
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), text, font=font, fill=outline_rgba)

        draw.text((x, y), text, font=font, fill=text_rgba)

    def _create_single_watermark_layer(
        self, size: Tuple[int, int], font: ImageFont.FreeTypeFont
    ) -> Image.Image:
        """Crée un layer avec un seul filigrane centré."""
        watermark = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        bbox = draw.textbbox((0, 0), self.text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2

        alpha = int(255 * self.opacity)
        self._draw_text_with_outline(draw, (x, y), self.text, font, alpha)

        return watermark

    def _create_tiled_watermark_layer(
        self, size: Tuple[int, int], font: ImageFont.FreeTypeFont
    ) -> Image.Image:
        """Crée un layer avec filigrane répété en diagonale."""
        temp_img = Image.new("RGBA", (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), self.text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        spacing_x = int(text_width * self.spacing)
        spacing_y = int(text_height * self.spacing * 2)

        diagonal = int(math.sqrt(size[0] ** 2 + size[1] ** 2))
        canvas_size = (diagonal * 2, diagonal * 2)

        canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        alpha = int(255 * self.opacity)

        y = 0
        row = 0
        while y < canvas_size[1]:
            x_offset = (spacing_x // 2) if row % 2 else 0
            x = -spacing_x + x_offset

            while x < canvas_size[0]:
                self._draw_text_with_outline(draw, (x, y), self.text, font, alpha)
                x += spacing_x

            y += spacing_y
            row += 1

        rotated = canvas.rotate(self.rotation, expand=False, resample=Image.BICUBIC)

        center_x = rotated.width // 2
        center_y = rotated.height // 2
        left = center_x - size[0] // 2
        top = center_y - size[1] // 2
        right = left + size[0]
        bottom = top + size[1]

        return rotated.crop((left, top, right, bottom))

    def create_watermark_layer(
        self, size: Tuple[int, int], font: ImageFont.FreeTypeFont = None
    ) -> Image.Image:
        """Crée le layer de filigrane selon le mode choisi."""
        if font is None:
            font_size = self.calculate_font_size(size)
            font = self.get_font(font_size)

        if self.pattern == "tiled":
            return self._create_tiled_watermark_layer(size, font)
        else:
            return self._create_single_watermark_layer(size, font)

    def apply_watermark(self, image: Image.Image) -> Image.Image:
        """
        Applique le filigrane sur une image PIL.
        
        Args:
            image: Image PIL (sera convertie en RGBA si nécessaire)
            
        Returns:
            Image PIL avec le filigrane appliqué
        """
        # Convertir en RGBA si nécessaire
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Calculer la taille de police et créer le layer
        font_size = self.calculate_font_size(image.size)
        font = self.get_font(font_size)
        watermark = self.create_watermark_layer(image.size, font)

        # Composer
        return Image.alpha_composite(image, watermark)
