#!/usr/bin/python
from logging import Logging
import ftplib
class FTP():
	def __init__(self,IP,USER,PASSWORD) :
		self.FILE_LOG = "Folder_log/ftp.log"
		self.logging = Logging(self.FILE_LOG)

		self.IP = IP
		self.USER = USER
		self.PASSWORD = PASSWORD
		self.CONNECT = ftplib(self.IP,self.USER,self.PASSWORD)

	def envoyer_file(self,fichier):
		file = open(fichier, 'rb') # ici, j'ouvre le fichier ftp.py 
		self.CONNECT.storbinary('STOR '+fichier, file) # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
		file.close() # on ferme le fichier

	def list_folder(self):
		return self.CONNECT.dir() # on récupère le listing

	def rename_file(self,old_name,new_name):
		return self.CONNECT.rename(old_name,new_name)

if __name__ == '__main__':
	print ("veillez importer le script")
	ftp = FTP("172.20.20.30","gfive","gfvie")
else:
	print ("Le script tools a été importer avec succès")