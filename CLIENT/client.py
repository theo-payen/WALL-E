import socket , hashlib ,re, sys, ftplib

# TODO : TRIE LES IMPORT NON UTILISE

class FTP():
	def __init__(self,IP,USER,PASSWORD):
		self.IP = IP
		self.USER = USER
		self.PASSWORD = PASSWORD
		self.CONNECT = self.connect(self.IP,self.USER,self.PASSWORD)

	def connect(self,IP,USER,PASSWORD):
		try :
			return ftplib.FTP(IP,USER,PASSWORD)
		except(ftplib.error_temp):
			print("Erreur impossible de joindre le serveur FTP")

	def upload_file(self,fichier):
		open_f = open(fichier, 'rb')
		self.CONNECT.storbinary(f'STOR {fichier}', open_f)
		open_f.close()

	def dowload_file(self,fichier):
		with open(fichier, 'wb') as fp:
			self.CONNECT.retrbinary('RETR %s' % fichier, fp.write)

	def dir(self):
		return self.CONNECT.dir()

	def rename(self,old_name,new_name):
		return self.CONNECT.rename(old_name,new_name)

	def delete(self,file):
		return self.CONNECT.delete(file)

	def mkd(self,folder):
		self.CONNECT.mkd(folder)

	def rmd(self,folder):
		self.CONNECT.rmd(folder)
	def  nlst(self):
		return self.CONNECT.nlst()
	def retrbinary(self,file,file2):
		self.CONNECT.retrbinary(file,file2)

	def exit(self):
		self.CONNECT.quit()



class CLIENT:
	def __init__(self, IP, PORT):
		self.IP = IP
		self.PORT = PORT
		
	def connection(self):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.IP, self.PORT))
		except (ConnectionRefusedError):
			print ("Impossible d'établir la connexion entre le serveur et le client !")
			print ("Assurez-vous que le serveur est bien démarré")
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


IP = "127.0.0.1"
PORT = 3401
CLIENT = CLIENT(IP,PORT)

i = 0
while True :
	i = i + 1

	CLIENT.connection()
	LOGIN = input("Saisir votre login: ")
	PASSWORD = input("Saisir votre mot de passe: ")

	CLIENT.send(LOGIN + "," + CLIENT.hashe_password(PASSWORD))

	MESSAGE_CONNECTION = CLIENT.recv().split(",")

	STATUS_CONNECTION = MESSAGE_CONNECTION[0]

	if STATUS_CONNECTION == ("ERROR_CONNECTION"):
		print ("Login ou mot de passe incorrect")
		CLIENT.close
		if i == 3 :
			print("Nombre de tentatives max atteint")
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

print ("\nBienvenue",PRENOM,",",NOM,"du site de",SITE)
if ROLE == "1":
	print("Tu es connecté en tant qu'administrateur")
