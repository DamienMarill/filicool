"""
Fillico - Core Package
🍭 Le filigrane n'est plus une corvée, c'est une friandise visuelle !
"""

__version__ = "1.0.0"
__author__ = "Damien Marill"

from .watermark_engine import WatermarkEngine
from .image_processor import ImageProcessor
from .pdf_processor import PDFProcessor

__all__ = ["WatermarkEngine", "ImageProcessor", "PDFProcessor"]
