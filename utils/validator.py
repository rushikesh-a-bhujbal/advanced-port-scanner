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



print(is_valid_domain("google.com"))
print(is_valid_domain("abc..com"))
print(is_valid_domain(".com"))
print(is_valid_domain("nodot"))