#!/usr/bin/python
from server import Serveur
import threading

IP = "localhost"
PORT = 3401
DATA_BASE = "DataBase.db"

SERVER = Serveur(IP,PORT,DATA_BASE)
SERVER.start()

threadsClients = []

while True:
	SERVER.accept()
	threadsClients.append(threading.Thread(None, SERVER.Instruction, None, (SERVER.client, SERVER.infosClient, SERVER.server), {}))
	threadsClients[-1].start()


#serveur.close()