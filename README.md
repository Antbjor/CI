# CI
Assignment #2: Continuous Integration

Part of the course DD2480 &ndash; Software Engineering Fundamentals at KTH

A simple CI server. This project is not suitable for use in production.
No security checks are performed.

### Building
TODO

### Testing
The file `CI_server_test.py` contains various tests that can be run.

To run all the test cases existing in `CI_server_test.py` on the code, run `python3 CI_server_test.py` from the main directory.

To run a specific test case existing in `CI_server_test.py` on the code, run `python3 -m unittest CI_server_test.CIServerTest.test_name` from the main directory, replacing test_name with the name of the test (the function to be run).

### Running
TODO

### Github webhook documentation
Github sends a HTTP POST request to the URL specified in the repo settings.
This request contains a number of headers. The main one we are interested in
is `X-GitHub-Event` which specifies which event triggered the hook. The list of
possible values can be found at 
[Webhook events and payloads](https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads)
in the Github Docs.

The body of the request is a JSON object. The documentation for what it
contains can be found at the above URL.

### How notification has been implemented and tested


### Way of working according to Essence
Our team is currently in the "Collaborating" state. The team members are working together as one unit and the team is focused on achieving the mission. The members of the team have gotten to know each other more and trust each other to get the work done. The communication is good in the team so there is almost zero wated work and minimal avoidable backtracking. To get to the "Performing" state the team needs to collaborate more on the divided subsections of work, so that the team consistently can meet its commitments. This is achieved by adapting to changing context, in the regard of workload. It is difficult to make the workload even for each team member at a first look.

### Statement of contributions
Patrik Kinnunen: Wrote the base-code for the server as well as the testing for it. Did work on the README. Helped with the functionality to send results of the testing/building to github.

Adam Genell:

Anton Björklund:

Wenqi Cao: 

### License
The project is available under the MIT license. See the LICENSE file for more info.