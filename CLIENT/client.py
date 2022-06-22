import socket , threading, hashlib , os, random, string, re, sys


def password_alleatoire():
	length = 8
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	return (''.join(random.choice(chars) for i in range(length)))



class CLIENT:
	def __init__(self, IP, PORT):
		self.IP = IP
		self.PORT = PORT
		
	def connection(self):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.IP, self.PORT))
		except (ConnectionRefusedError):
			print ("impossible d'établir la connection entre le serveur et le client")
			print ("assurez vous que le serveur est bien démarer")
			sys.exit()
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
		return str(hashlib.sha256(PASSWORD.encode()).hexdigest())

	def password_check(pwd):
		if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', pwd):
			return True
		else:
			return False
	"""
	a voir non prioritaire
	def ecoute_infini(self):
		message_serveur = threading.Thread(target=self.recv)
		message_serveur.start()
	"""


IP = "localhost"
PORT = 3401
CLIENT = CLIENT(IP,PORT)

i = 0
while True :
	i = i + 1

	CLIENT.connection()
	LOGIN = input("saisir votre login: ")
	PASSWORD = input("saisir votre mots de passe: ")

	CLIENT.send(LOGIN + "," + CLIENT.hashe_password(PASSWORD))

	MESSAGE_CONNECTION = CLIENT.recv().split(",")

	STATUS_CONNECTION = MESSAGE_CONNECTION[0]

	if STATUS_CONNECTION == ("ERROR_CONNECTION"):
		print ("Login ou Mots de passe incorect")
		CLIENT.close
		if i == 3 :
			print("trop de t'entative")
			sys.exit()
	elif STATUS_CONNECTION == ("APPROUVE"):
		LOGIN = MESSAGE_CONNECTION[1]
		ROLE = MESSAGE_CONNECTION[2]
		NOM = MESSAGE_CONNECTION[3]
		PRENOM = MESSAGE_CONNECTION[4]
		SITE = MESSAGE_CONNECTION[5]
		break
	else:
		print("Error")
		sys.exit()

print ("\nBienvenu",PRENOM,",",NOM,"du site de",SITE)
if ROLE == "1":
	print("tu est connecter en t'en qu'administrateur")
else:
	print ("Tu est connecter en t'en qu'utilisateur")
while True:
		#MENU
		print("[1]		.modifier le mot de passe")
		print("[2]		.FTP")
		print("[3]		.BACKUP")
		if ROLE == "1":
			print("[9]		.Menu Admin")
		print("[0]		.quitter")
		option=input("?")

		if ROLE == "1":
			if option == "9":
				while True:
					print("[1]     .afficher les utilisateurs")
					print("[2]     .ajouter un nouvau utilisateur")
					print("[3]     .modifier un utilisateur")
					print("[4]     .supprimer un utilisateur")
					print("[5]     .TOOLS")
					print("[6]     .stop le server")
					print("[0]     .quitter")
					option2=input("?")

					if option2 == "1":	
						#LISTER LES UTILISATEURS
						CLIENT.send("LISTE_ALL_USER")
						while True:
							Reponse_List_User = CLIENT.recv()
							if Reponse_List_User == "List_User_END":
								break
							CLIENT.send("OK")
							print (Reponse_List_User)
					elif option2 == "2":
						#AJOUTER UN USER

						print ("Création d'un nouvelle utilisateur")
						NEW_USER_LOGIN = input("Le LOGIN\n->")
						NEW_USER_PASSWORD = CLIENT.hashe_password(input("Le mots de passe:\n->"))
						ROLE_confirm = input("Votre utilisateur est t-il admin (y)(n):\n->")
						if ROLE_confirm == "y":
							NEW_USER_ROLE = "1"
						elif ROLE_confirm == "n":
							NEW_USER_ROLE = "0"
						else:
							print("\n choix non valide veuillez saisir une option") 
				
						NEW_USER_NOM = input("NOM\n->")
						NEW_USER_PRENOM = input("PRENOM\n->")
						NEW_USER_SITE = input("SITE\n->")
						CLIENT.send("ADD_NEW_USER"+ "," + NEW_USER_LOGIN + "," + NEW_USER_PASSWORD + "," + NEW_USER_ROLE + "," + NEW_USER_NOM + "," + NEW_USER_PRENOM + "," + NEW_USER_SITE)

					elif option2 == "3":
						#EDIT USER
						pass
					elif option2 == "4":
						#DELET USER
						pass
					elif option2 == "5":
						CLIENT.send("STOP_SERVER")
						sys.exit()
					elif option2 == "0":
						break
					else:
						print("veillez retester")
		if option == "1":
		#modifier le MDP
			while True:
				#TODO a amelioré
				print ("0 pour quité")
				OLD_PASSWORD = input("saisir votre ancien mots de passe:\n->")
				NEW_PASSWORD = input("saisir votre nouveau mots de passe:\n->")
				NEW_PASSWORD2 = input("Valider votre nouveau mots de passe:\n->")

				if not NEW_PASSWORD == NEW_PASSWORD2 or CLIENT.password_check == False:
					print("Une erreur est survenu veillez retester")
				elif OLD_PASSWORD == "0" or NEW_PASSWORD == "0" or NEW_PASSWORD2 == "0":
					break
				else:
					CLIENT.send("CHANGE_PASSWORD" + "," + CLIENT.hashe_password(NEW_PASSWORD))
					break
		elif option == "2":
			#FTP
			while True:
				print("[1]     .afficher les fichier")
				print("[2]     .supprimer un fichier")
				print("[3]     .renomé un fichier")
				print("[0]     .quitter")
				optionFTP=input("?")
				if optionFTP == "1":
					CLIENT.send("FTP_CLIENT" + "," + "LISTE_FILE")

					while True:
						Reponse_List_User = CLIENT.recv()
						if Reponse_List_User == "LISTE_FILE_END":
							break
						CLIENT.send("OK")
						print (Reponse_List_User)

				elif optionFTP == "2":
					pass
				elif optionFTP == "3":
					pass
				elif option2 == "0":
					break
				else:	
					print("error")

		elif option == "3":
			pass
		elif option == "4":
			pass
		elif option == "0":
			CLIENT.send("CLOSE_CLIENT")
			print("exit")
			break
		else:
			print("option invalide")



CLIENT.close()