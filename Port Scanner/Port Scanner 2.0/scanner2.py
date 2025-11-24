# scanner2.py
# formatted to be used as a module for port scanning

import socket
import sys
import concurrent.futures

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def format_port_results(results):
    formatted_results = "Port Scan Results:\n"
    formatted_results += "{:<8} {:<15} {:<10}\n".format("Port", "Service", "Status")
    formatted_results += '-' * 85 + "\n"

    for port, service, banner, status in results:
        if status:
            formatted_results += f"{RED}{port:<8} {service:<15} {'Open':<10}{RESET}\n"
            if banner:
                for line in banner.split("\n"):
                    formatted_results += f"{GREEN}{'':<8}{line}{RESET}\n"
    return formatted_results


def get_banner(sock):
    try:
        sock.settimeout(1)
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return ""


def scan_tcp_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = 'Unknown'
            banner = get_banner(sock)
            return port, service, banner, True

        return port, "", "", False

    except:
        return port, "", "", False

    finally:
        try: sock.close()
        except: pass


def tcp_scan(target_host, start_port, end_port, progress_callback=None):
    target_ip = socket.gethostbyname(target_host)
    results = []

    ports = range(start_port, end_port + 1)
    total_ports = len(ports)

    with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
        futures = {executor.submit(scan_tcp_port, target_ip, p): p for p in ports}

        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            port, service, banner, status = future.result()
            results.append((port, service, banner, status))

            if progress_callback:
                progress_callback(i, total_ports)
            else:
                sys.stdout.write(f"\rProgress: {i}/{total_ports}")
                sys.stdout.flush()

    return results
