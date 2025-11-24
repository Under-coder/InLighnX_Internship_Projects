#importing libraries 
import scapy.all as scapy
import socket
import threading
from queue import Queue
import ipaddress
import tkinter as tk
from tkinter import ttk

# Function to detect OS based on TTL value
def detect_os(ip):
    try:
        packet = scapy.IP(dst=ip)/scapy.ICMP()
        reply = scapy.sr1(packet, timeout=1, verbose=0)
        if reply is None:
            return "Unknown"

        ttl = reply.ttl

        if ttl <= 64:
            return "Linux/Unix"
        elif ttl <= 128:
            return "Windows"
        elif ttl <= 255:
            return "Cisco/Networking Device"
        else:
            return "Unknown"
    except:
        return "Unknown"


def scan(ip, results_queue):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    answer = scapy.srp(packet, timeout=1, verbose=False)[0]

    clients = []
    for client in answer:
        client_info = {"IP": client[1].psrc, "MAC": client[1].hwsrc}

        # Hostname
        try:
            hostname = socket.gethostbyaddr(client_info["IP"])[0]
        except socket.herror:
            hostname = "Unknown"
        client_info["Hostname"] = hostname

        # OS Detection
        client_info["OS"] = detect_os(client_info["IP"])
        clients.append(client_info)
    results_queue.put(clients)


# Function to print results
def print_result(result):
    print("IP\t\t\tMAC Address\t\tHostname\t\t\tOS")
    print("-"*110)
    for client in result:
        print(f"{client['IP']}\t\t{client['MAC']}\t{client['Hostname']}\t{client['OS']}")


# Main function to handle threading and scanning
def main(cidr, gui_table=None):
    results_queue = Queue()
    threads = []
    network = ipaddress.ip_network(cidr, strict=False)

    for ip in network.hosts():
        thread = threading.Thread(target=scan, args=(str(ip), results_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    all_clients = []
    while not results_queue.empty():
        all_clients.extend(results_queue.get())

    # If GUI mode: insert into table instead of printing
    if gui_table:
        for client in all_clients:
            gui_table.insert("", tk.END, values=(
                client["IP"],
                client["MAC"],
                client["Hostname"],
                client["OS"]
            ))
    else:
        print_result(all_clients)


# GUI Functionality
def launch_gui():
    root = tk.Tk()
    root.title("Network Scanner (ARP + OS Detection)")
    root.geometry("800x450")

    tk.Label(root, text="Enter CIDR (Example: 192.168.1.0/24)", font=("Arial", 12)).pack(pady=5)
    cidr_entry = tk.Entry(root, width=30, font=("Arial", 12))
    cidr_entry.pack(pady=5)

    columns = ("IP", "MAC", "Hostname", "OS")
    table = ttk.Treeview(root, columns=columns, show="headings", height=15)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=180)
    table.pack(pady=10)

    def start_scan():
        cidr = cidr_entry.get()
        for row in table.get_children():
            table.delete(row)

        threading.Thread(target=main, args=(cidr, table), daemon=True).start()

    tk.Button(root, text="Start Scan", font=("Arial", 12), command=start_scan).pack(pady=5)

    root.mainloop()


# Entry point
if __name__ == "__main__":
    mode = input("Choose your interface: (1) CLI  (2) GUI  : ")

    if mode == "2":
        launch_gui()
    else:
        cidr = input("Enter network IP Address: ")
        main(cidr)
