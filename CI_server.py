import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import git
import yaml
import json


class CIServer(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)
        self.payload = []

    def response(self, message="Default"):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))

    def do_GET(self):
        print(self.headers)
        self.response()

    def do_POST(self):
        CI = CIServerHelper()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = CI.parse_header(self.headers)
        self.payload = json.loads(post_data.decode('utf-8'))
        commit_id = self.payload["after"]
        clone_url = self.payload["repository"]["clone_url"]
        repo_name = self.payload["repository"]["name"]
        branch = self.payload["ref"].replace("refs/heads/", "")
        self.response(f'Recieved Event: {event}, Commit_id: {commit_id}, Clone_url: {clone_url}')
        CI.clone_repo(clone_url, branch, repo_name)
        # ADD ci_build() here. (will return a tuple)


class CIServerHelper:
    def parse_header(self, header):
        if 'X-Github-Event' in header:
            event = header['X-Github-Event']
        else:
            event = "Unknown event"
        return event

    def clone_repo(self, clone_url, branch, repo_name):
        dir_name = os.path.dirname(os.path.realpath(__file__))
        new_dir = "CI-clonedir/" + repo_name
        repo_path = os.path.join(dir_name, new_dir)

        try:
            repo = git.Repo(repo_path)
        except(git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError):
            repo = None

        if repo is not None:
            repo.remotes.origin.fetch()
        else:
            git.Repo.clone_from(clone_url, repo_path)
            repo = git.Repo(repo_path)

        repo.git.checkout(branch)

        return repo

    def ci_build(self):
        # TODO: read from .sh file and return the result as a tuple
        return  # (True/False, string)




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
