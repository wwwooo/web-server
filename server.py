import socket


def response(req):
    # print(req)
    if req:
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
    return b'blalala'

sock = socket.socket()
sock.bind(('localhost', 80))
sock.listen()
sock.settimeout(1)

while True:
    try:
        try:
            conn, addr = sock.accept()
            conn.settimeout(1)
            data = b''
            while data.find(b'\r\n\r\n') == -1:
                a = conn.recv(1024)
                if a:
                    data += a
                else:
                    break
            conn.sendall(response(data))
            conn.close()
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        print('pressed Ctrl-C')
        sock.close()
        break