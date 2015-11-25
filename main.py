import sys
from router import Router

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage python3 main.py <PORT>")
        exit(1)

    router = Router()
    router.serve('', port)
