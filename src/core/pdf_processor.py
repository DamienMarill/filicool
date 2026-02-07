"""
Fililico - PDF Processor
Gère le filigranage des fichiers PDF
"""

from pathlib import Path
from typing import Optional
import io

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import white


class PDFProcessor:
    """Processeur de filigrane pour les fichiers PDF."""

    SUPPORTED_FORMATS = {".pdf"}

    def __init__(
        self,
        text: str = "CONFIDENTIEL",
        opacity: float = 0.3,
        font_size: int = 60,
    ):
        """
        Initialise le processeur PDF.

        Args:
            text: Texte du filigrane
            opacity: Opacité du filigrane (0.0 à 1.0)
            font_size: Taille de la police
        """
        self.text = text
        self.opacity = max(0.0, min(1.0, opacity))
        self.font_size = font_size

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        """Vérifie si le format de fichier est supporté."""
        return file_path.suffix.lower() in cls.SUPPORTED_FORMATS

    def _create_watermark_pdf(
        self, page_width: float, page_height: float
    ) -> io.BytesIO:
        """
        Crée un PDF contenant uniquement le filigrane.

        Args:
            page_width: Largeur de la page
            page_height: Hauteur de la page

        Returns:
            BytesIO contenant le PDF du filigrane
        """
        packet = io.BytesIO()

        # Créer un canvas avec les dimensions de la page
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Configurer la transparence
        c.setFillAlpha(self.opacity)
        c.setFillColor(white)

        # Calculer la position centrale
        text_width = c.stringWidth(self.text, "Helvetica", self.font_size)
        x = (page_width - text_width) / 2
        y = page_height / 2

        # Dessiner le texte
        c.setFont("Helvetica", self.font_size)
        c.drawString(x, y, self.text)

        c.save()
        packet.seek(0)

        return packet

    def process(
        self, input_path: Path, output_path: Optional[Path] = None
    ) -> Path:
        """
        Applique le filigrane sur toutes les pages d'un PDF.

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
            output_path = input_path.parent / f"{input_path.stem}_watermarked.pdf"

        # Lire le PDF source
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Appliquer le filigrane sur chaque page
        for page in reader.pages:
            # Obtenir les dimensions de la page
            media_box = page.mediabox
            page_width = float(media_box.width)
            page_height = float(media_box.height)

            # Créer le PDF du filigrane pour cette taille de page
            watermark_pdf = self._create_watermark_pdf(page_width, page_height)
            watermark_reader = PdfReader(watermark_pdf)
            watermark_page = watermark_reader.pages[0]

            # Fusionner le filigrane avec la page
            page.merge_page(watermark_page)
            writer.add_page(page)

        # Copier les métadonnées
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        # Sauvegarder
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        return output_path

    def get_page_count(self, file_path: Path) -> int:
        """
        Retourne le nombre de pages d'un PDF.

        Args:
            file_path: Chemin du fichier PDF

        Returns:
            Nombre de pages
        """
        reader = PdfReader(file_path)
        return len(reader.pages)
