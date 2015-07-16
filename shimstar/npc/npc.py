#~ from shimstar.core.constantes import *
#~ from shimstar.bdd.dbconnector import *
import os, sys
import os.path
import xml.dom.minidom
from dbconnector import *
#~ from shimstar.npc.intelligence.attitude import *
#~ from shimstar.items.ship import *

class NPC:
	def __init__(self,id=0):
		self.id=id
		self.name=""
		self.idZone=0
		self.templateShip=0
		self.idBehavior=0
		self.idFaction=0
		
		if self.id!=0:
			self.loadFromBDD()
			
	def getTemplateShip(self):
		return self.templateShip
		
	def setTemplateShip(self,t):
		self.templateShip=t
		
	def getIdBehavior(self):
		return self.idBehavior
		
	def setIdBehavior(self,b):
		self.idBehavior=b
		
	def getIdZone(self):
		return self.idZone
		
	def setIdZone(self,i):
		self.idZone=i

	def getIdFaction(self):
		return self.idFaction
		
	def setIdFaction(self,id):
		self.idFaction=id
	
	@staticmethod
	def getListOfNpcInZone(idZone):
		query = "select star035_id from star035_npc_template where star035_id_zone_behaviour_star011 =" + str(idZone)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfNpc=[]
		for row in result_set:			
			listOfNpc.append(int(row[0]))
		return listOfNpc
	
	def loadFromBDD(self):
		query = "select star035_name,star035_ship_star005,star035_id_behaviour,star035_id_zone_behaviour_star011"
		query +=", star035_id_faction_star059"
		query += " from star035_npc_template "
		query +=" where star035_id =" + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
	
		for row in result_set:			
			self.name=row[0]
			self.idZone=int(row[3])
			self.templateShip=int(row[1])
			self.idBehavior=int(row[2])
			self.idFaction=int(row[4])
			
	
	def getName(self):
		return self.name
		
	def setName(self,n):
		self.name=n
		
	def getId(self):
		return self.id
		
	def saveToBDD(self):
		if self.id>0:
			query="update star035_npc_template"
			query+=" set star035_name = '" + str (self.name) + "', star035_ship_star005 = '" + str(self.templateShip) + "'"
			query+=",star035_id_behaviour='" + str(self.idBehavior) + "',star035_id_zone_behaviour_star011 = '" + str(self.idZone)+"'"
			query+=",star035_id_faction_star059 = '" + str(self.idFaction) + "'"
			query+=" where star035_id = '" + str(self.id) + "'"
			print query
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
		else:
			query="insert into star035_npc_template"
			query+="(star035_name,star035_ship_star005,star035_id_behaviour,star035_id_zone_behaviour_star011,star035_id_faction_star059)"
			query+="values"
			query+=" ('" + str(self.name) + "','" + str(self.templateShip) +"','" + str(self.idBehavior) + "','" + str(self.idZone) + "','" + str(self.idFaction) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
		cursor.close()
		instanceDbConnector.commit()
		
		
	def deleteFromBDD(self):
		query="delete from star035_npc_template where star035_id ='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		instanceDbConnector.commit()