import socket
import numpy as np

class OpenCR_CTCR_tcp:
    def __init__(self, port=8083):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddr = ('127.0.0.1', port)
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
    
    def home_position(self):
        return self.set_joint_values([0, 0, 0, 0, 0, 0])
    
    def full_position(self):
        return self.set_joint_values([0, -16, 0, -22.25, 0, -28.7])
    
ctcr = OpenCR_CTCR_tcp()
print(ctcr.get_joint_values())