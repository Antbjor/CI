from http.server import BaseHTTPRequestHandler, HTTPServer
import yaml
import json

class CIServer(BaseHTTPRequestHandler):
    def response(self, message="Default"):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))

    def do_GET(self):
        print(self.headers)
        self.response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = self.parse_header(self.headers)
        commit_id, clone_url = self.parse_payload(post_data.decode('utf-8'))
        self.response(f'Recieved Event: {event}, Commit_id: {commit_id}, Clone_url: {clone_url}')
        self.clone_repo(event, commit_id, clone_url)

    def parse_header(self, header):
        if 'X-Github-Event' in header:
            event = header['X-Github-Event']
        else:
            event = "Unknown event"
        return event

    def parse_payload(self, payload):
        try:
            payload = json.loads(payload)
            commit_id = payload["after"]
            clone_url = payload["repository"]["clone_url"]
            return commit_id, clone_url
        except:
            print("Exception when trying to parse POST payload.")

    def clone_repo(self, event, commit_id, clone_url):
        """ 
        TODO 
        Do the continous integration tasks,
        1. clone the repo..
        2. compile the code..
        """

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

def main():
    with open('config.yml') as fin:
        data = yaml.load(fin, Loader=yaml.FullLoader)
    PORT = data["PORT"]
    run(port=PORT)

if __name__ == '__main__':
    main()