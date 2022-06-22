#!/usr/bin/python
from sql import SQL
from tools import TOOLS
from logging import Logging
from ftp import FTP
import socket, sys

# TODO FAIRE LES LOG !!!!
class Serveur():
	def __init__(self,IP,PORT,DATA_BASE):
		self.IP = IP
		self.PORT = PORT

		self.ID_client = 0
		self.infosocket = {"ID":[],"SOCKET":[]}
		# FILE LOG
		self.FILE_LOG = "Folder_log/server.log"
		self.logging = Logging(self.FILE_LOG)
		# BASE SQL
		self.DATA_BASE = DATA_BASE
		self.SQL = SQL(self.DATA_BASE)
		# TOOLS
		self.TOOLS = TOOLS()

	def CONNECTION_FTP_SITE_SIEGE(self):
		self.FTP_SIEGE = FTP("172.20.20.35","siege","siege")
	def CONNECTION_FTP_SITE_RENNES(self):
		self.FTP_RENNES = FTP("172.20.20.35","rennes","rennes")
	def CONNECTION_FTP_SITE_STRASBOURG(self):
		self.FTP_STRASBOURG = FTP("172.20.20.35","strasbourg","strasbourg")
	def CONNECTION_FTP_SITE_GRENOBLE(self):
		self.FTP_GRENOBLE = FTP("172.20.20.35","grenoble","grenoble")



	def start(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((self.IP, self.PORT))
			self.server.listen(5)
		except:
			self.logging.error("Impossible de démmaré le serveur")
			sys.exit()
		else:
			self.logging.info("Serveur start")

	def accept(self):
		try:
			self.client,self.infosClient = self.server.accept()
		except:
			self.logging.error("Impossible detablire la connexion avec le client")
			sys.exit()
		else:
			self.ID_client = self.ID_client + 1
			self.infosocket["ID"].append(self.ID_client)
			self.infosocket["SOCKET"].append(self.client)

	def closeServer(self):
		self.server.close()
	"""
	non prioritaire a voir
	def All_users(self,msg):
		for socket in self.infosocket["SOCKET"]:
			try:
				socket.send((msg).encode())
			except:
				self.logging.error("impossible envoyer le message")
	"""
	def recv(self):
		try:
			rep = self.client.recv(255)
			return rep.decode()
		except:
			self.logging.error("impossible de resevoir le message")
			self.close()

	def send(self,msg):
		try:
			msg = msg.encode()
			self.client.send(msg)
		except : 
			self.logging.error("impossible d'envoyer un message")
			self.close()

	def close(self):
		try:
			self.client.close()
		except:
			self.logging.error("Impossible de fermer la connection avec le client")
			sys.exit()

	def Instruction(self,client, infosClient, server):   
		adresseIP = infosClient[0]
		port = str(infosClient[1])
		self.logging.info("START threadsClients for " + adresseIP + " : " +str(port))

		MESSAGE = self.recv().split(",")
		self.RECV_LOGIN = MESSAGE[0]
		self.RECV_PASSWORD = MESSAGE[1]

		self.DATA_USER = str(self.SQL.Search_LOGIN_and_PASSWORD(self.RECV_LOGIN))
		characters_a_supprimé = "()[]' "

		for x in range(len(characters_a_supprimé)):
			self.DATA_USER = self.DATA_USER.replace(characters_a_supprimé[x],"")
		self.DATA_USER = self.DATA_USER.split(",")

		self.ID = self.DATA_USER[0]
		self.LOGIN = self.DATA_USER[1]
		self.PASSWORD = self.DATA_USER[2]
		self.ROLE = self.DATA_USER[3]
		self.NOM = self.DATA_USER[4]
		self.PRENOM = self.DATA_USER[5]
		self.SITE = self.DATA_USER[6]

		if self.RECV_LOGIN is None or self.RECV_PASSWORD is None or not self.RECV_LOGIN in self.LOGIN or not self.RECV_PASSWORD in self.PASSWORD:
			self.send("ERROR_CONNECTION")
			self.logging.warning("CONNECTION REFUSE FOR " + self.LOGIN)
			self.close()
		else:
			self.send("APPROUVE" + "," + self.LOGIN + "," + self.ROLE + "," + self.NOM + "," +self.PRENOM + "," + self.SITE)
			self.logging.info("CONNECTION APPROUVE FOR " + self.LOGIN)

			while True:
				MESSAGE_FROM_CLIENT = self.recv().split(",")
				ACTION = MESSAGE_FROM_CLIENT[0]
				self.logging.info("ACTION "+ ACTION + " " + self.LOGIN)
				if self.ROLE == "1":
					if ACTION == "LISTE_ALL_USER":		
						LISTE_USER = self.SQL.Get_all()
						for user in LISTE_USER:
							self.send(str(user))
							self.recv()
						self.send("List_User_END")

					elif ACTION == "ADD_NEW_USER":
						NEW_USER_LOGIN = MESSAGE_FROM_CLIENT[1]
						NEW_USER_PASSWORD = MESSAGE_FROM_CLIENT[2]
						NEW_USER_ROLE = MESSAGE_FROM_CLIENT[3]
						NEW_USER_NOM = MESSAGE_FROM_CLIENT[4]
						NEW_USER_PRENOM = MESSAGE_FROM_CLIENT[5]
						NEW_USER_SITE = MESSAGE_FROM_CLIENT[6]

						self.SQL.New_User(NEW_USER_LOGIN,NEW_USER_PASSWORD,NEW_USER_ROLE,NEW_USER_NOM,NEW_USER_PRENOM,NEW_USER_SITE)
					elif ACTION == "EDIT_USER":
						ACTION2 = MESSAGE_FROM_CLIENT[1]
						ID_UPDATE = MESSAGE_FROM_CLIENT[2]
						VALUE = MESSAGE_FROM_CLIENT[3]
						
						if ACTION2 == "CHANGE_LOGIN_USER":
							self.SQL.Update_LOGIN(VALUE,ID_UPDATE)
						elif ACTION2 == "CHANGE_PASSWORD_USER":
							self.SQL.Update_PASSWORD(VALUE,ID_UPDATE)
						elif ACTION2 == "CHANGE_NOM_USER":
							self.SQL.Update_NOM(VALUE,ID_UPDATE)
						elif ACTION2 == "CHANGE_PRENOM_USER":
							self.SQL.Update_PRENOM(VALUE,ID_UPDATE)
						elif ACTION2 == "CHANGE_ROLE_USER":
							self.SQL.Update_ROLE(VALUE,ID_UPDATE)
						elif ACTION2 == "CHANGE_SITE_USER":
							self.SQL.Update_SITE(VALUE,ID_UPDATE)
						else:
							self.logging.warning("ACTION inconue:" + ACTION2)
					elif ACTION == "DELET_USER":
						pass
					elif ACTION == "TOOLS":
						TOOLS = MESSAGE_FROM_CLIENT[1]
						if TOOLS == "Brute force":
							pass
						elif TOOLS == "Brute force dico":
							pass
						elif TOOLS == "scan port":
							pass
					elif ACTION == "STOP_SERVER":
						self.closeServer()

				#FIN DROIT ADMIN

				if ACTION == "CHANGE_PASSWORD":
					ACTION2 = MESSAGE_FROM_CLIENT[1]
					self.SQL.Update_PASSWORD(ACTION2,self.ID)
					pass
 
				#TODO A TESTER PLUS INTERNET !!!!!
				if ACTION == "FTP_CLIENT":
					SITE_FOR_ADMIN = MESSAGE_FROM_CLIENT[1]
					if self.SITE == "SIEGE" or self.ROLE == "1" and SITE_FOR_ADMIN == "SIEGE":
						self.CONNECTION_FTP_SITE_SIEGE()
					elif self.SITE == "GRENOBLE" or self.ROLE == "1" and SITE_FOR_ADMIN == "GRENOBLE":
						self.CONNECTION_FTP_SITE_GRENOBLE()
					elif self.SITE == "RENNES" or self.ROLE == "1" and SITE_FOR_ADMIN == "RENNES":
						self.CONNECTION_FTP_SITE_RENNES()
					elif self.SITE == "STRASBOURG" or self.ROLE == "1" and SITE_FOR_ADMIN == "STRASBOURG":
						self.CONNECTION_FTP_SITE_STRASBOURG()

					ACTION2 = MESSAGE_FROM_CLIENT[2]
					if ACTION2 == "LISTE_FILE":
						if self.SITE == "SIEGE" or self.ROLE == "1" and SITE_FOR_ADMIN == "SIEGE":
							DIR_SIEGE = self.FTP_SIEGE.dir()
							for file in DIR_SIEGE:
								self.send(str(file))
								self.recv()
							self.send("LISTE_FILE_END")

						elif self.SITE == "GRENOBLE" or self.ROLE == "1" and SITE_FOR_ADMIN == "GRENOBLE":
							DIR_GRENOBLE = self.FTP_GRENOBLE.dir()
							for file in DIR_GRENOBLE:
								self.send(str(file))
								self.recv()
							self.send("LISTE_FILE_END")

						elif self.SITE == "RENNES" or self.ROLE == "1" and SITE_FOR_ADMIN == "RENNES":
							DIR_RENNES = self.FTP_RENNES.dir()
							for file in DIR_RENNES:
								self.send(str(file))
								self.recv()
							self.send("LISTE_FILE_END")

						elif self.SITE == "STRASBOURG":
							DIR_STRASBOURG = self.FTP_STRASBOURG.dir()
							for file in DIR_STRASBOURG:
								self.send(str(file))
								self.recv()
							self.send("LISTE_FILE_END")

					elif ACTION2 == "DELET_FILE":
						FILE_DELET = MESSAGE_FROM_CLIENT[3]
						if self.SITE == "SIEGE" or self.ROLE == "1" and SITE_FOR_ADMIN == "SIEGE":
							self.FTP_SIEGE.delete(FILE_DELET)
						elif self.SITE == "GRENOBLE" or self.ROLE == "1" and SITE_FOR_ADMIN == "GRENOBLE":
							self.FTP_GRENOBLE.delete(FILE_DELET)
						elif self.SITE == "RENNES" or self.ROLE == "1" and SITE_FOR_ADMIN == "RENNES":
							self.FTP_RENNES.delete(FILE_DELET)
						elif self.SITE == "STRASBOURG" or self.ROLE == "1" and SITE_FOR_ADMIN == "STRASBOURG":
							self.FTP_STRASBOURG.delete(FILE_DELET)

					elif ACTION2 == "RENAME_FILE":
						OLD_RENAME_FILE = MESSAGE_FROM_CLIENT[3]
						NEW_RENAME_FILE = MESSAGE_FROM_CLIENT[4]
						if self.SITE == "SIEGE" or self.ROLE == "1" and SITE_FOR_ADMIN == "SIEGE":
							self.FTP_SIEGE.rename(OLD_RENAME_FILE,NEW_RENAME_FILE)
						elif self.SITE == "GRENOBLE" or self.ROLE == "1" and SITE_FOR_ADMIN == "GRENOBLE":
							self.FTP_GRENOBLE.rename(OLD_RENAME_FILE,NEW_RENAME_FILE)
						elif self.SITE == "RENNES" or self.ROLE == "1" and SITE_FOR_ADMIN == "RENNES":
							self.FTP_RENNES.rename(OLD_RENAME_FILE,NEW_RENAME_FILE)
						elif self.SITE == "STRASBOURG" or self.ROLE == "1" and SITE_FOR_ADMIN == "STRASBOURG":
							self.FTP_STRASBOURG.rename(OLD_RENAME_FILE,NEW_RENAME_FILE)
					elif ACTION2 == "NEW_FILE":
						pass



				if ACTION == "BACKUP":
					pass	
				elif ACTION == "CLOSE_CLIENT":
					self.logging.info("STOP CLIENT")
					self.close()
					break

					"""
					if ACTION == "SERVEUR MAINTENANCE":
						self.logging.critical("SERVEUR MAINTENANCE")
						self.All_users("SERVER MAINTENANCE")
						self.logging.critical("STOP SERVEUR")
						self.closeServer()
						break
					"""


				break

			self.close()


if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script Serveur a été importer avec succès")