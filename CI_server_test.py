import unittest
import CI_server
import requests
from threading import Thread, Event
import os
import shutil
import git
from http.server import BaseHTTPRequestHandler, HTTPServer


class StoppableThread(Thread):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class CIServerTest(unittest.TestCase):
    def test_get_response(self):
        """
        Test case to see if GET-request response is correct
        Expected response is Default
        """
        # Start server on its own thread
        server_thread = StoppableThread(target=CI_server.main)
        server_thread.start()
        r = requests.get('http://127.0.0.1:1337/')
        self.assertEqual(r.text, "Default")
        # Stop/Close the thread
        server_thread.stop()
    
    def test_header_no_event(self):
        """
        Test case to see if parsing header works as expected when tag is missing
        Expected response is 'Unknown event'
        """
        server = CI_server.CIServerHelper()
        header = {"X-GitHub-Hook-ID": "399544828"}
        event = server.parse_header(header)
        
        self.assertEqual(event, "Unknown event")
    
    def test_header_event(self):
        """
        Test case to see if parsing header works as expected
        Expected response is 'push'
        """
        server = CI_server.CIServerHelper()
        header = {"X-Github-Event": "push", "X-GitHub-Hook-ID": "399544828"}
        event = server.parse_header(header)
        
        self.assertEqual(event, "push")


    def test_clone_repo(self):
        """
        Test case to see if cloning repo work as expected.
        Expected outcome is to see that the git working_dir is found locally
        after the function is run.
        """
        server = CI_server.CIServerHelper()
        clone_url = "https://github.com/githubtraining/hellogitworld.git"
        branch = "master"
        repo_name = "CI"
        repo_path = server.clone_repo(clone_url, branch, repo_name).working_dir

        self.assertTrue(os.path.exists(repo_path))
        # Remove directory after testing
        shutil.rmtree(repo_path)


    def test_clone_repo_branch(self):
        """
        Test case to see if cloning repo and switching branch works as exspected.
        Expected outcome is to see that a file that only exists in a specific branch
        can be found locally after the function is run.
        """
        server = CI_server.CIServerHelper()
        clone_url = "https://github.com/githubtraining/hellogitworld.git"
        branch = "gh-pages"
        repo_name = "CI"
        repo_path = server.clone_repo(clone_url, branch, repo_name).working_dir
        file_path = repo_path + "/index.html"

        self.assertTrue(os.path.isfile(file_path))
        # Remove directory after testing
        shutil.rmtree(repo_path)


if __name__ == '__main__':
    unittest.main()
