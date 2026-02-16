## How This Proxy Works

    Listens on a local port and waits for connections.
    Forwards incoming traffic to a remote host and port.
    Receives responses from the remote host.
    Passes traffic through handlers (request_handler and response_handler), allowing modifications.
    Sends modified data back to the local client.

## Fixes & Improvements

    Fixed hexdump Function: Now correctly processes byte sequences.
    Improved Exception Handling: More specific error messages.
    Fixed TimeoutError Handling: Used socket.timeout instead.
    Enhanced Readability: Added comments and clarified logic.

## Running the Script

`python3 tcp_proxy.py 127.0.0.1 9000 example.com 80 True`

    This sets up a proxy that listens on 127.0.0.1:9000 and forwards traffic to example.com:80.
    The True argument means it will receive data first from example.com before forwarding the client’s request.

## Possible Use Cases

✔️ Traffic Inspection: View raw data between client and server.
✔️ Modifying Requests/Responses: Test security vulnerabilities.
✔️ Debugging Network Issues: Understand network behavior.
✔️ Network Analysis: Monitor network traffic patterns.
✔️ Security Auditing: Detect anomalies and potential threats.
