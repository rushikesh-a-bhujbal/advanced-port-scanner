import queue
import threading

from scanner.port_scanner import ScanProgress
from scanner.worker import worker


class TestWorker:
    def test_drains_queue_and_calls_task_done(self) -> None:
        q: "queue.Queue[int]" = queue.Queue()
        for port in (20, 21, 22):
            q.put(port)

        results = []
        lock = threading.Lock()
        progress = ScanProgress(total=3, verbose=False)

        def fake_scan_port(target_ip: str, port: int) -> bool:
            return port == 22

        worker(q, "127.0.0.1", results, lock, 1.0, progress, fake_scan_port)

        assert q.unfinished_tasks == 0
        assert [r[0] for r in results] == [22]

    def test_task_done_called_even_if_scan_raises(self) -> None:
        q: "queue.Queue[int]" = queue.Queue()
        q.put(80)

        results = []
        lock = threading.Lock()
        progress = ScanProgress(total=1, verbose=False)

        def failing_scan_port(target_ip: str, port: int) -> bool:
            raise RuntimeError("boom")

        try:
            worker(q, "127.0.0.1", results, lock, 1.0, progress, failing_scan_port)
        except RuntimeError:
            pass

        # task_done() must have fired in the finally block despite the exception,
        # otherwise a real q.join() in scan_ports() would hang forever.
        assert q.unfinished_tasks == 0
