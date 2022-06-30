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
		self.CONNECT = self.connect(self.IP,self.USER,self.PASSWORD)

	def connect(self,IP,USER,PASSWORD):
		try :
			return ftplib.FTP(IP,USER,PASSWORD)
		except(ftplib.error_temp):
			return (print("Erreur impossible de joindre le serveur FTP"))
	def send_file(self,fichier):
		file = open(fichier, 'rb') # ici, j'ouvre le fichier ftp.py 
		self.CONNECT.storbinary('STOR '+fichier, file) # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
		file.close() # on ferme le fichier

	def dir(self):
		data = []
		self.CONNECT.dir(data.append) # on récupère le listing
		return data
	def rename(self,old_name,new_name):
		return self.CONNECT.rename(old_name,new_name)
	def delete(self,file):
		return self.CONNECT.delete(file)
	def mkd(self,folder):
		self.CONNECT.mkd(folder)
	def rmd(self,folder):
		self.CONNECT.rmd(folder)
	def exit(self):
		self.CONNECT.quit()



if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script ftp a été importer avec succès")