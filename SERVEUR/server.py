#!/usr/bin/python
from SQL import SQL
from tools import TOOLS
from logging import Logging
import socket, os
# TODO mettre en place les try
# TODO commanter le code
# TODO FINALISER LA CLASS
class Serveur():
	def __init__(self,IP,PORT):
		
		self.IP = IP
		self.PORT = PORT

		self.ID_client = 0
		self.infosocket = {"ID":[],"SOCKET":[]}

		self.FILE_LOG = "Folder_log/server.log"
		self.logging = Logging(self.FILE_LOG)

		self.logging.info("Serveur start")


	def initialise_sql(self,DATA_BASE):
		self.DATA_BASE = DATA_BASE
		self.SQL = SQL(self.DATA_BASE)
		if self.SQL.Get_file_DB() == False:
			self.logging.info("fichier db crée")

	def initialise_tools(self):
		self.TOOLS = TOOLS()

	def start(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((self.IP, self.PORT))
			self.server.listen(5)
		except:
			self.logging.error("Impossible de démmaré le serveur")
			os.exit()

	def accept(self):
		try:
			self.client,self.infosClient = self.server.accept()
		except:
			self.logging.error("Impossible detablire la connexion avec le client")
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
		rep = self.client.recv(255)
		rep = rep.decode()
		return rep

	def send(self,msg):
		try:
			msg = msg.encode()
			self.client.send(msg)
		except : 
			self.logging.error("impossible d'envoyer un message")

	def close(self):
		self.client.close()
	
	def threading (self,client, infosClient, server):   
		
		self.logging.info("START threadsClients for client" + infosClient[0] + str(infosClient[1]))

		adresseIP = infosClient[0]
		port = str(infosClient[1])
		self.logging.info(str(client) + str(adresseIP) + str(port) + str(server))
		self.logging.info(self.SQL.Get_Value("*","ID","*"))
		
		if self.recv() == "CONNECTION":
			self.logging.info("CONNECTION")
			# TODO ## test
			self.logging.info("CONNECTION APPROUVE")
			self.logging.info("APPROUVE")
			self.send("APPROUVE")
		else:
			self.logging.warning("CONNECTION REFUSE")
			self.send("REFUSE")
			self.close()
		
		#
		# connexion a la db 
		#

		#
		# apres connexion
		#
		

		admin = True
		while True:
			ClientMessage = self.recv()
			ClientMessage = ClientMessage.upper()
			if admin == True:
				if ClientMessage == "SERVEUR MAINTENANCE":
					self.logging.critical("SERVEUR MAINTENANCE")
					self.All_users("SERVER MAINTENANCE")
					self.logging.critical("STOP SERVEUR")
					self.closeServer()
					break
				
				elif ClientMessage == "TOOLS":
					ClientMessage_for_tools = self.recv()
					ClientMessage_for_tools = ClientMessage.upper()
					if ClientMessage_for_tools == "Brute force":
						pass
					elif ClientMessage_for_tools == "Brute force dico":
						pass
					elif ClientMessage_for_tools == "scan port":
						pass


			if ClientMessage == "CLOSE CLIENT":
				self.logging.info("STOP CLIENT")
				self.close()
				break
			elif ClientMessage == "FTP LOGIN":
				pass
			elif ClientMessage == "CHANGE PASSWORD":
				pass
			else:
				# TODO a faie 
				#print ("error")
				pass
		self.close()


if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script Serveur a été importer avec succès")