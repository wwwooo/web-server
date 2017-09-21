import socket
import threading
import time

def response(req):
    arr_req = req.decode().split('\n')
    arr_req_line = arr_req[0].split(' ')
    resource = arr_req_line[1]
    headers = ''

    if resource == '/':
        resource = '/index.html'

    with open('.' + resource, 'rb') as file:
        message_body = file.read()

    if resource.endswith('.css'):
        headers = 'Content-Type: text/css'
    elif resource.endswith('.ico'):
        headers = 'Content-Type: image/x-icon'

    return bytes('HTTP/1.1 200 OK\n' + headers + '\n\n', encoding='utf-8') + message_body


def server():
    try:
        while True:
            conn, addr = sock.accept()
            conn.send(response(conn.recv(1024)))
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
