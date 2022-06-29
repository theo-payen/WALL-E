#!/usr/bin/python
from sqlite3 import connect
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


		self.FTP_IP_SIEGE = "172.20.20.35"
		self.FTP_LOGIN_SIEGE = "siege"
		self.FTP_PASSWORD_SIEGE = "siege"

		self.FTP_IP_RENNES = "172.20.20.35"
		self.FTP_LOGIN_RENNES = "rennes"
		self.FTP_PASSWORD_RENNES = "rennes"

		self.FTP_IP_STRASBOURG = "172.20.20.35"
		self.FTP_LOGIN_STRASBOURG = "strasbourg"
		self.FTP_PASSWORD_STRASBOURG = "strasbourg"

		self.FTP_IP_GRENOBLE = "172.20.20.35"
		self.FTP_LOGIN_GRENOBLE = "grenoble"
		self.FTP_PASSWORD_GRENOBLE = "grenoble"




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
		try:
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
		except:
			print("erreur conection")
		try:
			if self.RECV_LOGIN is None or self.RECV_PASSWORD is None or not self.RECV_LOGIN in self.LOGIN or not self.RECV_PASSWORD in self.PASSWORD:
				self.send("ERROR_CONNECTION")
				self.logging.warning("CONNECTION REFUSE FOR " + self.LOGIN)
				self.close()
			else:
				self.send("APPROUVE" + "," + self.LOGIN + "," + self.ROLE + "," + self.NOM + "," +self.PRENOM + "," + self.SITE)
				self.logging.info("CONNECTION APPROUVE FOR " + self.LOGIN)
		except:
			self.send("ERROR_CONNECTION")
			self.logging.warning("CONNECTION REFUSE FOR " + self.LOGIN)
			self.close()

		while True:
			MESSAGE_FROM_CLIENT = self.recv().split(",")
			ACTION = MESSAGE_FROM_CLIENT[0]
			self.logging.info("ACTION "+ ACTION + " PAR " + self.LOGIN)
			if self.ROLE == "1":
				if ACTION == "LISTE_ALL_USER":		
					LISTE_USER = self.SQL.Get_all()
					for user in LISTE_USER:
						self.send(str(user))
						self.recv()
					self.send("List_User_END")
					del user
					continue

				elif ACTION == "ADD_NEW_USER":
					NEW_USER_LOGIN = MESSAGE_FROM_CLIENT[1]
					NEW_USER_PASSWORD = MESSAGE_FROM_CLIENT[2]
					NEW_USER_ROLE = MESSAGE_FROM_CLIENT[3]
					NEW_USER_NOM = MESSAGE_FROM_CLIENT[4]
					NEW_USER_PRENOM = MESSAGE_FROM_CLIENT[5]
					NEW_USER_SITE = MESSAGE_FROM_CLIENT[6]

					self.SQL.New_User(NEW_USER_LOGIN,NEW_USER_PASSWORD,NEW_USER_ROLE,NEW_USER_NOM,NEW_USER_PRENOM,NEW_USER_SITE)
					continue
				elif ACTION == "EDIT_USER":
					try:
						ACTION2 = MESSAGE_FROM_CLIENT[1]
						VALUE = MESSAGE_FROM_CLIENT[2]
						ID_UPDATE = MESSAGE_FROM_CLIENT[3]
					except:
						print("error")

					print(ACTION2,ID_UPDATE,VALUE)
					if ACTION2 == "CHANGE_LOGIN_USER":
						self.SQL.Update_LOGIN(VALUE,ID_UPDATE)
					elif ACTION2 == "CHANGE_PASSWORD_USER":
						self.SQL.Update_PASSWORD(VALUE,ID_UPDATE)
					elif ACTION2 == "CHANGE_ROLE_USER":
						self.SQL.Update_ROLE(VALUE,ID_UPDATE)
					elif ACTION2 == "CHANGE_NOM_USER":
						self.SQL.Update_NOM(VALUE,ID_UPDATE)
					elif ACTION2 == "CHANGE_PRENOM_USER":
						self.SQL.Update_PRENOM(VALUE,ID_UPDATE)
					elif ACTION2 == "CHANGE_SITE_USER":
						self.SQL.Update_SITE(VALUE,ID_UPDATE)
					else:
						self.logging.warning("ACTION inconue:" + ACTION2)
					continue
				elif ACTION == "DELET_USER":
					ID_DELET = MESSAGE_FROM_CLIENT[1]
					self.SQL.Del_User(ID_DELET)
					continue

				elif ACTION == "TOOLS":
					# TODO: a faire						
					TOOLS = MESSAGE_FROM_CLIENT[1]
					if TOOLS == "Brute force":
						continue
					elif TOOLS == "Brute force dico":
						continue
					elif TOOLS == "SCAN_PORT":
						ip = MESSAGE_FROM_CLIENT[2]
						port_min = MESSAGE_FROM_CLIENT[3]
						port_max = MESSAGE_FROM_CLIENT[4]
						self.send(str(self.TOOLS.ScanPorts(ip,port_min,port_max)))
						continue
					elif TOOLS == "EXPORT_SCAN":
						file = MESSAGE_FROM_CLIENT[2]
						try:
							open_file = open(file, "r")
							for line in open_file:
								self.send(line)
						except:
							print("error")
						else:
							self.send("end")
							open_file.close()
							continue
				elif ACTION == "STOP_SERVER":
					self.close()
					self.closeServer()
					sys.exit()

				#FIN DROIT ADMIN

			if ACTION == "CHANGE_PASSWORD":
				ACTION2 = MESSAGE_FROM_CLIENT[1]
				self.SQL.Update_PASSWORD(ACTION2,self.ID)

				#FIXME:
				#TODO A METTRE TOUTE LA PARTIE FTP VERS LE CLIENT
				# TODO: viré tous
			elif ACTION == "FTP_CLIENT" or ACTION == "BACKUP":
				if self.ROLE == "1":
					# ADMIN
					SITE_FOR_ADMIN = MESSAGE_FROM_CLIENT[1]
					if SITE_FOR_ADMIN == "SIEGE":
						self.send(self.FTP_IP_SIEGE + "," + self.FTP_LOGIN_SIEGE + "," + self.FTP_PASSWORD_SIEGE)

					elif SITE_FOR_ADMIN == "GRENOBLE":
						self.send(self.FTP_IP_GRENOBLE + "," + self.FTP_LOGIN_GRENOBLE + "," + self.FTP_PASSWORD_GRENOBLE)

					elif SITE_FOR_ADMIN == "RENNES":
						self.send(self.FTP_IP_RENNES + "," + self.FTP_LOGIN_RENNES + "," + self.FTP_PASSWORD_RENNES)

					elif SITE_FOR_ADMIN == "STRASBOURG":
						self.send(self.FTP_IP_STRASBOURG + "," + self.FTP_LOGIN_STRASBOURG + "," + self.FTP_PASSWORD_STRASBOURG)

				else:
						# NO ADMIN
					if self.SITE == "SIEGE":
						self.send(self.FTP_IP_SIEGE + "," + self.FTP_LOGIN_SIEGE + "," + self.FTP_PASSWORD_SIEGE)

					elif self.SITE == "GRENOBLE":
						self.send(self.FTP_IP_GRENOBLE + "," + self.FTP_LOGIN_GRENOBLE + "," + self.FTP_PASSWORD_GRENOBLE)

					elif self.SITE == "RENNES":
						self.send(self.FTP_IP_RENNES + "," + self.FTP_LOGIN_RENNES + "," + self.FTP_PASSWORD_RENNES)

					elif self.SITE == "STRASBOURG":
						self.send(self.FTP_IP_STRASBOURG + "," + self.FTP_LOGIN_STRASBOURG + "," + self.FTP_PASSWORD_STRASBOURG)

			elif ACTION == "CLOSE_CLIENT":
				self.logging.info("STOP CLIENT")
				self.close()
				break
			else:
				print(ACTION,"ERROR")
				self.close()
				break
					
			# FIN BLOUCLE INFINI
				"""
					if ACTION == "SERVEUR MAINTENANCE":
						self.logging.critical("SERVEUR MAINTENANCE")
						self.All_users("SERVER MAINTENANCE")
						self.logging.critical("STOP SERVEUR")
						self.closeServer()
						break
				"""

if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script Serveur a été importer avec succès")