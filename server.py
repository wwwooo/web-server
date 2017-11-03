import socket
import sqlite3
from creator import create_html


def response(req_line, req_headers, req_message_body):
    resource = req_line.split(' ')[1]
    headers = ''

    if resource == '/':
        if 'Content-Length' not in req_headers:
            message_body = bytes(create_html(template='index.html'), encoding='utf-8')
        else:
            message_body = bytes(create_html(), encoding='utf-8')
    elif resource == '/admin.html':
        if not len(req_message_body):
            message_body = bytes(create_html(msg='Protected Information. Enter the password',
                                         template='authorization.html'), encoding='utf-8')
        elif req_message_body['password'] == str(1234):
            message_body = b''
            conn_db = sqlite3.connect('contacts_db.sqlite')
            c = conn_db.cursor()
            for row in c.execute("SELECT * FROM contacts"):
                message_body += bytes(str(row), encoding='utf-8') + b'\n'
            c.close()
        else:
            message_body = bytes(create_html(msg='Sorry, you\'re wrong'), encoding='utf-8')

    if resource.find('.') == -1:
        resource += '.html'

    try:
        if 'message_body' not in locals():
            with open('.' + resource, 'rb') as file:
                message_body = file.read()
    except FileNotFoundError:
        return b'HTTP/1.1 404 Not Found\n\n\n' + \
                   bytes(create_html(msg='File not found'), encoding='utf-8')

    if resource.endswith('.css'):
        headers = 'Content-Type: text/css'
    elif resource.endswith('.ico'):
        headers = 'Content-Type: image/x-icon'

    return bytes('HTTP/1.1 200 OK\n' + headers + '\n\n', encoding='utf-8') + message_body


def readData(sock):
    data = ''
    while '\r\n\r\n' not in data:
        data += sock.recv(1024).decode('utf-8')
    head, body = data.split('\r\n\r\n')
    parts = head.split('\r\n')
    start_line = parts[0]
    headers = {h[0]: h[1].strip() for h in (p.split(':') for p in parts[1:])}
    if 'Content-Length' in headers:
        body += sock.recv(int(headers['Content-Length']) - len(body)).decode('utf-8')
    return start_line, headers, body


def processing_body_req(body):
    barr = body.split('&')
    body = {h[0]: h[1].strip() for h in (p.split('=') for p in barr)}
    if 'name' in body:
        conn = sqlite3.connect('contacts_db.sqlite')
        c = conn.cursor()
        print(tuple(body.values()))
        c.execute("INSERT INTO contacts(name, mail, msg) VALUES (?, ?, ?)", tuple(body.values()))

        conn.commit()
        conn.close()
    return body

sock = socket.socket()
sock.bind(('0.0.0.0', 8000))
sock.listen()
sock.settimeout(1)

while True:
    try:
        try:
            conn, addr = sock.accept()
            conn.settimeout(1)
            l, h, b = readData(conn)
            print(l, b)
            if b:
                b = processing_body_req(b)
            conn.sendall(response(l, h, b))
            conn.close()
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        print('pressed Ctrl-C')
        sock.close()
        break