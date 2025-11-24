# Main entry point for Port Scanner 2.0

# importing modules
import tkinter as tk
from gui import ScannerGUI
from scanner2 import tcp_scan
from udp_scanner import udp_scan
from os_detect import detect_os

# command-line interface
def cli():
    target = input("Target host: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))

    use_udp = input("UDP scan? (y/n): ").lower() == "y"
    use_os = input("OS detection? (y/n): ").lower() == "y"

    os_info = detect_os(target) if use_os else ""

    print("\nTCP Scan:")
    for r in tcp_scan(target, start, end):
        print(r, "OS:", os_info if r[3] else "")

    if use_udp:
        print("\nUDP Scan:")
        for r in udp_scan(target, start, end):
            print(r, "OS:", os_info if r[3] else "")


def main():
    mode = input("Choose mode: 1) CLI  2) GUI : ")
    if mode == "2":
        root = tk.Tk()
        ScannerGUI(root)
        root.mainloop()
    else:
        cli()


if __name__ == "__main__":
    main()
