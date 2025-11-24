# GUI for Port Scanner 2.0

# importing libraries
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from scanner2 import tcp_scan
from udp_scanner import udp_scan
from os_detect import detect_os

# GUI Class
class ScannerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Port Scanner GUI")
        root.geometry("900x550")

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Target:").grid(row=0, column=0)
        self.target = tk.Entry(frame, width=25)
        self.target.grid(row=0, column=1)

        tk.Label(frame, text="Start Port:").grid(row=1, column=0)
        self.start = tk.Entry(frame, width=10)
        self.start.grid(row=1, column=1)

        tk.Label(frame, text="End Port:").grid(row=2, column=0)
        self.end = tk.Entry(frame, width=10)
        self.end.grid(row=2, column=1)

        self.use_tcp = tk.IntVar(value=1)
        self.use_udp = tk.IntVar()
        self.use_os = tk.IntVar()

        # Checkbuttons for options
        tk.Checkbutton(frame, text="TCP Scan", variable=self.use_tcp).grid(row=3, column=0)
        tk.Checkbutton(frame, text="UDP Scan", variable=self.use_udp).grid(row=3, column=1)
        tk.Checkbutton(frame, text="OS Detection", variable=self.use_os).grid(row=3, column=2)

        tk.Button(frame, text="Start Scan", command=self.start_scan).grid(row=4, column=0, pady=10)

        cols = ("Port", "Protocol", "Service", "Status", "Banner", "OS")
        self.tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True)

        self.progress = ttk.Progressbar(root, length=700, mode="determinate")
        self.progress.pack(pady=5)

    def start_scan(self):
        target = self.target.get().strip()
        if not target:
            messagebox.showwarning("Input Error", "Enter a target!")
            return

        try:
            s = int(self.start.get())
            e = int(self.end.get())
        except:
            messagebox.showwarning("Error", "Invalid port range")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        self.progress["value"] = 0

        threading.Thread(target=self.run_scan, args=(target, s, e), daemon=True).start()

    def run_scan(self, target, s, e):
        tasks = 0
        if self.use_tcp.get(): tasks += (e - s + 1)
        if self.use_udp.get(): tasks += (e - s + 1)

        self.progress["maximum"] = tasks

        def cb(a, b): self.progress["value"] += 1

        os_info = detect_os(target) if self.use_os.get() else ""

        if self.use_tcp.get():
            results = tcp_scan(target, s, e, cb)
            for port, svc, banner, open_ in results:
                self.tree.insert("", "end", values=(
                    port, "TCP", svc, "Open" if open_ else "Closed", banner, os_info if open_ else ""
                ))

        if self.use_udp.get():
            results = udp_scan(target, s, e, cb)
            for port, svc, banner, open_ in results:
                self.tree.insert("", "end", values=(
                    port, "UDP", svc, "Open/Filtered" if open_ else "Closed", banner, os_info if open_ else ""
                ))
