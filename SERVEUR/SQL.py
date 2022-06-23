#!/usr/bin/python
import sqlite3, os
from logging import Logging

class SQL():
	def __init__(self,DATA_BASE):
		self.DATA_BASE = DATA_BASE
		self.DataBase = sqlite3.connect(self.DATA_BASE, check_same_thread=False)
		self.QueryCurs = self.DataBase.cursor()

		self.FILE_LOG = "Folder_log/sql.log"
		self.logging = Logging(self.FILE_LOG)
		
		self.Get_file_DB()

	# met a jour la bdd avec les nouvelle données
	def commit(self):
		self.DataBase.commit()

	# crée la Table Utilisateur dans la base de donées
	def Create_table(self):
		self.QueryCurs.execute('''CREATE TABLE Utilisateur (
				ID INTEGER PRIMARY KEY,
				LOGIN TEXT,
				PASSWORD TEXT,
				ROLE INTEGER,
				NOM TEXT,
				PRENOM TEXT,
				SITE TEXT
				)''')

	# verifie si la basse de donées existe si elle existe pas elle crée une nouvelle base de donées en créant la Table Utilisateur et en créant l'utilisateur root
	def Get_file_DB(self):
		if os.path.getsize(self.DATA_BASE) == 0:
			self.logging.warning("génération de la base de donées")		
			self.Create_table()
			self.logging.warning("création de l'utilisateur par default root avec comme mdp root ")
			self.New_User("root", "4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2","1","root","root","SIEGE")
			return False
		else:
			return True

	# Crée un nouvelle utilisateur
	def New_User(self,LOGIN,PASSWORD,ROLE,NOM,PRENOM,SITE):
		self.QueryCurs.execute('''INSERT INTO Utilisateur (LOGIN,PASSWORD,ROLE,NOM,PRENOM,SITE)
		VALUES (?,?,?,?,?,?)''',(LOGIN,PASSWORD,ROLE,NOM,PRENOM,SITE))
		self.commit()
		self.logging.info("New User:" + LOGIN)
	
	# GET VALUE ON TAB Utilisateur
	def Get_all(self):
		return self.QueryCurs.execute("SELECT * FROM Utilisateur",).fetchall()
	def Get_LOGIN(self,ID):
		return self.QueryCurs.execute("SELECT LOGIN FROM Utilisateur WHERE ID=?",(ID,),).fetchall()
	def Get_PASSWORD(self,ID):
		return self.QueryCurs.execute("SELECT PASSWORD FROM Utilisateur WHERE ID=?",(ID,),).fetchall()
	def Get_ROLE(self,ID):
		return self.QueryCurs.execute("SELECT ROLE FROM Utilisateur WHERE ID=?",(ID,),).fetchall()
	def Get_SITE(self,ID):
		return self.QueryCurs.execute("SELECT SITE FROM Utilisateur WHERE ID=?",(ID,),).fetchall()

	# UPDATE VALUE ON TAB Utilisateur
	def Update_LOGIN(self,UPDATE,ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET LOGIN = ? WHERE ID = ?",(UPDATE,ID,),).fetchall()
		self.commit()
		self.logging.info("UPDATE LOGIN ID:" + ID)
	def Update_PASSWORD(self,UPDATE,ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET PASSWORD = ? WHERE ID = ?",(UPDATE,ID,),).fetchall()
		self.commit()
		self.logging.info("UPDATE PASSWORD ID:" + ID)
	def Update_ROLE(self,UPDATE,ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET ROLE = ? WHERE ID = ?",(UPDATE,ID,),).fetchall()
		self.commit()
		self.logging.info("UPDATE ROLE ID:" + ID)
	def Update_NOM(self,UPDATE,ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET NOM = ? WHERE ID = ?",(UPDATE,ID,),).fetchall()
		self.commit()
		self.logging.info("UPDATE NOM ID:" + ID)
	def Update_PRENOM(self,UPDATE,ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET PRENOM = ? WHERE ID = ?",(UPDATE,ID,),).fetchall()
		self.commit()
		self.logging.info("UPDATE PRENOM ID:" + ID)
	def Update_SITE(self,UPDATE,ID):
		self.QueryCurs.execute("UPDATE Utilisateur SET SITE = ? WHERE ID = ?",(UPDATE,ID,),).fetchall()
		self.commit()
		self.logging.info("UPDATE SITE ID:" + ID)

	# recherche
	def Search_LOGIN_and_PASSWORD(self,LOGIN):
		return self.QueryCurs.execute("SELECT * FROM Utilisateur WHERE LOGIN=?",(LOGIN,),).fetchall()
	def Search_LOGIN(self,LOGIN):
		return self.QueryCurs.execute("SELECT LOGIN FROM Utilisateur WHERE LOGIN=?",(LOGIN,),).fetchall()
	def Search_PASSWORD(self,LOGIN):
		return self.QueryCurs.execute("SELECT PASSWORD FROM Utilisateur WHERE LOGIN=?",(LOGIN,),).fetchall()
	def Search_ID(self,LOGIN):
		return self.QueryCurs.execute("SELECT ID FROM Utilisateur WHERE LOGIN=?",(LOGIN,),).fetchall()

	# supprimer
	def Del_User(self,ID):
		self.QueryCurs.execute("DELETE FROM Utilisateur WHERE ID = ?",(ID,),).fetchall()
		self.commit()

if __name__ == '__main__':
	print ("veillez importer le script")
else:
	print ("Le script SQL a été importer avec succès")