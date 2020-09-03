import socket
import time
import pickle
import torch
from common_methods import receive_msg, send_msg
from net import TwoLayerNet, train

HEADERSIZE = 10
N, D_in, H, D_out = 64, 1000, 100, 10

x = torch.randn(N, D_in)
y = torch.randn(N, D_out)
model = TwoLayerNet(D_in, H, D_out)
train(model, x, y)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket is created.")
s.bind((socket.gethostname(), 1243))
# Set the queue size for connection
s.listen(5)
print("Listening for incoming connection ...")

connected = False
accept_timeout = 100
s.settimeout(accept_timeout)
d = model.state_dict()
send_msg(s, d, HEADERSIZE)

