import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import git
import yaml
import json
import requests


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
        repo = CI.clone_repo(clone_url, branch)

        build_result = CI.ci_build(repo)
        test_result = CI.ci_test(repo)
        repo_full_name = self.payload["repository"]["full_name"]
        statuses_url = self.payload["repository"]["statuses_url"]
        CI.log_results(repo_full_name, commit_id, build_result, test_result)
        CI.send_results(repo_full_name, commit_id, build_result, test_result, os.environ.get('GITHUB_PAT'), statuses_url)

class CIServerHelper:
    def parse_header(self, header):
        if 'X-Github-Event' in header:
            event = header['X-Github-Event']
        else:
            event = "Unknown event"
        return event

    def clone_repo(self, clone_url, branch):
        dir_path = os.path.realpath(__file__)
        dir_name = os.path.dirname(dir_path)
        repo_path = os.path.join(dir_name, "CI-clonedir")

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
        # TODO: read from .YML file and return the build result as a tuple
        return  # (True/False, string)
    
    def ci_test(self):
        # TODO: read from .YML file and return the rtest result as a tuple
        return  # (True/False, string)

    def log_results(self, name, commit_id, build_result, test_result):
        """
        Log the results of build_result and test_result to persistent storage
        """
        log_dir = os.path.join('results', name)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, commit_id)

        f = open(log_file, 'w')

        if build_result[0]:
            f.write("Lint or build successful!\n\n")
        else:
            f.write("Lint or build failed!\n\n")
        f.write(f"Message:\n{build_result[1]}\n")
        f.write("\n----\n")

        if test_result[0]:
            f.write("Tests successful!\n\n")
        else:
            f.write("Tests failed!\n\n")
        f.write(f"Message:\n{test_result[1]}\n")

        f.close()

    def send_results(self, name, commit_id, build_result, test_result, token, statuses_url):
        """
        Set the commit status on Github for commit_id according to build_result and test_result
        """
        # statuses_url is on the format "https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"
        # owner and repo is already set, therefore we set sha here
        statuses_url = statuses_url.format(sha=commit_id)
        # Token, fetch from local YML-file..
        token = ""

        build_state = "failure"
        test_state = "failure"
        if build_result[0]:
            build_state = "success"
        if test_result[0]:
            test_state = "success"
        
        headers = {"Accept": "application/vnd.github+json", 
                   "Authorization": "Bearer " + token,
                   "X-GitHub-Api-Version": "2022-11-28"}
        data_build = {"state": build_state, "description": "The build was a " + build_state}
        data_test = {"state": test_state, "description": "The tests was a " + test_state}
        # TODO: complete feature after log_results
        requests.post(url=statuses_url, header=headers, data=data_build)



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