else:
	print ("Tu es connecté en tant qu'utilisateur")
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

						print ("Création d'un nouvel utilisateur")
						NEW_USER_LOGIN = input("Le LOGIN\n->")
						NEW_USER_PASSWORD = CLIENT.hashe_password(input("Le mot de passe:\n->"))
						ROLE_confirm = input("Votre utilisateur est t-il admin ? (y)(n):\n->")
						if ROLE_confirm == "y":
							NEW_USER_ROLE = "1"
						elif ROLE_confirm == "n":
							NEW_USER_ROLE = "0"
						else:
							print("\n Choix non valide veuillez saisir une option") 
				
						NEW_USER_NOM = input("NOM\n->")
						NEW_USER_PRENOM = input("PRENOM\n->")
						NEW_USER_SITE = input("SITE\n->")
						CLIENT.send("ADD_NEW_USER"+ "," + NEW_USER_LOGIN + "," + NEW_USER_PASSWORD + "," + NEW_USER_ROLE + "," + NEW_USER_NOM + "," + NEW_USER_PRENOM + "," + NEW_USER_SITE)

					elif option2 == "3":
						#EDIT USER

						Modif_ID = input("Séléctionnez l'ID de l'utilisateur à modifier:")
						while True:
							print("[1]     .modifier le login")
							print("[2]     .modifier le mot de passe")
							print("[3]     .modifier le rôle")
							print("[4]     .modifier le nom ")
							print("[5]     .modifier le prénom")
							print("[6]     .modifier le site")
							print("[0]     .quiter")
							modif_option=input("?")
							
							if modif_option=="1":                            
								Modif_LOGIN =input ("Modifier le login en: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_LOGIN_USER"+ "," + Modif_LOGIN + "," + Modif_ID)

							elif modif_option == "2":
								Modif_PASSWORD =input ("pwd:")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_PASSWORD_USER"+ "," + CLIENT.hashe_password(Modif_PASSWORD) + "," + Modif_ID)

							elif modif_option == "3":
								Modif_ROLE_CONFIRME = input("Voulez-vous lui attribuer les droits d'administrateur (y)(n)")
								if Modif_ROLE_CONFIRME == "y":
									CLIENT.send("EDIT_USER" + "," + "CHANGE_ROLE_USER"+ "," + "1" + "," + Modif_ID)
								elif Modif_ROLE_CONFIRME == "n" :
									CLIENT.send("EDIT_USER" + "," + "CHANGE_ROLE_USER"+ "," + "0" + "," + Modif_ID)
								else:
									print("\n Choix non valide veuillez saisir une option: ")

							elif modif_option == "4":
								Modif_NOM =input ("Modifier le nom: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_NOM_USER"+ Modif_NOM + "," + Modif_ID)
	
							elif modif_option == "5":
								Modif_PRENOM =input ("Modifier le prénom: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_PRENOM_USER"+ "," + Modif_PRENOM + "," + Modif_ID)

							elif modif_option == "6":
								Modif_SITE =input ("Modifier le site: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_SITE_USER"+ "," + Modif_SITE + "," + Modif_ID)

							elif modif_option == "0":
								print ("quiter")
								break
							else:
								print("\n Choix non valide veuillez saisir une option: ")

					elif option2 == "4":
						#DELET USER
						Del_ID = input("Séléctionnez l'ID de l'utilisateur:")
						CLIENT.send("DELET_USER" + "," + Del_ID)

					elif option2 == "5":
						while True:
							print("Choisir votre outil:")
							print("[1]     .scan port")
							print("[2]     .voir mes scans")
							print("[3]     .bruteforce")
							print("[4]     .bruteforce avec dico")
							print("[0]     .quitter")
							optionTOOLS=input("?")
							if optionTOOLS == "1":
								while True:
									print("Souhaitez-vous scanner un port unique ou une plage de ports ?")
									print("[1]     .port unique")
									print("[2]     .plage de ports")
									print("[0]     .exit")
									optionSCAN=input("?")
									ip = input("Entrer l'IP du serveur à scanner:")
									if optionSCAN == "1":
										port = input("Entrer un numéro de port à scanner:")
										CLIENT.send("TOOLS" + "," + "SCAN_PORT" + "," + ip + "," + port + "," + port)
										NAME_EXPORT = CLIENT.recv()
										print ("SCAN en cours, un rapport sera généré à la fin de celui-ci", NAME_EXPORT)
										break
									elif optionSCAN == "2":
										min_port = input("Port de début:")
										max_port = input("Port de fin:")
										CLIENT.send("TOOLS" + "," + "SCAN_PORT" + "," + ip + "," + min_port + "," + max_port)
										NAME_EXPORT = CLIENT.recv()
										print ("SCAN en cours, un rapport sera généré à la fin de celui-ci", NAME_EXPORT)
										break
									elif optionSCAN == "0":
										break
									else:
										print("invalide")

							elif optionTOOLS == "2":
								NAME_EXPORT=input("entrer le nom de votre export")
								CLIENT.send("TOOLS" + "," + "EXPORT_SCAN" + "," + NAME_EXPORT)
								while True:
									P = CLIENT.recv()
									if P == "end":
										break
									if P == "FILE_NOT_EXIST":
										print("Le rapport n'est pas disponible, le scan est en cours d'exécution ou aucun port n'est ouvert sur la cible")
									CLIENT.send("ok")
									print (P)



							elif optionTOOLS == "3":
									user = input("User à forcer:")
									ip = input("IP à forcer:")
									CLIENT.send("TOOLS" + "," + "BRUTE_FORCE" + "," + ip + "," + user)
									NAME_EXPORT = CLIENT.recv()
									print ("Bruteforce en cours d'exécution, un rapport sera généré. Si le rapport n'est pas disponible, alors l'attaque n'est pas terminée ou a échouée\n", NAME_EXPORT)
	
							elif optionTOOLS == "4":
								user = input("User à forcer")
								ip = input("IP à forcer")
								fichier = input("Votre le nom de votre fichier dico:")
								CLIENT.send("TOOLS" + "," + "BRUTE_FORCE_DICO" + "," + ip + "," + user + "," + fichier)
								NAME_EXPORT = CLIENT.recv()
								print ("Bruteforce en cours d'exécution, un rapport sera généré. Si le rapport n'est pas disponible, alors l'attaque n'est pas terminée ou a échouée\n", NAME_EXPORT)

							elif optionTOOLS == "0":
								break
							else:
								print("invalide")
							

					elif option2 == "6":
						CLIENT.send("STOP_SERVER")
						sys.exit()

					elif option2 == "0":
						break
					else:
						print("Veuillez retester")
		if option == "1":
		#modifier le MDP
			while True:
				#TODO a amelioré
				print ("0 pour quitter")
				OLD_PASSWORD = input("Saisir votre ancien mot de passe:\n->")
				NEW_PASSWORD = input("Saisir votre nouveau mot de passe:\n->")
				NEW_PASSWORD2 = input("Valider votre nouveau mot de passe:\n->")

				if not NEW_PASSWORD == NEW_PASSWORD2 and CLIENT.password_check == False:
					print("Une erreur est survenue veuillez retester")
				elif OLD_PASSWORD == "0" or NEW_PASSWORD == "0" or NEW_PASSWORD2 == "0":
					break
				else:
					CLIENT.send("CHANGE_PASSWORD" + "," + CLIENT.hashe_password(NEW_PASSWORD))
					break
		elif option == "2":
			#FTP
			if ROLE == "1":
				while True:
					print("Séléctionnez le site sur lequel vous souhaitez vous connecter:")
					print("[1]     .SIEGE")
					print("[2]     .RENNES")
					print("[3]     .STRASBOURG")
					print("[4]     .GRENOBLE")
					print("[0]     .quitter")
					optionSITE=input("?")

					if optionSITE == "1":
						CLIENT.send("FTP_CLIENT" + "," + "SIEGE")
						break
					elif optionSITE == "2":
						CLIENT.send("FTP_CLIENT" + "," + "RENNES")
						break
					elif optionSITE == "3":
						CLIENT.send("FTP_CLIENT" + "," + "STRASBOURG")
						break
					elif optionSITE == "4":
						CLIENT.send("FTP_CLIENT" + "," + "GRENOBLE")
						break
					elif optionSITE == "0":
						break
					else:
						pass
			else:
				CLIENT.send("FTP_CLIENT")

			FTP_INFO_CONNECTION = CLIENT.recv().split(",")
			FTP_IP = FTP_INFO_CONNECTION[0]
			FTP_LOGIN = FTP_INFO_CONNECTION[1]
			FTP_PASSWORD = FTP_INFO_CONNECTION[2]

			FTP_SERVER = FTP(FTP_IP,FTP_LOGIN,FTP_PASSWORD)		
			while True:

				print("[1]		.afficher les fichiers")
				print("[2]		.supprimer un fichier")
				print("[3]		.supprimer un dossier")
				print("[4]		.renommer un fichier")
				print("[5]		.créer un dossier")
				print("[6]		.upload un fichier")
				print("[7]		.download fichier")
				print("[0]		.quitter")
				optionFTP=input("?")

				if optionFTP == "1":
					FTP_SERVER.dir()

				elif optionFTP == "2":
					# DELET FILE
					Delete_name_file = input("Saisir le nom du fichier à supprimer")
					FTP_SERVER.delete(Delete_name_file)

				elif optionFTP == "3":
					# DELET FILE
					Delete_name_folder = input("Saisir le nom du fichier à supprimer")
					FTP_SERVER.rmd(Delete_name_folder)

				elif optionFTP == "4":
					# rename file
					old_rename_name_file = input("Saisir le nom du fichier à renommer:")
					new_rename_name_file = input("Entrez le nouveau nom du fichier:")
					FTP_SERVER.rename(old_rename_name_file,new_rename_name_file)

				elif optionFTP == "5":
					New_FOLDER = input("NAME FOLDER")
					FTP_SERVER.mkd(New_FOLDER)

				elif optionFTP == "6":
					upload_file = input("Chemin du fichier:")
					FTP_SERVER.upload_file(upload_file)

				elif optionFTP == "7":
					print("download file")
					Dowload_file = input("Chemin du fichier:")					
					FTP_SERVER.dowload_file(Dowload_file)

				elif optionFTP == "0":
					FTP_SERVER.exit()
					break

				else:	
					print("Veuillez réessayer:")

		elif option == "3":
			#TODO : BACKUP METTRE SUR SERVER
			#BACKUP

			if ROLE == "1":
				while True:
					print("Choisir le site sur lequel vous voulez vous connecter")
					print("[1]     .SIEGE")
					print("[2]     .RENNES")
					print("[3]     .STRASBOURG")
					print("[4]     .GRENOBLE")
					print("[0]     .quitter")
					optionSITE=input("?")

					if optionSITE == "1":
						CLIENT.send("BACKUP" + "," + "SIEGE")
						break
					elif optionSITE == "2":
						CLIENT.send("BACKUP" + "," + "RENNES")
						break
					elif optionSITE == "3":
						CLIENT.send("BACKUP" + "," + "STRASBOURG")
						break
					elif optionSITE == "4":
						CLIENT.send("BACKUP" + "," + "GRENOBLE")
						break
					elif optionSITE == "0":
						break
					else:
						pass
			else:
				CLIENT.send("BACKUP")


			while True:
				print("[1]		.afficher les sauvegardes")
				print("[2]		.sauvegarder les fichiers du serveur FTP")
				print("[3]		.supprimer une sauvegarde")
				print("[0]		.quitter")
				option_BACKUP=input("?")

				if option_BACKUP == "1":
					CLIENT.send("LIST_BACKUP")
					while True:
						Reponse_List_BACKUP = CLIENT.recv()
						if Reponse_List_BACKUP == "List_BACKUP_END":
							break
						CLIENT.send("OK")
						print (Reponse_List_BACKUP)

				elif option_BACKUP == "2":
					CLIENT.send("BACKUP_FILE")

				elif option_BACKUP == "3":
					folder = input("Le dossierr a bien été supprimé")
					CLIENT.send("DEL_BACKUP"+ "," + folder)
				elif option_BACKUP == "0":
					CLIENT.send("BACKUP_exit")
					break
				else:
					print("pas bon")




		elif option == "0":
			CLIENT.send("CLOSE_CLIENT")
			print("exit")
			break
		else:
			print("option invalide")



CLIENT.close()
