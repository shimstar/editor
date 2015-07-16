from dbconnector import *
from shimstar.character.character import *

class User:
	def __init__(self,id):
		self.id=id
		self.name=""
		self.pwd=""
		self.lastLogin=""
		self.dateCreation=""
		self.listOfCharacter=[]
		self.loadFromBDD()

	@staticmethod
	def getListOfUsers():
		query="select star001_id,star001_name from star001_user order by star001_name"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		
		result_set = cursor.fetchall ()
		listOfUser={}
		for row in result_set:
			listOfUser[int(row[0])]=str(row[1])
		cursor.close()
		return listOfUser
		
	def getId(self):
		return self.id
		
	def getListOfCharacter(self):
		return self.listOfCharacter
		
	def getName(self):
		return self.name
		
	def getPwd(self):
		return self.pwd
		
	def getLastLogin(self):
		return self.lastLogin
		
	def getDateCreation(self):
		return self.dateCreation
		
	def loadFromBDD(self):
		query="SELECT star001_passwd,star001_name,star001_lastlogin,star001_created FROM star001_user WHERE star001_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=row[1]
			self.password=row[0]
			self.lastLogin=str(row[2])
			self.dateCreation=str(row[3])
		cursor.close()
		
		query="Select star002_id from star002_character where star002_iduser_star001 = '" + str(self.id) +"'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		
		result_set = cursor.fetchall ()
		for row in result_set:
			idChar=int(row[0])
			temp=Character(idChar)
			self.listOfCharacter.append(temp)
		cursor.close()
		