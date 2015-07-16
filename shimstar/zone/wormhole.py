import os, sys
from dbconnector import *
import xml.dom.minidom
#~ import direct.directbase.DirectStart
#~ from direct.showbase.DirectObject import DirectObject
#~ from pandac.PandaModules import CollisionTraverser,CollisionNode
#~ from direct.task.TaskOrig import Task
#~ from direct.task import Task
#~ from pandac.PandaModules import BillboardEffect
#~ from shimstar.core.function import *

class wormhole:
	def __init__(self,id,idTemplate=0):
		self.id=id
		#~ self.zoneId=zoneId
		#~ self.name=name
		self.className="wormhole"
		self.idTemplate=idTemplate
		#~ self.scale=scale
		#~ self.pos=pos
		#~ self.hpr=hpr
		self.model=None
		self.egg=""
		self.destinations=[]
		if self.id>0:
			self.loadFromBdd()
		else:
			self.loadTemplate()
			
		
	@staticmethod
	def getListOfWormHoleTemplate():
		query="SELECT star061_id from star061_gate_template"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfWormHole=[]
		for row in result_set:			
			listOfWormHole.append(int(row[0]))
		return listOfWormHole
		
	@staticmethod
	def getListOfWormHole(zoneId):
		query="SELECT star060_id from star060_gate where star060_zone_star011 ='" + str(zoneId) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfWormHole=[]
		for row in result_set:			
			listOfWormHole.append(int(row[0]))
		return listOfWormHole
		
	def getDestinations(self):
		return self.destinations

	def getPos(self):
		return self.pos
		
	def getName(self):
		return self.name
		
	def loadTemplate(self):
		query="SELECT star061_name,star061_egg from star061_gate_template where star061_id='" + str(self.idTemplate)+ "'"
		instanceDbConnector=shimDbConnector.getInstance()

		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=row[0]
			self.egg=row[1]
			
		cursor.close()

	def loadDestinations(self):
		query="SELECT star062_zone_star011 from star062_gate_zone where star062_gate_star062='" + str(self.id)+ "'"
		instanceDbConnector=shimDbConnector.getInstance()

		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.destinations.append(int(row[0]))
			
		cursor.close()
		
	def getXmlTemplate(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		wormXml=docXml.createElement("wormhole")
		idXml=docXml.createElement("id")
		idXml.appendChild(docXml.createTextNode(str(self.idTemplate)))
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		eggXml=docXml.createElement("egg")
		eggXml.appendChild(docXml.createTextNode(str(self.egg)))
		wormXml.appendChild(idXml)
		wormXml.appendChild(nameXml)
		wormXml.appendChild(eggXml)
				
		return wormXml
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		wormXml=docXml.createElement("wormhole")
		idXml=docXml.createElement("id")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		idtemplateXml=docXml.createElement("idtemplate")
		idtemplateXml.appendChild(docXml.createTextNode(str(self.idTemplate)))
		posxXml=docXml.createElement("posx")
		posxXml.appendChild(docXml.createTextNode(str(self.posx)))
		posyXml=docXml.createElement("posy")
		posyXml.appendChild(docXml.createTextNode(str(self.posy)))
		poszXml=docXml.createElement("posz")
		poszXml.appendChild(docXml.createTextNode(str(self.posz)))
		hprhXml=docXml.createElement("hprh")
		hprhXml.appendChild(docXml.createTextNode(str(self.hprh)))
		hprpXml=docXml.createElement("hprp")
		hprpXml.appendChild(docXml.createTextNode(str(self.hprp)))
		hprrXml=docXml.createElement("hprr")
		hprrXml.appendChild(docXml.createTextNode(str(self.hprr)))
		if len(self.destinations)>0:
			destinationsXml=docXml.createElement("destinations")
			for m in self.destinations:
				destinationXml=docXml.createElement("destination")
				iddestinationXml=docXml.createElement("iddestination")
				iddestinationXml.appendChild(docXml.createTextNode(str(m)))
				destinationXml.appendChild(iddestinationXml)
			destinationsXml.appendChild(destinationXml)
			wormXml.appendChild(destinationsXml)
		wormXml.appendChild(idXml)
		wormXml.appendChild(idtemplateXml)
		wormXml.appendChild(posxXml)
		wormXml.appendChild(posyXml)
		wormXml.appendChild(poszXml)
		wormXml.appendChild(hprhXml)
		wormXml.appendChild(hprrXml)
		wormXml.appendChild(hprpXml)
				
		return wormXml
		
	def loadFromBdd(self):
			query="SELECT star060_template_star061, star060_zone_star011, star060_posx, star060_posy, star060_posz"
			query+=" ,star060_hprh, star060_hprp, star060_hprr"
			query+=" ,star061_egg"
			query+=" FROM star060_gate join star061_gate_template on star060_template_star061=star061_id"
			query+=" where star060_id ='" + str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()

			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			result_set = cursor.fetchall ()
			for row in result_set:
				self.zoneId=int(row[1])
				self.templateId=int(row[0])
				self.posx=float(row[2])
				self.posy=float(row[3])
				self.posz=float(row[4])
				self.hprh=float(row[5])
				self.hprp=float(row[6])
				self.hprr=float(row[7])
				self.pos=(float(row[2]),float(row[3]),float(row[4]))
				self.hpr=(float(row[5]),float(row[6]),float(row[7]))
				self.egg=row[8]
				self.idTemplate=int(row[0])

			cursor.close()
			
			self.loadDestinations()        