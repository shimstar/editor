# -*- coding: iso-8859-1 -*-
from dbconnector import *
import xml.dom.minidom
from skeyword import *

class Dialog:
	def __init__(self,id):
		self.id=id
		self.text=""
		self.readonce=0
		self.idType=0
		self.proba=0
		self.label=""
		self.dialogs=[]
		self.keywords=[]
		self.refDialog=0
		if id>0:
			self.loadFromBDD()
		
	def loadFromBDD(self):
		query="SELECT star025_text,star025_idtype_star024,star025_proba,star025_readonce,star025_dialogue_star025 FROM star025_dialogue WHERE star025_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.text=row[0]
			#~ print self.text
			#~ self.text=self.text.decode('utf-8')
			self.idType=int(row[1])
			self.proba=int(row[2])
			self.readonce=int(row[3])
			self.refDialog=int(row[4])
		cursor.close()
		
		self.loadKeyWords()
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		dialogXml=docXml.createElement("dialog")
		idXml=docXml.createElement("iddialog")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		textXml=docXml.createElement("text")
		textXml.appendChild(docXml.createTextNode(str(self.text)))
		typeXml=docXml.createElement("idtype")
		typeXml.appendChild(docXml.createTextNode(str(self.idType)))
		probaXml=docXml.createElement("proba")
		probaXml.appendChild(docXml.createTextNode(str(self.proba)))
		readonceXml=docXml.createElement("readonce")
		readonceXml.appendChild(docXml.createTextNode(str(self.readonce)))
		refdialogXml=docXml.createElement("refdialog")
		refdialogXml.appendChild(docXml.createTextNode(str(self.refDialog)))
		if len(self.keywords)>0:
			keywordsXml=docXml.createElement("keywords")
			for k in self.keywords:
				key=Keyword(k)
				keywordsXml.appendChild(key.getXml())
			dialogXml.appendChild(keywordsXml)
		dialogXml.appendChild(idXml)
		dialogXml.appendChild(textXml)
		dialogXml.appendChild(typeXml)
		dialogXml.appendChild(probaXml)
		dialogXml.appendChild(readonceXml)
		dialogXml.appendChild(refdialogXml)
	
		
		return dialogXml
		
	def loadKeyWords(self):
		query="SELECT star026_keyword_star023 FROM  star026_dialogue_keyword WHERE star026_dialogue_star025='" +  str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.keywords.append(int(row[0]))
			
		cursor.close
		
		
	def getKeywords(self):
		return self.keywords
		
	def saveToBDD(self):
		if self.id>0:
			query="UPDATE star025_dialogue SET STAR025_TEXT='" + self.text + "'"
			query+=" ,star025_idtype_star024='" + str(self.idType) + "',star025_proba='" + str(self.proba) +"'"
			query+=" ,star025_readonce='" + str(self.readonce)+ "',star025_dialogue_star025='" + str(self.refDialog)+ "'"
			query+=" WHERE STAR025_id = '" + str(self.id) + "'"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
		else:
			query="INSERT INTO star025_dialogue (STAR025_TEXT,star025_idtype_star024,star025_proba,star025_readonce,star025_dialogue_star025) "
			query+=" VALUES ('" + self.text+ "','"+str(self.idType)+"','"+str(self.proba)+"','"+str(self.readonce)+"','"+str(self.refDialog)+"')"
			#~ print query
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
			
		self.saveKeywords()		
		instanceDbConnector.commit()
		return self.id
		
	def saveKeywords(self):
		query="DELETE FROM star026_dialogue_keyword WHERE star026_dialogue_star025='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		
		for k in self.keywords:
			query="INSERT INTO star026_dialogue_keyword (star026_dialogue_star025,star026_keyword_star023) "
			query+=" values ('" + str(self.id) + "','" + str(k) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			cursor.close()
		
	def deleteFromBDD(self):
		query="DELETE FROM star025_dialogue WHERE STAR025_id ='"+str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		instanceDbConnector.commit()
		
		
	def getProba(self):
		return self.proba
		
	def setProba(self,proba):
		self.proba=proba
		
	def getReadOnce(self):
		return self.readonce
		
	def setReadOnce(self,readonce):
		self.readonce=readonce
		
	def getTypeDialogue(self):
		return self.idType
		
	def setTypeDialogue(self,idType):
		self.idType=idType
		
	def getRefDialogue(self):
		return self.refDialog
		
	def setRefDialogue(self,refDialogue):
		self.refDialog=refDialogue
		
	def setText(self,text):
		self.text=text
		
	def getText(self):
		return self.text
		
	def getId(self):
		return self.id
		
	def clearKeywords(self):
		self.keywords=[]
		
	def appendKeywords(self,id):
		self.keywords.append(int(id))
		
	@staticmethod
	def getListOfDialog():
		query="SELECT star025_id FROM STAR025_dialogue"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result
		
	