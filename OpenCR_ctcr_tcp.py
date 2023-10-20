import socket
import numpy as np
import time

class OpenCR_CTCR_tcp:
    def __init__(self, port=8119):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddr = ('127.0.0.1', port)
        self.clientsocket.connect(self.serverAddr)
    
    def get_joint_values(self):
        message = "gpos"
        self.clientsocket.send(message.encode())
        reply = self.clientsocket.recv(1024).decode()
        return np.fromstring(reply, dtype=float, sep=' ')
    
    def set_joint_values(self, target):
        message = "spos " + np.array2string(target, separator=' ', formatter={'float_kind':lambda x: "%2.4f" % x})[1:-1] + "\0"
        self.clientsocket.send(message.encode())
        # todo: add error checking
        return True
    
    def set_encoder_value_from_joint(self, joint):
        # input is alpha inner-middle-outer and beta inner-middle-outer
        # encoder values are in alpha_outer, beta_outer, alpha_middle, beta_middle, alpha_inner, beta_inner
        target = self.joint2encoder(joint)
        self.set_joint_values(target)
        return True
    
    def joint2encoder(self, joint):
        target = np.zeros_like(joint)
        target[0] = joint[2] * 4
        target[1] = -15 - joint[5] * 4 / (22.505 * 1e-3)
        target[2] = joint[1] * 4
        target[3] = - 21.5 - joint[4] * 4 / (22.505 * 1e-3)
        target[4] = joint[0] * 4
        target[5] = -27.5 - joint[3] * 4 / (22.505 * 1e-3)
        return target

    def go_to_target_slowly(self, n_steps=100, target=np.array([0, 0, 0, 0, 0, 0])):
        current = self.get_joint_values()
        for i in range(n_steps):
            self.set_joint_values(current + (target - current) * i / n_steps)
            time.sleep(0.05)
        return True
    
    def home_position(self):
        return self.set_joint_values(np.array([0, 0, 0, 0, 0, 0]))
    
    def full_position(self):
        return self.set_joint_values(np.array([0, -16, 0, -22, 0, -28.4]))
    
    def stop_robot(self):
        message = "quit"
        self.clientsocket.send(message.encode())
        # todo: add error checking
        return True
    
# ctcr = OpenCR_CTCR_tcp(8147)
# print(ctcr.get_joint_values())