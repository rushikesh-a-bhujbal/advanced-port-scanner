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



print(validate_target("192.168.1.1"))
print(validate_target("google.com"))

try:
    print(validate_target("abc..com"))
except ValueError as e:
    print(e)