#!/bin/python3
#  This server is responding with a fibonacci number given by a client
#  Asynchronous program with a select module


import socket
from fib import fib
from select import select


to_monitor = []  # monitor which sockets are ready to process
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind(('localhost', 5000))
serversock.listen()
to_monitor.append(serversock)


def accept_connection():
    clientsock, addr = serversock.accept()
    to_monitor.append(clientsock)
    print(f'Connection received {addr}')


def send_message(clientsock):  # return fibo num from client msg
    message = clientsock.recv(128)
    if not message:
        print('Connection refused')
        to_monitor.remove(clientsock)
        clientsock.close()
    result = str(fib(int(message.decode())))
    clientsock.send(result.encode() + b'\n')


def event_loop():  # handles control
    while True:
        to_read, _, _ = select(to_monitor, [], [])  # selecting ready sockets
        for sock in to_read:
            if sock is serversock:
                accept_connection()
            else:
                send_message(sock)


if __name__ == '__main__':
    event_loop()

