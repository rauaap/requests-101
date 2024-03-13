import sys
import requests

port = int(sys.argv[1])
message = sys.argv[2]

requests.post(f'http://127.0.0.1:{port}/api/insert', json = {'message': message})
