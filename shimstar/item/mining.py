from dbconnector import *
from item import *
import xml.dom.minidom

class miningItem(ShimstarItem):
	def __init__(self,id,idTemplate=0):
		super(miningItem,self).__init__(id,idTemplate)	
		super(miningItem,self).loadFromTemplate()	
		self.id=id
		self.label=""
		self.templateId=idTemplate
		self.location=0
		self.minerals=[]
		self.typeItem=C_ITEM_MINING
		self.tabSkill={'titi':'toto'}
		self.tabSkill.clear()
		self.minerals=[]
		if self.templateId==0:
			self.loadFromBdd()
		else:
			self.loadFromTemplate()
			
	def loadMineralToMine(self):
		query="SELECT star056_idmineral_star055"
		query+=" FROM star056_miningitem_mineral where star056_idmining_star054='" + str(self.templateId) + "'"
		instanceDbConnector=shimDbConnector.getInstance()

		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		self.minerals=[]
		for row in result_set:
			self.minerals.append(row[0])
			
		cursor.close()
			
	def loadFromTemplate(self):
		query="SELECT star004_name, star004_energy, star004_mass,star004_space, "
		query+=" star004_sell,star004_cost,star004_img"
		query+=",star055_vitesse,star055_perf,star055_nb,star055_range"
		query+=" FROM star004_item_template IT join star055_mining_item m on m.star055_id = IT.star004_specific_starxxx"
		query+=" WHERE IT.star004_id = '" +str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		#~ print query
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=row[0]
			self.space=int(row[3])
			self.mass=float(row[2])
			self.energy=int(row[1])
			self.cost=int(row[5])
			self.sell=int(row[4])
			self.img=row[6]
			self.vitesse=float(row[7])
			self.perf=float(row[8])
			self.nb=int(row[9])
			self.range=int(row[10])
			self.templateId=self.id
		cursor.close()
		self.loadMineralToMine()
	
	def loadFromBdd(self):
		query="SELECT star004_name, star004_energy, star004_mass,star004_space, "
		query+=" star004_sell,star004_cost,star004_img,star006_location, star006_template_star004,star006_container_starnnn,star006_containertype "
		query+=",star055_vitesse,star055_perf,star055_nb,star055_range"
		query+=" FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id join star055_mining_item m on m.star055_id = IT.star004_specific_starxxx "
		query+="WHERE I.star006_id = '" +str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		print query
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=row[0]
			self.space=int(row[3])
			self.mass=float(row[2])
			self.energy=int(row[1])
			self.cost=int(row[5])
			self.sell=int(row[4])
			self.img=row[6]
			self.location=int(row[7])
			self.template=int(row[8])
			self.container=row[9]
			self.containertype=row[10]
			self.vitesse=float(row[11])
			self.perf=float(row[12])
			self.nb=int(row[13])
			self.range=int(row[14])
		
		cursor.close()
		self.loadMineralToMine()
		
	def getSpecificXml(self,docXml,itemXml):
		vitesseXml=docXml.createElement("vitesse")
		vitesseXml.appendChild(docXml.createTextNode(str(self.vitesse)))
		nbXml=docXml.createElement("nbextract")
		nbXml.appendChild(docXml.createTextNode(str(self.nb)))
		perfXml=docXml.createElement("perf")
		perfXml.appendChild(docXml.createTextNode(str(self.perf)))
		rangeXml=docXml.createElement("range")
		rangeXml.appendChild(docXml.createTextNode(str(self.range)))
		itemXml.append(vitesseXml)
		itemXml.append(nbXml)
		itemXml.append(perfXml)
		itemXml.append(rangeXml)
		
		return itemXml
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		itemXml=docXml.createElement("item")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		typeitemXml=docXml.createElement("typeitem")
		typeitemXml.appendChild(docXml.createTextNode(str(self.typeItem)))
		tplXml=docXml.createElement("templateid")
		tplXml.appendChild(docXml.createTextNode(str(self.templateId)))
		vitesseXml=docXml.createElement("vitesse")
		vitesseXml.appendChild(docXml.createTextNode(str(self.vitesse)))
		nbXml=docXml.createElement("nbextract")
		nbXml.appendChild(docXml.createTextNode(str(self.nb)))
		perfXml=docXml.createElement("perf")
		perfXml.appendChild(docXml.createTextNode(str(self.perf)))
		rangeXml=docXml.createElement("range")
		rangeXml.appendChild(docXml.createTextNode(str(self.range)))
		costXml=docXml.createElement("cost")
		costXml.appendChild(docXml.createTextNode(str(self.cost)))
		sellXml=docXml.createElement("sell")
		sellXml.appendChild(docXml.createTextNode(str(self.sell)))
		energyXml=docXml.createElement("energyCost")
		energyXml.appendChild(docXml.createTextNode(str(self.energy)))
		spaceXml=docXml.createElement("space")
		spaceXml.appendChild(docXml.createTextNode(str(self.space)))
		imgXml=docXml.createElement("img")
		imgXml.appendChild(docXml.createTextNode(str(self.img)))
		locationXml=docXml.createElement("location")
		locationXml.appendChild(docXml.createTextNode(str(self.location)))
		
		
		if len(self.minerals)>0:
			mineralsXml=docXml.createElement("mineralstomine")
			for m in self.minerals:
				mineralXml=docXml.createElement("mineraltomine")
				mineralXml.appendChild(docXml.createTextNode(str(m)))		
				mineralsXml.appendChild(mineralXml)
			itemXml.appendChild(mineralsXml)
		
		if len(self.tabSkill)>0:
			skillItemsXml=docXml.createElement("skillsitem")
			for s in self.tabSkill:
				skillItemXml=docXml.createElement("skillitem")
				skillIdXml=docXml.createElement("skillid")
				skillIdXml.appendChild(docXml.createTextNode(str(s)))		
				skillLvlXml=docXml.createElement("skilllevel")
				skillLvlXml.appendChild(docXml.createTextNode(str(self.tabSkill[s])))		
				skillItemXml.appendChild(skillIdXml)
				skillItemXml.appendChild(skillLvlXml)
				skillItemsXml.appendChild(skillItemXml)
			itemXml.appendChild(skillItemsXml)
		
		itemXml.appendChild(nameXml)
		itemXml.appendChild(tplXml)
		itemXml.appendChild(typeitemXml)
		itemXml.appendChild(vitesseXml)
		itemXml.appendChild(nbXml)
		itemXml.appendChild(perfXml)
		itemXml.appendChild(rangeXml)
		itemXml.appendChild(sellXml)
		itemXml.appendChild(energyXml)
		itemXml.appendChild(spaceXml)
		itemXml.appendChild(imgXml)
		itemXml.appendChild(locationXml)
		itemXml.appendChild(costXml)
		
		print itemXml.toxml()
		return itemXml
		
	@staticmethod	
	def getListMining():
		query="SELECT STAR006_id FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id"
		query+=" WHERE star004_type_star003 = 10"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result
		
