import socket
from typing import Tuple


def is_valid_ip(target: str) -> bool:
    """Return True if target is a syntactically valid IPv4 address."""
    try:
        socket.inet_pton(socket.AF_INET, target)
        return True
    except (OSError, TypeError):
        return False


def is_valid_domain(target: str) -> bool:
    """Return True if target looks like a syntactically valid domain name."""
    if not target:
        return False

    if "." not in target:
        return False

    if target.startswith(".") or target.endswith("."):
        return False

    if ".." in target:
        return False

    return True


def validate_target(target: str) -> str:
    """Validate that target is a usable IP address or domain name, else raise ValueError."""
    if is_valid_ip(target):
        return target

    if is_valid_domain(target):
        return target

    raise ValueError(f"Invalid target: {target}")


def validate_port_range(start: str, end: str) -> Tuple[int, int]:
    """Parse and validate a start/end port pair, returning them as a (start, end) int tuple."""
    try:
        start_port = int(start)
        end_port = int(end)
    except ValueError as exc:
        raise ValueError("Ports must be integers") from exc

    if start_port < 1 or end_port > 65535:
        raise ValueError("Ports must be between 1 and 65535")

    if start_port > end_port:
        raise ValueError("Start port cannot be greater than end port")

    return start_port, end_port
