# sysmon.py - Monitor de Sistema con soporte Docker/n8n

import psutil
import time
import curses
from collections import deque

try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

# --- Variables Globales y Configuración ---
UPDATE_INTERVAL = 1  # Frecuencia de actualización en segundos
MAX_HISTORY = 30     # Número de puntos de historial para el gráfico de red

# Inicializar historial para el tráfico de red (Deque es inmutable y eficiente)
net_history = deque([(0, 0)] * MAX_HISTORY, maxlen=MAX_HISTORY) # (bytes_sent, bytes_recv)
prev_net = psutil.net_io_counters()

# Cliente Docker (si está disponible)
docker_client = None
if DOCKER_AVAILABLE:
    try:
        docker_client = docker.from_env()
    except Exception:
        DOCKER_AVAILABLE = False

# --- Funciones de Utilidad ---

def draw_bar(stdscr, y, x, label, percentage, width=50, color_pair=1):
    """Dibuja una barra de progreso basada en el porcentaje."""
    # Aseguramos que el porcentaje esté entre 0 y 100
    percentage = max(0, min(100, int(percentage)))
    
    # Calcular la longitud de la barra rellena
    filled_len = int(width * percentage // 100)
    
    # Crear la barra de texto
    bar = '[' + '#' * filled_len + '-' * (width - filled_len) + ']'
    
    # Mostrar la etiqueta, la barra y el porcentaje
    stdscr.addstr(y, x, f"{label:<12}", curses.color_pair(color_pair))
    stdscr.addstr(y, x + 12, bar, curses.color_pair(color_pair))
    stdscr.addstr(y, x + 12 + width + 2, f"{percentage:3.0f}%", curses.color_pair(color_pair))


def bytes_to_human(n):
    """Convierte bytes a un formato legible (KB, MB, GB)."""
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i * 10)
    
    for symbol in reversed(symbols):
        if n >= prefix[symbol]:
            value = n / prefix[symbol]
            return f"{value:.2f} {symbol}"
    return f"{n:.2f} B"

def draw_network_chart(stdscr, y, x, history, max_val):
    """Dibuja un gráfico simple de líneas para el tráfico de red."""
    stdscr.addstr(y, x, f"Tráfico de Red (Máx: {bytes_to_human(max_val)}/s)", curses.A_BOLD)
    height = 5
    width = MAX_HISTORY
    
    # Inicializar el área del gráfico
    for i in range(height):
        stdscr.addstr(y + 1 + i, x, " " * width)
        
    # Dibujar eje Y y escala
    stdscr.addstr(y + 1, x - 5, "⬆ Max", curses.color_pair(2))
    stdscr.addstr(y + height, x - 5, "⬇ Min", curses.color_pair(2))

    # Dibujar puntos de historial
    for i, (sent, recv) in enumerate(history):
        # Normalizar los valores para la altura del gráfico (0 a height-1)
        # sent_norm y recv_norm son la altura desde la parte inferior (y + height)
        sent_height = int(height * sent / max_val) if max_val else 0
        recv_height = int(height * recv / max_val) if max_val else 0
        
        # Sent (Salida) - Color verde
        if sent_height > 0:
            stdscr.addstr(y + height - sent_height + 1, x + i, "▲", curses.color_pair(3))
            
        # Recv (Entrada) - Color azul
        if recv_height > 0:
            stdscr.addstr(y + height - recv_height + 1, x + i, "▼", curses.color_pair(4))

def get_network_connections(limit=5):
    """Obtiene conexiones de red activas."""
    try:
        connections = psutil.net_connections(kind='inet')
        active_connections = []
        
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                active_connections.append({
                    'remote_ip': conn.raddr.ip,
                    'remote_port': conn.raddr.port,
                    'local_port': conn.laddr.port if conn.laddr else 0,
                    'status': conn.status
                })
        
        # Agrupar por IP remota para contar conexiones
        ip_counts = {}
        for conn in active_connections:
            ip = conn['remote_ip']
            if ip in ip_counts:
                ip_counts[ip]['count'] += 1
            else:
                ip_counts[ip] = {'count': 1, 'ports': [conn['remote_port']]}
        
        # Ordenar por número de conexiones
        sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1]['count'], reverse=True)
        return sorted_ips[:limit]
    except (psutil.AccessDenied, PermissionError):
        return []

