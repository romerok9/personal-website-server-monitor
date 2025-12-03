#!/usr/bin/env python3
# sysmon_web.py - Generador de dashboard web para métricas del sistema

import psutil
import time
import json
from datetime import datetime

try:
    import docker
    DOCKER_AVAILABLE = True
    docker_client = docker.from_env()
except:
    DOCKER_AVAILABLE = False
    docker_client = None

# Configuración
UPDATE_INTERVAL = 30  # Actualizar cada 30 segundos
OUTPUT_FILE = "/var/www/html/status.html"  # Ajustar según tu configuración

def bytes_to_human(n):
    """Convierte bytes a formato legible."""
    symbols = ('B', 'KB', 'MB', 'GB', 'TB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i * 10)
    
    for symbol in reversed(symbols):
        if n >= prefix[symbol]:
            value = n / prefix[symbol]
            return f"{value:.2f} {symbol}"
    return f"{n:.2f} B"

def get_system_metrics():
    """Obtener métricas del sistema."""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    
    # RAM
    mem = psutil.virtual_memory()
    
    # Disco
    disk = psutil.disk_usage('/')
    
    # Red
    net = psutil.net_io_counters()
    
    # Uptime
    boot_time = time.time() - psutil.boot_time()
    uptime = time.strftime('%dd %Hh %Mm', time.gmtime(boot_time))
    
    return {
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count
        },
        'memory': {
            'percent': mem.percent,
            'used': bytes_to_human(mem.used),
            'total': bytes_to_human(mem.total),
            'available': bytes_to_human(mem.available)
        },
        'disk': {
            'percent': disk.percent,
            'used': bytes_to_human(disk.used),
            'total': bytes_to_human(disk.total),
            'free': bytes_to_human(disk.free)
        },
        'network': {
            'sent': bytes_to_human(net.bytes_sent),
            'recv': bytes_to_human(net.bytes_recv)
        },
        'uptime': uptime
    }

def get_docker_metrics():
    """Obtener métricas de Docker."""
    if not DOCKER_AVAILABLE or not docker_client:
        return None
    
    try:
        containers = docker_client.containers.list(all=True)
        docker_info = {
            'running': 0,
            'stopped': 0,
            'containers': []
        }
        
        for container in containers:
            status = container.status
            docker_info['containers'].append({
                'name': container.name,
                'status': status,
                'image': container.image.tags[0] if container.image.tags else 'unknown'
            })
            
            if status == 'running':
                docker_info['running'] += 1
            else:
                docker_info['stopped'] += 1
        
        return docker_info
    except:
        return None

def generate_progress_bar(percent, width=20):
    """Generar barra de progreso HTML."""
    filled = int(width * percent / 100)
    empty = width - filled
    return '█' * filled + '░' * empty

