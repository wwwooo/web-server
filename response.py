import sqlite3
from creator import create_html


class Response:

    def __init__(self, req_line, req_headers, req_message_body):
        self.req_line = req_line
        self.req_headers = req_headers
        self.req_message_body = req_message_body
        self.resource = self._get_resource()
        self.status_line = 'HTTP/1.1 200 OK'
        self.message_body = b''

    def _get_resource(self):
        resource = self.req_line.split(' ')[1]
        if resource != '/' and resource.find('.') == -1:
            resource += '.html'
        return resource

    # def _authorization(self):

    def _get_headers_str(self):
        if self.resource.endswith('.css'):
            return 'Content-Type: text/css'
        elif self.resource.endswith('.ico'):
            return 'Content-Type: image/x-icon'
        return ''

    def _get_message_body(self):
        if self.resource == '/':
            if 'Content-Length' in self.req_headers:
                return create_html()
            else:
                return create_html(template='index.html')
        elif self.resource == '/admin.html':
            if not len(self.req_message_body):
                return create_html(msg='Protected Information. Enter the password',
                                             template='authorization.html')
            elif self.req_message_body['password'] == str(1234):
                message_body =  ''
                conn_db = sqlite3.connect('contacts_db.sqlite')
                c = conn_db.cursor()
                for row in c.execute("SELECT * FROM contacts"):
                    message_body += str(row) + '\n'
                c.close()
                return message_body
            else:
                return create_html(msg='Sorry, you\'re wrong')
        else:
            try:
                with open('.' + self.resource, 'rb') as file:
                    self.message_body =  file.read()
            except FileNotFoundError:
                self.status_line = 'HTTP/1.1 404 Not Found'
                return create_html(msg='File not found')
        return ''

    def get(self):
        return bytes(self.status_line + '\n' + self._get_headers_str() + '\n\n' +
                     self._get_message_body(), encoding='utf-8') + self.message_body
