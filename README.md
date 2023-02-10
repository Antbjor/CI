# CI
Assignment #2: Continuous Integration

Part of the course DD2480 &ndash; Software Engineering Fundamentals at KTH

A simple CI server. This project is not suitable for use in production.
No security checks are performed.

### Build list
A directory is created, called results + the name of the respository. In this directory, log files are created after each build and test.

The list can be found at http://sunasuna.mooo.com:1337/results.

### Testing
The file `CI_server_test.py` contains various tests that can be run.

To run all the test cases existing in `CI_server_test.py` on the code, run `python3 CI_server_test.py` from the main directory.

To run a specific test case existing in `CI_server_test.py` on the code, run `python3 -m unittest CI_server_test.CIServerTest.test_name` from the main directory, replacing test_name with the name of the test (the function to be run).

### Requirements
The requirements for the project can be found in requirements.txt.

To install the requirements, run `pip install -r requirements.txt`

### Running
To start the server the command `python3 CI_server.py` can be run. The webhooks of this repository is delivered to 'http://sunasuna.mooo.com/' on port '1337'. Therefore one needs access to that server, and from there run this CI-server to test it out.

### Github webhook documentation
Github sends a HTTP POST request to the URL specified in the repo settings.
This request contains a number of headers. The main one we are interested in
is `X-GitHub-Event` which specifies which event triggered the hook. The list of
possible values can be found at 
[Webhook events and payloads](https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads)
in the Github Docs.

The body of the request is a JSON object. The documentation for what it
contains can be found at the above URL.

### Browsable HTML documentation
To generate browsable html documentation use the following pdoc3 commands:
- (**pip install pdoc3** to install the tool)
- **pdoc --html \<filename\>**
  or 
- **pdoc --html \<filename\> --force** to overwrite an existing html file


### Notification implementation and testing
The CI server sets the commit status on the respository when a push occurs. This is achieved by using the above mentioned webhooks, retrieving and parse the payload on our server and lastly send a request with the correct header and payload to the url of the commit. In the sent payload we include the 'state'-tag, which basically is linked to a variable that either is "success" or "failure" depending on the state of the build result and test results that we run automatically. Every component of this feature has been tested by various testcases, as well as the communication to GitHub (Sending a response from the server with the current event, commit-id and repository url which can be seen on GitHub as a response-message). 


### Way of working according to Essence
Our team is currently in the "Collaborating" state. The team members are working together as one unit and the team is focused on achieving the mission. The members of the team have gotten to know each other more and trust each other to get the work done. The communication is good in the team so there is almost zero wated work and minimal avoidable backtracking. To get to the "Performing" state the team needs to collaborate more on the divided subsections of work, so that the team consistently can meet its commitments. This is achieved by adapting to changing context, in the regard of workload. It is difficult to make the workload even for each team member at a first look.

### Statement of contributions
Patrik Kinnunen: Wrote the base-code for the server as well as the testing for it. Did work on the README. Helped with the functionality to send results of the testing/building to github.

Adam Genell: Worked on the functionality to log the results of the testing/building in a separate file. Wrote parts of the README and did some cleanup on the code. Also helped the other members of the team with their tasks.

Anton Björklund: Worked on the functionality to clone a git repository. 

Wenqi Cao: Wrote functionality to build/perform static syntax on the code and to test the code. 

### License
The project is available under the MIT license. See the LICENSE file for more info.
