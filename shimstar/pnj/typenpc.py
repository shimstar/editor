from dbconnector import *

class TypeNPC:
	def __init__(self,id):
		self.id=id
		self.name=""
		self.loadFromBDD()
		
	def loadFromBDD(self):
		query="select star057_name from star057_typenpc where star057_id='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[0]
		cursor.close()
		
	def getId(self):
		return self.id
		
	def getName(self):
		return self.name
		
	def setName(self,n):
		self.name=n
		
	@staticmethod
	def getListOfTypeNpc():
		query = "Select star057_id, star057_name from star057_typenpc"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		returnResult={}
		for row in result_set:			
			returnResult[int(row[0])]=row[1]
		cursor.close()
		
		return returnResult
		
	def saveToBDD(self):
		if self.id>0:
			query="update star057_typenpc set star057_name='" + str(self.name) + "' where star057_id = '" + str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
		else:
			query="insert into star057_typenpc (star057_name) values ('" + self.name + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=int(cursor.lastrowid)
			cursor.close()
	
	