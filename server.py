import socket


def response(req_line, h, body):
    req_line = req_line.split(' ')
    resource = req_line[1]
    headers = ''

    if 'Content-Length' not in h:
        if resource == '/':
            resource = '/index.html'
    else:
        if resource == '/':
            resource = '/success.html'


    with open('.' + resource, 'rb') as file:
        message_body = file.read()

    if resource.endswith('.css'):
        headers = 'Content-Type: text/css'
    elif resource.endswith('.ico'):
        headers = 'Content-Type: image/x-icon'

    return bytes('HTTP/1.1 200 OK\n' + headers + '\n\n', encoding='utf-8') + message_body


def readData(s):
    data = ''
    while '\r\n\r\n' not in data:
        data += s.recv(1024).decode('utf-8')
    head, body = data.split('\r\n\r\n')
    parts = head.split('\r\n')
    start_line = parts[0]
    # headers = {h[0]: h[1].strip() for h in (p.split(':') for p in parts[1:])}
    headers = {}
    for p in parts[1:]:
        h = p.split(':')
        headers[h[0]] = h[1].strip()
    if 'Content-Length' in headers:
        body += s.recv(int(headers['Content-Length']) - len(body)).decode('utf-8')
    return start_line, headers, body

sock = socket.socket()
sock.bind(('localhost', 80))
sock.listen()
sock.settimeout(1)

while True:
    try:
        try:
            conn, addr = sock.accept()
            conn.settimeout(1)
            l, h, b = readData(conn)
            print(l, h, b)
            print('**********************')
            conn.sendall(response(l, h, b))
            conn.close()
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        print('pressed Ctrl-C')
        sock.close()
        break