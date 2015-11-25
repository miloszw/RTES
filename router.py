import socket
from enum import Enum
from string import ascii_uppercase
from ipaddress import ip_address, ip_network

class Router:

    version = 0.1

    def __init__(self):
        # Create a list of available interfaces (8 total, A .. H)
        Interfaces = Enum('Interfaces', zip(ascii_uppercase, ascii_uppercase[:8]))

        # A map of network submasks and interface,cost-tuples
        self.routing_table = {
            # Pre-populate with a 'catch all' route
            ip_network('0.0.0.0/0'): (Interfaces.A, 100)
        }

    def serve(self, host, port):
        # Create TCP socket
        self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow socket to be reused so we don't have to wait for OS to relase it
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to given port and start listening for connections
        sock.bind((host, port))
        sock.listen(0)
        print('Listening on port {}'.format(port))

        # Keep serving
        try:
            while True:
                # Accept new connection
                conn, addr = sock.accept()
                print('Connection from', addr)

                # Read binary data into buffer and convert it to string
                query = conn.recv(1024).decode()

                # Handle request
                try:
                    self.handle_request(conn, query)
                except RouterError as e:
                    print("Error: {}".format(e))

                # Close connection
                finally:
                    conn.close()
                print('Closed connection')
        except KeyboardInterrupt:
            print("Shutting down...")
            sock.close()
            exit(0)

    def handle_request(self, connection, query):
        pass

    def handle_update(self, query):
        pass
        # TODO

    def handle_update(self, query):
        pass
        # TODO

class RouterError(Exception):
    pass
