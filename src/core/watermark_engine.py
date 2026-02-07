"""
Fililico - Watermark Engine
Moteur principal qui unifie le traitement des images et des PDF
"""

from pathlib import Path
from typing import List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from .image_processor import ImageProcessor
from .pdf_processor import PDFProcessor


class FileType(Enum):
    """Type de fichier supporté."""
    IMAGE = "image"
    PDF = "pdf"
    UNKNOWN = "unknown"


@dataclass
class ProcessingResult:
    """Résultat du traitement d'un fichier."""
    input_path: Path
    output_path: Optional[Path]
    success: bool
    error: Optional[str] = None
    file_type: FileType = FileType.UNKNOWN


class WatermarkEngine:
    """
    Moteur principal de filigranage.
    Unifie le traitement des images et des PDF.
    """

    def __init__(
        self,
        text: str = "CONFIDENTIEL",
        opacity: float = 0.5,
    ):
        """
        Initialise le moteur de filigranage.

        Args:
            text: Texte du filigrane
            opacity: Opacité du filigrane (0.0 à 1.0)
        """
        self.text = text
        self.opacity = opacity

        # Initialiser les processeurs
        self._image_processor = ImageProcessor(text=text, opacity=opacity)
        self._pdf_processor = PDFProcessor(text=text, opacity=opacity)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        # Mettre à jour les processeurs si ils existent
        if hasattr(self, "_image_processor"):
            self._image_processor.text = value
        if hasattr(self, "_pdf_processor"):
            self._pdf_processor.text = value

    @property
    def opacity(self) -> float:
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        self._opacity = max(0.0, min(1.0, value))
        # Mettre à jour les processeurs si ils existent
        if hasattr(self, "_image_processor"):
            self._image_processor.opacity = self._opacity
        if hasattr(self, "_pdf_processor"):
            self._pdf_processor.opacity = self._opacity

    def get_file_type(self, file_path: Path) -> FileType:
        """
        Détermine le type de fichier.

        Args:
            file_path: Chemin du fichier

        Returns:
            Type de fichier (IMAGE, PDF, ou UNKNOWN)
        """
        file_path = Path(file_path)

        if ImageProcessor.is_supported(file_path):
            return FileType.IMAGE
        elif PDFProcessor.is_supported(file_path):
            return FileType.PDF
        else:
            return FileType.UNKNOWN

    def is_supported(self, file_path: Path) -> bool:
        """
        Vérifie si le fichier est supporté.

        Args:
            file_path: Chemin du fichier

        Returns:
            True si le fichier est supporté
        """
        return self.get_file_type(file_path) != FileType.UNKNOWN

    def get_supported_extensions(self) -> set:
        """Retourne l'ensemble des extensions supportées."""
        return ImageProcessor.SUPPORTED_FORMATS | PDFProcessor.SUPPORTED_FORMATS

    def process(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
    ) -> ProcessingResult:
        """
        Traite un fichier (image ou PDF).

        Args:
            input_path: Chemin du fichier source
            output_path: Chemin de sortie (optionnel)

        Returns:
            Résultat du traitement
        """
        input_path = Path(input_path)
        output_path = Path(output_path) if output_path else None

        file_type = self.get_file_type(input_path)

        try:
            if file_type == FileType.IMAGE:
                result_path = self._image_processor.process(input_path, output_path)
                return ProcessingResult(
                    input_path=input_path,
                    output_path=result_path,
                    success=True,
                    file_type=file_type,
                )
            elif file_type == FileType.PDF:
                result_path = self._pdf_processor.process(input_path, output_path)
                return ProcessingResult(
                    input_path=input_path,
                    output_path=result_path,
                    success=True,
                    file_type=file_type,
                )
            else:
                return ProcessingResult(
                    input_path=input_path,
                    output_path=None,
                    success=False,
                    error=f"Format non supporté: {input_path.suffix}",
                    file_type=file_type,
                )

        except Exception as e:
            return ProcessingResult(
                input_path=input_path,
                output_path=None,
                success=False,
                error=str(e),
                file_type=file_type,
            )

    def batch_process(
        self,
        input_paths: List[Union[str, Path]],
        output_dir: Optional[Union[str, Path]] = None,
    ) -> List[ProcessingResult]:
        """
        Traite plusieurs fichiers.

        Args:
            input_paths: Liste des chemins de fichiers sources
            output_dir: Dossier de sortie (optionnel, utilise le dossier source si None)

        Returns:
            Liste des résultats de traitement
        """
        results = []
        output_dir = Path(output_dir) if output_dir else None

        for input_path in input_paths:
            input_path = Path(input_path)

            # Calculer le chemin de sortie si un dossier est spécifié
            if output_dir:
                output_path = output_dir / f"{input_path.stem}_watermarked{input_path.suffix}"
            else:
                output_path = None

            result = self.process(input_path, output_path)
            results.append(result)

        return results

    def generate_preview(
        self,
        input_path: Union[str, Path],
        max_size: tuple = (800, 600),
    ) -> Optional[str]:
        """
        Génère une preview en base64.
        Fonctionne uniquement pour les images.

        Args:
            input_path: Chemin du fichier source
            max_size: Dimensions maximales

        Returns:
            Chaîne base64 ou None si non supporté
        """
        input_path = Path(input_path)
        file_type = self.get_file_type(input_path)

        if file_type == FileType.IMAGE:
            return self._image_processor.generate_preview(input_path, max_size)
        else:
            # Les previews PDF ne sont pas encore supportées
            return None
