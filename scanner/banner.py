import socket
from config import TIMEOUT

def grab_banner(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        sock.connect((target_ip, port))

        banner = sock.recv(1024).decode(errors="ignore").strip()

        sock.close()

        return banner

    except socket.error:
        return ""



if __name__ == "__main__":
    ip = socket.gethostbyname("scanme.nmap.org")

    print("80:", grab_banner(ip, 80))
    print("22:", grab_banner(ip, 22))