import socket
from _thread import *

from Request import Request


class Server:
    contexts = {}

    def __init__(self, port, backlog):
        # Initialize server on the localhost and the port specified
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", port))
        print("Started Server")

        # Listen for request using the specified backlog
        s.listen(backlog)
        self.socket = s

    def start(self):
        # Start to accept clients once the server is started
        self.accept_clients()

    def accept_clients(self):
        # Always accept clients
        while True:
            # Fetch the connection and the address from the incoming request
            conn, addr = self.socket.accept()

            print("New Client")
            # Initialize a new Request with the connection and address
            r = Request(conn, addr)

            # Send the request to the context if the path is to be used.
            if r.path in self.contexts:
                start_new_thread(self.contexts[r.path]().handle, (r,))

    # Add the path for the new context to the contexts
    def create_context(self, string, handler):
        self.contexts[string] = handler
        print("New Context")
