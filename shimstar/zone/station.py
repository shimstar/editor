from dbconnector import *
import xml.dom.minidom

class station:
	def __init__(self,id):
		self.id=id
		self.label=""
		self.name=""
		self.npc=[]
		query="SELECT star011_name,star022_posx, star022_posy,star022_posz,star022_hprh,star022_hprp,star022_hprr, "
		query+=" star022_mass,star011_egg,star011_typezone_star012,star011_scale,star022_inzone_star011,star022_screen "
		query+=" FROM  star011_zone JOIN  star022_station on STAR011_id = star022_zone_star011 WHERE STAR011_id ='" +str(self.id) + "'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=row[0]
			self.posx=float(row[1])
			self.posy=float(row[2])
			self.posz=float(row[3])
			self.hprh=float(row[4])
			self.hprp=float(row[5])
			self.hprr=float(row[6])
			self.mass=str(row[7])
			self.egg=str(row[8])
			self.typezone=int(row[9])
			self.scale=float(row[10])
			self.exitZone=int(row[11])
			self.background=str(row[12])
		cursor.close()
		
		self.loadNpc()
		
	def getBackground(self):
		return self.background
		
	def getExitZone(self):
		return self.exitZone
		
	def loadNpc(self):
		query="SELECT star027_id from star027_npc_station where star027_location_star022='" + str(self.id) +"'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.npc.append(int(row[0]))
		cursor.close()
		
	@staticmethod
	def getListOfStation():
		query="SELECT star011_id,star011_name from star011_zone where  star011_typezone_star012 = 2"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfStation={}
		for row in result_set:			
			listOfStation[int(row[0])]=row[1]
		cursor.close()
		return listOfStation
		
	@staticmethod		
	def getListOfStationByZone(zoneId):
		query="SELECT star022_zone_star011 from star022_station where star022_inzone_star011 = '" + str(zoneId) + "'"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfStation=[]
		for row in result_set:			
			listOfStation.append(int(row[0]))
		cursor.close()
		return listOfStation
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		stationXml=docXml.createElement("station")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		idXml=docXml.createElement("idstation")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
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
		massXml=docXml.createElement("mass")
		massXml.appendChild(docXml.createTextNode(str(self.mass)))
		eggXml=docXml.createElement("egg")
		eggXml.appendChild(docXml.createTextNode(str(self.egg)))
		typezoneXml=docXml.createElement("typezone")
		typezoneXml.appendChild(docXml.createTextNode(str(self.typezone)))
		scaleXml=docXml.createElement("scale")
		scaleXml.appendChild(docXml.createTextNode(str(self.scale)))
		exitZoneXml=docXml.createElement("exitzone")
		exitZoneXml.appendChild(docXml.createTextNode(str(self.exitZone)))
		if len(self.npc)>0:
			npcsXml=docXml.createElement("npcs")
			for n in self.npc:
				idnpcXml=docXml.createElement("idnpc")
				idnpcXml.appendChild(docXml.createTextNode(str(n)))
				npcsXml.appendChild(idnpcXml)
				
			stationXml.appendChild(npcsXml)
		
		stationXml.appendChild(nameXml)
		stationXml.appendChild(idXml)
		stationXml.appendChild(posxXml)
		stationXml.appendChild(posyXml)
		stationXml.appendChild(poszXml)
		stationXml.appendChild(hprhXml)
		stationXml.appendChild(hprpXml)
		stationXml.appendChild(hprrXml)
		stationXml.appendChild(massXml)
		stationXml.appendChild(eggXml)
		stationXml.appendChild(typezoneXml)
		stationXml.appendChild(scaleXml)
		stationXml.appendChild(exitZoneXml)
				
		return stationXml
		