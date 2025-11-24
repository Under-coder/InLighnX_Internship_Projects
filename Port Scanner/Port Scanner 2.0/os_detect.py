# OS Detection Module

# importing libraries
import scapy.all as scapy

# function to detect operating system based on TTL value
def detect_os(ip):
    try:
        reply = scapy.sr1(scapy.IP(dst=ip)/scapy.ICMP(), timeout=1, verbose=0)
        if not reply: return ""
        ttl = int(reply.ttl)

        if ttl <= 64: return "Linux/Unix/Android"
        if ttl <= 128: return "Windows"
        if ttl <= 255: return "Network Device"

        return "Unknown"

    except:
        return ""
