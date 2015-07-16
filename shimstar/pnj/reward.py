from dbconnector import *
import xml.dom.minidom

class Reward:
	def __init__(self,id):
		self.id=id
		self.typeReward=0
		self.templateItem=0
		self.nb=0
		self.loadFromBDD()
		
	def loadFromBDD(self):
		query="SELECT star042_typerewards_star043, star042_itemtemplate_star004, star042_nb"
		query+=" FROM star042_rewards_mission where star042_id=" + str(self.id)

		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.typeReward=int(row[0])
			self.templateItem=int(row[1])
			self.nb=int(row[2])
		cursor.close()
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		rewardXml=docXml.createElement("reward")
		idXml=docXml.createElement("idreward")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		typeXml=docXml.createElement("typereward")
		typeXml.appendChild(docXml.createTextNode(str(self.typeReward)))
		templateXml=docXml.createElement("templateitem")
		templateXml.appendChild(docXml.createTextNode(str(self.templateItem)))
		nbXml=docXml.createElement("nb")
		nbXml.appendChild(docXml.createTextNode(str(self.nb)))
		
		rewardXml.appendChild(idXml)
		rewardXml.appendChild(typeXml)
		rewardXml.appendChild(templateXml)
		rewardXml.appendChild(nbXml)
		
		return rewardXml
		
	def getId(self):
		return self.id
		
	def getTypeReward(self):
		return self.typeReward
		
	def getTemplateItem(self):
		return self.templateItem
		
	def getNb(self):
		return self.nb
		
