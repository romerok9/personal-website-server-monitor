#!/bin/bash
# start_monitor.sh - Iniciar el monitor de status web

echo "════════════════════════════════════════════════════"
echo "   SYSMON WEB - Server Status Monitor"
echo "════════════════════════════════════════════════════"
echo ""

# Verificar que el script existe
if [ ! -f "sysmon_web.py" ]; then
    echo "❌ Error: sysmon_web.py no encontrado"
    exit 1
fi

# Hacer ejecutable
chmod +x sysmon_web.py

# Matar proceso anterior si existe
pkill -f "python3.*sysmon_web.py" 2>/dev/null && echo "✓ Proceso anterior detenido"

# Verificar dependencias
echo "🔍 Verificando dependencias..."
python3 -c "import psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  psutil no instalado"
    echo "   Instalar con: sudo apt install python3-psutil"
    exit 1
fi

python3 -c "import docker" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  docker no instalado (opcional)"
    echo "   Para monitoreo Docker: sudo apt install python3-docker"
fi

echo ""
echo "🚀 Iniciando monitor de status..."
echo "   Actualización: cada 30 segundos"
echo ""
echo "Para detener: Ctrl+C o ejecuta: pkill -f sysmon_web.py"
echo ""
echo "════════════════════════════════════════════════════"
echo ""

# Ejecutar
python3 sysmon_web.py






















