import json
from http import HTTPStatus
from wsgiref.simple_server import make_server
import os
import sys
import pandas as pd
from . import frameup

dirname = os.path.dirname(os.path.realpath(__file__))

try:
    from jinja2 import Template
    templ = os.path.join(dirname, 'templates/example.j2.html')
    print(f'Using Jinja2 template: {templ}')
    template = Template(open(templ).read())
    render = lambda **kw: template.render(**kw)
except ModuleNotFoundError:
    templ = os.path.join(dirname, 'templates/example.html')
    print(f'Using python template: {templ}')
    template = open(templ).read()
    render = lambda **kw: template.format(**kw)

HOST = 'localhost'
PORT = 8000

STATUS_OK = f'{HTTPStatus.OK} {HTTPStatus.OK.phrase}'


class Server(object):

    def serve(self, environ, start_response):
        data = self.df.frameup.data(
            environ.get('QUERY_STRING', ''),
            justify='center',
            index_names=False,
            classes='pure-table-striped'
        )
        if 'text/html' in environ['HTTP_ACCEPT']:
            content_type = 'text/html; charset=utf-8'
            response = render(**data).encode('utf8')
        else:
            content_type = 'application/json; charset=utf-8'
            response = json.dumps(data).encode('utf8')
        headers = [
            ('Content-type', content_type),
            ('Content-Length', str(len(response)))
        ]
        start_response(STATUS_OK, headers)
        return [response]


def main():
    """Serve a csv file as a dataframe.
    """
    fn = sys.argv[1]
    server = Server()
    server.df = pd.read_csv(fn)
    server.df.frameup.default_page_size = 5
    print(f'Starting server on HOST: {HOST}; PORT: {PORT}')
    with make_server(HOST, PORT, server.serve) as httpd:
        httpd.serve_forever()


if __name__=='__main__':
    main()
