import socket

from utils.validator import is_valid_ip, validate_target


def resolve_target(target: str) -> str:
    """Validate target, then resolve it to an IPv4 address (via DNS if it's a domain)."""
    validated = validate_target(target)

    if is_valid_ip(validated):
        return validated

    try:
        return socket.gethostbyname(validated)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve domain: {target}") from exc
