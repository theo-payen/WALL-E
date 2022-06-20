import socket , threading, hashlib , os, random, string, re
# a faire
# thread ecoute a l'infini et renvoi des information au client
#
#




def password_alleatoire():
	length = 8
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	return (''.join(random.choice(chars) for i in range(length)))

def password_check(pwd):
	if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', pwd):
		return True
	else:
		return False

def Valide_password(): 
	while True:
		pwd =input ("modifier le mot de passe conetenant 8 caratere minimum : ")
		valid_pwd=password_check(pwd)
		if valid_pwd== True:
			pwd_h = hashe_password(pwd)
			return pwd_h
		elif valid_pwd== False:
			print ("mot de passe ne respecte pas l 'exigence ")




class CLIENT:
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
    
    def hashe_password(self,PASSWORD):
	    return hashlib.sha256(PASSWORD.encode()).hexdigest()


IP = "localhost"	
PORT = 3401
CLIENT = CLIENT(IP,PORT)
CLIENT.connection()
CLIENT.send("CONNECTION")
if CLIENT.recv() != ("APPROUVE"):
    print ("Error")
    exit
LOGIN = input("saisir votre login: ")
PASSWORD = input("saisir votre mots de passe: ")
print(CLIENT.hashe_password(PASSWORD))
CLIENT.send("root" + " " + CLIENT.hashe_password(PASSWORD))
print (CLIENT.recv())

CLIENT.close()