import socket


def response(req_line, h, body):
    req_line = req_line.decode().split(' ')
    resource = req_line[1]
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


def arr_into_dic(arr):
    dic = {}
    for elem in arr:
        mas = elem.split(b': ')
        dic[mas[0]] = mas[1]
    return dic


def readData(s):
    data = b''
    while b'\r\n' not in data:
        data += s.recv(1024)
    i = data.find(b'\r\n')
    start_line = data[:i]
    print(start_line)

    data = data[i + 2:]
    while b'\r\n\r\n' not in data:
        data += s.recv(1024)
    i = data.find(b'\r\n\r\n')
    headers = data[:i]
    arr = headers.split(b'\r\n')
    headers = arr_into_dic(arr)
    print(headers)

    body = data[i + 4:]
    if b'Content-Length' in headers:
        cont_l = headers[b'Content-Length']
        numb = int(cont_l) - len(body)
        if numb >= 0:
            body += s.recv(numb)
        print(body)
    print('-----------------')

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
            conn.sendall(response(l, h, b))
            conn.close()
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        print('pressed Ctrl-C')
        sock.close()
        break