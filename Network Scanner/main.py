#importing libraries

import scapy.all as scapy
import socket
import threading
from queue import Queue
import ipaddress


def scan(ip, results_queue):
    # Create ARP request packet
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    answer = scapy.srp(packet, timeout=1, verbose=False)[0]

    # Add client info to results
    clients = []

    for client in answer:
        client_info = {"IP": client[1].psrc, "MAC": client[1].hwsrc}
        try:
            hostname = socket.gethostbyaddr(client_info["IP"])[0]
            client_info["Hostname"] = hostname
        except socket.herror:
            client_info["Hostname"] = "Unknown"
        clients.append(client_info)
    results_queue.put(clients)

# Function to print results
def print_result(result):
    print("IP\t\t\tMAC Address\t\tHostname")
    print("-"*80)
    for client in result:
        print(f"{client['IP']}\t\t{client['MAC']}\t{client['Hostname']}")

# Main function to handle threading and scanning
def main(cidr):
    results_queue = Queue()
    threads = []
    network = ipaddress.ip_network(cidr, strict=False)      # Make a network object

    for ip in network.hosts():
        thread = threading.Thread(target=scan, args=(str(ip), results_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    all_clients = []
    while not results_queue.empty():
        all_clients.extend(results_queue.get())
    print_result(all_clients)


# Entry point
if __name__ == "__main__":
    cidr = input("Enter network IP Address: ")
    main(cidr)

