import socket

def is_valid_ip(target):
    try:
        socket.inet_aton(target)
        return True
    except:
        return False

def is_valid_domain(target):
    if not target:
        return False

    if "." not in target:
        return False

    if target.startswith(".") or target.endswith("."):
        return False

    if ".." in target:
        return False

    return True


def validate_target(target):
    if is_valid_ip(target):
        return target

    if is_valid_domain(target):
        return target

    raise ValueError("Invalid target")



def validate_port_range(start, end):
    try:
        start = int(start)
        end = int(end)
    except:
        raise ValueError("Ports must be integers")

    if start < 1 or end > 65535:
        raise ValueError("Ports must be between 1 and 65535")

    if start > end:
        raise ValueError("Start port cannot be greater than end port")

    return start, end



print(validate_port_range(20, 80))

try:
    print(validate_port_range(0, 80))
except ValueError as e:
    print(e)

try:
    print(validate_port_range(100, 50))
except ValueError as e:
    print(e)