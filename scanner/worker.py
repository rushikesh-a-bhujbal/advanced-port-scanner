from scanner.banner import grab_banner

def worker(queue, target_ip, results, scan_port):
    while not queue.empty():
        port = queue.get()

        is_open = scan_port(target_ip, port)

        if is_open:
            banner = grab_banner(target_ip, port)
            results.append((port, banner))

        queue.task_done()


