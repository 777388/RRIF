# RRIF
Recursive remote command injection fuzzer. Inject into a server and have them execute every possible execution in binary and send the requests to a server to be inspected as its running every possible binary execution.

Set up a listener on your end then hit this file remotely on a server

it will recursively cycle through every possible binary, even in large streams of 0's

it will then send its output to your server allowing you  to inspect each request to see what kind of errors are coming up in a all out binary assault until the process is killed
