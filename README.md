# Personal Website + Real-Time Server Monitor

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3)
![Docker](https://img.shields.io/badge/Docker-Monitoring-2496ED?style=flat-square&logo=docker)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

Portfolio personal minimalista con dashboard de monitoreo en tiempo real de servidor Debian/Linux. Métricas de CPU, RAM, disco, red y containers Docker actualizadas automáticamente cada 30 segundos.

## ✨ Demo

![Dashboard Preview](https://via.placeholder.com/800x450/0a0a0a/60a5fa?text=Server+Status+Dashboard)

## 🎯 Características

### Portfolio Website
- ✅ **Diseño minimalista** - Inspirado en portafolios tech profesionales
- ✅ **Responsive** - Se adapta a móvil, tablet y desktop
- ✅ **Dark theme** - Diseño moderno enfocado en legibilidad
- ✅ **Sin JavaScript** - HTML/CSS puro, ultra-rápido
- ✅ **SEO friendly** - Estructura semántica optimizada

### Server Monitor
- ✅ **Métricas del sistema**:
  - CPU: Uso en % y núcleos
  - RAM: Usado/Total/Disponible
  - Disco: Uso/Total/Libre  
  - Red: Tráfico total enviado/recibido
  - Uptime del sistema

- ✅ **Monitoreo Docker**:
  - Estado de containers (running/stopped)
  - Nombre e imagen de cada container
  - Destacado especial para n8n

- ✅ **Auto-actualización**: Dashboard se refresca cada 30s
- ✅ **Barras de progreso visuales** con colores por estado
- ✅ **Alertas por color**: Verde (<50%), Amarillo (50-80%), Rojo (>80%)

## 📋 Requisitos

- Python 3.10+
- Servidor Linux (Debian/Ubuntu recomendado)
- Docker (opcional, para monitoreo de containers)
- Nginx o servidor web similar

### Dependencias Python

```bash
# Debian/Ubuntu
sudo apt install python3-psutil python3-docker

# Otras distros con pip
pip3 install psutil docker
```

## 🚀 Quick Start

### 1. Clonar el repositorio

```bash
git clone https://github.com/romerok9/personal-website-server-monitor.git
cd personal-website-server-monitor
```

### 2. Personalizar el sitio web

Edita `website/index.html`:

```html
<!-- Cambiar información personal -->
<h1>Tu Nombre</h1>
<p class="subtitle">Tu Título Profesional</p>

<!-- Actualizar links -->
<a href="https://linkedin.com/in/tu-perfil">LinkedIn</a>
<a href="https://github.com/tu-usuario">GitHub</a>
```

### 3. Configurar el monitor

Edita `monitor/sysmon_web.py`:

```python
# Línea 13-14: Ajustar según tu configuración
UPDATE_INTERVAL = 30  # Segundos entre actualizaciones
OUTPUT_FILE = "/path/to/your/website/status.html"
```

### 4. Copiar archivos al servidor

```bash
# Sitio web
scp website/index.html user@your-server:/var/www/html/

# Monitor
scp monitor/sysmon_web.py user@your-server:/opt/monitor/
scp monitor/start_monitor.sh user@your-server:/opt/monitor/
```

### 5. Iniciar el monitor

```bash
ssh user@your-server

# Opción 1: Foreground (para pruebas)
cd /opt/monitor
python3 sysmon_web.py

# Opción 2: Background
nohup python3 sysmon_web.py > /tmp/sysmon.log 2>&1 &

# Opción 3: Systemd service (recomendado)
sudo cp monitor/sysmon-web.service /etc/systemd/system/
sudo systemctl enable sysmon-web
sudo systemctl start sysmon-web
```

### 6. Acceder

```
https://yourdomain.com/              → Portfolio
https://yourdomain.com/status.html   → Server Monitor
```

## 📂 Estructura del Proyecto

```
personal-website-server-monitor/
├── website/
│   └── index.html                  # Portfolio website
├── monitor/
│   ├── sysmon_web.py              # Monitor script (genera HTML)
│   ├── sysmon.py                  # Monitor terminal (TUI)
│   ├── start_monitor.sh           # Script de inicio
│   └── sysmon-web.service         # Systemd service
├── docs/
│   ├── INSTALLATION.md            # Guía de instalación detallada
│   ├── CUSTOMIZATION.md           # Guía de personalización
│   └── TROUBLESHOOTING.md         # Solución de problemas
├── screenshots/
│   ├── website.png
│   └── monitor.png
├── .gitignore
├── LICENSE
└── README.md
```

## 🎨 Personalización

### Colores del Website

Edita el `<style>` en `website/index.html`:

```css
/* Cambiar color de acentos */
.links a {
    color: #60a5fa;  /* Azul por defecto */
}

/* Cambiar background */
body {
    background: #0a0a0a;  /* Negro por defecto */
}
```

### Umbrales de Alerta del Monitor

Edita `monitor/sysmon_web.py`:

```python
# Línea ~115-117
cpu_color = '#ef4444' if metrics['cpu']['percent'] > 80 else \
            '#10b981' if metrics['cpu']['percent'] < 50 else '#f59e0b'

# Cambia los valores 80 y 50 según necesites
```

### Frecuencia de Actualización

```python
# monitor/sysmon_web.py, línea 13
UPDATE_INTERVAL = 30  # Cambiar a 10, 60, etc.
```

## 🖥️ Uso del Monitor de Terminal

Además del monitor web, incluye una versión TUI para uso interactivo:

```bash
python3 monitor/sysmon.py
```

**Características**:
- Interfaz ncurses en tiempo real
- Colores dinámicos según carga
- Lista de conexiones de red activas
- Actualización continua (no requiere refresh manual)

## 🔧 Instalación como Servicio Systemd

### 1. Crear el servicio

```bash
sudo nano /etc/systemd/system/sysmon-web.service
```

```ini
[Unit]
Description=System Monitor Web Dashboard
After=network.target docker.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/monitor
ExecStart=/usr/bin/python3 /opt/monitor/sysmon_web.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Activar e iniciar

```bash
sudo systemctl daemon-reload
sudo systemctl enable sysmon-web
sudo systemctl start sysmon-web
```

### 3. Verificar

```bash
sudo systemctl status sysmon-web
sudo journalctl -u sysmon-web -f
```

## 📊 Métricas Monitoreadas

| Métrica | Descripción | Fuente |
|---------|-------------|--------|
| **CPU** | Uso en % y núcleos disponibles | `/proc/stat` |
| **RAM** | Usado/Total/Disponible en GB | `/proc/meminfo` |
| **Disco** | Uso/Total/Libre en GB | `/proc/mounts` |
| **Red** | Total enviado/recibido acumulado | `/proc/net/dev` |
| **Uptime** | Tiempo desde último boot | `/proc/uptime` |
| **Docker** | Estado de containers | Docker API |

## 🛠️ Comandos Útiles

```bash
# Ver si el monitor está corriendo
ps aux | grep sysmon_web

# Ver logs en tiempo real
tail -f /tmp/sysmon.log

# Reiniciar el monitor
pkill -f sysmon_web.py
nohup python3 sysmon_web.py > /tmp/sysmon.log 2>&1 &

# Verificar última actualización del HTML
stat /var/www/html/status.html

# Ver permisos de escritura
ls -la /var/www/html/status.html
```

## 🐛 Troubleshooting

### El HTML no se genera

```bash
# Verificar que el script está corriendo
ps aux | grep sysmon_web

# Ver errores en logs
cat /tmp/sysmon.log

# Verificar permisos de escritura
touch /var/www/html/test.html
```

### Error: ModuleNotFoundError: psutil

```bash
# Debian/Ubuntu
sudo apt install python3-psutil python3-docker

# Con pip (si no es managed environment)
pip3 install psutil docker
```

### Docker containers no aparecen

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión
exit
# Volver a conectar via SSH
```

### 404 Not Found en /status.html

```bash
# Verificar que el archivo existe
ls -l /var/www/html/status.html

# Verificar configuración Nginx
sudo nginx -t
sudo systemctl restart nginx
```

## 📚 Documentación Adicional

- [Installation Guide](docs/INSTALLATION.md) - Instalación paso a paso
- [Customization Guide](docs/CUSTOMIZATION.md) - Personalización avanzada
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Solución de problemas comunes

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/MejorFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva feature'`)
4. Push (`git push origin feature/MejorFeature`)
5. Abre un Pull Request

## 💡 Ideas para Mejoras Futuras

- [ ] Gráficos históricos con Chart.js
- [ ] Alertas por email/webhook cuando se exceden umbrales
- [ ] API REST para consultar métricas programáticamente
- [ ] Dashboard multi-servidor
- [ ] Modo light theme
- [ ] Exportar métricas a Prometheus/Grafana

## 📝 Licencia

Este proyecto está bajo la licencia MIT - ver [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Kevin Jose Romero Perez**

- GitHub: [@romerok9](https://github.com/romerok9)
- LinkedIn: [kevs-romero](https://www.linkedin.com/in/kevs-romero/)
- Portfolio: [mytechzone.dev](https://mytechzone.dev) *(example)*

## ⭐ Show your support

Si este proyecto te fue útil, ¡dale una ⭐️!

## 🙏 Agradecimientos

- [psutil](https://github.com/giampaolo/psutil) - Librería para métricas del sistema
- [docker-py](https://github.com/docker/docker-py) - API de Docker para Python
- Inspiración de diseño: portfolios minimalistas en Dribbble

---

**Made with ❤️ for the DevOps community**

