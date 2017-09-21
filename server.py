import socket
import threading
import time

def respGener(reqst):
    arrReqst = reqst.decode().split('\n')
    startStr = arrReqst[0].split(' ')
    reqstFile = startStr[1]
    headers = b'\n\n'

    if reqstFile == '/':
        reqstFile = '/index.html'

    with open('.' + reqstFile, 'rb') as file:
        body = file.read()

    if reqstFile.endswith('.css'):
        headers = b'\nContent-Type: text/css\n\n'
    elif reqstFile.endswith('.ico'):
        headers = b'\nContent-Type: image/x-icon\n\n'
    return b'HTTP/1.1 200 OK' + headers + body


def server():
    try:
        while True:
            conn, addr = sock.accept()
            conn.send(respGener(conn.recv(1024)))
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