def get_docker_info():
    """Obtiene información sobre contenedores Docker y sus recursos."""
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
            if status == 'running':
                docker_info['running'] += 1
                
                # Obtener estadísticas de uso de recursos
                try:
                    stats = container.stats(stream=False)
                    
                    # Calcular uso de CPU
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
                    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                    cpu_percent = 0.0
                    if system_delta > 0 and cpu_delta > 0:
                        cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [1])) * 100.0
                    
                    # Calcular uso de memoria
                    mem_usage = stats['memory_stats'].get('usage', 0)
                    mem_limit = stats['memory_stats'].get('limit', 1)
                    mem_percent = (mem_usage / mem_limit) * 100 if mem_limit > 0 else 0
                    
                    docker_info['containers'].append({
                        'name': container.name,
                        'status': status,
                        'cpu_percent': cpu_percent,
                        'mem_usage': mem_usage,
                        'mem_percent': mem_percent
                    })
                except Exception:
                    # Si no se pueden obtener stats, solo mostrar el nombre y estado
                    docker_info['containers'].append({
                        'name': container.name,
                        'status': status,
                        'cpu_percent': 0,
                        'mem_usage': 0,
                        'mem_percent': 0
                    })
            else:
                docker_info['stopped'] += 1
        
        return docker_info
    except Exception:
        return None

