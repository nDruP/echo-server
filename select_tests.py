from echo_select_client import client
import threading
import os

if __name__ == '__main__':
    threads = []
    for _ in range(5):
        t = threading.Thread(target=client,
                             args=("This is a longer sentence",))
        t.start()
        threads.append(t)

    for a in threads:
        a.join()
