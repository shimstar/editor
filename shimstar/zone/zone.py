from dbconnector import *
from shimstar.zone.asteroid import *
from shimstar.zone.station import *
from shimstar.zone.wormhole import *
import xml.dom.minidom

C_TYPEZONE_SPACE=1
C_TYPEZONE_STATION=2

class Zone:
	def __init__(self,id):
		self.id=id
		self.label=""

		query="SELECT star011_name, star011_typezone_star012,star011_egg,star011_scale,star011_music"
		query+=" FROM STAR011_ZONE WHERE STAR011_id = '" + str(self.id) + "'"
		#~ print query
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		for row in result_set:			
			self.name=str(row[0])
			self.typeZone=int(row[1])
			self.egg=str(row[2])
			self.scale=float(row[3])
			self.music=str(row[4])
		cursor.close()
		
		self.listOfAsteroid=Asteroid.getListOfAsteroid(self.id)
		self.listOfStation=station.getListOfStationByZone(self.id)
		self.listOfWormHole=wormhole.getListOfWormHole(self.id)
		
	def getListOfAsteroid(self):
		return self.listOfAsteroid
	
	@staticmethod
	def getListOfZone():
		query="SELECT star011_id from star011_zone where star011_typezone_star012 = 1"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		listOfZone=[]
		for row in result_set:			
			listOfZone.append(int(row[0]))
		return listOfZone
			
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getXml(self,docXml=None):
		if docXml==None:
			docXml = xml.dom.minidom.Document()
		zoneXml=docXml.createElement("zone")
		nameXml=docXml.createElement("name")
		nameXml.appendChild(docXml.createTextNode(str(self.name)))
		idXml=docXml.createElement("id")
		idXml.appendChild(docXml.createTextNode(str(self.id)))
		typeZoneXml=docXml.createElement("typezone")
		typeZoneXml.appendChild(docXml.createTextNode(str(self.typeZone)))
		
		scaleXml=docXml.createElement("scale")
		scaleXml.appendChild(docXml.createTextNode(str(self.scale)))
		musicXml=docXml.createElement("music")
		musicXml.appendChild(docXml.createTextNode(str(self.music)))
		if int(self.typeZone)==C_TYPEZONE_SPACE:
			eggXml=docXml.createElement("egg")
			eggXml.appendChild(docXml.createTextNode(str(self.egg)))
		else:
			print "zone::getXml " + str(self.id) + "/" + str(self.typeZone)
			currentStation=station(self.id)
			eggXml=docXml.createElement("egg")
			eggXml.appendChild(docXml.createTextNode(str(currentStation.getBackground())))
			exitZoneXml=docXml.createElement("exitzone")
			exitZoneXml.appendChild(docXml.createTextNode(str(currentStation.getExitZone())))
			zoneXml.appendChild(exitZoneXml)
		zoneXml.appendChild(idXml)
		zoneXml.appendChild(nameXml)
		zoneXml.appendChild(typeZoneXml)
		zoneXml.appendChild(eggXml)
		zoneXml.appendChild(scaleXml)
		zoneXml.appendChild(musicXml)

		if len(self.listOfAsteroid)>0:
			asteroidsXml=docXml.createElement("asteroids")
			for a in self.listOfAsteroid:
				ast=Asteroid(a)
				astXml=ast.getXml()
				asteroidsXml.appendChild(astXml)
				
			zoneXml.appendChild(asteroidsXml)
			
		if len(self.listOfStation)>0:
			stationXml=docXml.createElement("stations")
			for s in self.listOfStation:
				st=station(s)
				stXml=st.getXml()
				stationXml.appendChild(stXml)
				
			zoneXml.appendChild(stationXml)
		
		if len(self.listOfStation)>0:
			wormXml=docXml.createElement("wormholes")
			for w in self.listOfWormHole:
				wo=wormhole(w)
				wXml=wo.getXml()
				wormXml.appendChild(wXml)
				
			zoneXml.appendChild(wormXml)
				
		return zoneXml
		
	@staticmethod
	def getListOfStation():
		query="SELECT star011_id		FROM star011_zone where star011_typezone_star012=2"
		instanceDbConnector=shimDbConnector.getInstance()
		cursor=instanceDbConnector.getConnection().cursor()
		cursor.execute(query)
		result_set = cursor.fetchall ()
		result=[]
		for row in result_set:			
			result.append(int(row[0]))
		cursor.close()
		
		return result