import threading

def worker(queue, target_ip, results, scan_port):
    while not queue.empty():
        port = queue.get()

        is_open = scan_port(target_ip, port)

        if is_open:
            results.append(port)

        queue.task_done()