def generate_html(metrics, docker_metrics):
    """Generar HTML con las métricas."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Determinar color según estado
    cpu_color = '#ef4444' if metrics['cpu']['percent'] > 80 else '#10b981' if metrics['cpu']['percent'] < 50 else '#f59e0b'
    mem_color = '#ef4444' if metrics['memory']['percent'] > 80 else '#10b981' if metrics['memory']['percent'] < 50 else '#f59e0b'
    disk_color = '#ef4444' if metrics['disk']['percent'] > 80 else '#10b981' if metrics['disk']['percent'] < 50 else '#f59e0b'
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>Server Status | MyTechZone</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #111;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 2rem;
        }}
        
        header {{
            border-bottom: 1px solid #333;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }}
        
        h1 {{
            font-size: 1.5rem;
            color: #60a5fa;
            margin-bottom: 0.5rem;
        }}
        
        .timestamp {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .status-online {{
            color: #10b981;
            font-weight: bold;
        }}
        
        .section {{
            margin-bottom: 2rem;
        }}
        
        h2 {{
            color: #888;
            font-size: 1rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding: 0.75rem;
            background: #0a0a0a;
            border-radius: 4px;
        }}
        
        .metric-label {{
            color: #b0b0b0;
            min-width: 100px;
        }}
        
        .metric-bar {{
            flex: 1;
            margin: 0 1rem;
            font-size: 0.9rem;
            letter-spacing: 2px;
        }}
        
        .metric-value {{
            color: #fff;
            font-weight: bold;
            min-width: 120px;
            text-align: right;
        }}
        
        .container-item {{
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.5rem;
            background: #0a0a0a;
            border-radius: 4px;
        }}
        
        .container-name {{
            color: #60a5fa;
        }}
        
        .status-running {{
            color: #10b981;
        }}
        
        .status-stopped {{
            color: #ef4444;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }}
        
        .info-item {{
            background: #0a0a0a;
            padding: 0.75rem;
            border-radius: 4px;
        }}
        
        .info-label {{
            color: #666;
            font-size: 0.85rem;
            margin-bottom: 0.25rem;
        }}
        
        .info-value {{
            color: #fff;
            font-size: 1.1rem;
        }}
        
        .back-link {{
            display: inline-block;
            margin-top: 2rem;
            color: #60a5fa;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .back-link:hover {{
            color: #93c5fd;
        }}
        
        @media (max-width: 768px) {{
            .info-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Server Status</h1>
            <p class="timestamp">Last updated: {timestamp} UTC</p>
            <p class="status-online">● System Online</p>
        </header>

        <div class="section">
            <h2>System Resources</h2>
            
            <div class="metric">
                <span class="metric-label">CPU</span>
                <span class="metric-bar" style="color: {cpu_color}">{generate_progress_bar(metrics['cpu']['percent'])}</span>
                <span class="metric-value">{metrics['cpu']['percent']:.1f}% ({metrics['cpu']['count']} cores)</span>
            </div>
            
            <div class="metric">
                <span class="metric-label">Memory</span>
                <span class="metric-bar" style="color: {mem_color}">{generate_progress_bar(metrics['memory']['percent'])}</span>
                <span class="metric-value">{metrics['memory']['percent']:.1f}% ({metrics['memory']['used']}/{metrics['memory']['total']})</span>
            </div>
            
            <div class="metric">
                <span class="metric-label">Disk</span>
                <span class="metric-bar" style="color: {disk_color}">{generate_progress_bar(metrics['disk']['percent'])}</span>
                <span class="metric-value">{metrics['disk']['percent']:.1f}% ({metrics['disk']['used']}/{metrics['disk']['total']})</span>
            </div>
        </div>
'''

    if docker_metrics and docker_metrics['containers']:
        html += f'''
        <div class="section">
            <h2>Docker Containers ({docker_metrics['running']} running, {docker_metrics['stopped']} stopped)</h2>
'''
        for container in docker_metrics['containers']:
            status_class = 'status-running' if container['status'] == 'running' else 'status-stopped'
            status_icon = '✓' if container['status'] == 'running' else '✗'
            
            html += f'''
            <div class="container-item">
                <span class="container-name">{container['name']}</span>
                <span class="{status_class}">{status_icon} {container['status']}</span>
            </div>
'''
        html += '        </div>\n'

    html += f'''
        <div class="section">
            <h2>Network & Uptime</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Total Sent</div>
                    <div class="info-value">↑ {metrics['network']['sent']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Received</div>
                    <div class="info-value">↓ {metrics['network']['recv']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">System Uptime</div>
                    <div class="info-value">{metrics['uptime']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Last Update</div>
                    <div class="info-value">{datetime.now().strftime('%H:%M:%S')}</div>
                </div>
            </div>
        </div>

        <a href="/" class="back-link">← Back to Home</a>
    </div>
</body>
</html>
'''
    
    return html

def main():
    """Loop principal."""
    print(f"Starting sysmon_web.py...")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Update interval: {UPDATE_INTERVAL}s")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            # Obtener métricas
            metrics = get_system_metrics()
            docker_metrics = get_docker_metrics()
            
            # Generar HTML
            html = generate_html(metrics, docker_metrics)
            
            # Escribir archivo
            with open(OUTPUT_FILE, 'w') as f:
                f.write(html)
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] ✓ Status updated - CPU: {metrics['cpu']['percent']:.1f}% | RAM: {metrics['memory']['percent']:.1f}%")
            
            # Esperar
            time.sleep(UPDATE_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\nStopping sysmon_web...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()

