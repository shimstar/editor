from dbconnector import *
import xml.dom.minidom
from constantes import *

class Faction:
	def __init__(self,id):
		self.id=id
		self.name=""
		if self.id>0:
			self.loadFromBdd()
		
	def getId(self):
		return self.id
		
	def getName(self):
		return self.name
		
	def setName(self,name):
		self.name=name
		
	@staticmethod
	def getListOfFactions():
		query="select star059_id,star059_name from star059_faction order by star059_name"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		returnList={}
		for row in result_set:
			returnList[int(row[0])]=str(row[1])
		cursor.close()
		return returnList
		
	def loadFromBdd(self):
		query = "select star059_name from star059_faction where star059_id = '" +str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=str(row[0])
			
		cursor.close()
		
	def saveToBDD(self):
		if self.id==0:
			query="insert into star059_faction (star059_name) values ('" + str(self.name) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
			instanceDbConnector.commit()
		else:
			query="update star059_faction set star059_name = '" + str(self.name) + "' where star059_id = '" + str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			instanceDbConnector.commit()
			
	def deleteFromBDD(self):
		if self.id>0:
			query="delete from star059_faction where star059_id = '" +str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			instanceDbConnector.commit()