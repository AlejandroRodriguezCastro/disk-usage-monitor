FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (incluyendo compiladores para psutil)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY requirements.txt .
COPY *.py ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorios necesarios
RUN mkdir -p logs data

# Variable de entorno para configuración
ENV CHECK_INTERVAL=300
ENV LOG_LEVEL=INFO
ENV EMAIL_ENABLED=False

# Tiempo de zona
ENV TZ=America/Bogota

# Volumen para persistencia de datos
VOLUME ["/app/logs", "/app/data"]

# Comando por defecto
CMD ["python", "main.py"]
