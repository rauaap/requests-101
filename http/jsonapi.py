#!/usr/bin/env python3
import socket

with socket.socket() as s:
    s.bind(('127.0.0.1', 8008))
    s.listen()
        
    while True:
        client, address = s.accept()
        print(client.recv(1024))
        client.send('''
HTTP/1.1 OK
Content-Type: application/json

{"message": "hello"}
        '''.strip().encode())
        client.close()
