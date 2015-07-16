#!/usr/bin/env python
import wx
import xml.dom.minidom
from shimstar.gui.item.wxitems import *
from shimstar.gui.item.wxitem import *
from shimstar.gui.zone.wxzones import *
from shimstar.gui.pnj.wxpnjs import *
from shimstar.gui.pnj.wxkeywords import *
from shimstar.gui.npc.wxnpcs import *
from shimstar.gui.pnj.wxdialogs import *
from shimstar.gui.pnj.wxmissions import *
from shimstar.gui.zone.wxasteroids import *
from shimstar.gui.character.wxskills import *
from shimstar.gui.world.wxfactions import *
from shimstar.gui.character.wxplayers import *

from shimstar.zone.station import *
from shimstar.pnj.dialog import *
from shimstar.zone.zone import *
from shimstar.item.item import *
from shimstar.item.engine import *
from shimstar.item.weapon import *
from constantes import *
from shimstar.pnj.mission import *
from shimstar.pnj.pnjtemplate import *
from shimstar.character.skill import *
from shimstar.item.mining import *
from shimstar.item.mineral import *
from shimstar.item.ship import *

ID_MENU_ITEMS=10
ID_MENU_ZONE=20
ID_MENU_PNJ=21
ID_MENU_STATION=22
ID_MENU_DIALOGUE=23
ID_MENU_KEYWORD=24
ID_MENU_MISSION=25
ID_MENU_ASTEROID=26
ID_MENU_ZONE_ZONE=27
ID_MENU_NPC=28
ID_MENU_WORLD=29
ID_MENU_WORLD_FACTION=30
ID_MENU_PLAYER=31

ID_MENU_XML=9
ID_MENU_ITEM_OUVRIR=11
ID_MENU_ITEM_NEW=12
ID_MENU_SKILL=13

