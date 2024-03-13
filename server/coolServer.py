import socketserver
import time
import sqlite3
import json

with open('index.html', 'rb') as f:
    index_html = f.read()

con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS api_requests;')
cur.execute('CREATE TABLE api_requests (id INTEGER PRIMARY KEY, message TEXT, time INTEGER);')
con.commit()

class MyTCPHandler(socketserver.BaseRequestHandler):

    # Very cool routing 
    def routing(self):
        if b'POST /api/insert' in self.data:
            currentTime = int( time.time() )
            header, body = self.data.decode().split('\r\n\r\n')
            message = json.loads(body).get('message')

            cur.execute(
                'INSERT INTO api_requests (message, time) values (?, ?);', 
                [message, currentTime]
            )

            con.commit();

            cur.execute('SELECT id from api_requests')
            count = len(cur.fetchmany(999))
            self.request.sendall(f'HTTP/1.1 200 OK\r\n\r\n{count} requests made to the API'.encode())
        elif b'GET /api/all' in self.data:
            cur.execute('SELECT message, time from api_requests')
            allRequests = cur.fetchmany(999)

            response = '\n'.join(
                f'{time.ctime(int(t))}: {m}' for m, t in allRequests
            )

            self.request.sendall(response.encode())
        else:
            self.request.sendall(index_html)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        # Let's print out the data for no reason
        print("Received from {}:".format(self.client_address[0]))
        print(self.data.decode())

        self.routing()

if __name__ == "__main__":
    import sys

    HOST, PORT = "127.0.0.1", int(sys.argv[1])

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

