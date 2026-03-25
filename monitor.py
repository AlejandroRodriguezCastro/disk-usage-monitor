"""
Lógica principal de monitoreo
"""
import psutil
from config import WARNING_THRESHOLD, CRITICAL_THRESHOLD
from logger_utils import logger
from alerts import AlertManager
from storage import CSVStorage


class DiskMonitor:
    """Monitor de espacio en disco"""
    
    def __init__(self):
        self.alert_manager = AlertManager()
        self.storage = CSVStorage()
        self.last_alerts = {}  # Para evitar alertas duplicadas seguidas
    
    def check_path(self, path):
        """Verifica el espacio disponible en una ruta"""
        try:
            usage = psutil.disk_usage(path)
            
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            percent_used = usage.percent
            
            return {
                'path': path,
                'total_gb': total_gb,
                'used_gb': used_gb,
                'free_gb': free_gb,
                'percent_used': percent_used
            }
        except Exception as e:
            logger.error(f"Error verificando {path}: {e}")
            return None
    
    def monitor_paths(self, paths):
        """Monitorea múltiples rutas"""
        results = []
        
        for path in paths:
            disk_info = self.check_path(path)
            if not disk_info:
                continue
            
            results.append(disk_info)
            
            # Determinar nivel de alerta
            percent_used = disk_info['percent_used']
            free_gb = disk_info['free_gb']
            
            status = "OK"
            
            if percent_used >= CRITICAL_THRESHOLD:
                # Evitar alertas duplicadas
                if self.last_alerts.get(path) != "CRITICAL":
                    self.alert_manager.generate_alert(
                        path, percent_used, free_gb, "CRITICAL"
                    )
                    self.last_alerts[path] = "CRITICAL"
                status = "CRITICAL"
            elif percent_used >= WARNING_THRESHOLD:
                if self.last_alerts.get(path) not in ["CRITICAL", "WARNING"]:
                    self.alert_manager.generate_alert(
                        path, percent_used, free_gb, "WARNING"
                    )
                    self.last_alerts[path] = "WARNING"
                status = "WARNING"
            else:
                # Situación normalizada
                if self.last_alerts.get(path) not in [None, "OK"]:
                    logger.info(f"✅ Situación normalizada en {path}: {percent_used:.1f}% usado")
                self.last_alerts[path] = "OK"
                status = "OK"
            
            # Guardar en CSV
            self.storage.save_event(
                disk_info['path'],
                disk_info['total_gb'],
                disk_info['used_gb'],
                disk_info['free_gb'],
                disk_info['percent_used'],
                status
            )
        
        return results
    
    def print_status(self, results):
        """Muestra el estado en formato tabla"""
        if not results:
            return
        
        print("\n" + "="*100)
        print(f"{'Path':<30} {'Total':<12} {'Usado':<12} {'Libre':<12} {'% Usado':<10} {'Estado':<10}")
        print("="*100)
        
        for result in results:
            path = result['path']
            total = result['total_gb']
            used = result['used_gb']
            free = result['free_gb']
            percent = result['percent_used']
            
            state = "🟢 OK"
            if percent >= CRITICAL_THRESHOLD:
                state = "🔴 CRÍTICO"
            elif percent >= WARNING_THRESHOLD:
                state = "🟡 ALERTA"
            
            print(f"{path:<30} {total:>10.2f}GB {used:>10.2f}GB {free:>10.2f}GB {percent:>8.1f}% {state:<10}")
        
        print("="*100 + "\n")
