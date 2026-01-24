import socket

s = socket.socket()
s.bind(("localhost", 8080))
s.listen(1)
conn, addr = s.accept()
conn.send(b"Hello from Server")
conn.close()
