"""
Gestión de almacenamiento en CSV
"""
import csv
from datetime import datetime
from pathlib import Path
from config import HISTORY_FILE
from logger_utils import logger


class CSVStorage:
    """Guarda eventos en archivo CSV"""
    
    def __init__(self, filepath=HISTORY_FILE):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Crea el archivo CSV si no existe"""
        if not self.filepath.exists():
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'timestamp', 'path', 'total_gb', 'used_gb', 'free_gb', 
                    'percent_used', 'status'
                ])
                writer.writeheader()
            logger.info(f"Archivo CSV creado: {self.filepath}")
    
    def save_event(self, path, total_gb, used_gb, free_gb, percent_used, status):
        """Guarda un evento de disco en el CSV"""
        try:
            with open(self.filepath, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'timestamp', 'path', 'total_gb', 'used_gb', 'free_gb', 
                    'percent_used', 'status'
                ])
                writer.writerow({
                    'timestamp': datetime.now().isoformat(),
                    'path': path,
                    'total_gb': f"{total_gb:.2f}",
                    'used_gb': f"{used_gb:.2f}",
                    'free_gb': f"{free_gb:.2f}",
                    'percent_used': f"{percent_used:.2f}",
                    'status': status
                })
            logger.debug(f"Evento guardado en CSV: {path} - {status}")
        except Exception as e:
            logger.error(f"Error guardando evento en CSV: {e}")
    
    def get_history(self, limit=100):
        """Retorna los últimos N eventos del historial"""
        try:
            with open(self.filepath, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows[-limit:]
        except Exception as e:
            logger.error(f"Error leyendo historial: {e}")
            return []
