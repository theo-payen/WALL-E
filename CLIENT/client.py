import socket , threading
# a faire
# thread ecoute a l'infini et renvoi des information au client
#
#

class CLIENT_TO_SERVER:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        
    def connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.IP, self.PORT))
    def encode(self,msg):
        return msg.encode()
    def decode(self,msg):
        return msg.decode()
    def recv(self):
        rep = self.client.recv(255)
        rep = self.decode(rep)
        return rep
    def send(self,msg):
        msg = self.encode(msg)
        self.client.send(msg)
    def close(self):
        self.client.close()


IP = "localhost"	
PORT = 3401
CLIENT_TO_SERVER = CLIENT_TO_SERVER(IP,PORT)
CLIENT_TO_SERVER.connection()
CLIENT_TO_SERVER.send("CONNECTION")
if CLIENT_TO_SERVER.recv() == ("APPROUVE"):
    print ("ok")
    pass
else:
    print ("refusse")
    exit

CLIENT_TO_SERVER.send("root" + " " + "MDP")
print (CLIENT_TO_SERVER.recv())

CLIENT_TO_SERVER.close()