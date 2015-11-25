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
            sort all matching entries by cost
            if several entries with same cost exists:
                return interface of entry with longest matching prefix
            else:
                return interface of the entry with lowest cost

def main:
    setup()
    run()
