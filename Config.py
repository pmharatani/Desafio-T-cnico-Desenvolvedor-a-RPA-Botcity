"""Módulo de Configuração - Configura caminhos, diretórios e logging da automação."""

import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "resultados"
LOG_FILE = RESULTS_DIR / "execucao.log"
SCREENSHOTS_DIR = RESULTS_DIR / "screenshots"
ASSETS_DIR = BASE_DIR / "assets"


def preparar_diretorios():
    """Cria, se necessário, as pastas resultados e resultados/screenshots."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def configurar_logger():
    """Configura os logs da automação para arquivo e console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                mode="w",
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )
