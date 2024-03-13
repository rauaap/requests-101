import socket
import sys

with socket.socket() as s:
    s.connect(('127.0.0.1', 8008))
    s.send(sys.argv[1].encode())
    print(s.recv(1024))
