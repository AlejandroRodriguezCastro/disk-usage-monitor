"""
Configuración centralizada del disk monitor
"""
import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Configuración de umbrales (en porcentaje de ESPACIO USADO)
WARNING_THRESHOLD = 40  # Alerta WARNING cuando el disco esté > 40% usado (para demo)
CRITICAL_THRESHOLD = 50  # Alerta CRITICAL cuando el disco esté > 50% usado (para demo)

# Rutas a monitorear
PATHS_TO_MONITOR = [
    "/",  # Raíz del sistema
    "/home",  # HOME en Linux
    "/var",  # Logs en Linux
    "/app",  # Carpeta de la aplicación
    "/test_data"  # Carpeta de prueba para demo
]

# Si es Windows, ajustar las rutas
import platform
if platform.system() == "Windows":
    PATHS_TO_MONITOR = [
        "C:\\",
        "D:\\",  # Si existe unidad D
    ]

# Configuración de logs
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "disk_monitor.log"

# Configuración de CSV
CSV_DIR = BASE_DIR / "data"
CSV_DIR.mkdir(exist_ok=True)
HISTORY_FILE = CSV_DIR / "history.csv"

# Configuración de email (SMTP)
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "False").lower() == "true"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "").split(",") if os.getenv("RECIPIENT_EMAILS") else []

# Intervalo de chequeo en segundos
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # 5 minutos por defecto

# Nivel de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
