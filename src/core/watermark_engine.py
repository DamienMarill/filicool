"""
Fililico - Watermark Engine
Moteur principal qui unifie le traitement des images et des PDF
"""

from pathlib import Path
from typing import List, Optional, Union, Tuple
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
        opacity: float = 0.3,
        pattern: str = "tiled",
        rotation: int = -45,
        spacing: float = 1.8,
        outline: bool = True,
        text_color: Tuple[int, int, int] = (0, 0, 0),
        outline_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        """
        Initialise le moteur de filigranage.

        Args:
            text: Texte du filigrane
            opacity: Opacité du filigrane (0.0 à 1.0)
            pattern: Mode de rendu ("single" ou "tiled")
            rotation: Angle de rotation en degrés
            spacing: Espacement entre répétitions
            outline: Ajouter un contour au texte
            text_color: Couleur du texte (RGB)
            outline_color: Couleur du contour (RGB)
        """
        self._text = text
        self._opacity = max(0.0, min(1.0, opacity))
        self._pattern = pattern
        self._rotation = rotation
        self._spacing = spacing
        self._outline = outline
        self._text_color = text_color
        self._outline_color = outline_color

        # Les processeurs seront recréés à la demande
        self._processors_dirty = True
        self._image_processor = None
        self._pdf_processor = None

    def _create_processors(self):
        """Crée ou recrée les processeurs avec les options actuelles."""
        self._image_processor = ImageProcessor(
            text=self._text,
            opacity=self._opacity,
            pattern=self._pattern,
            rotation=self._rotation,
            spacing=self._spacing,
            outline=self._outline,
            text_color=self._text_color,
            outline_color=self._outline_color,
        )
        self._pdf_processor = PDFProcessor(
            text=self._text,
            opacity=self._opacity,
            pattern=self._pattern,
            rotation=self._rotation,
            spacing=self._spacing,
            outline=self._outline,
            text_color=self._text_color,
            outline_color=self._outline_color,
        )
        self._processors_dirty = False

    def _ensure_processors(self):
        """S'assure que les processeurs sont à jour."""
        if self._processors_dirty or self._image_processor is None:
            self._create_processors()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if self._text != value:
            self._text = value
            self._processors_dirty = True

    @property
    def opacity(self) -> float:
        return self._opacity

    @opacity.setter
    def opacity(self, value: float):
        value = max(0.0, min(1.0, value))
        if self._opacity != value:
            self._opacity = value
            self._processors_dirty = True

    @property
    def pattern(self) -> str:
        return self._pattern

    @pattern.setter
    def pattern(self, value: str):
        if self._pattern != value:
            self._pattern = value
            self._processors_dirty = True

    @property
    def rotation(self) -> int:
        return self._rotation

    @rotation.setter
    def rotation(self, value: int):
        if self._rotation != value:
            self._rotation = value
            self._processors_dirty = True

    @property
    def spacing(self) -> float:
        return self._spacing

    @spacing.setter
    def spacing(self, value: float):
        if self._spacing != value:
            self._spacing = value
            self._processors_dirty = True

    @property
    def outline(self) -> bool:
        return self._outline

    @outline.setter
    def outline(self, value: bool):
        if self._outline != value:
            self._outline = value
            self._processors_dirty = True

    def get_file_type(self, file_path: Path) -> FileType:
        """Détermine le type de fichier."""
        file_path = Path(file_path)

        if ImageProcessor.is_supported(file_path):
            return FileType.IMAGE
        elif PDFProcessor.is_supported(file_path):
            return FileType.PDF
        else:
            return FileType.UNKNOWN

    def is_supported(self, file_path: Path) -> bool:
        """Vérifie si le fichier est supporté."""
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
        # S'assurer que les processeurs sont à jour
        self._ensure_processors()

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
            output_dir: Dossier de sortie (optionnel)

        Returns:
            Liste des résultats de traitement
        """
        results = []
        output_dir = Path(output_dir) if output_dir else None

        for input_path in input_paths:
            input_path = Path(input_path)

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

        Args:
            input_path: Chemin du fichier source
            max_size: Dimensions maximales

        Returns:
            Chaîne base64 ou None si non supporté
        """
        self._ensure_processors()
        
        input_path = Path(input_path)
        file_type = self.get_file_type(input_path)

        if file_type == FileType.IMAGE:
            return self._image_processor.generate_preview(input_path, max_size)
        else:
            return None
