import socket
import threading
import time


def server():
    try:
        while True:
            conn, addr = sock.accept()
            resp = conn.recv(1024).decode()
            print(resp)
            with open('index.html') as file:
                bHtml = file.read().encode()
            conn.send(b'HTTP/1.1 200 OK\n\n' + bHtml)
            conn.close()
    except OSError:
        print('pressed Ctrl-C')


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


