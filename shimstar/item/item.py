from dbconnector import *
import xml.dom.minidom
from constantes import *

class ShimstarItem(object):
	def __init__(self,id,idTemplate,new=False):
		#~ print "shimstaritem::init " + str(id) + "/" +str(idTemplate)
		self.container=0
		self.owner=0
		self.typeItem=0
		self.typeItemLabel=""
		self.name=""
		self.template=0
		self.energy=0
		self.owner=0
		self.img=""
		self.cost=0
		self.sell=0
		self.location=0
		self.place=0
		self.space=0
		self.id=id
		self.itemTemplateId=idTemplate
		self.templateId=idTemplate
		self.container=0
		self.templateLabel=""
		self.typeContainer=""
		self.tabSkill=[]

		if new==False:
			if self.id>0:
				self.loadFromBdd()
			else:
				self.loadFromTemplate()
				
	def getTemplate(self):
		return self.templateId
				
	
	@staticmethod
	def getListOfInstanciedObject(id):
		query = "SELECT star006_id FROM star006_item WHERE star006_template_star004 = " + str(id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfItem=[]
		for row in result_set:			
			listOfItem.append(int(row[0]))
		return listOfItem
				
	@staticmethod
	def getListOfItemTemplates():
		query="SELECT star004_id from star004_item_template "
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfItemTemplates=[]
		for row in result_set:			
			listOfItemTemplates.append(int(row[0]))
		return listOfItemTemplates
			
	@staticmethod
	def getListOfItemTemplatesByType(listOfType):
		listOfTypeForQuery=""
		for l in listOfType:
			if listOfTypeForQuery!="":
				listOfTypeForQuery+=","
			listOfTypeForQuery+="'" + str(l) + "'"
		query="SELECT star004_id from star004_item_template where star004_type_star003 in (" + listOfTypeForQuery + ")"
		query+=" order by star004_type_star003, star004_name"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfItemTemplates=[]
		for row in result_set:			
			listOfItemTemplates.append(int(row[0]))
		return listOfItemTemplates
				
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		
		itemXml=docXml.createElement("item")
		templateLabelXml=docXml.createElement("templateLabel")
		templateLabelXml.appendChild(docXml.createTextNode(str(self.templateLabel)))
		tplXml=docXml.createElement("templateid")
		tplXml.appendChild(docXml.createTextNode(str(self.itemTemplateId)))
		typeitemXml=docXml.createElement("typeitem")
		typeitemXml.appendChild(docXml.createTextNode(str(self.typeItem)))
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		energyXml=docXml.createElement("energyCost")
		energyXml.appendChild(docXml.createTextNode(str(self.energy)))
		costXml=docXml.createElement("cost")
		costXml.appendChild(docXml.createTextNode(str(self.cost)))
		sellXml=docXml.createElement("sell")
		sellXml.appendChild(docXml.createTextNode(str(self.sell)))
		spaceXml=docXml.createElement("space")
		spaceXml.appendChild(docXml.createTextNode(str(self.space)))
		massXml=docXml.createElement("mass")
		massXml.appendChild(docXml.createTextNode(str(self.mass)))
		locationXml=docXml.createElement("location")
		locationXml.appendChild(docXml.createTextNode(str(self.location)))
		imgXml=docXml.createElement("img")
		imgXml.appendChild(docXml.createTextNode(str(self.img)))
		typeItemXml=docXml.createElement("typeItem")
		typeItemXml.appendChild(docXml.createTextNode(str(self.typeItem)))		
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
		
		itemXml.appendChild(templateLabelXml)
		itemXml.appendChild(tplXml)
		itemXml.appendChild(nameXml)
		itemXml.appendChild(typeitemXml)
		itemXml.appendChild(energyXml)
		itemXml.appendChild(costXml)
		itemXml.appendChild(sellXml)
		itemXml.appendChild(spaceXml)
		itemXml.appendChild(locationXml)
		itemXml.appendChild(massXml)
		itemXml.appendChild(imgXml)
		itemXml.appendChild(typeItemXml)
		#~ if typeItem==C_ITEM_ENGINE:
			#~ eng=engine(0,self.specific)
		#~ elif typeItem==C_ITEM_WEAPON:
			#~ pass
				
		return itemXml
		
	def getTypeItem(self):
		return self.typeItem
		
	def getSpecific(self):
		return self.specific
		
	def getTypeItemLabel(self):
		return self.typeItemLabel
	
	def loadFromTemplate(self):
		instanceDbConnector=shimDbConnector.getInstance()
		query="SELECT star003_label,star004_name, star004_energy,star004_cost,star004_sell,star004_space,star004_mass,star004_img,star003_id"
		query+=", star004_specific_starxxx,star004_id, star003_label"
		query+=" FROM  star004_item_template inner join star003_typeitem on star003_id = star004_type_star003"
		query+=" WHERE star004_id='" + str(self.itemTemplateId) + "'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.templateLabel=row[0]
			self.name=row[1]
			self.energy=int(row[2])
			self.cost=int(row[3])
			self.sell=int(row[4])
			self.space=int(row[5])
			self.mass=int(row[6])
			self.img=row[7]
			self.typeItem=int(row[8])
			self.specific=int(row[9])
			self.itemTemplateId=int(row[10])
			self.typeItemLabel=str(row[11])
			
		cursor.close()
		
		#~ self.loadSkill()
		
	def loadFromBdd(self):
		query="SELECT star006_template_star004,star006_container_starnnn,star006_containertype,star006_owner_star001,star006_location "
		query+=" FROM  star006_item "
		query+=" WHERE star006_id = '" + str(self.id) + "'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.templateId=int(row[0])
			self.container=int(row[1])
			self.typeContainer=row[2]
			self.owner=int(row[3])
			self.location=int(row[4])
		cursor.close()
		
		self.loadFromTemplate()
		
	def loadSkill(self):
		query="SELECT star030_id,star053_level from star053_skill_item where star004_id = '" + str(self.templateId) + "'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		self.tabSkill={'tti':'tott'}
		self.tabSkill.clear()
		for row in result_set:
			self.tabSkill[int(row[0])]=int(row[1])
		cursor.close()
		
		
	def getOwner(self):
		return self.owner

	def saveInstance(self):
		if self.id==0:
			query="insert into star006_item"
			query+=" (star006_template_star004) values ('" + str(self.templateId) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
			instanceDbConnector.commit()
			print "@@@@@@@@" + str(self.id)
		else:
			query="update star006_item"
			query+=" set star006_container_starnnn='" + str(self.container) +"',star006_containertype='" + self.typeContainer +"'"
			query+=" where star006_id = '" + str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
			instanceDbConnector.commit()
		
	def saveToBDD(self):
		if self.templateId>0:
			query="update star004_item_template"
			query+=" set star004_name='" + self.name + "', star004_img='" + self.img +"', star004_type_star003 ='"+ str(self.typeItem)+"'"
			query+=" WHERE star004_id='" + str(self.templateId)+ "'"
			
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			instanceDbConnector.commit()
		else:
			query="insert into star004_item_template (star004_name,star004_img,star004_type_star003)"
			query+=" values ('"+self.name+"','"+self.img +"','"+ str(self.typeItem)+"')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
			instanceDbConnector.commit()
			
	def setContainer(self,id):
		self.container=id
		
	def getContainerType(self):
		return self.typeContainer
		
	def setContainerType(self,tc):
		self.typeContainer=tc
		
	def getContainer(self):
		return self.container
		
	def setOwner(self,id):
		self.owner=id
		
	def getId(self):
		return self.id
		
	def setId(self,id):
		self.id=id
		
	def getTypeLabel(self):
		return self.templateLabel
		
	def getTypeItem(self):
		return self.typeItem
		
	def setTypeItem(self,ti):
		self.typeItem=ti
		
	def setName(self,name):
		self.name=name
		
	def setImg(self,img):
		self.img=img
		
	def getPlace(self):
		return self.place
	
	def getLocation(self):
		return self.location
		
	def setPlace(self,place):
		self.place=place
		
	def setLocation(self,location):
		self.location=location
		
	def getName(self):
		return self.name
		
	def getImg(self):
		return self.img
		
	def getEnergy(self):
		return self.energy
		
	def getCost(self):
		return self.cost
		
	def getSell(self):
		return self.sell
	
