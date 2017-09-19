import socket
import threading
import time


def server():
    while True:
        conn, addr = sock.accept()
        conn.recv(1024)
        conn.send(b'HTTP/1.1 200 OK\n\nhello')
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 80))
sock.listen()

t = threading.Thread(target=server)
t.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sock.close()
        break

t.join()

