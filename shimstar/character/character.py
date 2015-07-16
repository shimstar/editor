from dbconnector import *

class Character:
	def __init__(self,id):
		self.id=id
		self.name=""
		self.face=""
		self.idZone=0
		self.lastStation=0
		self.idFaction=0
		
		self.loadFromBDD()
		
	def getId(self):
		return self.id
		
	def getName(self):
		return self.name
		
	def getFace(self):
		return self.face
		
	def getIdZone(self):
		return self.idZone
		
	def getLastStation(self):
		return self.lastStation
		
	def getIdFaction(self):
		return self.idFaction
		
	def loadFromBDD(self):
		query="select star002_name,star002_face,star002_zone_star011zone,star002_laststation_star022station,star002_faction_star059"
		query+=" from star002_character where star002_id = '" + str(self.id) + "'"
		
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)		
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=str(row[0])
			self.face=str(row[1])
			self.idZone=int(row[2])
			self.lastStation=int(row[3])
			self.idFaction=int(row[4])
		cursor.close()