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
Content-Type: text/html

<head>
    <title>Wow!</title>
    <style>
        body {
            font-family: Monospace, Arial;
            background-color: #333;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div>Very cool!</div> 
</body>
        '''.strip().encode())
        client.close()
