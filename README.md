# Disk Space Monitor

Script en Python para monitorear espacio en disco, generar logs y enviar alertas cuando una unidad o path tiene poco espacio disponible.

## Objetivo

Este proyecto permite supervisar automáticamente el uso de disco en una o varias rutas del sistema.  
Si el espacio libre baja de un umbral definido, el sistema puede:

- mostrar alertas en consola
- guardar eventos en logs
- guardar historial en CSV
- enviar alertas por email

Es ideal para:

- servidores Linux
- servidores Windows
- PCs de oficina
- máquinas virtuales
- entornos de desarrollo
- carpetas críticas de backups o logs

---

# Características

- Monitoreo de uno o varios discos/rutas
- Umbral de alerta `WARNING`
- Umbral de alerta `CRITICAL`
- Logs automáticos
- Historial en CSV
- Soporte para alertas por email (usando SNMP de GMAIL)
- Estructura simple y fácil de extender
- Compatible con Windows, Linux y macOS

---

# Estructura del proyecto

```bash
disk_monitor/
│
├── main.py
├── config.py
├── monitor.py
├── alerts.py
├── storage.py
├── logger_utils.py
├── requirements.txt
├── history.csv
└── README.md