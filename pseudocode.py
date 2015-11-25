def setup:
    init look up table (subnet mask | cost)
    init A 0.0.0.0 100

def run:
    listen on port argv-1 forever
    switch(connection):
        case update:
            if mask in table:
                if new cost < old cost:
                    update with new cost and relevant interface
            else:
                add mask to table with relevant interface and cost

        case query:
            match longest prefix:
                return interface


def main:
    setup()
    run()
