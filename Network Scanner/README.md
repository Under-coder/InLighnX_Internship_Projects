 **Network Scanner**
----------------------------------------------------

This project is a Python-based network scanner that discovers active devices on a local network using ARP requests. It retrieves each device’s IP address, MAC address, hostname, and also performs OS detection using TTL-based fingerprinting (without relying on Nmap).

The scanner works by generating all hosts within a CIDR range, sending ARP requests to each IP using multithreading for fast scanning, resolving hostnames, and analyzing TTL values from responses to guess the operating system. An optional GUI interface (Tkinter) is included for users who prefer a visual workflow in addition to the original CLI output.

------------------------------------------------------------------

**📌 Features**

- ARP-based device discovery
- IP, MAC, and Hostname resolution
- OS Detection via TTL analysis
- Multithreaded scanning for speed
- Optional GUI for easier input and result display

----------------------------------------------------------------------------------------------
*⚠️ Windows Users: Scapy requires Npcap to be installed to send/receive layer-2 packets.
Download from: https://nmap.org/npcap/*

------------------------------------------------------------------------------------------------
