from enum import Enum
from string import ascii_uppercase
from ipaddress import ip_address, ip_network

class Router:

    version = 0.1

    def __init__(self, port):
        # Set port
        self.port = port

        # Create a list of available interfaces (8 total, A .. H)
        Interfaces = Enum('Interfaces', zip(ascii_uppercase, ascii_uppercase[:8]))

        # A map of network submasks and interface,cost-tuples
        self.routing_table = {
            # Pre-populate with a 'catch all' route
            ip_network('0.0.0.0/0'): (Interfaces.A, 100)
        }

    
