import socket
import time
import pickle
import torch
import threading
from common_methods import receive_msg, send_msg
from net import TwoLayerNet, train
import pdb

HEADERSIZE = 10
N, D_in, H, D_out = 64, 1000, 100, 10

x = torch.randn(N, D_in)
y = torch.randn(N, D_out)
model = TwoLayerNet(D_in, H, D_out)
train(model, x, y)

class SocketThread(threading.Thread):

    def __init__(self, connection, client_info, buffer_size=1024, recv_timeout=5, header_size=10):
        threading.Thread.__init__(self)
        self.connection = connection
        self.client_info = client_info
        self.buffer_size = buffer_size
        self.recv_timeout = recv_timeout
        self.header_size = header_size

    def recv(self):
        """
        The original recv function from the other code. 
        But it was not using headersize which leads to truncation of the pickle
        """
        pass
    

    def receive_msg(self):
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
            # msg = s.recv(16)
            msg = self.connection.recv(self.buffer_size)
            if new_msg:
                # pdb.set_trace()
                print("new msg len:",msg[:self.header_size])
                msglen = int(msg[:self.header_size])
                new_msg = False

            # print(f"full message length: {msglen}")
            print("full message length: {}".format(msglen))

            full_msg += msg
            print(len(full_msg))

            if len(full_msg)-self.header_size == msglen:

                print("All data ({data_len} bytes) Received from \
                            {client_info}.".format(client_info=self.client_info, \
                            data_len=msglen))
                print(full_msg[self.header_size:])
                try:
                    decodeded_msg = pickle.loads(full_msg[self.header_size:])
                    print(decodeded_msg)
                    print(decodeded_msg.keys())
                    # for k in decodeded_msg:
                    #     print("key: {} shape: {}".format(k, decodeded_msg[k].shape))
                    
                    print("Received all messages!")

                    return decodeded_msg, 1
                
                except BaseException as e:
                    print("Error Decoding the Client's Data: {msg}.\n".format(msg=e))
                    return None, 0
                # break
                # new_msg = True
                # full_msg = b""
    def send_msg(self, raw_msg):
        """
        Receives msg from connection
        
        """

        # try:
        #     clientsocket, address = soc.accept()
        print("Connected to a client: {client_info}.".format(client_info=self.client_info))
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
            
        msg = bytes("{:<{headersize}}".format(len(msg), headersize=self.header_size)) + msg
        print(msg)
            # clientsocket.send(msg)
        self.connection.send(msg)
            # clientsocket.close()
        # s.close()
        
    
    def model_average(self, model, other_model):
        pass

    def reply(self, received_data):
        pass

    def run(self):
        
        # print("Running a Thread for the Connection with {client_info}.".format(client_info=self.client_info))
        # d = {1: 'hi', 2: 'there'}
        # print("Preparing to send data")
        # self.send_msg(d)
        # print("Data sent from the server")
            
        while True:            
            # This while loop allows the server to wait for the client to send data more than once within the same connection.
            self.recv_start_time = time.time()
            time_struct = time.gmtime()
            date_time = "Waiting to Receive Data Starting from {day}/{month}/{year} {hour}:{minute}:{second} GMT".format(year=time_struct.tm_year, month=time_struct.tm_mon, day=time_struct.tm_mday, hour=time_struct.tm_hour, minute=time_struct.tm_min, second=time_struct.tm_sec)
            print(date_time)
            received_data, status = self.receive_msg()
            # received_data, status = self.recv

            if status == 0:
                self.connection.close()
                print("Connection Closed with {client_info} either due to inactivity for {recv_timeout} seconds or due to an error.".format(client_info=self.client_info, recv_timeout=self.recv_timeout))
                break

            print(received_data)

            # Test reply function later
            # Add a echo step to varify the simple case
            #self.reply(received_data)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket is created.")

soc.bind((socket.gethostname(), 1243))
# Set the queue size for connection
print("Socket Bound to IPv4 Address & Port Number.\n")

soc.listen(1)
print("Listening for incoming connection ...")

connected = False
accept_timeout = 100
soc.settimeout(accept_timeout)

while True:
    try:
        connection, client_info = soc.accept()
        print("New Connection from {client_info}.".format(client_info=client_info))
        socket_thread = SocketThread(connection=connection,
                                     client_info=client_info, 
                                     buffer_size=1024,
                                     recv_timeout=10)
        socket_thread.start()
    except:
        soc.close()
        print("(Timeout) Socket Closed Because no Connections Received.\n")
        break
# d = model.state_dict()
# send_msg(soc, d, HEADERSIZE)