import socket
import pickle

# Takes socket input and receive msg from a connected server
def receive_msg(s, headersize):
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new msg len:",msg[:headersize])
            msglen = int(msg[:headersize])
            new_msg = False

        # print(f"full message length: {msglen}")
        print("full message length: {}".format(msglen))

        full_msg += msg

        print(len(full_msg))

        if len(full_msg)-headersize == msglen:
            print("full msg recvd")
            print(full_msg[headersize:])
            decodeded_msg = pickle.loads(full_msg[headersize:])
            print(decodeded_msg)
            print(decodeded_msg.keys())
            for k in decodeded_msg:
                print("key: {} shape: {}".format(k, decodeded_msg[k].shape))

            break
            # new_msg = True
            # full_msg = b""
    print("Received all messages!")
    

def send_msg(s, raw_msg, headersize):

    try:
        clientsocket, address = s.accept()
        print("Connected to a client: {client_info}.".format(client_info=address))
        connected = True
    except socket.timeout:
        print("A socket.timeout exception occurred because the server did not receive any connection for {accept_timeout} seconds.".format(accept_timeout=accept_timeout))

    received_data = b''
    # while True:
    if connected:
        
        print("Connection from {} has been established.".format(address))
        
        # d = model.state_dict()
        msg = pickle.dumps(raw_msg)
        
        # msg = bytes(f"{len(msg):<{headersize}}", 'utf-8')+msg
        # msg = bytes("{:<{headersize}}".format(len(msg),headersize=headersize), 'utf-8')+msg
        
        msg = bytes("{:<{headersize}}".format(len(msg), headersize=headersize)) + msg
        print(msg)
        clientsocket.send(msg)
        # clientsocket.close()
    # s.close()
