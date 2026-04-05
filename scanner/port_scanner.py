import socket
import threading
import queue
from scanner.worker import worker
from utils.formatter import format_results
from config import THREAD_COUNT, TIMEOUT

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        result = sock.connect_ex((target_ip, port))

        sock.close()

        if result == 0:
            return True
        else:
            return False

    except socket.error:
        return False



def scan_ports(target_ip, start_port, end_port):
    q = queue.Queue()
    results = []

    # fill queue
    for port in range(start_port, end_port + 1):
        q.put(port)

    threads = []

    # create threads
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=worker, args=(q, target_ip, results, scan_port))
        t.start()
        threads.append(t)

    # wait for queue to finish
    q.join()

    return results


if __name__ == "__main__":

    target = "scanme.nmap.org"
    ip = socket.gethostbyname(target)

    open_ports = scan_ports(ip, 20, 90)
    format_results(open_ports)