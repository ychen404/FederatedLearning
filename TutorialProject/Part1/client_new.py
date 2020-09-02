import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket is created.")

s.connect((socket.gethostname(), 1243))
print("Connected to the server.")

# send state_dict
# msg = "A message from the client."
# msg = pickle.dumps(msg)
# print(msg)
# s.sendall(msg)
# print("Client sent a message to the server.")

# receive state_dict
# while True:
full_msg = b''
new_msg = True
while True:
    msg = s.recv(16)
    if new_msg:
        print("new msg len:",msg[:HEADERSIZE])
        msglen = int(msg[:HEADERSIZE])
        new_msg = False

    # print(f"full message length: {msglen}")
    print("full message length: {}".format(msglen))

    full_msg += msg

    print(len(full_msg))

    if len(full_msg)-HEADERSIZE == msglen:
        print("full msg recvd")
        print(full_msg[HEADERSIZE:])
        print(pickle.loads(full_msg[HEADERSIZE:]))
        break
        # new_msg = True
        # full_msg = b""

# while True:
#     print("done sending")
#     pass
