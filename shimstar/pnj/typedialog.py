from dbconnector import *

class typeDialog:
	def __init__(self,id):
		self.id=id
		self.label=""
		query="SELECT star024_label FROM star024_typedialogue WHERE star024_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.label=row[0]
		cursor.close()
		
	def getName(self):
		return self.label
		
	def getId(self):
		return self.id
		
	@staticmethod
	def getListOfTypeDialogue():
		query="SELECT star024_id FROM star024_typedialogue"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result
		
	@staticmethod
	def getListOfDialogueByType(typeDialogue):
		if typeDialogue!=-1:
			query="SELECT star025_id FROM star025_dialogue where star025_idtype_star024='" + str(typeDialogue) + "'"
		else:
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