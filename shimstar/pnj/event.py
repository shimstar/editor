from dbconnector import *

class Event:
	def __init__(self,id):
		self.id=id
		self.type=0
		self.idZone=0
		self.point=(0,0,0)
		self.idtrigger=0
		self.npcTemplate=0
		self.idMission=0
		
	@staticmethod
	def getTypeEvent():
		query="select star048_id,star048_label from star048_type_event order by star048_label"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result={}
		for row in result_set:
			result[int(row[0])]=row[1]
		cursor.close()
		return result
		
	def loadFromBDD(self):
		query="select star047_type_star048, star047_mission_star036,star047_npc_star035"
		query+=" ,star047_pointX,star047_pointY,star047_pointZ,star047_zone_star011,star047_idtrigger_star064"
		query+=" FROM star047_event "
		query+=" where star047_id = " + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.type=int(row[0])
			self.idMission=int(row[1])
			self.npcTemplate=int(row[2])
			self.point=(int(row[3]),int(row[4]),int(row[5]))
			self.idZone=int(row[6])
			self.idTrigger=int(row[7])
		cursor.close()
		
	def saveToBDD(self):
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		if self.id>0:
			query="update star047_event"
			query+=" set star047_type_star048=" + str(self.type) + ",star047_idzone_star011=" + str(self.idZone)
			query+=",star047_pointx=" + str(self.point[0]) + ",star047_pointy=" + str(self.point[1]) + ",star047_pointz=" + str(self.point[2])
			query+=",star047_mission_star036=" + str(self.idMission) +",star047_idtrigger_star064=" + str(self.idTrigger) 
			query+=" where star047_id = " +str(self.id)
			cursor.execute(query)
			cursor.close()
		else:
			query="insert into star047_event"
			query+=" (star047_type_star048,star047_idzone_star011,star047_pointx,star047_pointy,star047_pointz"
			query+=",star047_mission_star036,star047_idtrigger_star064)"
			query+=" values (" + str(self.type)+"," + str(self.idZone) + "," + str(self.point[0]) + "," + str(self.point[1]) + "," + str(self.point[2])
			query+="," + str(self.idMission) + "," + str(self.idTrigger) + ")"
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
		instanceDbConnector.commit()
		
	def deleteFromBDD(self):
		if self.id>0:
			query="delete from star047_event where star047_id = " + str(self.id)
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			instanceDbConnector.commit()
		
	def getIdMission(self):
		return self.idMission
		
	def setIdMission(self,i):
		self.idMission=i
	
	def getId(self):
		return self.id
		
	def getType(self):
		return self.type
		
	def setType(self,t):
		self.type=t
	
	def getIdZone(self):
		return self.idZone
		
	def setIdZone(self,i):
		self.idZone=i
		
	def getPoint(self):
		return self.point
	
	def setPoint(self,p):
		self.point=p
		
	def getIdTrigger(self):
		return self.idTrigger
		
	def setIdTrigger(self,i):
		self.idTrigger=i
		
	def getNpcTemplate(self):
		return self.npcTemplate
		
	def setNpcTemplate(self,c):
		self.npcTemplate=c
		
