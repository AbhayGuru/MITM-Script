**🕵️‍♂️ MITM ARP Spoofing Script:**

A Python-based ARP spoofing script for performing **Man-in-the-Middle (MITM)** attacks.  
This tool is intended for educational and penetration testing purposes only.


**⚡ Features:**
- ARP spoofing to intercept traffic between victim and gateway.
- Enables and disables IP forwarding automatically.
- Restores original ARP tables after exit (safe cleanup).
- Displays packet count while spoofing is active.
- Lightweight and easy to use.


**🖥️ Requirements:**
- Python 3.x
- [Scapy](https://scapy.net/) library
- Install via:
              **pip install scapy**

**🚀 Usage:**
**sudo python3 mitm-script.py <victim_ip> <gateway_ip>**

**Flow Diagram:**
   [ Victim ]  <--->  [ Attacker (You) ]  <--->  [ Gateway / Router ]
        |                     |                           |
        |---------------------|---------------------------|
                 Fake ARP replies make attacker 
                 appear as both victim & gateway
