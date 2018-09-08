import socket
import sys

def port_list(low=0, high=65535, showall=False):
    host = '127.0.0.1'
    for port in range(low, high+1):
        info = socket.getnameinfo((host, port), 0)
        if showall or not info[1].isdigit():
            print(str(port)+': '+str(info))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        port_list()
        sys.exit(1)
    low = int(sys.argv[1])
    high = int(sys.argv[2])
    port_list(low, high)
