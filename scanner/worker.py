import queue
import threading
from typing import TYPE_CHECKING, Callable, List, Tuple

from scanner.banner import grab_banner

if TYPE_CHECKING:
    from scanner.port_scanner import ScanProgress


def worker(
    q: "queue.Queue[int]",
    target_ip: str,
    results: List[Tuple[int, str]],
    results_lock: threading.Lock,
    timeout: float,
    progress: "ScanProgress",
    scan_port: Callable[[str, int], bool],
) -> None:
    """Drain ports from the shared queue, scan each one, and record any that are open.

    Uses get_nowait/Empty instead of `while not q.empty()` because empty()-then-get()
    is a check-then-act race: two threads can both see a non-empty queue and then
    have only one of them actually get an item, leaving the other blocked on get().
    task_done() is called in a finally block so a q.join() in the caller can never
    hang, even if scan_port raises something unexpected.
    """
    while True:
        try:
            port = q.get_nowait()
        except queue.Empty:
            break
        try:
            if scan_port(target_ip, port):
                banner = grab_banner(target_ip, port, timeout)
                with results_lock:
                    results.append((port, banner))
        finally:
            q.task_done()
            progress.increment()
