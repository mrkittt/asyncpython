#!/bin/python3
#  This server is responding with a fibonacci number given by a client
#  Asynchronous program with generators, a.k.a Round Robin


import socket
from fib import fib
from select import select


tasks = []  # Contains generators of that are ready to process

#  queue for sockets
to_read = {}
to_write = {}


def server():

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind(('', 5000))
    serversock.listen(5)

    while True:

        yield ('read', serversock)
        clientsock, addr = serversock.accept()
        print(f'Connection from {addr}')
        tasks.append(client(clientsock))


def client(clientsock):

    while True:
        yield ('read', clientsock)
        message = clientsock.recv(128)
        if not message:
            break
        else:
            result = str(fib(int(message.decode())))
            yield ('write', clientsock)
            clientsock.send(result.encode() + b'\n')

    clientsock.close()


def event_loop():

    while any([tasks, to_read, to_write]):  # While we have something to do

        while not tasks:  # If there are no tasks, we add them

            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            #  Execute next lines of gen
            #  Because we know that socket is ready, it won't be blocking
            reason, sock = next(task)

            #  After processing a socket, add them back to queue
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task

        except StopIteration:  # If a client disconnects, gen will break
            pass


tasks.append(server())
event_loop()
