#!/usr/bin/env python3

import socket

# assigns socket.socket() to s
# socket is cleaned up after "with" block is exited
# 
# roughly equivalent to:
"""
s = socket.socket()
[code inside the context manager goes here]
s.close()
"""

with socket.socket() as s:
    s.bind(('127.0.0.1', 8008))
    s.listen()
        
    while True:
        client, address = s.accept()
        print(client.recv(1024))
        client.send(b'data received')
