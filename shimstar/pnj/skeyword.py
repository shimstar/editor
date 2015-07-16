from dbconnector import *
import xml.dom.minidom

class Keyword:
	def __init__(self,id):
		self.id=id
		self.label=""
		if id>0:
			self.loadFromBDD()
			
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		keyXml=docXml.createElement("keyword")
		idXml=docXml.createElement("idkeyword")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		labelXml=docXml.createElement("labelkeyword")
		labelXml.appendChild(docXml.createTextNode(str(self.label)))
		
		keyXml.appendChild(idXml)
		keyXml.appendChild(labelXml)
		
		return keyXml
		
	def loadFromBDD(self):
		query="SELECT star023_label FROM star023_keyword WHERE star023_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.label=row[0]
		cursor.close()
		
	def saveToBDD(self):
		if self.id>0:
			query="UPDATE STAR023_KEYWORD SET STAR023_LABEL='" + self.name + "' WHERE STAR023_id = '" + str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
		else:
			query="INSERT INTO STAR023_KEYWORD (STAR023_LABEL) VALUES ('" + self.name + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
		instanceDbConnector.commit()
		return self.id
		
	def deleteFromBDD(self):
		query="DELETE FROM STAR023_KEYWORD WHERE STAR023_id ='"+str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		instanceDbConnector.commit()
		
	def setName(self,name):
		self.name=name
		
	def getName(self):
		return self.label
		
	def getId(self):
		return self.id
		
	@staticmethod
	def getListOfKeyword():
		query="SELECT star023_id FROM STAR023_keyword"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result
		
	