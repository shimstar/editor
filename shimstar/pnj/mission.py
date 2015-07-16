import xml.dom.minidom
import os, sys
from dbconnector import *
from shimstar.pnj.objectif import *
from shimstar.pnj.reward import *
from shimstar.pnj.trigger import *

C_TYPE_MISSION_SHIPTODESTROY=1
C_STATEMISSION_DONTHAVE=0
C_STATEMISSION_GOTIT=1
C_STATEMISSION_SUCCESS=2
C_STATEMISSION_FINISHED=3
C_TYPEMISSION_COIN=1

class mission:
	def __init__(self,id,ichar=0):
		self.id=int(id)
		self.idChar=ichar
		self.label=""
		self.preItems=[]
		self.status=0
		self.trigger=[]
		self.events=[]
		self.loadFromBDD()
		
	def getTrigger(self):
		return self.trigger
		
	def addTrigger(self,t):
		self.trigger.append(t)
		
	def removeTrigger(self,t):
		if self.trigger.count(t)>0:
			self.trigger.remove(t)
		
	def getId(self):
		return self.id
		
	def getLabel(self):
		return self.label
		
	def setEndingNPC(self,endNPC):
		self.endingNPC=endNPC
		
	def setBeginDiag(self,bd):
		self.begindiag=bd
		
	def setCurrentDiag(self,cd):
		self.currentdiag=cd
		
	def setEndingDiag(self,ed):
		self.endingdiag=ed
		
	def setNpc(self,npc):
		self.npc=npc
		
	def setLabel(self,label):
		self.label=label
		
	def setDepMission(self,dep):
		self.depMission=dep
		
	def getDepMission(self):
		return self.depMission
		
	def saveToBDD(self):
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		if self.id==0:
			query="insert into star036_mission (star036_label,star036_endingnpc_star034,star036_begindialog_star025,currentstar036_dialog_star025,star036_postdialog_star025,star036_npc_star034,star036_mission_star036)"
			query+=" values ('" + str(self.label) + "','" + str(self.endingNPC) + "','" +  str(self.begindiag) + "','" +  str(self.currentdiag) + "'"
			query+=",'" + str(self.endingdiag) + "','" + str(self.npc) + "','" + str(self.depMission) + "')"
			cursor.execute(query)
			self.id=cursor.lastrowid
			cursor.close()
		else:
			query="update star036_mission"
			query+=" set star036_label='" + str(self.label) + "'"
			query+=", star036_endingnpc_star034='" + str(self.endingNPC) + "'"
			query+=",star036_begindialog_star025='" + str(self.begindiag) + "'"
			query+=", currentstar036_dialog_star025='" +  str(self.currentdiag) + "'"
			query+=", star036_postdialog_star025='" + str(self.endingdiag) +"'"
			query+=", star036_npc_star034='" +  str(self.npc) +"'"
			query+=", star036_mission_star036='" +  str(self.depMission) +"'"
			query+=" where star036_id='" + str(self.id) +"'"
			cursor.execute(query)
			cursor.close()
		instanceDbConnector.commit()
		return self.id
		
	def deleteFromBDD(self):
		query="delete from star036_mission where star036_id = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		cursor.close()
		instanceDbConnector.commit()

	@staticmethod
	def getListOfMissions():
		missions=[]
		query="SELECT star036_id from star036_mission"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			missions.append(row[0])
		cursor.close()
		return missions
		
	def loadFromBDD(self):
		query="SELECT star036_label,star036_endingnpc_star034,star036_begindialog_star025,currentstar036_dialog_star025,star036_postdialog_star025,star036_npc_star034,star036_mission_star036 "
		query+="FROM star036_mission where star036_id='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.label=row[0]
			self.endingNPC=int(row[1])
			self.begindiag=int(row[2])
			self.currentdiag=int(row[3])
			self.endingdiag=int(row[4])
			self.npc=int(row[5])
			self.depMission=int(row[6])
		cursor.close()
		self.loadPreItems()
		self.loadObjectifFromBDD()
		self.loadRewardsFromBDD()
		self.loadTriggerFromBDD()
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		missionXml=docXml.createElement("mission")
		labelXml=docXml.createElement("label")
		labelXml.appendChild(docXml.createTextNode(str(self.label)))
		idmissionXml=docXml.createElement("idmission")
		idmissionXml.appendChild(docXml.createTextNode(str(self.id)))
		endingnpcXml=docXml.createElement("endingnpc")
		endingnpcXml.appendChild(docXml.createTextNode(str(self.endingNPC)))
		begindiagXml=docXml.createElement("begindiag")
		begindiagXml.appendChild(docXml.createTextNode(str(self.begindiag)))
		currentdiagXml=docXml.createElement("currentdiag")
		currentdiagXml.appendChild(docXml.createTextNode(str(self.currentdiag)))
		endingdiagXml=docXml.createElement("endingdiag")
		endingdiagXml.appendChild(docXml.createTextNode(str(self.endingdiag)))
		npcXml=docXml.createElement("npc")
		npcXml.appendChild(docXml.createTextNode(str(self.npc)))
		depMissionXml=docXml.createElement("depmission")
		depMissionXml.appendChild(docXml.createTextNode(str(self.depMission)))
		
		missionXml.appendChild(labelXml)
		missionXml.appendChild(idmissionXml)
		missionXml.appendChild(endingnpcXml)
		missionXml.appendChild(begindiagXml)
		missionXml.appendChild(currentdiagXml)
		missionXml.appendChild(endingdiagXml)
		missionXml.appendChild(npcXml)
		missionXml.appendChild(depMissionXml)
		
		if len(self.preItems)>0:
			preitemsXml=docXml.createElement("preitems")
			for i in self.preItems:
				preitemXml=docXml.createElement("templateiditem")
				preitemXml.appendChild(docXml.createTextNode(str(i)))
				preitemsXml.appendChild(preitemXml)
			missionXml.appendChild(preitemsXml)
			
		if len(self.rewards)>0:
			rewardsXml=docXml.createElement("rewards")
			for r in self.rewards:
				rewardsXml.appendChild(r.getXml())
			missionXml.appendChild(rewardsXml)
			
		if len(self.objectifs)>0:
			objectifsXml=docXml.createElement("objectifs")
			for o in self.objectifs:
				objectifsXml.appendChild(o.getXml())
			missionXml.appendChild(objectifsXml)
		
		return missionXml
		
	def getNPC(self):
		return self.npc
		
	def getBeginDiag(self):
		return self.begindiag
		
	def getCurrentDiag(self):
		return self.currentdiag
	
	def getEndingDiag(self):
		return self.endingdiag
	
	def loadPreItems(self):
		query="SELECT star041_itemtemplate_star004, star041_nb FROM  star041_givenitem_mission where star041_mission_star036='" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			nb=int(row[1])
			for i in range(nb):
				self.preItems.append(int(row[0]))
		cursor.close()
		
	def loadTriggerFromBDD(self):
		query="select star064_id from star064_trigger_mission where star064_idmission_star036=" + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.trigger.append(Trigger(int(row[0])))
		cursor.close()
		
	def loadObjectifFromBDD(self):
		self.objectifs=[]
		query="SELECT star038_id FROM STAR038_OBJECTIF WHERE star038_mission_star036=" + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			tempObjectif=Objectif(row[0])
			self.objectifs.append(tempObjectif)
		cursor.close()
		
		if self.idChar>0:
			for o in self.objectifs:
				query="SELECT star040_nbitem FROM star040_character_objectif WHERE star040_character_star002='" + str(self.idChar) + "' and star040_objectif_star038='" + str(self.id) + "'"
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			result_set = cursor.fetchall ()
			for row in result_set:
				nbItem=int(row[0])
				o.setNbItemCharacter(nbItem)
			cursor.close()
		
	def loadRewardsFromBDD(self):
		self.rewards=[]
		query="SELECT star042_id FROM STAR042_rewards_mission WHERE star042_mission_star036=" + str(self.id)
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.rewards.append(Reward(row[0]))
		cursor.close()
		
	def loadEventFromBDD(self):
		self.events=[]
		query="SELECT star047_id FROM STAR047_event WHERE star047_mission_star036 = '" + str(self.id) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:
			self.events.append(event(row[0]))
		cursor.close()
		
	def getEvents(self):
		return self.events
		
	def setCharacterStatus(self,status):
		self.status=status
		
	def getStatus(self):
		return self.status
		
	def setStatus(self,status):
		self.status=status
		
	def getObjectifs(self):
		return self.objectifs

	def getId(self):
		return self.id
		
	def getRewards(self):
		return self.rewards
		
	def getEndingNPC(self):
		return self.endingNPC
		
	def getPreItems(self):
		return self.preItems
		
	def evaluateStatus(self):
		"""
			each time, an objectif is updated, evaluate new status of the mission. Is it still in progress, or maybe it is successfull.
		"""
		finished=False
		for o in self.objectifs:
			if o.getIdType()==C_OBJECTIF_DESTROY:
				if o.getNbItemCharacter()==o.getNbItem():
					finished=True
			else:
				finished=False
				break
				
		if finished==True:
			self.status=C_STATEMISSION_SUCCESS
		