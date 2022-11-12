# asyncpython

## Synchronous vs Asynchronous
When you implement a simple socket server without any process management logic(event loop), code will work in a synchronous way. 
It means an applicaton can't handle multiple tasks at the same time. For instance, let's say you have a socket server like below:

```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
```python
import socket
from fib import fib


serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind(('localhost', 5000))
serversock.listen()


while True:
    clientsock, addr = serversock.accept()
    print(f'Connection received {addr}')
    while True:
        message = clientsock.recv(256)
        if not message:
            break
        else:
            result = str(fib(int(message.decode())))
            clientsock.send(result.encode() + b'\n')

    clientsock.close()
```
