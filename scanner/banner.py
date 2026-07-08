import socket

from config import TIMEOUT


def grab_banner(target_ip: str, port: int, timeout: float = TIMEOUT) -> str:
    """Connect to an already-open port and read whatever banner the service sends.

    Returns an empty string if the service doesn't send a banner within the
    timeout, or if the connection fails outright.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((target_ip, port))
            return sock.recv(1024).decode(errors="ignore").strip()
    except OSError:
        return ""
