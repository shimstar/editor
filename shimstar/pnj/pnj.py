from dbconnector import *
import xml.dom.minidom

class PNJ:
	def __init__(self,id):
		self.id=id
		self.label=""
		self.dialogs=[]
		self.missions=[]
		self.typeNPC=0
		self.zone=0
		if id>0:
			self.loadFromBDD()
			
	def getDialogs(self):
		return self.dialogs
		
	def getMissions(self):
		return self.missions
		
	def getIdStation(self):
		return self.idStation
		
	def loadFromBDD(self):
		query="SELECT star027_name, star027_face, star027_location_star022,star027_type_star057 FROM star027_npc_station WHERE star027_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[0]
			self.face= row[1]
			self.zone=int(row[2])
			self.typeNPC=int(row[3])
		cursor.close()
		
		self.loadDialogue()
		self.loadMission()
		
	def getTypeNPC(self):
		return self.typeNPC
		
	def loadDialogue(self):
		query="SELECT star028_dialogue_star025 FROM star028_npc_dialogue WHERE star028_npc_star027 ='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			idDiag=int(row[0])
			self.dialogs.append(idDiag)
		cursor.close()
		
	def loadMission(self):
		query="SELECT star036_id FROM STAR036_mission WHERE star036_npc_star034='"  + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.missions.append(int(row[0]))
		cursor.close()
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getFace(self):
		return self.face
		
	def getZone(self):
		return self.zone
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		pnjXml=docXml.createElement("pnj")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		idXml=docXml.createElement("id")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		faceXml=docXml.createElement("face")
		faceXml.appendChild(docXml.createTextNode(str(self.face)))
		typeXml=docXml.createElement("typenpc")
		typeXml.appendChild(docXml.createTextNode(str(self.typeNPC)))
		zoneXml=docXml.createElement("zone")
		zoneXml.appendChild(docXml.createTextNode(str(self.zone)))
		if len(self.dialogs)>0:
			diagsXml=docXml.createElement("dialogues")
			for d in self.dialogs:
				iddiagXml=docXml.createElement("iddialogue")
				iddiagXml.appendChild(docXml.createTextNode(str(d)))
				diagsXml.appendChild(iddiagXml)
			pnjXml.appendChild(diagsXml)
		if len(self.missions)>0:
			missionsXml=docXml.createElement("missions")
			for m in self.missions:
				idmissionXml=docXml.createElement("idmission")
				idmissionXml.appendChild(docXml.createTextNode(str(m)))
				missionsXml.appendChild(idmissionXml)
			pnjXml.appendChild(missionsXml)
		pnjXml.appendChild(nameXml)
		pnjXml.appendChild(idXml)
		pnjXml.appendChild(faceXml)
		pnjXml.appendChild(zoneXml)
		pnjXml.appendChild(typeXml)
				
		return pnjXml
		
	@staticmethod
	def getListOfPNJ():
		query="SELECT star027_id FROM star027_npc_station"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result