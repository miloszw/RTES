import sys, socket

def send(msg, port):
    # open socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('', port))

    # prep message
    msg = msg.replace(',','\r\n')

    # send message, get response, close socket
    clientSocket.send(msg.encode())
    response = clientSocket.recv(2048)
    clientSocket.close()
    print("Response: {}".format(response))

if __name__ == '__main__':
    port = int(sys.argv[1])
    f = open(sys.argv[2])
    data = f.read()
    requests = data.split('--')
    for i, request in enumerate(requests):
        print("Sending request ", i)
        send(request, port)
