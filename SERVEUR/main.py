#!/usr/bin/python
from server import Serveur
import threading, os

IP = "localhost"
PORT = 3400
DATA_BASE = "DataBase.db"

SERVER = Serveur(IP,PORT)


SERVER.initialise_sql(DATA_BASE)
SERVER.start()
threadsClients = []

while True:
	SERVER.accept()
	threadsClients.append(threading.Thread(None, SERVER.threading, None, (SERVER.client, SERVER.infosClient, SERVER.server), {}))
	threadsClients[-1].start()


#fichier.close()
#serveur.close()

os.pause()