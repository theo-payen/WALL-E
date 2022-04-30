#!/usr/bin/python
from datetime import datetime

class Logging():
	def __init__(self,FILE_LOG):
		self.FILE_LOG = FILE_LOG
		self.right = "a+"

	def open(self):
		self.FILE = open(self.FILE_LOG,self.right) 

	def close(self):
		self.FILE.close()

	def Getdate(self):
		return f'{datetime.now():%m/%d/%Y %H:%M:%S}'

	def print(self,msg,status):
		self.open()  
		Message = self.Getdate(),status,msg
		self.FILE.write(str(Message) + "\n")
		print(Message)
		self.close()

	def info(self,msg):
		self.print(msg,"INFO")

	def warning(self,msg):
		self.print(msg,"WARNING")

	def error(self,msg):
		self.print(msg,"ERROR")

	def critical(self,msg):
		self.print(msg,"CRITICAL")

	def debug(self,msg):
		self.print(msg,"DEBUG")


if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script log a été importer avec succès")