def main(stdscr):
    # Configuración de Curses
    curses.curs_set(0) # Ocultar cursor
    stdscr.nodelay(1)  # No bloquear la espera de entrada
    
    # Inicializar colores (Color Pair 1: Default, 2: Info/Warning, 3: Success/Up, 4: Info/Down, 5: Red/Critical)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Referenciar las variables globales
    global prev_net, net_history
    
    while True:
        stdscr.clear()
        y = 1
        
        # --- Cabecera (Documentation-as-Code) ---
        header = "SysDevOps-Pro v2.0: Monitor Sistema + Docker/n8n | Presione 'q' para salir"
        stdscr.addstr(0, 0, header.ljust(curses.COLS - 1), curses.A_REVERSE)
        
        # --- 1. CPU (Procesador) ---
        cpu_percent = psutil.cpu_percent(interval=None) # Non-blocking
        draw_bar(stdscr, y, 0, "CPU Total", cpu_percent, color_pair=3)
        y += 1
        stdscr.addstr(y, 0, f"  Núcleos (Físicos/Lógicos): {psutil.cpu_count(logical=False)} / {psutil.cpu_count(logical=True)}", curses.color_pair(2))
        y += 2
        
        # --- 2. RAM (Memoria) ---
        mem = psutil.virtual_memory()
        draw_bar(stdscr, y, 0, "RAM Usada", mem.percent, color_pair=4)
        y += 1
        stdscr.addstr(y, 0, f"  Total: {bytes_to_human(mem.total)} | Usado: {bytes_to_human(mem.used)} | Disponible: {bytes_to_human(mem.available)}", curses.color_pair(2))
        y += 2

        # --- 3. Disco (Sistema de Archivos) ---
        # Monitorear la partición raíz '/' donde está el SO y Docker
        disk = psutil.disk_usage('/')
        draw_bar(stdscr, y, 0, "Disco (Root)", disk.percent, color_pair=1)
        y += 1
        stdscr.addstr(y, 0, f"  Total: {bytes_to_human(disk.total)} | Usado: {bytes_to_human(disk.used)} | Disponible: {bytes_to_human(disk.free)}", curses.color_pair(2))
        y += 2
        
        # --- 4. Red (Tráfico) ---
        current_net = psutil.net_io_counters()
        
        # Calcular tasas (bytes por segundo)
        time_diff = UPDATE_INTERVAL
        sent_rate = (current_net.bytes_sent - prev_net.bytes_sent) / time_diff
        recv_rate = (current_net.bytes_recv - prev_net.bytes_recv) / time_diff
        
        prev_net = current_net # Actualizar contador previo
        
        # Añadir al historial
        net_history.append((sent_rate, recv_rate))

        # Determinar el valor máximo para normalizar el gráfico
        max_rate = max([max(s, r) for s, r in net_history])
        if max_rate == 0: max_rate = 1 # Evitar división por cero

        # Mostrar tasas actuales
        stdscr.addstr(y, 0, f"Salida (Sent): {bytes_to_human(sent_rate)}/s | Entrada (Recv): {bytes_to_human(recv_rate)}/s", curses.A_BOLD)
        y += 1
        
        # Dibujar el gráfico de red
        draw_network_chart(stdscr, y, 5, net_history, max_rate)
        y += 7 # Espacio para el gráfico

        # --- 5. Docker & Contenedores ---
        if DOCKER_AVAILABLE:
            docker_info = get_docker_info()
            if docker_info:
                stdscr.addstr(y, 0, "═" * 70, curses.color_pair(2))
                y += 1
                stdscr.addstr(y, 0, f"🐳 DOCKER - Contenedores: {docker_info['running']} activos | {docker_info['stopped']} detenidos", curses.A_BOLD | curses.color_pair(3))
                y += 1
                
                # Mostrar detalles de cada contenedor activo
                for container in docker_info['containers'][:5]:  # Limitar a 5 contenedores
                    name = container['name'][:20]  # Limitar longitud del nombre
                    cpu = container['cpu_percent']
                    mem = container['mem_percent']
                    mem_usage = bytes_to_human(container['mem_usage'])
                    
                    # Destacar n8n si está presente
                    color = curses.color_pair(3) if 'n8n' in container['name'].lower() else curses.color_pair(1)
                    stdscr.addstr(y, 2, f"▸ {name:<20} CPU: {cpu:5.1f}%  RAM: {mem:5.1f}% ({mem_usage})", color)
                    y += 1
                y += 1
        else:
            stdscr.addstr(y, 0, "Docker no disponible (instalar: pip install docker)", curses.color_pair(2))
            y += 2

        # --- 6. Conexiones de Red Activas ---
        connections = get_network_connections(limit=5)
        if connections:
            stdscr.addstr(y, 0, "═" * 70, curses.color_pair(2))
            y += 1
            stdscr.addstr(y, 0, "🌐 CONEXIONES DE RED ACTIVAS", curses.A_BOLD | curses.color_pair(4))
            y += 1
            
            for ip, info in connections:
                # Verificar si es IP local o remota
                is_local = ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.') or ip == '127.0.0.1'
                color = curses.color_pair(3) if is_local else curses.color_pair(4)
                
                stdscr.addstr(y, 2, f"▸ {ip:<15}  {info['count']} conexión(es)", color)
                y += 1
            y += 1

        # --- 7. Temperatura CPU (si está disponible) ---
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                stdscr.addstr(y, 0, "🌡️  Temperatura CPU:", curses.A_BOLD)
                y += 1
                for name, entries in temps.items():
                    for entry in entries[:2]:  # Limitar a 2 sensores por categoría
                        temp_color = curses.color_pair(1)
                        if entry.current > 80:
                            temp_color = curses.color_pair(2)  # Amarillo si es alta
                        stdscr.addstr(y, 2, f"{entry.label or name}: {entry.current:.1f}°C", temp_color)
                        y += 1
                y += 1
        except (AttributeError, OSError):
            # Sensores no disponibles en este sistema
            pass

        # --- 8. Info de Tiempo de Ejecución (SRE) ---
        boot_time = time.time() - psutil.boot_time()
        stdscr.addstr(y, 0, f"⏱️  Tiempo activo (Uptime): {time.strftime('%H:%M:%S', time.gmtime(boot_time))}", curses.A_BOLD)
        
        
        # Actualizar la pantalla
        stdscr.refresh()
        
        # Control de Salida y Pausa
        key = stdscr.getch()
        if key == ord('q'):
            break

        # Pausa
        time.sleep(UPDATE_INTERVAL)

# Ejecutar el wrapper de curses
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario.")
    except Exception as e:
        print(f"\nOcurrió un error: {e}")