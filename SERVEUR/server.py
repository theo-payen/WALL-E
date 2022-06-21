#!/usr/bin/python
from SQL import SQL
from tools import TOOLS
from logging import Logging
import socket, sys

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

	def All_users(self,msg):
		for socket in self.infosocket["SOCKET"]:
			try:
				socket.send((msg).encode())
			except:
				self.logging.error("impossible envoyer le message")

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
		
		MESSAGE = self.recv().split(" ")
		self.RECV_LOGIN = MESSAGE[0]
		self.RECV_PASSWORD = MESSAGE[1]
		# faire les requet dans bdd
		
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
			#send role au client
			self.send("APPROUVE")
			self.logging.info("CONNECTION APPROUVE FOR " + self.LOGIN)
			
			#send nom prenom SITE ROLE
			while True:

				if self.ROLE == "0":
					# NON ADMIN
					USER_MESSAGE_FROM_CLIENT = self.recv().split(" ")
					
					pass
				else:
					# ADMIN
					ADM_MESSAGE_FROM_CLIENT = self.recv().split(" ")

					if ADM_MESSAGE_FROM_CLIENT == "SERVEUR MAINTENANCE":
						self.logging.critical("SERVEUR MAINTENANCE")
						self.All_users("SERVER MAINTENANCE")
						self.logging.critical("STOP SERVEUR")
						self.closeServer()
						break

					elif ADM_MESSAGE_FROM_CLIENT == "TOOLS":
						ADM_MESSAGE_FROM_CLIENT_FOR_TOOLS = self.recv()
						ADM_MESSAGE_FROM_CLIENT_FOR_TOOLS = ADM_MESSAGE_FROM_CLIENT.upper()
						if ADM_MESSAGE_FROM_CLIENT_FOR_TOOLS == "Brute force":
							pass
						elif ADM_MESSAGE_FROM_CLIENT_FOR_TOOLS == "Brute force dico":
							pass
						elif ADM_MESSAGE_FROM_CLIENT_FOR_TOOLS == "scan port":
							pass

					if ADM_MESSAGE_FROM_CLIENT == "CLOSE CLIENT":
						self.logging.info("STOP CLIENT")
						self.close()
						break
					elif ADM_MESSAGE_FROM_CLIENT == "FTP LOGIN":
						pass
					elif ADM_MESSAGE_FROM_CLIENT == "CHANGE PASSWORD":
						pass
					else:
						print ("error")

			self.close()





if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script Serveur a été importer avec succès")