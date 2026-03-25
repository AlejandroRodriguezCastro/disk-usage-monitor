"""
Utilidades de logging
"""
import logging
import sys
from config import LOG_FILE, LOG_LEVEL

def setup_logger():
    """Configura el logger centralizado"""
    logger = logging.getLogger("DiskMonitor")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Formato de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Handler para archivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Instancia global
logger = setup_logger()
