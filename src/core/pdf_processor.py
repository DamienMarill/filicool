"""
Fililico - PDF Processor
Gère le filigranage des fichiers PDF via conversion en images
Le filigrane est "burnt-in" dans les pixels, impossible à supprimer sans altérer le document
"""

from pathlib import Path
from typing import Optional, Tuple
import io
import tempfile
import os

from PIL import Image

from .watermark_renderer import WatermarkRenderer


class PDFProcessor:
    """Processeur de filigrane pour les fichiers PDF."""

    SUPPORTED_FORMATS = {".pdf"}

    def __init__(
        self,
        text: str = "CONFIDENTIEL",
        opacity: float = 0.3,
        font_size_ratio: float = 0.05,  # Plus petit pour les PDFs (haute résolution)
        min_font_size: int = 20,
        max_font_size: int = 80,
        pattern: str = "tiled",
        rotation: int = -45,
        spacing: float = 1.8,
        outline: bool = True,
        text_color: Tuple[int, int, int] = (0, 0, 0),
        outline_color: Tuple[int, int, int] = (255, 255, 255),
        dpi: int = 150,  # Résolution de conversion (équilibre qualité/taille)
    ):
        """Initialise le processeur PDF avec le renderer partagé."""
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
        self.dpi = dpi

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        """Vérifie si le format de fichier est supporté."""
        return file_path.suffix.lower() in cls.SUPPORTED_FORMATS

    def _pdf_to_images(self, pdf_path: Path) -> list:
        """
        Convertit un PDF en liste d'images PIL.
        Utilise pdf2image si disponible, sinon PyMuPDF (fitz).
        """
        images = []
        
        # Essayer pdf2image d'abord
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(str(pdf_path), dpi=self.dpi)
            return images
        except ImportError:
            pass
        
        # Fallback sur PyMuPDF (fitz)
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(pdf_path))
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Calculer le facteur de zoom pour le DPI souhaité
                zoom = self.dpi / 72  # 72 est le DPI par défaut des PDFs
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
            doc.close()
            return images
        except ImportError:
            pass

        raise ImportError(
            "Aucune bibliothèque PDF trouvée. "
            "Installez pdf2image (pip install pdf2image) ou PyMuPDF (pip install pymupdf)"
        )

    def _images_to_pdf(self, images: list, output_path: Path):
        """Convertit une liste d'images PIL en PDF."""
        if not images:
            raise ValueError("Aucune image à convertir")

        # Convertir toutes les images en RGB
        rgb_images = []
        for img in images:
            if img.mode != "RGB":
                rgb_images.append(img.convert("RGB"))
            else:
                rgb_images.append(img)

        # Sauvegarder en PDF
        first_image = rgb_images[0]
        if len(rgb_images) > 1:
            first_image.save(
                output_path,
                "PDF",
                save_all=True,
                append_images=rgb_images[1:],
                resolution=self.dpi,
            )
        else:
            first_image.save(output_path, "PDF", resolution=self.dpi)

    def process(
        self, input_path: Path, output_path: Optional[Path] = None
    ) -> Path:
        """
        Applique le filigrane sur toutes les pages d'un PDF.
        
        Le PDF est converti en images, le filigrane est appliqué sur chaque page,
        puis les images sont reconverties en PDF.

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
            output_path = input_path.parent / f"{input_path.stem}_watermarked.pdf"

        # Convertir PDF en images
        print(f"  📄 Conversion du PDF en images ({self.dpi} DPI)...")
        pages = self._pdf_to_images(input_path)
        print(f"  📄 {len(pages)} page(s) à traiter")

        # Appliquer le filigrane sur chaque page
        watermarked_pages = []
        for i, page in enumerate(pages):
            print(f"  🍭 Filigranage page {i + 1}/{len(pages)}...")
            watermarked = self.renderer.apply_watermark(page)
            watermarked_pages.append(watermarked)

        # Reconvertir en PDF
        print(f"  📄 Création du PDF final...")
        self._images_to_pdf(watermarked_pages, output_path)

        return output_path

    def get_page_count(self, file_path: Path) -> int:
        """Retourne le nombre de pages d'un PDF."""
        # Essayer PyPDF2 d'abord (plus léger)
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            return len(reader.pages)
        except ImportError:
            pass

        # Fallback sur PyMuPDF
        try:
            import fitz
            doc = fitz.open(str(file_path))
            count = len(doc)
            doc.close()
            return count
        except ImportError:
            pass

        return 0
