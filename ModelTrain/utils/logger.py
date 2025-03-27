"""
Este módulo configura un logger con soporte para:
- Consola con colores (si está disponible `colorlog`)
- Archivo de logs con rotación automática
- Nivel de log configurable
- Formato de timestamp detallado
"""

import logging
from logging.handlers import RotatingFileHandler
import pathlib

BASE_DIR = pathlib.Path.cwd()
LOG_FILE_PATH = BASE_DIR / "logs" / "model_app.log"

try:
    import colorlog  # Para logs en color en la consola
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False


def setup_logger(logger_name="models-utils", log_file=LOG_FILE_PATH, log_level=logging.INFO, max_bytes=5*1024*1024, backup_count=3):
    """
    Configura el logger con soporte para:
    - Consola con colores (si está disponible `colorlog`)
    - Archivo de logs con rotación automática
    - Nivel de log configurable
    - Formato de timestamp detallado
    """
    
    # Crear logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Formato de logs
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S"
    )

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para consola con colores (si está disponible)
    if COLORLOG_AVAILABLE:
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


# Inicializar logger
logger = setup_logger()
