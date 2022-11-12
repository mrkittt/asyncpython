# asyncpython

## Synchronous
When you implement a simple socket server without any process management logic(event loop), code will work in a synchronous way. 
It means an applicaton can't handle multiple tasks at the same time. For instance, let's say you write a socket server like below
which responds with fibonacci number of your input:


```python
#  Synchronous socket server
import socket
from fib import fib


serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instance of server socket
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind(('localhost', 5000))
serversock.listen()


while True:  # listen continuously for client connections
    clientsock, addr = serversock.accept()
    print(f'Connection received {addr}')
    while True:  # listen for each message of a single client
        message = clientsock.recv(256)
        if not message:
            break
        else:
            result = str(fib(int(message.decode())))  # result of the user input
            clientsock.send(result.encode() + b'\n')

    clientsock.close()
```

## Problem and solution
If you connect to it through a netcat, everything goes fine and a client can see the results. However, if you try to connect as a
second client, nothing happens because server is still listening for messages of the first one. The second client can normally
talk to a server only when you shut the first. That is the problem of synchronous coding, which is unacceptable for public servers
where you need to handle thousands and thousands of different clients. This repository contains various implementations of asynchronous servers with
possibility to handle multiple connections
