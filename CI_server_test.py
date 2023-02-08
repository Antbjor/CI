import unittest
import CI_server
import requests
from threading import Thread, Event
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


if __name__ == '__main__':
    unittest.main()
