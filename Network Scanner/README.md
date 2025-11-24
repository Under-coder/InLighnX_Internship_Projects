**Network Scanner**

A simple multi-threaded network scanning tool built using Python, Scapy, and ARP requests.
This tool discovers devices connected to a local network by scanning all hosts in a given subnet (CIDR) and displaying their:

-->IP Address

-->MAC Address

-->Hostname (if available)

🔧 Features

-->Fast scanning using multi-threading

-->ARP-based host discovery

-->Reverse DNS lookup for hostnames

-->Supports any subnet in CIDR notation (e.g., 192.168.1.0/24)

-->Clean and readable output table





*Note for Windows Users*

To run ARP-based scanning with Scapy, you must install Npcap (with WinPcap API-compatible mode enabled).
