from echo_client import client
import socket
import threading
import os


if __name__ == '__main__':
    threads = []
    for x in range(5):
        thread = threading.Thread(target=client, args=("This is a longer sentence",))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
