import socket , hashlib , os, re, sys, ftplib, shutil
from datetime import datetime
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


IP = "127.0.0.1"
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

						Modif_ID = input("slect l'id de l'utilisateur :")
						while True:
							print("[1]     .modif login")
							print("[2]     .pwd")
							print("[3]     .role")
							print("[4]     .nom")
							print("[5]     .prenom")
							print("[6]     .SITE")
							print("[0]     .quiter")
							modif_option=input("?")
							
							if modif_option=="1":                            
								Modif_LOGIN =input ("modif login en : ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_LOGIN_USER"+ "," + Modif_LOGIN + "," + Modif_ID)

							elif modif_option == "2":
								Modif_PASSWORD =input ("pwd:")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_PASSWORD_USER"+ "," + CLIENT.hashe_password(Modif_PASSWORD) + "," + Modif_ID)

							elif modif_option == "3":
								Modif_ROLE_CONFIRME = input("voulez vous lui donne des droit administrateur (y)(n)")
								if Modif_ROLE_CONFIRME == "y":
									CLIENT.send("EDIT_USER" + "," + "CHANGE_ROLE_USER"+ "," + "1" + "," + Modif_ID)
								elif Modif_ROLE_CONFIRME == "n" :
									CLIENT.send("EDIT_USER" + "," + "CHANGE_ROLE_USER"+ "," + "0" + "," + Modif_ID)
								else:
									print("\n choix non valide veuillez saisir une option ")

							elif modif_option == "4":
								Modif_NOM =input ("modif nom: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_NOM_USER"+ Modif_NOM + "," + Modif_ID)
	
							elif modif_option == "5":
								Modif_PRENOM =input ("modif prenom: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_PRENOM_USER"+ "," + Modif_PRENOM + "," + Modif_ID)

							elif modif_option == "6":
								Modif_SITE =input ("modif SITE: ")
								CLIENT.send("EDIT_USER" + "," + "CHANGE_SITE_USER"+ "," + Modif_SITE + "," + Modif_ID)

							elif modif_option == "0":
								print ("quiter")
								break
							else:
								print("\n choix non valide veuillez saisir une option ")

					elif option2 == "4":
						#DELET USER
						Del_ID = input("slect l'id de l'utilisateur :")
						CLIENT.send("DELET_USER" + "," + Del_ID)

					elif option2 == "5":
						while True:
							print("Choisir le site sur le quelle vous voulez vous connecter")
							print("[1]     .scan port")
							print("[2]     .Voir mes scan")
							print("[0]     .quitter")
							optionTOOLS=input("?")
							if optionTOOLS == "1":
								while True:
									print("scanner 1 ou plusieur portr")
									print("[1]     .1 port")
									print("[2]     .plusieurs port")
									optionSCAN=input("?")
									ip = input("entrer l'ip du server a scanner")
									if optionSCAN == "1":
										port = input("le port a scanner")
										CLIENT.send("TOOLS" + "," + "SCAN_PORT" + "," + ip + "," + port + "," + port)
										NAME_EXPORT = CLIENT.recv()
										print ("SCAN en cours retrouver votre scan dans le rapport", NAME_EXPORT)
									elif optionSCAN == "2":
										min_port = input("le port min a scanner")
										max_port = input("le port max a scanner")
										CLIENT.send("TOOLS" + "," + "SCAN_PORT" + "," + ip + "," + min_port + "," + max_port)
										NAME_EXPORT = CLIENT.recv()
										print ("SCAN en cours retrouver votre scan dans le rapport", NAME_EXPORT)
										break
									else:
										print("pas bon")
										break

							elif optionTOOLS == "2":
								NAME_EXPORT=input("entrer le nom de votre export")
								CLIENT.send("TOOLS" + "," + "EXPORT_SCAN" + "," + NAME_EXPORT)
								while True:
									P = CLIENT.recv()
									if not P == "end":
										print(P)
									else:
										break
							elif optionTOOLS == "0":
								break
							else:
								print("pas bon")
							
							break


					elif option2 == "6":
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

				if not NEW_PASSWORD == NEW_PASSWORD2 and CLIENT.password_check == False:
					print("Une erreur est survenu veillez retester")
				elif OLD_PASSWORD == "0" or NEW_PASSWORD == "0" or NEW_PASSWORD2 == "0":
					break
				else:
					CLIENT.send("CHANGE_PASSWORD" + "," + CLIENT.hashe_password(NEW_PASSWORD))
					break
		elif option == "2":
			#FTP
			if ROLE == "1":
				while True:
					print("Choisir le site sur le quelle vous voulez vous connecter")
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

				print("[1]		.afficher les fichier")
				print("[2]		.supprimer un fichier")
				print("[3]		.supprimer un dossier")
				print("[4]		.renomé un fichier")
				print("[5]		.Crée un dossier")
				print("[6]		.upload fichier")
				print("[7]		.download fichier")
				print("[0]		.quitter")
				optionFTP=input("?")

				if optionFTP == "1":
					FTP_SERVER.dir()

				elif optionFTP == "2":
					# DELET FILE
					Delete_name_file = input("saisir le nom du fichier a supprimé")
					FTP_SERVER.delete(Delete_name_file)

				elif optionFTP == "3":
					# DELET FILE
					Delete_name_folder = input("saisir le nom du folder a supprimé")
					FTP_SERVER.rmd(Delete_name_folder)

				elif optionFTP == "4":
					# rename file
					old_rename_name_file = input("saisir le nom du fichier a renomé")
					new_rename_name_file = input("saisir le nom nouveau non du fichier")
					FTP_SERVER.rename(old_rename_name_file,new_rename_name_file)

				elif optionFTP == "5":
					New_FOLDER = input("NAME FOLDER")
					FTP_SERVER.mkd(New_FOLDER)

				elif optionFTP == "6":
					upload_file = input("chemain du fichier")
					FTP_SERVER.upload(upload_file)

				elif optionFTP == "7":
					print("download file")
					Dowload_file = input("chemain du fichier")					
					FTP_SERVER.dowload_file(Dowload_file)

				elif optionFTP == "0":
					FTP_SERVER.exit()
					break

				else:	
					print("veillez retester")

		elif option == "3":
			#TODO : BACKUP METTRE SUR SERVER
			#BACKUP

			if ROLE == "1":
				while True:
					print("Choisir le site sur le quelle vous voulez vous connecter")
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


			BACKUP_INFO_CONNECTION = CLIENT.recv().split(",")
			BACKUP_IP = BACKUP_INFO_CONNECTION[0]
			BACKUP_LOGIN = BACKUP_INFO_CONNECTION[1]
			BACKUP_PASSWORD = BACKUP_INFO_CONNECTION[2]

			BACKUP_SERVER = FTP(BACKUP_IP,BACKUP_LOGIN,BACKUP_PASSWORD)
			folder_backup = "BACKUP/" + BACKUP_LOGIN + "/" 
			while True:
				print("[1]		.afficher les backup")
				print("[2]		.backup les fichier du server ftp")
				print("[3]		.supprimé une backup")
				print("[0]		.quitter")
				option_BACKUP=input("?")

				if option_BACKUP == "1":
					dir = os.listdir(folder_backup)
					for i in dir:
						print (i)
				elif option_BACKUP == "2":
					date = f'{datetime.now():%m_%d_%Y-%H_%M_%S}'

					folder = folder_backup + date + "/"
					os.makedirs(folder)
					files = BACKUP_SERVER.nlst()
					for file in files:
						BACKUP_SERVER.retrbinary("RETR " + file ,open(folder + file, 'wb').write)

					shutil.make_archive(folder, 'zip', folder)
					shutil.rmtree(folder)

				elif option_BACKUP == "3":
					print("nom du dossierra supprimé")
					shutil.rmtree(folder)
				elif option_BACKUP == "0":
					BACKUP_SERVER.exit()
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
