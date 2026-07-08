import csv
import json
from typing import Any, Dict, List, Tuple


def build_result_rows(results: List[Tuple[int, str]]) -> List[Dict[str, Any]]:
    """Convert raw (port, banner) scan results into sorted structured rows.

    This is the single source of truth for result shape - the console printer
    and the JSON/CSV exporters all consume these rows instead of each
    re-deriving formatting from raw tuples.
    """
    rows = []
    for port, banner in sorted(results):
        rows.append(
            {
                "port": port,
                "state": "open",
                "service": banner if banner else "(no banner)",
            }
        )
    return rows


def print_results(rows: List[Dict[str, Any]]) -> None:
    """Print scan result rows as a simple aligned table."""
    print("\nPORT     STATE     SERVICE")
    for row in rows:
        print(f"{row['port']:<8} {row['state'].upper():<9} {row['service']}")


def print_summary(total_scanned: int, open_count: int, elapsed_seconds: float) -> None:
    """Print a one-line summary of the scan: ports scanned, ports open, elapsed time."""
    print(f"\nScanned {total_scanned} ports in {elapsed_seconds:.2f}s - {open_count} open")


def export_json(rows: List[Dict[str, Any]], path: str) -> None:
    """Write scan result rows to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)


def export_csv(rows: List[Dict[str, Any]], path: str) -> None:
    """Write scan result rows to a CSV file with port, state, service columns."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["port", "state", "service"])
        writer.writeheader()
        writer.writerows(rows)
