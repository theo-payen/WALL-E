import socket , threading, hashlib , os, random, string, re, sys
from telnetlib import STATUS

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

i = 0
while True :
	i = i + 1
	CLIENT.connection()
	LOGIN = input("saisir votre login: ")
	PASSWORD = input("saisir votre mots de passe: ")

	CLIENT.send(LOGIN + " " + CLIENT.hashe_password(PASSWORD))

	STATUS_CONNECTION = CLIENT.recv()	

	if STATUS_CONNECTION == ("ERROR_CONNECTION"):
		print ("Login ou Mots de passe incorect")
		CLIENT.close
		if i == 3 :
			print("trop de t'entative")
			sys.exit()
	elif STATUS_CONNECTION == ("APPROUVE"):
		print ("t co mon ruf")
		break

print (CLIENT.recv())

CLIENT.close()