import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = ('127.0.0.1', 8083)
clientsocket.connect(serverAddr)

message = "gpos"
clientsocket.send(message.encode())
clientsocket.recv(1024).decode()
