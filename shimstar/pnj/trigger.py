from dbconnector import *

class Trigger:
	def __init__(self,id):
		self.id=id
		self.type=0
		self.idZone=0
		self.point=(0,0,0)
		self.radius=0
		self.itemTemplate=0
		self.nbTemplate=0
		self.timer=0
		self.npcTemplate=0
		self.order=0
		self.idMission=0
		
	@staticmethod
	def getTypeTrigger():
		query="select star065_id,star065_label from star065_type_trigger_mission order by star065_label"
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
		query="select star064_type_star065,star064_idzone_star011,star064_point_x,star064_point_y,star064_point_z"
		query+=",star064_radius,star064_itemtemplate_star004,star064_nb_template,star064_timer"
		query+=",star064_npctemplate_star035,star064_order"
		query+=" FROM star064_trigger_mission,star064_idmission_star036"
		query+=" where star064_id = " + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.type=int(row[0])
			self.idZone=int(row[1])
			self.point=(int(row[2]),int(row[3]),int(row[4]))
			self.radius=int(row[5])
			self.itemTemplate=int(row[6])
			self.nbTemplate=int(row[7])
			self.timer=int(row[8])
			self.npcTemplate=int(row[9])
			self.order=int(row[10])
			self.idMission=int(row[11])
		cursor.close()
		
	def saveToBDD(self):
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		if self.id>0:
			query="update star064_trigger_mission"
			query+=" set star064_type_star064=" + str(self.type) + ",star064_idzone_star011=" + str(self.idZone)
			query+=",star064_point_x=" + str(self.point[0]) + ",star064_point_y=" + str(self.point[1]) + ",star064_point_z=" + str(self.point[2])
			query+=",star064_radius=" + str(self.radius) +",star064_itemtemplate_star004=" + str(self.itemTemplate) +",star064_nb_template=" + str(self.nbTemplate)
			query+=",star064_timer=" + str(self.timer) + ",star064_npctemplate_star035=" + str(self.npcTemplate) + ",star064_order=" + str(self.order)
			query+=",star064_idmission_star036=" + str(self.idMission)
			query+=" where star064_id = " +str(self.id)
			cursor.execute(query)
			cursor.close()
		else:
			query="insert into star064_trigger_mission"
			query+=" (star064_type_star065,star064_idzone_star011,star064_point_x,star064_point_y,star064_point_z"
			query+=",star064_radius,star064_itemtemplate_star004,star064_nb_template,star064_timer,star064_idmission_star036)"
			query+=" values (" + str(self.type)+"," + str(self.idZone) + "," + str(self.point[0]) + "," + str(self.point[1]) + "," + str(self.point[2])
			query+="," + str(self.radius) + "," + str(self.itemTemplate) + "," + str(self.nbTemplate) + "," + str(self.timer) + "," +str(self.npcTemplate) + "," + str(self.order)
			query+="," + str(self.idMission) + ")"
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
		instanceDbConnector.commit()
		
	def deleteFromBDD(self):
		if self.id>0:
			query="delete from star064_trigger_mission where star064_id = " + str(self.id)
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
		
	def getRadius(self):
		return self.radius
		
	def setRadius(self,r):
		self.radius=r
		
	def setItemTempalte(self,i):
		self.itemTemplate=i
		
	def getItemTemplate(self):
		return self.itemTemplate
		
	def getNbTemplate(self):
		return self.nbTemplate
		
	def setNbTemplate(self,n):
		self.nbTemplate=n
		
	def getTimer(self):
		return self.timer
		
	def setTimer(self,t):
		self.timer=t
		
	def getNpcTemplate(self):
		return self.npcTemplate
		
	def setNpcTemplate(self,c):
		self.npcTemplate=c
		
	def getOrder(self):
		return self.order
		
	def setOrder(self,o):
		self.order=o