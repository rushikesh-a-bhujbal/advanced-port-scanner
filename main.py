import argparse
from scanner.resolver import resolve_target
from scanner.port_scanner import scan_ports
from utils.validator import validate_port_range
from utils.formatter import format_results


def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")

    parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
    parser.add_argument("-p", "--ports", required=True, help="Port range (e.g. 20-80)")

    args = parser.parse_args()

    try:
        # Resolve target
        target_ip = resolve_target(args.target)

        # Parse and validate ports
        start_port, end_port = args.ports.split("-")
        start_port, end_port = validate_port_range(start_port, end_port)

        # Scan
        results = scan_ports(target_ip, start_port, end_port)

        # Output
        format_results(results)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()