from dbconnector import *
import xml.dom.minidom

class Objectif:
	def __init__(self,id):
		self.id=id
		self.nbItemCharacter=0
		self.loadFromBDD()
		self.status=False
		
	def loadFromBDD(self):
		query="SELECT star038_mission_star036, star038_type_star037, star038_text, star038_item_starXXX,star038_item_table, star038_zone_star012,star038_nbitem"
		query+=" FROM star038_objectif where star038_id=" + str(self.id)

		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.idType=int(row[1])
			self.text=row[2]
			self.idItem=int(row[3])
			self.tableItem=row[4]
			self.zone=int(row[5])
			self.nbItem=int(row[6])
		cursor.close()
		
	@staticmethod
	def getTypeObjectifById(id):
		query="SELECT star037_id, star037_label FROM STAR037_typeobjectif where star037_id='" + str(id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		objType=""
		for row in result_set:
			objType=str(row[0]) + " | " + str(row[1])
		cursor.close()
		return objType
		
	@staticmethod
	def getListOfTypeObjectif():
		query="SELECT star037_id, star037_label FROM STAR037_typeobjectif"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listType=[]
		for row in result_set:
			listType.append(str(row[0]) + " | " + str(row[1]))
			
		cursor.close()
		return listType
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		missionXml=docXml.createElement("objectif")
		idXml=docXml.createElement("idobjectif")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		idtypeXml=docXml.createElement("idtype")
		idtypeXml.appendChild(docXml.createTextNode(str(self.idType)))
		textXml=docXml.createElement("text")
		textXml.appendChild(docXml.createTextNode(str(self.text)))
		idItemXml=docXml.createElement("iditem")
		idItemXml.appendChild(docXml.createTextNode(str(self.idItem)))
		tableItemXml=docXml.createElement("tableitem")
		tableItemXml.appendChild(docXml.createTextNode(str(self.tableItem)))
		zoneXml=docXml.createElement("zone")
		zoneXml.appendChild(docXml.createTextNode(str(self.zone)))
		nbItemXml=docXml.createElement("nbitem")
		nbItemXml.appendChild(docXml.createTextNode(str(self.nbItem)))
		
		missionXml.appendChild(idXml)
		missionXml.appendChild(idtypeXml)
		missionXml.appendChild(textXml)
		missionXml.appendChild(idItemXml)
		missionXml.appendChild(tableItemXml)
		missionXml.appendChild(zoneXml)
		missionXml.appendChild(nbItemXml)
		
		return missionXml
		
	def setNbItemCharacter(self,nb):
		self.nbItemCharacter=nb
		
	def getNbItemCharacter(self):
		return self.nbItemCharacter
		
	def getId(self):
		return self.id
		
	def getIdType(self):
		return self.idType
		
	def getText(self):
		return self.text
		
	def getIdItem(self):
		return self.idItem
		
	def getTableItem(self):
		return self.tableItem
		
	def getZone(self):
		return self.zone
		
	def getNbItem(self):
		return self.nbItem
		
	def getStatus(self):
		return self.status
		
	def setStatus(self,status):
		self.status=status
	