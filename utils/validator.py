import socket

def is_valid_ip(target):
    try:
        socket.inet_aton(target)
        return True
    except:
        return False


print(is_valid_ip("192.168.1.1"))
print(is_valid_ip("999.999.999.999"))