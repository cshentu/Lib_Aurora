import socket
import numpy as np

class OpenCR_CTCR_tcp:
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddr = ('127.0.0.1', 8083)
        self.clientsocket.connect(self.serverAddr)
    
    def get_joint_values(self):
        message = "gpos"
        self.clientsocket.send(message.encode())
        reply = self.clientsocket.recv(1024).decode()
        return np.fromstring(reply, dtype=float, sep=' ')
    
    def set_joint_values(self, target):
        message = "spos " + np.array2string(target, separator=' ', formatter={'float_kind':lambda x: "%.3f" % x})[1:-1]
        self.clientsocket.send(message.encode())
        # todo: add error checking
        return True
    
ctcr = OpenCR_CTCR_tcp()
print(ctcr.get_joint_values())