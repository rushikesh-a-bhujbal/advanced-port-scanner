import socket
from utils.validator import is_valid_ip, is_valid_domain

def resolve_target(target):
    if is_valid_ip(target):
        return target

    if is_valid_domain(target):
        try:
            ip = socket.gethostbyname(target)
            return ip
        except socket.gaierror:
            raise ValueError("Could not resolve domain")

    raise ValueError("Invalid target")




if __name__ == "__main__":
    print(resolve_target("192.168.1.1"))
    print(resolve_target("google.com"))

    try:
        print(resolve_target("abc..com"))
    except ValueError as e:
        print(e)