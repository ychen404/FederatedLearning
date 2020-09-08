import socket
import pickle
from common_methods import receive_msg

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket is created.")

s.connect((socket.gethostname(), 1243))
print("Connected to the server.")

receive_msg(s, HEADERSIZE)

# send state_dict
# msg = "A message from the client."
# msg = pickle.dumps(msg)
# print(msg)
# s.sendall(msg)
# print("Client sent a message to the server.")

# receive state_dict
# while True: