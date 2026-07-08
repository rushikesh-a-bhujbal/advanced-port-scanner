import argparse
import sys
import time

from config import TIMEOUT, THREAD_COUNT
from scanner.port_scanner import scan_ports
from scanner.resolver import resolve_target
from utils.formatter import (
    build_result_rows,
    export_csv,
    export_json,
    print_results,
    print_summary,
)
from utils.validator import validate_port_range


def build_arg_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser for the scanner."""
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")

    parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
    parser.add_argument("-p", "--ports", required=True, help="Port range (e.g. 20-80)")
    parser.add_argument(
        "--threads",
        type=int,
        default=None,
        help=f"Number of worker threads (default: {THREAD_COUNT})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help=f"Socket timeout in seconds (default: {TIMEOUT})",
    )
    parser.add_argument(
        "--output",
        choices=["json", "csv"],
        default=None,
        help="Export results in this format (requires --outfile)",
    )
    parser.add_argument(
        "--outfile",
        default=None,
        help="File path to write --output results to",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print progress updates while scanning",
    )

    return parser


def main() -> None:
    """Parse CLI arguments, run the scan, and print/export the results."""
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.output and not args.outfile:
        parser.error("--output requires --outfile")

    try:
        target_ip = resolve_target(args.target)

        if "-" not in args.ports:
            raise ValueError("Port range must be in format start-end")

        start_str, end_str = args.ports.split("-", 1)
        start_port, end_port = validate_port_range(start_str, end_str)

        thread_count = args.threads if args.threads is not None else THREAD_COUNT
        timeout = args.timeout if args.timeout is not None else TIMEOUT

        start_time = time.perf_counter()
        results = scan_ports(
            target_ip,
            start_port,
            end_port,
            thread_count=thread_count,
            timeout=timeout,
            verbose=args.verbose,
        )
        elapsed = time.perf_counter() - start_time

        rows = build_result_rows(results)
        print_results(rows)
        print_summary(end_port - start_port + 1, len(rows), elapsed)

        if args.output == "json":
            export_json(rows, args.outfile)
        elif args.output == "csv":
            export_csv(rows, args.outfile)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
