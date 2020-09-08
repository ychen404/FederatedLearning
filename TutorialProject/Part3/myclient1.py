import socket
import pickle
import numpy

def recv(soc, buffer_size=1024, recv_timeout=10):
    """
    This method comes with the template but does not work.
    Use my own method, receive_msg, instead
    """
    received_data = b""
    while str(received_data)[-2] != '.':
        try:
            soc.settimeout(recv_timeout)
            received_data += soc.recv(buffer_size)
        except socket.timeout:
            print("A socket.timeout exception occurred because the server did not send any data for {recv_timeout} seconds.".format(recv_timeout=recv_timeout))
            return None, 0
        except BaseException as e:
            return None, 0
            print("An error occurred while receiving data from the server {msg}.".format(msg=e))

    try:
        received_data = pickle.loads(received_data)
    except BaseException as e:
        print("Error Decoding the Client's Data: {msg}.\n".format(msg=e))
        return None, 0

    return received_data, 1


def receive_msg(soc, buffer_size=1024, recv_timeout=10, header_size=10):
    """
    Takes socket object as input and receives msg from a connected server

    Args:
        s (int): socket object
        headersize (int): The header size to add before the message, which contains the 
        length of the message
    """
    full_msg = b''
    new_msg = True
    while True:
        msg = soc.recv(buffer_size)
        if new_msg:
            print("new msg len:",msg[:header_size])
            msglen = int(msg[:header_size])
            new_msg = False

        # print(f"full message length: {msglen}")
        print("full message length: {}".format(msglen))

        full_msg += msg

        print(len(full_msg))

        if len(full_msg)-header_size == msglen:
            print("full msg recvd")
            print(full_msg[header_size:])
           
            try:
                decodeded_msg = pickle.loads(full_msg[header_size:])
                print(decodeded_msg)
                print(decodeded_msg.keys())
                for k in decodeded_msg:
                    print("key: {} shape: {}".format(k, decodeded_msg[k].shape))

            except BaseException as e:
                print("Error Decoding the Client's Data: {msg}.\n".format(msg=e))
                return None, 0

            return decodeded_msg, 1
            # break
            # new_msg = True
            # full_msg = b""
    print("Received all messages!")

def send_msg(soc, raw_msg, headersize):
    """
    Receives msg from connected socket

    Args:
        s (int): Socket object
        raw_msg (object): The message needs to be sent 
        headersize (int): The header size added before a message containing the length of the message
    """

    # try:
    #     clientsocket, address = soc.accept()
    #     print("Connected to a client: {client_info}.".format(client_info=address))
    #     connected = True
    # except socket.timeout:
    #     print("A socket.timeout exception occurred because the server did not receive any connection for {accept_timeout} seconds.".format(accept_timeout=accept_timeout))

    received_data = b''
    # while True:
    # if connected:  
    # print("Connection from {} has been established.".format(address))

    # d = model.state_dict()
    msg = pickle.dumps(raw_msg)
        
    # msg = bytes(f"{len(msg):<{headersize}}", 'utf-8')+msg
    # msg = bytes("{:<{headersize}}".format(len(msg),headersize=headersize), 'utf-8')+msg
        
    msg = bytes("{:<{headersize}}".format(len(msg), headersize=headersize)) + msg
    print(msg)
        # clientsocket.send(msg)
    soc.sendall(msg)
        # clientsocket.close()
    # s.close()

soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
print("Socket is created.")

try:
    soc.connect((socket.gethostname(), 1243))
    print("Connected to the server.")

except BaseException as e:
    print("Error Connecting to the Server: {msg}".format(msg=e))
    soc.close()
    print("Socket Closed.")


sent = 1
# while True:
while sent:
    
    # print("Receiving Reply from the Server.")
    # received_data, status = receive_msg(soc=soc, 
    #                              buffer_size=1024, 
    #                              recv_timeout=10,
    #                              header_size=10)
    # if status == 0:
    #     print("Nothing Received from the Server.")
    #     break
    # else:
    #     print(received_data)
    
    data = {1:"hi", 2:"this is client"}
    send_msg(soc, data, 10)
    # data_byte = pickle.dumps(data)
    print("Sending the Model to the Server.\n")
    # soc.sendall(data_byte)
        
    sent -= 1
    # subject = received_data["subject"]
    # if subject == "model":
    #     GANN_instance = received_data["data"]
    # elif subject == "done":
    #     print("Model is trained.")
    #     break
    # else:
    #     print("Unrecognized message type.")
    #     break
soc.close()
print("Socket Closed.\n")