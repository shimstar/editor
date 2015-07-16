from dbconnector import *
from item import *
import xml.dom.minidom

class Weapon(ShimstarItem):
	def __init__(self,id,idTemplate=0,new=False):
		#~ print "weapon :: init" + str(id) + "/" + str(idTemplate)
		super(Weapon,self).__init__(id,idTemplate)	
		
		self.id=id
		self.label=""
		self.templateId=idTemplate
		self.location=0
		self.typeItem=0
		if new==False:
			if self.templateId==0:
				self.loadFromBdd()
			else:
				self.loadFromTemplate()
			
	def getDamage(self):
		return self.damage

	def setDamage(self,d):
		self.damage=d
			
	def getRange(self):
		return self.range
		
	def setRange(self,r):
		self.range=r
		
	def getCadence(self):
		return self.cadence
		
	def setCadence(self,c):
		self.cadence=c
		
	def getSpeed(self):
		return self.speed
		
	def setSpeed(self,s):
		self.speed=s
		
	def getEgg(self):
		return self.egg
		
	def setEgg(self,e):
		self.egg=e
			
	def loadFromTemplate(self):
		query="SELECT star018_damage,star018_range,star018_egg,star018_cadence,star018_speed, "
		query+=" star004_name, star004_energy, star004_mass,star004_space,star004_sell,star004_cost,star004_img,star004_type_star003,star004_id"
		query+=" ,star018_weapon_sound,star018_bullet_sound"
		query+=" FROM star004_item_template IT"
		query+=" join star018_weapon w on w.star018_id = IT.star004_specific_starxxx "
		query+="WHERE star018_id = '" +str(self.templateId) + "' and star004_id='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.damage=row[0]
			self.range=row[1]
			self.egg=row[2]
			self.cadence=row[3]
			self.speed=row[4]
			self.name=row[5]
			self.energyCost=int(row[6])
			self.mass=float(row[7])
			self.space=int(row[8])
			self.sell=int(row[9])
			self.cost=int(row[10])
			self.img=row[11]
			self.typeItem=row[12]
			self.itemTemplateId=int(row[13])
			#~ self.templateId=int(row[13])
			self.weaponSound=str(row[14])
			self.bulletSound=str(row[15])
			#~ self.location=row[12]
		cursor.close()
		self.loadSkill()
		super(Weapon,self).loadFromTemplate()	
			
	def loadFromBdd(self):
		query="SELECT star018_damage,star018_range,star018_egg,star018_cadence,star018_speed, "
		query+=" star004_name, star004_energy, star004_mass,star004_space,star004_sell,star004_cost,star004_img,star006_location,star004_type_star003,star004_id "
		query+=" ,star018_weapon_sound,star018_bullet_sound"
		query+=" FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id "
		query+=" join star018_weapon w on w.star018_id = IT.star004_specific_starxxx "
		query+="WHERE I.star006_id = '" +str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.damage=row[0]
			self.range=row[1]
			self.egg=row[2]
			self.cadence=row[3]
			self.speed=row[4]
			self.name=row[5]
			self.energyCost=int(row[6])
			self.mass=float(row[7])
			self.space=int(row[8])
			self.sell=int(row[9])
			self.cost=int(row[10])
			self.img=row[11]
			self.location=row[12]
			self.typeItem=row[13]
			self.itemTemplateId=int(row[14])
			self.templateId=int(row[14])
			self.weaponSound=str(row[15])
			self.bulletSound=str(row[16])
		cursor.close()
		self.loadSkill()
		
	def getSpecificXml(self,docXml,itemXml):
		damageXml=docXml.createElement("damage")
		damageXml.appendChild(docXml.createTextNode(str(self.damage)))
		rangeXml=docXml.createElement("range")
		rangeXml.appendChild(docXml.createTextNode(str(self.range)))
		eggXml=docXml.createElement("egg")
		eggXml.appendChild(docXml.createTextNode(str(self.egg)))
		cadenceXml=docXml.createElement("cadence")
		cadenceXml.appendChild(docXml.createTextNode(str(self.cadence)))
		speedXml=docXml.createElement("speed")
		speedXml.appendChild(docXml.createTextNode(str(self.speed)))
		weaponsoundXml=docXml.createElement("weaponsound")
		weaponsoundXml.appendChild(docXml.createTextNode(str(self.weaponSound)))
		bulletsoundXml=docXml.createElement("bulletsound")
		bulletsoundXml.appendChild(docXml.createTextNode(str(self.bulletSound)))
		itemXml.append(damageXml)
		itemXml.append(rangeXml)
		temXml.append(eggXml)
		itemXml.append(cadenceXml)
		itemXml.append(speedXml)
		itemXml.append(weaponsoundXml)
		itemXml.append(bulletsoundXml)
		
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
		tplXml.appendChild(docXml.createTextNode(str(self.itemTemplateId)))
		damageXml=docXml.createElement("damage")
		damageXml.appendChild(docXml.createTextNode(str(self.damage)))
		rangeXml=docXml.createElement("range")
		rangeXml.appendChild(docXml.createTextNode(str(self.range)))
		eggXml=docXml.createElement("egg")
		eggXml.appendChild(docXml.createTextNode(str(self.egg)))
		cadenceXml=docXml.createElement("cadence")
		cadenceXml.appendChild(docXml.createTextNode(str(self.cadence)))
		speedXml=docXml.createElement("speed")
		speedXml.appendChild(docXml.createTextNode(str(self.speed)))
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
		weaponsoundXml=docXml.createElement("weaponsound")
		weaponsoundXml.appendChild(docXml.createTextNode(str(self.weaponSound)))
		bulletsoundXml=docXml.createElement("bulletsound")
		bulletsoundXml.appendChild(docXml.createTextNode(str(self.bulletSound)))
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
		itemXml.appendChild(damageXml)
		itemXml.appendChild(rangeXml)
		itemXml.appendChild(eggXml)
		itemXml.appendChild(cadenceXml)
		itemXml.appendChild(speedXml)
		itemXml.appendChild(sellXml)
		itemXml.appendChild(energyXml)
		itemXml.appendChild(spaceXml)
		itemXml.appendChild(imgXml)
		itemXml.appendChild(locationXml)
		itemXml.appendChild(costXml)
		itemXml.appendChild(bulletsoundXml)
		itemXml.appendChild(weaponsoundXml)
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
			#~ print query
			query="update star018_weapon"
			query+=" set star018_damage='" + self.damage+ "', star018_range='" + self.range +"', star018_egg='"+ str(self.egg)+"'"
			query+=", star018_speed='" + str(self.speed) + "',star018_cadence='" + str(self.cadence) + "'"
			query+=" WHERE star018_id='" + str(self.templateId)+ "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			instanceDbConnector.commit()
		else:
			query="insert into star018_weapon"
			query+=" (star018_damage,star018_range,star018_egg,star018_cadence,star018_speed)"
			query+=" values('" + str(self.damage)+"','" + str(self.range) + "','" + str(self.egg) + "','" + str(self.cadence) + "','" + str(self.speed)+"')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			id=int(cursor.lastrowid)
			cursor.close()
			#~ print query
			query="insert into star004_item_template"
			query+=" (star004_name,star004_img,star004_type_star003,star004_specific_starxxx) values"
			query+=" ('" + str(self.name) + "','" + str(self.img) + "','" + str(self.typeItem) + "','" + str(id) +"')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			instanceDbConnector.commit()
			
	def delete(self):
		#~ print "weapon::delete"
		query="delete from star004_item_template where star004_id = " + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		
		query="delete from star018_weapon where star018_id = " + str(self.templateId)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		
		instanceDbConnector.commit()