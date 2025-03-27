"""
Este módulo configura un logger con las siguientes características:

- **Salida en consola** con colores (si `colorlog` está disponible)
- **Salida a archivo de logs** con rotación automática
- **Nivel de log configurable**
- **Formato detallado de timestamp**
"""

import logging
from logging.handlers import RotatingFileHandler
import pathlib

# Definir la ruta base del proyecto
BASE_DIR = pathlib.Path(__file__).resolve().parent
LOG_FILE_PATH = BASE_DIR / "logs" / "model_app.log"

# Intentar importar colorlog para logs en consola con colores
try:
    import colorlog  # Para logs en color en la consola
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False

def setup_logger(
    logger_name="models-utils", 
    log_file=LOG_FILE_PATH, 
    log_level=logging.INFO, 
    max_bytes=5*1024*1024, 
    backup_count=3
):
    """
    Configura un logger con las siguientes características:
    
    - **Salida en consola** con colores (si `colorlog` está disponible)
    - **Salida a archivo de logs** con rotación automática
    - **Nivel de log configurable**
    - **Formato detallado de timestamp**
    
    ### Parámetros:
    - `logger_name` (str): Nombre del logger.
    - `log_file` (str): Ruta del archivo de logs.
    - `log_level` (int): Nivel de logging (`logging.DEBUG`, `logging.INFO`, etc.).
    - `max_bytes` (int): Tamaño máximo del archivo antes de rotar.
    - `backup_count` (int): Cantidad de archivos de respaldo a mantener.
    
    ### Retorna:
    - `logger` (logging.Logger): Objeto logger configurado.
    """
    
    # Crear logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Formato de logs con timestamp detallado
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S"
    )

    # Configurar handler para archivo con rotación automática
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Configurar handler para consola con colores si `colorlog` está disponible
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

# Inicializar logger global
logger = setup_logger()