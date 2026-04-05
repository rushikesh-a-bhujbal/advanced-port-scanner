import socket

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        sock.close()

        if result == 0:
            return True
        else:
            return False

    except Exception:
        return False


if __name__ == "__main__":
    target = "scanme.nmap.org"
    ip = socket.gethostbyname(target)

    print("Port 80:", scan_port(ip, 80))
    print("Port 81:", scan_port(ip, 81))