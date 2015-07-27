from dbconnector import *
import xml.dom.minidom

class Asteroid:
	def __init__(self,id,idTemplate=0):
		#~ print "Asteroid::init " + str(id)
		self.id=id
		self.idTemplate=idTemplate
		self.label=""
		self.posx=0
		self.posy=0
		self.posz=0
		self.scale = 0
		self.eggMiddle= ""
		self.eggFar = ""
		self.minerals={}
		if self.idTemplate>0:
			self.loadFromTemplate()
		else:
			self.loadFromBdd()
		
	def getPos(self):
		return self.posx,self.posy,self.posz
		
	def loadFromTemplate(self):
		query="SELECT star013_name, star013_egg, star013_mass, star013_text,star013_egg_midle,star013_egg_far"
		query+=" FROM STAR013_asteroid_template"
		query+=" WHERE star013_id='" + str(self.idTemplate) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[0]
			self.egg=row[1]
			self.mass=float(row[2])
			self.text=row[3]
			self.eggMiddle = row[4]
			self.eggFar = row[5]
		cursor.close()
		
		query="SELECT STAR058_idmineral_star004, star058_nb from star058_ast_mineral where star058_idast_star013 = '" + str(self.idTemplate) + "'"
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.minerals[int(row[0])]=int(row[1])
			
		#~ print self.minerals
		cursor.close()
	
	def loadFromBdd(self):
		#~ query="SELECT STAR013_name, STAR013_egg, STAR013_mass, STAR013_text FROM star013_asteroid_template"
		#~ query+=" WHERE STAR013_id = '" + self.id + "'"
		query="SELECT STAR014_posx, star014_posy, star014_posz, star014_hprh,star014_hprp,star014_hprr"
		query+=" ,star013_name, star013_egg, star013_mass, star013_text,STAR013_id, star014_scale,star013_egg_midle,star013_egg_far"
		query+=" FROM STAR014_asteroid JOIN star013_asteroid_template on STAR014_template_star013 = STAR013_id"
		query+=" WHERE STAR014_ID = '" + str(self.id)+ "'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.posx=float(row[0])
			self.posy=float(row[1])
			self.posz=float(row[2])
			self.hprh=float(row[3])
			self.hprp=float(row[4])
			self.hprr=float(row[5])
			self.name=row[6]
			self.egg=row[7]
			self.mass=float(row[8])
			self.text=row[9]
			self.idTemplate=int(row[10])
			self.scale=float(row[11])
			self.eggMiddle = row[12]
			self.eggFar = row[13]
		cursor.close()
		
		
		

	@staticmethod
	def getListOfAsteroid(zoneId):
		query="SELECT star014_id from star014_asteroid where star014_zone_star011 ='" + str(zoneId) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfAsteroid=[]
		for row in result_set:			
			listOfAsteroid.append(int(row[0]))
		return listOfAsteroid
		
	def deleteFromBDD(self):
		query="delete from star013_asteroid_template where star013_id = '" + str(self.idTemplate) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		instanceDbConnector.commit()
		
	def saveToBDD(self):
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		if self.idTemplate>0:
			query="Update star013_asteroid_template"
			query+=" set star013_name='" + str(self.name) + "'"
			query+=", star013_egg='" + str(self.egg) + "'"
			query+=", star013_mass='" + str(self.mass) + "'"
			query+=", star013_text='" + str(self.text) + "'"
			query+=" where star013_id = '" + str(self.idTemplate) + "'"
			cursor.execute(query)
			cursor.close()
			
		else:
			query="insert into star013_asteroid_template"
			query+=" (star013_name,star013_egg,star013_mass,star013_text)"
			query+=" values ('" + str(self.name) +"','" + str(self.egg) + "','" + str(self.mass) + "','" + str(self.text) +"')"
			cursor.execute(query)
			self.idTemplate=cursor.lastrowid
			cursor.close()
		instanceDbConnector.commit()
		return self.idTemplate
		
	@staticmethod
	def getListOfAsteroidTemplate():
		query="SELECT star013_id from star013_asteroid_template"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfAsteroid=[]
		for row in result_set:			
			listOfAsteroid.append(int(row[0]))
		return listOfAsteroid
			
	def getName(self):
		return self.name
		
	def getEgg(self):
		return self.egg
		
	def getMass(self):
		return self.mass
		
	def getText(self):
		return self.text
		
	def setName(self,name):
		self.name=name
		
	def setEgg(self,egg):
		self.egg=egg
		
	def setMass(self,mass):
		self.mass=mass
		
	def setText(self,text):
		self.text=text
		
	def getId(self):
		return self.id
		
	def getXmlTemplate(self,docXml=None):	
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		astXml=docXml.createElement("asteroidtemplate")
		idtemplateXml=docXml.createElement("idtemplate")
		idtemplateXml.appendChild(docXml.createTextNode(str(self.idTemplate)))
		eggXml=docXml.createElement("egg")
		eggXml.appendChild(docXml.createTextNode(str(self.egg)))
		eggMiddleXml=docXml.createElement("eggmiddle")
		eggMiddleXml.appendChild(docXml.createTextNode(str(self.eggMiddle)))
		eggFarXml=docXml.createElement("eggfar")
		eggFarXml.appendChild(docXml.createTextNode(str(self.eggFar)))
		massXml=docXml.createElement("mass")
		massXml.appendChild(docXml.createTextNode(str(self.mass)))
		textXml=docXml.createElement("text")
		textXml.appendChild(docXml.createTextNode(str(self.text)))
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		if len(self.minerals)>0:
			mineralsXml=docXml.createElement("minerals")
			for m in self.minerals:
				mineralXml=docXml.createElement("mineral")
				idmineralXml=docXml.createElement("idmineral")
				idmineralXml.appendChild(docXml.createTextNode(str(m)))
				nbmineralXml=docXml.createElement("nbmineral")
				nbmineralXml.appendChild(docXml.createTextNode(str(self.minerals[m])))
				mineralXml.appendChild(idmineralXml)
				mineralXml.appendChild(nbmineralXml)
				mineralsXml.appendChild(mineralXml)
			astXml.appendChild(mineralsXml)
		astXml.appendChild(nameXml)
		astXml.appendChild(eggXml)
		astXml.appendChild(eggMiddleXml)
		astXml.appendChild(eggFarXml)
		astXml.appendChild(idtemplateXml)
		astXml.appendChild(massXml)
		astXml.appendChild(textXml)
		# print astXml.toxml()
		return astXml
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		astXml=docXml.createElement("asteroid")
		idXml=docXml.createElement("id")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		idtemplateXml=docXml.createElement("idtemplate")
		idtemplateXml.appendChild(docXml.createTextNode(str(self.idTemplate)))
		posxXml=docXml.createElement("posx")
		posxXml.appendChild(docXml.createTextNode(str(self.posx)))
		posyXml=docXml.createElement("posy")
		posyXml.appendChild(docXml.createTextNode(str(self.posy)))
		poszXml=docXml.createElement("posz")
		poszXml.appendChild(docXml.createTextNode(str(self.posz)))
		hprhXml=docXml.createElement("hprh")
		hprhXml.appendChild(docXml.createTextNode(str(self.hprh)))
		hprpXml=docXml.createElement("hprp")
		hprpXml.appendChild(docXml.createTextNode(str(self.hprp)))
		hprrXml=docXml.createElement("hprr")
		hprrXml.appendChild(docXml.createTextNode(str(self.hprr)))
		scaleXml=docXml.createElement("scale")
		scaleXml.appendChild(docXml.createTextNode(str(self.scale)))
		
		astXml.appendChild(idXml)
		astXml.appendChild(idtemplateXml)
		astXml.appendChild(posxXml)
		astXml.appendChild(posyXml)
		astXml.appendChild(poszXml)
		astXml.appendChild(hprhXml)
		astXml.appendChild(hprrXml)
		astXml.appendChild(hprpXml)
		astXml.appendChild(scaleXml)
		
		#~ print astXml.toxml()		
		return astXml
	