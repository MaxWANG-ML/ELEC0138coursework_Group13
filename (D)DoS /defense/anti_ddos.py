from scapy.all import *
import threading
import time
#username = Kitty
#password = 234567
SERVER_IP = "192.168.1.20"    # Server IP
# SERVER_IP = "127.0.0.1"    # Server IP
SERVER_PORT = 5000            # Server port
WHITELIST = set()             # Whitelist of IP addresses that successfully completed the handshake
ACK_TIMEOUT = 5               # The time to wait for ACK, in seconds

print("Anti-DDoS proxy is running... Listening for SYN packets...")

def reply_synack(pkt):
    ip = pkt[IP]
    tcp = pkt[TCP]

    # Generate SYN-ACK
    ip_reply = IP(src=ip.dst, dst=ip.src)
    tcp_reply = TCP(sport=tcp.dport, dport=tcp.sport, flags="SA", seq=1000, ack=tcp.seq + 1)

    send(ip_reply / tcp_reply, verbose=False)
    print(f"[+] Sent SYN-ACK to {ip.src}")

    # Wait for ACK
    def wait_for_ack(client_ip, client_port):
        def ack_filter(x):
            return (IP in x and TCP in x and
                    x[IP].src == client_ip and
                    x[IP].dst == SERVER_IP and
                    x[TCP].sport == client_port and
                    x[TCP].dport == SERVER_PORT and
                    x[TCP].flags == "A")  # Only ACK flag

        try:
            pkt = sniff(lfilter=ack_filter, timeout=ACK_TIMEOUT, count=1)
            if pkt:
                print(f"[✓] Completed handshake with {client_ip}. Added to whitelist.")
                WHITELIST.add(client_ip)
            else:
                print(f"[-] No ACK received from {client_ip}. Connection dropped.")
        except Exception as e:
            print(f"[!] Error sniffing for ACK: {e}")

    threading.Thread(target=wait_for_ack, args=(ip.src, tcp.sport)).start()

def main():
    # Get TCP SYN packets only
    def syn_filter(pkt):
        return IP in pkt and TCP in pkt and pkt[TCP].flags == "S" and pkt[TCP].dport == SERVER_PORT

    sniff(filter=f"tcp port {SERVER_PORT}", prn=reply_synack, lfilter=syn_filter, store=False, promisc=True)

if __name__ == "__main__":
    main()
