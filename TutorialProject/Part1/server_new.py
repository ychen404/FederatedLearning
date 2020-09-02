import socket
import time
import pickle
import torch


HEADERSIZE = 10

class TwoLayerNet(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        """
        In the constructor we instantiate two nn.Linear modules and assign them as
        member variables.
        """
        super(TwoLayerNet, self).__init__()
        self.linear1 = torch.nn.Linear(D_in, H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, x):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        h_relu = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(h_relu)
        return y_pred

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# Create random Tensors to hold inputs and outputs
x = torch.randn(N, D_in)
y = torch.randn(N, D_out)

# Construct our model by instantiating the class defined above
model = TwoLayerNet(D_in, H, D_out)

# Construct our loss function and an Optimizer. The call to model.parameters()
# in the SGD constructor will contain the learnable parameters of the two
# nn.Linear modules which are members of the model.
criterion = torch.nn.MSELoss(reduction='sum')
optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
for t in range(5):
    # Forward pass: Compute predicted y by passing x to the model
    y_pred = model(x)

    # Compute and print loss
    loss = criterion(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())

    # Zero gradients, perform a backward pass, and update the weights.
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket is created.")

s.bind((socket.gethostname(), 1243))

# Set the queue size for connection
s.listen(5)
print("Listening for incoming connection ...")

connected = False
accept_timeout = 100
s.settimeout(accept_timeout)

try:
    clientsocket, address = s.accept()
    print("Connected to a client: {client_info}.".format(client_info=address))
    connected = True
except socket.timeout:
    print("A socket.timeout exception occurred because the server did not receive any connection for {accept_timeout} seconds.".format(accept_timeout=accept_timeout))

received_data = b''
# while True:
if connected:
    # now our endpoint knows about the OTHER endpoint.
    # clientsocket, address = s.accept()
    # print(f"Connection from {address} has been established.")
    print("Connection from {} has been established.".format(address))

    # receive state_dict
       
    # while str(received_data)[-2] != '.':
    # # while received_data is not None: 
    #     data = clientsocket.recv(8)
    #     received_data += data
    # print(received_data)
    # received_data = pickle.loads(received_data)
    # # received_data = torch.load(received_data)
    # # print("Received data from the client: {received_data}".format(received_data=received_data))
    # print("Received data from the client: {received_data}".format(received_data=received_data))

    # aggregate

    # send state_dict back
    # d = {1:"hi", 2: "client"}
    d = model.state_dict()
    msg = pickle.dumps(d)
    # msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    # msg = bytes("{:<{HEADERSIZE}}".format(len(msg),HEADERSIZE=HEADERSIZE), 'utf-8')+msg
    
    msg = bytes("{:<{HEADERSIZE}}".format(len(msg), HEADERSIZE=HEADERSIZE)) + msg
    print(msg)
    clientsocket.send(msg)
    # clientsocket.close()
# s.close()
