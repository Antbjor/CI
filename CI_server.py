import os
import git
import yaml
import json
import subprocess
import socketserver

from typing import Tuple
from http.server import BaseHTTPRequestHandler, HTTPServer


class CIServer(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
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
        CI.ci_build(repo)
        CI.ci_test(repo)


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

    def ci_build(self, repo, filepath="workflow.yml"):
        """ Read from workflow file and execute related jobs if triggerred.
        :return: a tuple of (boolean, string) that contains the build result
        """
        path = repo.working_dir + '/' + filepath
        with open(path) as fin:
            work = yaml.load(fin, Loader=yaml.FullLoader)

        # Find the jobs to be executed
        for job in work["jobs"]:
            # Skip the test part
            if job["name"] == 'Run tests':
                continue
            # Print the current job name
            print("CI Server: " + job["name"])
            # Execute the shell commands
            result = subprocess.run(job["run"], shell=True, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Print the output of the shell commands
            print(result.stdout)
            # Return at once if build fails
            if result.stderr != "":
                return False, result.stderr

        return True, "Good News: All is Fine."

    def ci_test(self, repo, filepath="workflow.yml"):
        """ Read from workflow file and execute related jobs if triggerred.
        :return: a tuple of (boolean, string) that contains the test result
        """
        path = repo.working_dir + '/' + filepath
        with open(path) as fin:
            work = yaml.load(fin, Loader=yaml.FullLoader)

        # Find the jobs to be executed
        for job in work["jobs"]:
            # Skip the build part
            if job["name"] == 'Build project':
                continue
            # Print the current job name
            print("CI Server: " + job["name"])
            # Execute the shell commands
            result = subprocess.run(job["run"], shell=True, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Print the output of the shell commands
            print(result.stdout)
            # Return at once if build fails
            if job["name"] == 'Run tests':
                if result.stderr[0] == 'E' or result.stderr[0] == 'F':
                    return False, result.stderr
            elif result.stderr != "":
                return False, result.stderr

        return True, "Good News: All is Fine."


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
