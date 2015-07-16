import os, sys
import xml.dom.minidom
from item import *

class mineral(ShimstarItem):
	def __init__(self,id,template=0):
		self.id=id
		self.name=""
		self.template=template
		self.mission=0
		self.container=0
		self.location=0
		self.containertype=0
		self.typeItem=C_ITEM_MINERAL
		if self.id!=0:
			self.loadFromBdd()
		else:
			self.loadFromTemplate()
			self.id=0
				
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		itemXml=docXml.createElement("mineral")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		templateXml=docXml.createElement("id")
		templateXml.appendChild(docXml.createTextNode(str(self.template)))
		imgXml=docXml.createElement("img")
		imgXml.appendChild(docXml.createTextNode(str(self.img)))
		spaceXml=docXml.createElement("space")
		spaceXml.appendChild(docXml.createTextNode(str(self.space)))
		itemXml.appendChild(templateXml)
		itemXml.appendChild(nameXml)
		itemXml.appendChild(imgXml)
		itemXml.appendChild(spaceXml)
		return itemXml
		
	def getId(self):
		return self.id
		
	@staticmethod	
	def getListMineral():
		query="SELECT STAR004_id FROM star004_item_template"
		query+=" WHERE star004_type_star003 = 11"
		print query
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
		if self.id==0:
			query="INSERT INTO STAR006_ITEM (star006_template_star004,star006_container_starnnn,star006_containertype,star006_location,star006_id_star036) "
			query+=" values ('" + str(self.template) + "','"+str(self.container)+"','"+self.containertype+"','"+ str(self.location)+"','" + str(self.mission) +"')"
		else:
			query="UPDATE STAR006_ITEM SET star006_container_starnnn='"+ str(self.container)+ "', star006_containertype='"+ self.containertype+"', star006_location='" + str(self.location)+ "'"
			query+=", star006_id_star036='" + str(self.mission) + "'"
			query+= " WHERE STAR006_ID ='"+str(self.id)+"'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		if self.id==0:
			self.id=int(cursor.lastrowid)
		cursor.close()
		
		instanceDbConnector.commit()
		
	def loadFromTemplate(self):
		query="SELECT star004_name, star004_energy, star004_mass,star004_space, "
		query+=" star004_sell,star004_cost,star004_img"
		query+=" FROM star004_item_template IT join star054_mineral m on m.star054_id = IT.star004_specific_starxxx"
		query+=" WHERE star004_id = '" +str(self.template) + "'"
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
		cursor.close()
	
	def loadFromBdd(self):
		query="SELECT star004_name, star004_energy, star004_mass,star004_space, "
		query+=" star004_sell,star004_cost,star004_img,star006_location, star006_template_star004,star006_container_starnnn,star006_containertype "
		query+=" FROM star006_item I Join  star004_item_template IT on I.star006_template_star004=star004_id join star054_mineral m on m.star054_id = IT.star004_specific_starxxx"
		query+="WHERE I.star006_id = '" +str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()

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
		
		cursor.close()
				
	