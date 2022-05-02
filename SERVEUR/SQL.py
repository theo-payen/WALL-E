#!/usr/bin/python
import sqlite3, os
class SQL():
	def __init__(self,DATA_BASE):
		self.DATA_BASE = DATA_BASE
		self.DataBase = sqlite3.connect(self.DATA_BASE, check_same_thread=False)
		self.QueryCurs = self.DataBase.cursor()

	def commit(self):
		self.DataBase.commit()

	def New_table(self):
		self.QueryCurs.execute('''CREATE TABLE Utilisateur (
				id INTEGER PRIMARY KEY,
				LOGIN TEXT,
				PASSWORD TEXT,
				ROLE INTEGER,
				NOM TEXT,
				PRENOM TEXT,
				SITE TEXT
				)''')

	def Get_file_DB(self):
		if os.path.getsize(self.DATA_BASE) == 0:
			print ("génération de la base de donées")		
			self.New_table()
			print ("création de l'utilisateur par default root avec comme mdp root ")
			self.add_User("root", "4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2","1","root","root","SIEGE")
			return False
		else:
			return True

	def add_User(self,LOGIN,PASSWORD,ROLE,NOM,PRENOM,SITE):
		self.QueryCurs.execute('''INSERT INTO Utilisateur (LOGIN,PASSWORD,ROLE,NOM,PRENOM,SITE)
		VALUES (?,?,?,?,?,?)''',(LOGIN,PASSWORD,ROLE,NOM,PRENOM,SITE))
		self.commit()

	def Get_Value (self,SELECT,WHERE,ID):
		def User():
			pass
		GET = self.QueryCurs.execute("SELECT ? FROM Utilisateur WHERE ?=?",(SELECT,WHERE,ID,),).fetchall()
		return GET

	def Set_value (self,SET, SET_value, ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET ? = ? WHERE id = ?",(SET,SET_value,ID,),).fetchall()
		self.commit() 
	

if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script SQL a été importer avec succès")