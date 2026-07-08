import functools
import queue
import socket
import threading
from typing import List, Tuple

from config import TIMEOUT, THREAD_COUNT
from scanner.worker import worker


class ScanProgress:
    """Thread-safe counter that prints periodic "scanned N/total" updates when verbose."""

    def __init__(self, total: int, verbose: bool) -> None:
        self.total = total
        self.verbose = verbose
        self._scanned = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        """Record that one more port has been scanned, printing progress if it's due."""
        if not self.verbose:
            return
        with self._lock:
            self._scanned += 1
            scanned = self._scanned
        if scanned % 50 == 0 or scanned == self.total:
            print(f"[*] Scanned {scanned}/{self.total} ports...")


def scan_port(target_ip: str, port: int, timeout: float) -> bool:
    """Attempt a TCP connect to a single port and report whether it accepted the connection."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((target_ip, port)) == 0
    except OSError:
        return False


def scan_ports(
    target_ip: str,
    start_port: int,
    end_port: int,
    thread_count: int = THREAD_COUNT,
    timeout: float = TIMEOUT,
    verbose: bool = False,
) -> List[Tuple[int, str]]:
    """Scan a range of ports across a thread pool and return the open ones with their banners."""
    q: "queue.Queue[int]" = queue.Queue()
    results: List[Tuple[int, str]] = []
    results_lock = threading.Lock()

    for port in range(start_port, end_port + 1):
        q.put(port)

    total_ports = end_port - start_port + 1
    progress = ScanProgress(total_ports, verbose)
    num_threads = min(thread_count, total_ports)
    bound_scan_port = functools.partial(scan_port, timeout=timeout)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(
            target=worker,
            args=(q, target_ip, results, results_lock, timeout, progress, bound_scan_port),
            daemon=True,
        )
        t.start()
        threads.append(t)

    q.join()
    return results
