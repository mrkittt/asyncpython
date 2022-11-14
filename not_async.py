import socket
from fib import fib


serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind(('localhost', 5000))
serversock.listen()


while True:
    clientsock, addr = serversock.accept()
    print(f'Connection received {addr}')
    message = clientsock.recv(256)
    if not message:
        clientsock.close()
        break
    else:
        result = str(fib(int(message.decode())))
        clientsock.send(result.encode() + b'\n')
