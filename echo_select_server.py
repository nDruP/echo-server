import socket
import sys
import traceback
import select
import queue


buffer_size = 16


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10002)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(8)
    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        inputs = [sock]
        outputs = []
        msg_queue = {}
        while inputs:
            
            read, write, err_in = select.select(inputs, outputs, inputs)
            conn, addr = None, None
            
            for s in read:
                if s is sock:
                    print('waiting for a connection', file=log_buffer)
                    conn, addr = sock.accept()
                    print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                    conn.setblocking(0)
                    inputs.append(conn)
                    msg_queue[conn] = queue.Queue()
                    
                else:
                    try:
                        data = s.recv(buffer_size)
                        if data:
                            print('received "{0}"'.format(data.decode('utf8')))
                            msg_queue[s].put_nowait(data)
                            if s not in outputs:
                                outputs.append(s)
                        else:
                            if s in outputs:
                                outputs.remove(s)
                            inputs.remove(s)
                            s.close()
                            del msg_queue[s]

                    except Exception as e:
                        traceback.print_exc()
                        sys.exit(1)

            for s in write:
                try:
                    next_msg = msg_queue[s].get_nowait()
                except queue.Empty:
                    outputs.remove(s)
                else:
                    s.send(next_msg)

            for s in err_in:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del msg_queue[s]

    except KeyboardInterrupt:
        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
