import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 8025))
s.listen(1)
client, addr = s.accept()
client.settimeout(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1)
server.connect(('smtp.usd.edu', 25))

while True:
    try:
        upward = client.recv(1024)
        print('Upward: {}'.format(upward))
        server.send(upward)
    except KeyboardInterrupt:
        break
    except:
        print('nothing to pass up')
    try:
        downward = server.recv(1024)
        print('Downward: {}'.format(downward))
        client.send(downward)
    except KeyboardInterrupt:
        break
    except:
        print('nothing to pass down')
