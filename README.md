# Advanced Port Scanner (Recon Engine)

## Developed By

Rushikesh Bhujbal

## Description

A multi-threaded port scanner built in Python that detects open ports and performs basic service detection using banner grabbing. Designed to demonstrate networking, concurrency, and system-level programming.

## Features

* Scan target IP or domain
* Domain to IP resolution
* Custom port range scanning
* Multi-threaded scanning using queue and workers
* TCP connect-based port detection
* Banner grabbing (basic service detection)
* Clean CLI output
* Input validation and error handling

## Technologies Used

* Python (socket, threading, queue, argparse)
* CLI-based interface

## Usage

```bash
python main.py -t <target> -p <start-end>
```

## Example

```bash
python main.py -t scanme.nmap.org -p 20-90
```

## Sample Output

```
PORT     STATE     SERVICE
22       OPEN      SSH-2.0-OpenSSH_6.6.1p1
80       OPEN      (no banner)
```

## Limitations

* Only TCP connect scan (no SYN/stealth scan)
* Banner grabbing not guaranteed on all ports
* No UDP scanning
* Scans one target at a time

## Legal Disclaimer

This tool is for educational purposes only. Only scan systems you own or have permission to test.
