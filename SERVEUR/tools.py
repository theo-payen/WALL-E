#!/usr/bin/python
from logging import Logging
import threading

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
	def TestConnection (self,IP):
		print(IP)
		pass
	def BruteForce (self,nombre_caractaire):
		pass
	def BruteForce_dico (self,file):
		pass
	def ScanPorts (self,IP,port_min,port_max):
		self.TestConnection(IP)
		# boucle for qui liste les port min a port _max
		# pour tous les prot ouvert les renseigner dans un tableau
		# affiche le tableau
		# /!\ threading
		# utiliser la commande socket
		pass
	def affiche_log(self):
		pass


if __name__ == '__main__':
	print ("veillez importer le script")
	#
	# LES TESTS
	#
	boite_a_outils = TOOLS()

	IP = "192.168.1.1"
	boite_a_outils.TestConnection(IP)
	pass
else:
	print ("Le script tools a été importer avec succès")