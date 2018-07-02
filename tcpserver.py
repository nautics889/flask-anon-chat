import socket

s = socket.socket()
s.bind(('', 3636))
s.listen(20)

conn, addr = s.accept()

while 1:
    if conn:
        data = conn.recv(1024)
        print(data)
        if data:
            conn.send(data)
            conn.close()
            conn, addr = s.accept()

conn.close()