class MyFrame(wx.MDIParentFrame):
	def __init__(self, parent, title):
			wx.MDIParentFrame.__init__(self, None,-1, title=title, size=(300,800))
			self.Maximize()
			filemenu= wx.Menu()

			# wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
			menuItemXml=filemenu.Append(ID_MENU_XML,"Generate Xml files"," Terminate the program")
			self.Bind(wx.EVT_MENU, self.onGenerateXml, menuItemXml)
			filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
			filemenu.AppendSeparator()
			menuItemExit=filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
			self.Bind(wx.EVT_MENU, self.onExit, menuItemExit)
			# Creating the menubar.
			menuBar = wx.MenuBar()
			menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
			
			self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
			filemenu= wx.Menu()
			menuItemOuvrir=filemenu.Append(ID_MENU_ITEM_OUVRIR,"Ouvrir"," Afficher les items")
			self.Bind(wx.EVT_MENU, self.onItems, menuItemOuvrir)
			menuItemNew=filemenu.Append(ID_MENU_ITEM_NEW,"Nouveau Template"," Nouveau Template")
			menuBar.Append(filemenu,"&Template Item")
			self.Bind(wx.EVT_MENU, self.onNewTemplateItem, menuItemNew)
			menuItem=filemenu.Append(ID_MENU_SKILL,"Skills","")
			self.Bind(wx.EVT_MENU, self.onSkills, menuItem)
			
			filemenu= wx.Menu()
			menuBar.Append(filemenu,"&Player") # Adding the "Player" to the MenuBar
			menuItem=filemenu.Append(ID_MENU_PLAYER,"player","")
			self.Bind(wx.EVT_MENU, self.onPlayer, menuItem)
			
			filemenu= wx.Menu()
			menuBar.Append(filemenu,"&Zone") # Adding the "Zone" to the MenuBar
			menuItem=filemenu.Append(ID_MENU_ZONE,"zone","")
			self.Bind(wx.EVT_MENU, self.onZone, menuItem)
			menuItem=filemenu.Append(ID_MENU_STATION,"station","")
			menuItem=filemenu.Append(ID_MENU_ASTEROID,"asteroid","")
			self.Bind(wx.EVT_MENU, self.onAsteroid, menuItem)
			
			filemenu= wx.Menu()
			menuBar.Append(filemenu,"&World") # Adding the "World" to the MenuBar
			menuItem=filemenu.Append(ID_MENU_WORLD_FACTION,"faction","")
			self.Bind(wx.EVT_MENU, self.onFaction, menuItem)
			
			filemenu= wx.Menu()
			menuBar.Append(filemenu,"&Pnj") # Adding the "filemenu" to the MenuBar
			menuItem=filemenu.Append(ID_MENU_PNJ,"pnj","")
			self.Bind(wx.EVT_MENU, self.onPNJ, menuItem)
			menuItem=filemenu.Append(ID_MENU_DIALOGUE,"dialogue","")
			self.Bind(wx.EVT_MENU, self.onDialogue, menuItem)
			menuItem=filemenu.Append(ID_MENU_KEYWORD,"keyword","")
			self.Bind(wx.EVT_MENU, self.onKeyword, menuItem)
			menuItem=filemenu.Append(ID_MENU_MISSION,"mission","")
			self.Bind(wx.EVT_MENU, self.onMission, menuItem)
			menuItem=filemenu.Append(ID_MENU_NPC,"Npc","")
			self.Bind(wx.EVT_MENU, self.onNPC, menuItem)
			
			self.Show(True)
			self.activeWindows=None

	
		
	def onExit(self,e):
		self.Close(True)
		
	def onGenerateXml(self,e):
		########## Dialogue###################
		docXml = xml.dom.minidom.Document()
		dialogsXml=docXml.createElement("dialogs")
		listOfDialogs=Dialog.getListOfDialog()
		for d in listOfDialogs:
			di=Dialog(d)
			dXml=di.getXml(docXml)
			dialogsXml.appendChild(dXml)
		docXml.appendChild(dialogsXml)
		fileHandle = open ( "./datas/dialogs.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		########## Mission###################
		docXml = xml.dom.minidom.Document()
		missionsXml=docXml.createElement("missions")
		listOfMissions=mission.getListOfMissions()
		for m in listOfMissions:
			mi=mission(m)
			mXml=mi.getXml(docXml)
			missionsXml.appendChild(mXml)
		docXml.appendChild(missionsXml)
		fileHandle = open ( "./datas/missions.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		########## Station ###################
		docXml = xml.dom.minidom.Document()
		stationXml=docXml.createElement("stations")
		listOfStation=station.getListOfStation()
		for s in listOfStation:
			st=station(s)
			sXml=st.getXml(docXml)
			stationXml.appendChild(sXml)
		docXml.appendChild(stationXml)
		fileHandle = open ( "./datas/stations.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		########## PNJ ###################
		docXml = xml.dom.minidom.Document()
		pnjsXml=docXml.createElement("pnjs")
		listOfPnj=PNJ.getListOfPNJ()
		for p in listOfPnj:
			pn=PNJ(p)
			pXml=pn.getXml(docXml)
			pnjsXml.appendChild(pXml)
		docXml.appendChild(pnjsXml)
		fileHandle = open ( "./datas/pnjs.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		########## Zone ###################
		docXml = xml.dom.minidom.Document()
		zoneXml=docXml.createElement("zones")
		listOfZone=Zone.getListOfZone()
		for z in listOfZone:
			zo=Zone(z)
			zXml=zo.getXml(docXml)
			zoneXml.appendChild(zXml)
		docXml.appendChild(zoneXml)
		fileHandle = open ( "./datas/zones.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		##########Item Template###############
		docXml = xml.dom.minidom.Document()
		itemsXml=docXml.createElement("items")
		listOfItemTemplates=ShimstarItem.getListOfItemTemplates()
		for i in listOfItemTemplates:
			it=ShimstarItem(0,i)
			if it.getTypeItem()==C_ITEM_ENGINE:
				eng=engine(0,i)
				itXml=eng.getXml()
			elif it.getTypeItem()==C_ITEM_WEAPON:
				wea=Weapon(i,it.getSpecific())
				itXml=wea.getXml()
			elif it.getTypeItem()==C_ITEM_MINING:
				min=miningItem(i,it.getSpecific())
				itXml=min.getXml()
			elif it.getTypeItem()==C_ITEM_SHIP:
				print "main::ship " + str(i) + "/" + str(it.getSpecific())
				sh=Ship(0,i)
				itXml=sh.getXml()
			else:
				itXml=it.getXml(docXml)
			itemsXml.appendChild(itXml)
		docXml.appendChild(itemsXml)
		fileHandle = open ( "./datas/itemtemplates.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		#############Asteroid##################
		docXml = xml.dom.minidom.Document()
		astXml=docXml.createElement("asteroids")
		listOfAst=Asteroid.getListOfAsteroidTemplate()
		#~ print listOfAst
		for ida in listOfAst:
			a=Asteroid(0,ida)
			aXml=a.getXmlTemplate(docXml)
			astXml.appendChild(aXml)
		docXml.appendChild(astXml)
		fileHandle = open ( "./datas/asteroids.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		#############WormHole##################
		docXml = xml.dom.minidom.Document()
		wormXml=docXml.createElement("wormholes")
		listOfWorm=wormhole.getListOfWormHoleTemplate()
		#~ print listOfAst
		for idW in listOfWorm:
			w=wormhole(0,idW)
			wXml=w.getXmlTemplate(docXml)
			wormXml.appendChild(wXml)
		docXml.appendChild(wormXml)
		fileHandle = open ( "./datas/wormholes.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		#############PnjTemplate##################
		docXml = xml.dom.minidom.Document()
		pnjXml=docXml.createElement("pnjtemplates")
		listOfP=PNJtemplate.getListOfPNJTemplate()
		#~ print listOfAst
		for idp in listOfP:
			p=PNJtemplate(idp)
			pXml=p.getXml(docXml)
			pnjXml.appendChild(pXml)
		docXml.appendChild(pnjXml)
		fileHandle = open ( "./datas/pnjtemplate.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		#############Skill##################
		docXml = xml.dom.minidom.Document()
		skillXml=docXml.createElement("skills")
		listOfSkill=Skill.getListOfSkills()
		#~ print listOfAst
		for ids in listOfSkill:
			s=Skill(ids)
			sXml=s.getXml(docXml)
			skillXml.appendChild(sXml)
		docXml.appendChild(skillXml)
		fileHandle = open ( "./datas/skills.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		#############Minerals##################
		docXml = xml.dom.minidom.Document()
		mineralXml=docXml.createElement("minerals")
		listOfMinerals=mineral.getListMineral()
		#~ print listOfAst
		for idm  in listOfMinerals:
			s=mineral(0,idm)
			sXml=s.getXml(docXml)
			print sXml
			mineralXml.appendChild(sXml)
		docXml.appendChild(mineralXml)
		fileHandle = open ( "./datas/mineral.xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		
	def onNewTemplateItem(self,e):
		ItemPanel(self,0,0)
		
	def onItems(self,e):
		#~ self.activeWindows=ItemsPanel(self)
		ItemsPanel(self)
		
	def onPNJ(self,e):
		PNJsPanel(self)
		
	def onNPC(self,e):
		NPCsPanel(self)
		
	def onMission(self,e):
		#~ PNJPanel(self)
		MissionsPanel(self)
		
	def onAsteroid(self,e):
		AsteroidsPanel(self)
		
	def onSkills(self,e):
		SkillsPanel(self)
		
	def onKeyword(self,e):
		KeywordsPanel(self)
		
	def onDialogue(self,e):
		DialogsPanel(self)
		
	def onZone(self,e):
		ZonesPanel(self)
		
	def onFaction(self,e):
		FactionsPanel(self)
		
	def onPlayer(self,e):
		UsersPanel(self)

app = wx.App(False)
frame = MyFrame(None, 'Shimstar editor')
app.MainLoop()

