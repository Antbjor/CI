from http.server import BaseHTTPRequestHandler, HTTPServer
import yaml

class CIServer(BaseHTTPRequestHandler):
    def response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET")
        print(self.path)
        print(self.headers)
        self.response()
        #self.wfile.write("GET requeaaaast for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        print("POST")
        print(self.path)
        print(self.headers)
        print(str(post_data.decode('utf-8')))

        self.response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=CIServer, port=8030):
    server_address = ('', port)
    server = server_class(server_address, handler_class)
    print("Starting server\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Stopping server\n')

if __name__ == '__main__':
    with open('config.yml') as fin:
        data = yaml.load(fin, Loader=yaml.FullLoader)
    PORT = data["PORT"]
    run(port=PORT)