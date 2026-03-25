"""
Sistema de alertas
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import (
    EMAIL_ENABLED, SMTP_SERVER, SMTP_PORT, 
    SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAILS
)
from logger_utils import logger


class AlertManager:
    """Gestiona alertas por consola y email"""
    
    def __init__(self):
        self.email_enabled = EMAIL_ENABLED
        self.alert_history = []
    
    def generate_alert(self, path, percent_used, free_gb, alert_level):
        """Genera alerta visual en consola"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if alert_level == "CRITICAL":
            message = f"🔴 CRÍTICO [{timestamp}] - {path}: {percent_used:.1f}% usado, {free_gb:.2f}GB libres"
            print("\n" + "="*80)
            print(message)
            print("="*80 + "\n")
        elif alert_level == "WARNING":
            message = f"🟡 ADVERTENCIA [{timestamp}] - {path}: {percent_used:.1f}% usado, {free_gb:.2f}GB libres"
            print(message)
        
        logger.warning(message) if alert_level in ["CRITICAL", "WARNING"] else logger.info(message)
        self.alert_history.append({
            'timestamp': timestamp,
            'path': path,
            'level': alert_level,
            'percent_used': percent_used,
            'free_gb': free_gb
        })
        
        # Enviar email si está habilitado
        if self.email_enabled and alert_level == "CRITICAL":
            self.send_email_alert(path, percent_used, free_gb, alert_level)
    
    def send_email_alert(self, path, percent_used, free_gb, alert_level):
        """Envía alerta por email"""
        if not SENDER_EMAIL or not SENDER_PASSWORD or not RECIPIENT_EMAILS:
            logger.warning("Email no configurado correctamente. Contacta con el administrador.")
            return
        
        try:
            subject = f"⚠️ ALERTA DE DISCO: {alert_level} en {path}"
            body = f"""
Hola,

Se detectó una condición CRÍTICA en el monitoreo de disco:

Path: {path}
Espacio usado: {percent_used:.1f}%
Espacio libre: {free_gb:.2f} GB
Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Nivel: {alert_level}

Por favor, revisar el sistema lo antes posible.

---
Disk Space Monitor
            """
            
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = ', '.join(RECIPIENT_EMAILS)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Alerta por email enviada a {RECIPIENT_EMAILS}")
        
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
    
    def get_alert_history(self):
        """Retorna el historial de alertas"""
        return self.alert_history
