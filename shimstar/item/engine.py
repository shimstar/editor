from dbconnector import *
from item import *
import xml.dom.minidom

class engine(ShimstarItem):
	def __init__(self,id,idTemplate=0,new=False):
		super(engine,self).__init__(id,idTemplate)	
		print "engine::init " + str(id) + "/" + str(idTemplate)
		self.id=id
		self.label=""
		self.templateId=idTemplate
		self.location=0
		self.name=""
		self.speedMax=0
		self.acceleration=0
		self.cost=0
		self.sell=0
		self.energyCost=0
		self.space=0
		self.img=""
		self.typeItem=0
		self.itemTemplateId=0
		
		if new==False:
			if self.templateId==0:
				self.loadFromBdd()
			else:
				self.loadFromTemplate()
		
	def getSpeedMax(self):
		return self.speedMax
		
	def setSpeedMax(self,s):
		self.speedMax=s
		
	def getAcceleration(self):
		return self.acceleration
		
	def setAcceleration(self,a):
		self.acceleration=a
	
	def loadFromTemplate(self):
		query="SELECT star017_acceleration,star017_speed,star004_name, star004_energy, star004_mass,star004_space,star004_sell,star004_cost,star004_img,star004_type_star003,star004_id"
		query+=", star017_sound"
		query+=" FROM star004_item_template IT"
		query+=" join star017_engine w on w.star017_id = IT.star004_specific_starxxx "
		#~ query+=" WHERE w.star017_id ='" + str(self.templateId) + "' and star004_id='" + str(self.id) + "'"
		query+=" WHERE star004_id='" + str(self.templateId) + "'"
		#~ print "Engine::loadFromTemplate " + query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[2]
			self.speedMax=int(row[1])
			self.acceleration=int(row[0])
			self.cost=int(row[7])
			self.sell=int(row[6])
			self.energyCost=int(row[3])
			self.space=int(row[5])
			self.img=row[8]
			self.typeItem=row[9]
			self.itemTemplateId=int(row[10])
			#~ self.templateId=int(row[10])
			self.sound=str(row[11])
			#~ self.location=row[9]
		cursor.close()
		self.loadSkill()
		#~ super(engine,self).loadFromTemplate()	
			
	def loadFromBdd(self):
		query="SELECT star017_acceleration,star017_speed, star004_name, star004_energy, star004_mass,star004_space,star004_sell,star004_cost,star004_img"
		query+=",star004_type_star003,star006_location,star004_id "
		query+=", star017_sound"
		query+=" FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id "
		query+=" join star017_engine w on w.star017_id = IT.star004_specific_starxxx "
		query+="WHERE I.star006_id = '" +str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		#~ print "Engine::loadFromBdd" + query
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[2]
			self.speedMax=int(row[1])
			self.acceleration=int(row[0])
			self.cost=int(row[7])
			self.sell=int(row[6])
			self.energyCost=int(row[3])
			self.space=int(row[5])
			self.img=row[8]
			self.location=row[10]
			self.typeItem=row[9]
			self.itemTemplateId=int(row[10])
			self.templateId=int(row[10])
			self.sound=str(row[11])
		cursor.close()
		self.loadSkill()
		
	def getSpecificXml(self,docXml,itemXml):
		speedXml=docXml.createElement("speedMax")
		speedXml.appendChild(docXml.createTextNode(str(self.speedMax)))
		accelerationXml=docXml.createElement("acceleration")
		accelerationXml.appendChild(docXml.createTextNode(str(self.acceleration)))
		soundXml=docXml.createElement("sound")
		soundXml.appendChild(docXml.createTextNode(str(self.sound)))
		
		itemXml.append(speedXml)
		itemXml.append(accelerationXml)
		itemXml.append(soundXml)
		
	def getXml(self,docXml=None):		
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		itemXml=docXml.createElement("item")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		tplXml=docXml.createElement("templateid")
		tplXml.appendChild(docXml.createTextNode(str(self.templateId)))
		typeitemXml=docXml.createElement("typeitem")
		typeitemXml.appendChild(docXml.createTextNode(str(self.typeItem)))
		speedXml=docXml.createElement("speedMax")
		speedXml.appendChild(docXml.createTextNode(str(self.speedMax)))
		accelerationXml=docXml.createElement("acceleration")
		accelerationXml.appendChild(docXml.createTextNode(str(self.acceleration)))
		costXml=docXml.createElement("cost")
		costXml.appendChild(docXml.createTextNode(str(self.cost)))
		sellXml=docXml.createElement("sell")
		sellXml.appendChild(docXml.createTextNode(str(self.sell)))
		energyXml=docXml.createElement("energyCost")
		energyXml.appendChild(docXml.createTextNode(str(self.energyCost)))
		spaceXml=docXml.createElement("space")
		spaceXml.appendChild(docXml.createTextNode(str(self.space)))
		imgXml=docXml.createElement("img")
		imgXml.appendChild(docXml.createTextNode(str(self.img)))
		locationXml=docXml.createElement("location")
		locationXml.appendChild(docXml.createTextNode(str(self.location)))
		soundXml=docXml.createElement("sound")
		soundXml.appendChild(docXml.createTextNode(str(self.sound)))
		
		itemXml.appendChild(nameXml)
		itemXml.appendChild(tplXml)
		itemXml.appendChild(typeitemXml)
		itemXml.appendChild(speedXml)
		itemXml.appendChild(accelerationXml)
		itemXml.appendChild(sellXml)
		itemXml.appendChild(energyXml)
		itemXml.appendChild(spaceXml)
		itemXml.appendChild(imgXml)
		itemXml.appendChild(locationXml)
		itemXml.appendChild(costXml)
		itemXml.appendChild(soundXml)
		#~ print "engine::getXml" + itemXml.toxml()
		return itemXml
		
	@staticmethod	
	def getListEngine():
		query="SELECT STAR006_id FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id"
		query+=" WHERE star004_type_star003 = 1"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result
		
	def saveToBDD(self):
		if self.templateId>0:
			query="update star004_item_template"
			query+=" set star004_name='" + self.name + "', star004_img='" + self.img +"', star004_type_star003 ='"+ str(self.typeItem)+"'"
			query+=" WHERE star004_id='" + str(self.id)+ "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			query="update star017_engine"
			query+=" set star017_acceleration = " + str(self.acceleration) + ", star017_speed = " + str(self.speedMax)
			query+=" where star017_id = " + str(self.templateId) 
			#~ print query
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			instanceDbConnector.commit()
		else:
			query="insert into star017_engine "
			query+=" (star017_acceleration, star017_speed) values ('" + str(self.acceleration) + "','" + str(self.speedMax) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			id=int(cursor.lastrowid)
			cursor.close()
			
			query="insert into star004_item_template"
			query+=" (star004_name,star004_img,star004_type_star003,star004_specific_starxxx) values"
			query+=" ('" + str(self.name) + "','" + str(self.img) + "','" + str(self.typeItem) + "','" + str(id) +"')"
			#~ print query
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			instanceDbConnector.commit()
		
	def delete(self):
		#~ print "engine::delete"
		query="delete from star004_item_template where star004_id = " + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		
		query="delete from star017_engine where star017_id = " + str(self.templateId)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		
		instanceDbConnector.commit()
		
	
	