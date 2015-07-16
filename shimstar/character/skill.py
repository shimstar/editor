from dbconnector import *
import xml.dom.minidom

class Skill:
	def __init__(self,id):
		self.id=id
		self.isPrimary=0
		self.name=""
		self.text=""
		self.base=0
		self.level=0
		self.parents=[]
		self.loadFromBDD()
		
	def getId(self):
		return self.id
		
	def getName(self):
		return self.name
		
	def setName(self,name):
		self.name=name
		
	def getText(self):
		return self.text
		
	def setText(self,text):
		self.text=text
		
	def getLevel(self):
		return self.level
		
	def getIsPrimary(self):
		return self.isPrimary
		
	def getParents(self):
		return self.parents
		
	def setParents(self,par):
		self.parents=par
		
	def setIsPrimary(self,p):
		self.isPrimary=p
		
	def setLevel(self,level):
		self.level=level
		
	def getBase(self):
		return self.base
		
	def setBase(self,base):
		self.base=base
		
	def removeParent(self,id):
		parent=None
		for p in self.parents:
			if p.getId()==id:
				parent=p
				break
		if parent!=None:
			self.parents.remove(parent)
		
	def loadFromBDD(self):
		query="SELECT star030_name,star030_description,star030_base"
		query+=" FROM star030_skill where star030_id=" + str(self.id)

		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.name=str(row[0])
			self.text=str(row[1])
			self.base=int(row[2])
		cursor.close()
		self.loadParentsFromBDD()
		
	def saveToBDD(self):
		if self.id>0:
			query="update star030_skill set star030_name='" + self.name + "'"
			query+=",star030_description='" + self.text + "', star030_base='" + str(self.base) +"'"
			query+=" where star030_id='" + str(self.id) +"'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
		else:
			query="insert into star030_skill (star030_name, star030_description, star030_base)"
			query+=" values ('"+ self.name + "','" + self.text + "','" + str(self.base) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
			
		self.saveParentsToBDD()
		instanceDbConnector.commit()
		return self.id
	
	def saveParentsToBDD(self):
		query="delete from star032_parent_skill where star032_skill_star030 = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		for p in self.parents:
			query="insert into star032_parent_skill (star032_skill_star030,star032_skillparent_star030,star032_level_needed,star032_primary_parent)"
			query+=" values ('" + str(self.id) + "','" + str(p.getId()) + "','1','0')"
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
			
		
	def loadParentsFromBDD(self):
		query="SELECT star032_skillparent_star030,star032_level_needed,star032_primary_parent"
		query+=" FROM star032_parent_skill where star032_skill_star030=" + str(self.id)
		self.parents=[]
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			idParent=int(row[0])
			skillParent=Skill(idParent)
			skillParent.setLevel(int(row[1]))
			skillParent.setIsPrimary(int(row[2]))
			self.parents.append(skillParent)
		cursor.close()
		
	@staticmethod
	def getListOfSkills():
		skills=[]
		query="SELECT star030_id from star030_skill"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			skills.append(row[0])
		cursor.close()
		return skills
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		skillXml=docXml.createElement("skill")
		idXml=docXml.createElement("idskill")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		textXml=docXml.createElement("text")
		textXml.appendChild(docXml.createTextNode(str(self.text)))
		skillXml.appendChild(idXml)
		skillXml.appendChild(nameXml)
		skillXml.appendChild(textXml)
		
		if len(self.parents)>0:
			parentsXml=docXml.createElement("parents")
			for p in self.parents:
				parentXml=docXml.createElement("parent")
				parentIdXml=docXml.createElement("idparent")
				parentIdXml.appendChild(docXml.createTextNode(str(p.getId())))
				isPrimaryXml=docXml.createElement("primary")
				isPrimaryXml.appendChild(docXml.createTextNode(str(p.getIsPrimary())))
				levelXml=docXml.createElement("level")
				levelXml.appendChild(docXml.createTextNode(str(p.getLevel())))
				parentXml.appendChild(parentIdXml)
				parentXml.appendChild(isPrimaryXml)
				parentXml.appendChild(levelXml)
				parentsXml.appendChild(parentXml)
			skillXml.appendChild(parentsXml)
		return skillXml
