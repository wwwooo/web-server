import socket
import sqlite3
from response import Response

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
            response = Response(l, h, b).get()
            conn.sendall(response)
            conn.close()
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        print('pressed Ctrl-C')
        sock.close()
        break