import socket, re
from enum import Enum
from string import ascii_uppercase
from ipaddress import ip_address, ip_network

CRLF = '\r\n'

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
        while True:
            # Accept new connection -- accept() returns a (conn, addr) tuple
            try:
                self.handle_connection(sock.accept())
            except KeyboardInterrupt:
                print("Shutting down...")
                self.sock.close()
                exit(0)


    def handle_connection(self, connectionTuple):
        cc = self.ClientConnection(self, *connectionTuple)
        print('\nConnection from', cc.address)

        # Read binary data into buffer and convert it to string
        request = cc.socketConnection.recv(1024).decode()
        print("Request: {}".format(repr(request)))

        # Handle request
        try:
            cc.handle_request(request)
        except Exception as e:
            print("[!!] Error: {}".format(e))

        # Close connection
        finally:
            cc.socketConnection.close()
        print('Closed connection\n')

    class ClientConnection:

        def __init__(self, router, connection, address):
            self.router = router
            self.socketConnection = connection
            self.address = address

        def handle_request(self, request):
            request_lines = request.split(CRLF)
            request_type = request_lines[0]
            request_body = request_lines[1:-1]

            # Check whether request is an update or query
            if request_type == 'UPDATE':
                self.handle_update(request_body)
            elif request_type == 'QUERY':
                self.handle_query(request_body)
            else:
                raise Exception("Unknown request type")

        def send(self, msg):
            self.socketConnection.send(msg.encode())

        def send_ack(self, body=None):
            self.send("ACK{}{}END{}".format(CRLF, body+CRLF if body else '', CRLF))

        def handle_update(self, request):
            for line in request:
                # For each entry compare its cost
                interface, mask, cost = line.split(' ')
                mask = ip_network(mask)

                # Add new entry if mask doesn't exist in the routing table, or
                # update an existing entry only if the new cost is lower.
                if mask not in self.router.routing_table or self.router.routing_table[mask][1] > cost:
                    self.router.routing_table[mask] = (interface, cost)
            self.send_ack()

        def handle_query(self, request):
            print('query')
            # TODO
