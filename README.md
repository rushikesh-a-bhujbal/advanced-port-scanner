# Recon Scanner

A multi-threaded TCP connect-scan port scanner with banner grabbing.

## Developed By

Rushikesh Bhujbal

## Overview

Recon Scanner is a command-line port scanner written in pure Python. It resolves a
target hostname or IP, scans a given port range using a pool of worker threads, and
grabs service banners from any open ports it finds. It exists as a networking and
concurrency demonstration: a queue-backed thread pool, TCP connect scanning, and
socket-level banner grabbing, all built without any third-party libraries.

## Features

* Scan a target IP address or domain name
* Domain-to-IP resolution via DNS, with strict IPv4 validation for literal IPs
* Custom port range scanning (e.g. `20-8080`)
* Multi-threaded scanning using a `queue.Queue` + worker thread pool, sized down
  automatically for small port ranges
* TCP connect-based port detection
* Banner grabbing on open ports (best-effort; not all services send one)
* Configurable thread count and socket timeout via CLI flags
* Optional verbose progress output during long scans
* Scan summary (ports scanned, ports open, elapsed time)
* JSON/CSV export of results
* Clean Ctrl+C handling mid-scan
* Input validation and error handling throughout

## Project Structure

```
recon_scanner/
├── main.py                # CLI entry point: arg parsing, orchestration, output
├── config.py               # Default THREAD_COUNT and TIMEOUT values
├── scanner/
│   ├── __init__.py
│   ├── resolver.py         # Target validation + hostname-to-IP resolution
│   ├── port_scanner.py     # Thread pool orchestration, scan_port(), ScanProgress
│   ├── worker.py            # Per-thread queue-draining scan loop
│   └── banner.py            # Banner grabbing on open ports
├── utils/
│   ├── __init__.py
│   ├── validator.py         # IP/domain/port-range validation
│   └── formatter.py         # Structured result rows, printing, JSON/CSV export
├── tests/                    # pytest unit tests (mocked sockets, no live network)
├── pyproject.toml           # Project metadata, pytest config; zero runtime deps
└── LICENSE
```

## How It Works

`main.py` resolves and validates the target and port range, then calls
`scan_ports()`, which fills a `queue.Queue` with every port in the range and starts
a pool of worker threads (sized to `min(thread_count, port_count)`). Each worker
pulls ports off the queue with `get_nowait()` in a loop until it's empty, attempts a
TCP connect (`connect_ex`) against each one, and — if the port is open — grabs
whatever banner the service sends within the timeout window. Results are collected
into a shared list behind a lock, then handed to `formatter.py`, which turns them
into structured rows for console printing and optional JSON/CSV export.

## Installation

```bash
git clone <repository-url>
cd recon_scanner
```

No third-party runtime dependencies are required — the scanner only uses Python's
standard library (`socket`, `threading`, `queue`, `argparse`, `csv`, `json`). Install
`pytest` (see below) only if you want to run the test suite.

## Usage

```bash
python main.py -t <target> -p <start-end> [options]
```

| Flag | Description | Default |
|---|---|---|
| `-t`, `--target` | Target IP address or domain (required) | — |
| `-p`, `--ports` | Port range, e.g. `20-80` (required) | — |
| `--threads` | Number of worker threads | `THREAD_COUNT` in `config.py` (100) |
| `--timeout` | Socket timeout in seconds | `TIMEOUT` in `config.py` (1) |
| `--output` | Export format: `json` or `csv` (requires `--outfile`) | none |
| `--outfile` | File path to write `--output` results to | none |
| `-v`, `--verbose` | Print progress updates while scanning | off |

## Example Commands

```bash
python main.py -t 127.0.0.1 -p 7990-8010
```

Sample output (with a local HTTP server listening on port 8000):

```
PORT     STATE     SERVICE
8000     OPEN      (no banner)

Scanned 21 ports in 1.04s - 1 open
```

Exporting results to JSON:

```bash
python main.py -t 127.0.0.1 -p 1-1024 --output json --outfile results.json
```

## Running Tests

```bash
pip install pytest
pytest
```

Tests mock `socket` calls directly (e.g. `socket.gethostbyname`) and don't require
network access or a live target.

## Limitations

* TCP connect scan only — no SYN/stealth scan
* No UDP scanning
* Banner grabbing is best-effort; many services don't send one without a request
* Scans one target at a time

## Legal Disclaimer

This tool is for educational purposes only. Only scan systems you own or have
permission to test.

## License

Released under the [MIT License](LICENSE).
