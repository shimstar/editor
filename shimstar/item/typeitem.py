from dbconnector import *

class typeItem:
	def __init__(self,id):
		self.id=id
		self.label=""
		query="SELECT star003_label FROM STAR003_typeitem WHERE star003_id = '" + str(self.id) + "'"
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
	def getListOfTypeItem():
		query="SELECT star003_id FROM STAR003_typeitem"
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
	def getListOfItemByTypeItem(typeItem):
		if typeItem!=-1:
			query="SELECT star004_id FROM STAR004_item_template where star004_type_star003='" + str(typeItem) + "'"
		else:
			query="SELECT star004_id FROM STAR004_item_template"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result