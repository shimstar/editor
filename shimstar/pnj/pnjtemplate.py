from dbconnector import *
import xml.dom.minidom

class PNJtemplate:
	def __init__(self,id):
		self.id=id
		self.label=""
		self.dialogs=[]
		self.missions=[]
		query="SELECT star035_name, star035_ship_star005 FROM star035_npc_template WHERE star035_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[0]
			self.ship= int(row[1])
		cursor.close()
	
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getShip(self):
		return self.ship
				
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		pnjXml=docXml.createElement("pnjtemplate")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		idXml=docXml.createElement("id")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		shipXml=docXml.createElement("ship")
		shipXml.appendChild(docXml.createTextNode(str(self.ship)))
		pnjXml.appendChild(nameXml)
		pnjXml.appendChild(idXml)
		pnjXml.appendChild(shipXml)
				
		return pnjXml
		
	@staticmethod
	def getListOfPNJTemplate():
		query="SELECT star035_id FROM star035_npc_template"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result