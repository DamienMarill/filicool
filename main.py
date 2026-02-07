#!/usr/bin/env python3
"""
🍭 Fililico - Main Entry Point
Le filigrane n'est plus une corvée, c'est une friandise visuelle !
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from ui import start_app

if __name__ == "__main__":
    start_app()
