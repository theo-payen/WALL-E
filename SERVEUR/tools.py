#!/usr/bin/python
from itertools import chain
from logging import Logging
import threading, socket, ftplib, re


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
	def export_CSV(self):
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


	def BruteForce_dico (self,file):
		USER = "root"
		try :
			ftplib.FTP(IP,USER,PASSWORD)
		except(ConnectionRefusedError):
			print("port fermé")
		except(ftplib.error_perm):
			print("impoissible de se log")
		else:
			print ("ok")

	def ScanPorts (self,IP,port_min,port_max):
		def Scan(IP,port):
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			result = sock.connect_ex((IP,port))
			if result == 0:
				print("Port", str(port), "ouvert !")
			sock.close()

		while port_min < port_max:
			threading.Thread(target=Scan, args=(IP,port_min,)).start()
			port_min = port_min + 1


if __name__ == '__main__':
	print ("veillez importer le script")
	#
	# LES TESTS
	#
	boite_a_outils = TOOLS()
	IP = "172.20.20.35"
	boite_a_outils.BruteForce(IP,0)

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



	# Driver code
	



	pass
else:
	print ("Le script tools a été importer avec succès")