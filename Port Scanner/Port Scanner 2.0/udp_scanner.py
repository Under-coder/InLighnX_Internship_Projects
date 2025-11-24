# UDP Port Scanner; to be used alongside TCP scanner as a module

# importing libraries
import socket
import concurrent.futures
import sys

# scanning UDP ports
def scan_udp_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)

        try: s.sendto(b"\x00", (ip, port))
        except: pass

        try:
            data, _ = s.recvfrom(1024)
            banner = data.decode(errors="ignore")
            try: service = socket.getservbyport(port, "udp")
            except: service = "Unknown"
            return port, service, banner, True
        except socket.timeout:
            try: service = socket.getservbyport(port, "udp")
            except: service = "Unknown"
            return port, service, "", True

    except:
        return port, "", "", False

    finally:
        try: s.close()
        except: pass

# main UDP scanning function
def udp_scan(target, start, end, progress_callback=None):
    ip = socket.gethostbyname(target)
    results = []

    ports = range(start, end + 1)
    total = len(ports)

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
        futs = {ex.submit(scan_udp_port, ip, p): p for p in ports}

        for i, f in enumerate(concurrent.futures.as_completed(futs), start=1):
            port, svc, banner, status = f.result()
            results.append((port, svc, banner, status))

            if progress_callback:
                progress_callback(i, total)
            else:
                sys.stdout.write(f"\rUDP {i}/{total}")
                sys.stdout.flush()

    return results
