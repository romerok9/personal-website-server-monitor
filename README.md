# Personal Website + Blog + Real-Time Server Monitor

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Monitoring-2496ED?style=flat-square&logo=docker)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

Portfolio personal minimalista con blog técnico bilingüe (EN/ES) y dashboard de monitoreo en tiempo real de servidor Debian/Linux. Incluye métricas de CPU, RAM, disco, red, **temperatura del CPU** y containers Docker, actualizadas automáticamente cada 30 segundos.

**🌐 Live Demo:** [mytechzone.dev](https://mytechzone.dev)

---

## ✨ Features Overview

Modern, minimalist portfolio combined with a technical blog and powerful real-time server monitoring solution.

---

## 🎯 Características

### 📝 Portfolio Website + Technical Blog

- ✅ **Diseño minimalista** - Inspirado en portfolios tech profesionales
- ✅ **Blog técnico completo** - 18 posts sobre DevOps, AWS, IA y Home Lab
- ✅ **Bilingüe (EN/ES)** - Selector de idioma con localStorage
- ✅ **Responsive** - Se adapta a móvil, tablet y desktop
- ✅ **Dark theme** - Diseño moderno enfocado en legibilidad
- ✅ **Vanilla JavaScript** - Sin frameworks pesados, ultra-rápido
- ✅ **SEO friendly** - Estructura semántica optimizada
- ✅ **Custom favicon** - Diseño DevOps/Terminal style

#### Series del Blog:
- 🏠 **Home Lab DevOps** (6 posts) - Notebook antigua → servidor profesional
- ☁️ **Automatización AWS** (5 posts) - Scripts, CLI y cost optimization
- 🤖 **Agentes de IA en DevOps** (4 posts) - Prompt engineering y límites
- 🛠️ **AWS CLI Mastery** (3 posts) - JMESPath, workflows y best practices

### 🖥️ Server Monitor v2.0

- ✅ **Métricas del sistema**:
  - CPU: Uso en % y núcleos
  - 🌡️ **Temperatura del CPU** con alertas por color (NUEVO en v2.0)
  - RAM: Usado/Total/Disponible
  - Disco: Uso/Total/Libre  
  - Red: Tráfico total enviado/recibido
  - Uptime del sistema

- ✅ **Monitoreo Docker**:
  - Estado de containers (running/stopped)
  - Nombre e imagen de cada container
  - Contador de containers activos/detenidos

- ✅ **Sistema de alertas inteligente**:
  - 🟢 < 60°C: OK
  - 🟡 60-69°C: Warm
  - 🟠 70-79°C: Warning
  - 🔴 ≥ 80°C: Critical
  - ⚠️ Warning automático si temperatura ≥ 75°C

- ✅ **Auto-actualización**: Dashboard se refresca cada 30s
- ✅ **Barras de progreso visuales** con colores por estado
- ✅ **Ligero**: < 20 MB RAM consumidos

---

## 🌟 Open Source

Este proyecto es de código abierto para que otros puedan aprender y crear sus propios portfolios. El código está diseñado para ser fácil de entender y personalizar.

**Si encuentras útil este proyecto, considera dejarle una ⭐ al repo!**

### 📄 License

- **Code:** MIT License (libre uso con atribución)
- **Blog Content:** © 2025-2026 Kevin Romero (All rights reserved)

Puedes usar libremente el código HTML/CSS/Python como base para tu propio sitio. El contenido escrito del blog está protegido por copyright.

---

## 📋 Requisitos

- Python 3.10+
- Servidor Linux (Debian/Ubuntu recomendado)
- Docker (opcional, para monitoreo de containers)
- Nginx o servidor web similar

### Dependencias Python

\`\`\`bash
# Debian/Ubuntu
sudo apt install python3-psutil python3-docker

# Otras distros con pip
pip3 install psutil docker
\`\`\`

---

## 🚀 Quick Start

### 1. Clonar el repositorio

\`\`\`bash
git clone https://github.com/romerok9/personal-website-server-monitor.git
cd personal-website-server-monitor
\`\`\`

### 2. Personalizar el sitio web

Edita \`website/index.html\`:

\`\`\`html
<!-- Cambiar información personal -->
<h1>Tu Nombre</h1>
<p class="subtitle" data-en="Your Title" data-es="Tu Título">Your Title</p>

<!-- Actualizar links -->
<a href="https://linkedin.com/in/tu-perfil">LinkedIn</a>
<a href="https://github.com/tu-usuario">GitHub</a>
\`\`\`

### 3. Personalizar el blog

Los posts están en \`blog/posts/\`. Para crear un nuevo post:

\`\`\`bash
# Usar el template
cp blog/posts/_TEMPLATE.html blog/posts/mi-nuevo-post.html

# Editar contenido
nano blog/posts/mi-nuevo-post.html

# Agregar al index
nano blog/index.html  # Agregar entrada en el array 'posts'
\`\`\`

### 4. Configurar el monitor

Edita \`monitor/sysmon_web.py\`:

\`\`\`python
# Línea 13-14: Ajustar según tu configuración
UPDATE_INTERVAL = 30  # Segundos entre actualizaciones
OUTPUT_FILE = "/path/to/your/website/status.html"
\`\`\`

### 5. Copiar archivos al servidor

\`\`\`bash
# Sitio web + blog
scp -r website/* user@your-server:/var/www/html/
scp -r blog/ user@your-server:/var/www/html/

# Monitor
scp monitor/sysmon_web.py user@your-server:/opt/monitor/
scp monitor/start_monitor.sh user@your-server:/opt/monitor/
\`\`\`

### 6. Iniciar el monitor

\`\`\`bash
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
\`\`\`

### 7. Acceder

\`\`\`
https://yourdomain.com/              → Portfolio
https://yourdomain.com/blog/         → Blog técnico
https://yourdomain.com/status.html   → Server Monitor
\`\`\`

---

## 📂 Estructura del Proyecto

\`\`\`
personal-website-server-monitor/
├── website/
│   ├── index.html                  # Portfolio principal (bilingüe)
│   ├── favicon.svg                 # Favicon terminal-style
│   └── *.sh                        # Scripts de generación
├── blog/
│   ├── index.html                  # Blog index con filtros
│   └── posts/
│       ├── _TEMPLATE.html          # Template para nuevos posts
│       ├── notebook-a-servidor-homelab.html
│       ├── monitoreo-python-ligero.html
│       ├── cloudflare-tunnel-setup.html
│       └── ... (15 posts más)
├── monitor/
│   ├── sysmon_web.py              # Monitor web (genera HTML)
│   ├── sysmon.py                  # Monitor terminal (TUI)
│   ├── start_monitor.sh           # Script de inicio
│   └── sysmon-web.service         # Systemd service
├── .gitignore
├── LICENSE
└── README.md
\`\`\`

---

##

 📊 Métricas Monitoreadas

| Métrica | Descripción | Fuente |
|---------|-------------|--------|
| **CPU** | Uso en % y núcleos disponibles | \`/proc/stat\` |
| **Temperatura** | Temperatura del CPU en °C | \`/sys/class/thermal/thermal_zone*/temp\` |
| **RAM** | Usado/Total/Disponible en GB | \`/proc/meminfo\` |
| **Disco** | Uso/Total/Libre en GB | \`/proc/mounts\` |
| **Red** | Total enviado/recibido acumulado | \`/proc/net/dev\` |
| **Uptime** | Tiempo desde último boot | \`/proc/uptime\` |
| **Docker** | Estado de containers | Docker API |

---

## ⭐ Show Your Support

Si este proyecto te fue útil o aprendiste algo nuevo, ¡dale una ⭐️!

También puedes:
- Compartirlo con otros que estén aprendiendo DevOps
- Dejar feedback en Issues
- Contribuir con mejoras vía Pull Requests

---

## 👤 Autor

**Kevin Jose Romero Perez**  
*DevOps Engineer | SRE | Cloud Infrastructure*

- 🌐 Website: [mytechzone.dev](https://mytechzone.dev)
- 💼 LinkedIn: [kevs-romero](https://www.linkedin.com/in/kevs-romero/)
- 🐙 GitHub: [@romerok9](https://github.com/romerok9)
- 🎓 Credly: [kevs-romero](https://www.credly.com/users/kevs-romero)

---

**Made with ❤️ for the DevOps community**
