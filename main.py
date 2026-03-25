#!/usr/bin/env python3
"""
Disk Space Monitor
Script para monitorear espacio en disco con alertas y logs
"""
import sys
import time
from config import PATHS_TO_MONITOR, CHECK_INTERVAL
from monitor import DiskMonitor
from logger_utils import logger


def main():
    """Función principal"""
    logger.info("="*80)
    logger.info("Iniciando Disk Space Monitor")
    logger.info("="*80)
    
    monitor = DiskMonitor()
    
    try:
        while True:
            logger.info(f"Verificando {len(PATHS_TO_MONITOR)} rutas...")
            results = monitor.monitor_paths(PATHS_TO_MONITOR)
            monitor.print_status(results)
            
            logger.debug(f"Próxima verificación en {CHECK_INTERVAL} segundos")
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        logger.info("Monitor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error crítico: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
