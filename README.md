# CI
Assignment #2: Continuous Integration

Part of the course DD2480 &ndash; Software Engineering Fundamentals at KTH

A simple CI server. This project is not suitable for use in production.
No security checks are performed.

### Building
TODO

### Testing
TODO

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
