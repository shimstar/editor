from dbconnector import *
from item import *
from slot import *
import xml.dom.minidom


class Ship(ShimstarItem):
	className="ship"
	def __init__(self,id=0,template=0,new=False):
		#~ print "ship::init " + str(id) + "/" + str(template)
		super(Ship,self).__init__(id,template)	
		
		self.slots=[]
		#~ self.template=template
		self.itemInInventory=[]
		self.engine=None
		self.owner=None
		self.torque=0
		self.frictionAngular=0
		self.frictionVelocity=0
		self.weapon=None
		self.state=0
		self.maxhullpoints=0
		self.hullpoints=0
		self.egg=""
		self.poussee=0
		self.name=""
		if new==False:
			if self.templateId==0:
				self.loadFromBdd()
			else:
				super(Ship,self).loadFromTemplate()	
				self.loadFromTemplate()
			
				
	def addSlot(self,s):
		self.slots.append(s)
		
	def removeSlot(self,s):
		self.slots.remove(s)
		
				
	def getEgg(self):
		return self.egg
		
	def setEgg(self,e):
		self.egg=e
		
	def getHull(self):
		return self.maxhullpoints
		
	def setHull(self,h):
		self.maxhullpoints=h
		
	def setMasse(self,m):
		self.mass=m
		
	def getMasse(self):
		return self.mass
		
	def getImg(self):
		return self.img

	def setImg(self,i):
		self.img=i
		
	def getTorque(self):
		return self.torque
		
	def setTorque(self,t):
		self.torque=t
		
	def getFrictionAngular(self):
		return self.frictionAngular
		
	def setFrictionAngular(self,f):
		self.frictionAngular=f
		
	def getFrictionVelocity(self):
		return self.frictionVelocity
		
	def setFrictionVelocity(self,f):
		self.frictionVelocity=f
				
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
		hullpointsXml=docXml.createElement("hullpoints")
		hullpointsXml.appendChild(docXml.createTextNode(str(self.hullpoints)))
		maxhullpointsXml=docXml.createElement("maxhullpoints")
		maxhullpointsXml.appendChild(docXml.createTextNode(str(self.maxhullpoints)))
		eggXml=docXml.createElement("egg")
		eggXml.appendChild(docXml.createTextNode(self.egg))
		imgXml=docXml.createElement("img")
		imgXml.appendChild(docXml.createTextNode(self.img))
		itemXml.appendChild(tplXml)
		itemXml.appendChild(typeitemXml)
		itemXml.appendChild(nameXml)
		itemXml.appendChild(maxhullpointsXml)
		itemXml.appendChild(hullpointsXml)
		itemXml.appendChild(eggXml)
		itemXml.appendChild(imgXml)
		if len(self.slots)>0:
			slotsXml=docXml.createElement("slots")
			for s in self.slots:
				slotXml=s.getXml(docXml)
				slotsXml.appendChild(slotXml)
			itemXml.appendChild(slotsXml)
			
		if len(self.itemInInventory)>0:
			invXml=docXml.createElement("inventory")
			for i in self.itemInInventory:
				itemXml=docXml.createElement("invitem")
				idXml=docXml.createElement("iditem")
				idXml.appendChild(docXml.createTextNode(str(i.getId())))
				typeitemXml=docXml.createElement("typeitem")
				typeitemXml.appendChild(docXml.createTextNode(str(i.getTypeItem())))
				templateXml=docXml.createElement("template")
				templateXml.appendChild(docXml.createTextNode(str(i.getTemplate())))
				if i.getTypeItem()==C_ITEM_MINERAL:
					qtyXml=docXml.createElement("quantity")
					qtyXml.appendChild(docXml.createTextNode(str(i.getNb())))
					itemXml.appendChild(qtyXml)
				itemXml.appendChild(idXml)
				itemXml.appendChild(typeitemXml)
				itemXml.appendChild(templateXml)
				invXml.appendChild(itemXml)
			itemXml.appendChild(invXml)
		return itemXml
		
	def loadFromTemplate(self):
		"""
			Load a ship from a template (the id of the template is given in the constructor)
		"""
		#~ print "ship::loadFromTemplate"
		instanceDbConnector=shimDbConnector.getInstance()
		query="SELECT star005_egg,star005_hull,star005_mass, star004_name"
		query+=",star005_friction_angular,star005_friction_velocity,star005_torque,star004_id"
		query+=",star005_id,star004_type_star003"
		query+=" FROM STAR005_SHIP_TEMPLATE join star004_item_template on star005_id=star004_specific_starxxx"
		query+=" WHERE STAR004_id ='" + str(self.templateId) + "'"
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		#~ print query
		result_set = cursor.fetchall ()
		for row in result_set:
			self.maxhullpoints=int(row[1])
			self.egg=row[0]
			self.fitted=1
			self.mass=float(row[2])
			self.typeItem=int(row[9])
			self.hullpoints=int(row[1])
			self.frictionAngular=float(row[4])
			self.frictionVelocity=float(row[5])
			self.torque=int(row[6])
			self.name=str(row[3])
			self.itemTemplateId=int(row[8])
		cursor.close()
		
		cursor=instanceDbConnector.getConnection().cursor()
		query="SELECT star009_id FROM star009_slot WHERE star009_ship_star005='" + str(self.itemTemplateId) + "'"

		cursor.execute(query)
		result_set = cursor.fetchall ()
		self.slots=[]
		for row in result_set:
			tempSlot=Slot(0,row[0])
			self.slots.append(tempSlot)
			if tempSlot.getItem()!=None and tempSlot.getItem().getTypeItem()==C_ITEM_ENGINE:
				self.engine=tempSlot.getItem()
			if tempSlot.getItem()!=None and tempSlot.getItem().getTypeItem()==C_ITEM_WEAPON:
				self.weapon=tempSlot.getItem()
		cursor.close()
		
	def getSlots(self):
		return self.slots
	
			
	def saveToBDD(self):
		if self.templateId>0:
			query="update star004_item_template"
			query+=" set star004_name='" + self.name + "', star004_img='" + self.img +"', star004_type_star003 ='"+ str(self.typeItem)+"'"
			query+=" WHERE star004_id='" + str(self.id)+ "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			query="update star005_ship_template"
			query+=" set star005_egg = '" + str(self.egg)+"'"
			query+= ", star005_hull = " + str(self.maxhullpoints)
			query+=",star005_mass="+str(self.mass)
			query+=",star005_torque=" + str(self.torque)
			query+=",star005_friction_angular="+str(self.frictionAngular)
			query+=",star005_friction_velocity="+str(self.frictionVelocity)
			query+=" where star005_id = " + str(self.templateId) 
			#~ print query
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
			instanceDbConnector.commit()
		else:
			query="insert into star005_ship_template "
			query+=" (star005_egg, star005_hull,star005_mass,star005_torque,star005_friction_angular,star005_friction_velocity) values "
			query+="('" + str(self.egg) + "','" + str(self.maxhullpoints) + "','" + str(self.mass) + "','" + str(self.torque) + "','" + str(self.frictionAngular) + "','" + str(self.frictionVelocity) + "')"
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
		