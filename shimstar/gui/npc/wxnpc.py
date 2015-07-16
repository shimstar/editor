import os,sys
import wx
import xml.dom.minidom
from dbconnector import *
from shimstar.npc.npc import *
from shimstar.item.typeitem import *
from shimstar.item.item import *
from shimstar.item.ship import *
from shimstar.gui.item.wxitemship import *
from shimstar.world.faction import *
from shimstar.zone.zone import *

class Attitude:
	def __init__(self):
		self.typeAttitude=0
		self.levelAttitude=0
		self.faction=0
		
	def setProperties(self,ta,la,f):
		self.typeAttitude=ta
		self.levelAttitude=la
		self.faction=f
		
	def getProperties(self):
		return self.typeAttitude,self.levelAttitude,self.faction

class BehaviorPanel(wx.MDIChildFrame):
	def __init__(self, parent,idZone,idBehavior,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Behavior Description",size=(1000,500),pos=(300,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500),pos=(0,0))
		
		self.prt=prt
		self.parent=parent
		self.idZone=idZone
		self.idBehavior=idBehavior
		self.widgetPP=[]
		self.widgetAttitude=[]
		self.patrolPoints=[]
		self.attitudes=[]
		
		if self.idBehavior>0:
			dom = xml.dom.minidom.parse("./datas/behaviour/zone"+str(idZone) + "/" + str(self.idBehavior) + ".xml")
			pp=dom.getElementsByTagName('patrolpoint')
			
			
			for p in pp:
				pos=p.firstChild.data
				tabpos=pos.split(",")
				self.patrolPoints.append((float(tabpos[0]),float(tabpos[1]),float(tabpos[2])))
			
			self.showPatrolPoints()
			atti=dom.getElementsByTagName('attitude')
			
			for a in atti:
				typeAtti=int(a.getElementsByTagName('typeattitude')[0].firstChild.data)
				lvlAtti=int(a.getElementsByTagName('levelattitude')[0].firstChild.data)
				faction=int(a.getElementsByTagName('faction')[0].firstChild.data)
				temp=Attitude()
				temp.setProperties(typeAtti,lvlAtti,faction)
				self.attitudes.append(temp)
			self.showAttitudes()
			
		btn=wx.Button(self.panel1, -1, "Ajouter un PP", (420,10))
		self.Bind(wx.EVT_BUTTON, self.addPP, btn)
		btn=wx.Button(self.panel1, -1, "Ajouter une attitude", (50,10))
		self.Bind(wx.EVT_BUTTON, self.addAttitude, btn)
		btn=wx.Button(self.panel1, -1, "Save", (10,300 ))
		self.Bind(wx.EVT_BUTTON, self.saveBehavior, btn)
		
		
	def addPP(self,e):
		self.patrolPoints.append((0,0,0))
		self.showPatrolPoints()
		
	def addAttitude(self,e):
		self.attitudes.append(Attitude())
		self.showAttitudes()
		
	def showPatrolPoints(self):
		for w in self.widgetPP:
			w.Destroy()
			
		self.widgetPP=[]
		i=1
		for p in self.patrolPoints:
			lbl=wx.StaticText(self.panel1, label="Point de Patrouille "+ str(i) + " :", pos=(420,50 + (i-1)*20))
			self.widgetPP.append(lbl)
			input1= wx.TextCtrl(self.panel1,value=str(p[0]), pos=(580, 50 + (i-1)*20), size=(100,-1) )
			self.widgetPP.append(input1)
			input2= wx.TextCtrl(self.panel1,value=str(p[1]), pos=(680, 50 + (i-1)*20), size=(100,-1) )
			self.widgetPP.append(input2)
			input3= wx.TextCtrl(self.panel1,value=str(p[2]), pos=(780, 50 + (i-1)*20), size=(100,-1) )
			self.widgetPP.append(input3)
			btn=wx.Button(self.panel1, -1, "Delete", (880,50 + (i-1)*20))
			self.widgetPP.append(btn)
			self.Bind(wx.EVT_BUTTON, lambda event,temp=(i-1):self.deletePP(event,temp), btn)
			self.Bind(wx.EVT_TEXT, lambda event,numPP=(i-1),inp1=input1,inp2=input2,inp3=input3:self.changePP(event,numPP,inp1,inp2,inp3), input1)
			self.Bind(wx.EVT_TEXT, lambda event,numPP=(i-1),inp1=input1,inp2=input2,inp3=input3:self.changePP(event,numPP,inp1,inp2,inp3), input2)
			self.Bind(wx.EVT_TEXT, lambda event,numPP=(i-1),inp1=input1,inp2=input2,inp3=input3:self.changePP(event,numPP,inp1,inp2,inp3), input3)
			i+=1
			
	def changePP(self,e,numPP,inp1,inp2,inp3):
		self.patrolPoints[numPP]=(inp1.GetValue(),inp2.GetValue(),inp3.GetValue())
		
	def showAttitudes(self):
		lbl=wx.StaticText(self.panel1, label="Type :", pos=(80,50 ))
		lbl=wx.StaticText(self.panel1, label="Level :", pos=(180,50 ))
		lbl=wx.StaticText(self.panel1, label="Faction :", pos=(280,50 ))
		i=1
		for a in self.attitudes:
			ta,la,fa=a.getProperties()
			lbl=wx.StaticText(self.panel1, label="Attitude "+ str(i) + " :", pos=(10,90 + (i-1)*20))
			cb1 = wx.ComboBox(self.panel1, -1,choices=('1 | Aggressive','2 | Defensive'),pos=(80, 90 + (i-1)*20),style=wx.CB_DROPDOWN|wx.CB_SORT)
			if ta==1:
				cb1.SetStringSelection('1 | Aggressive')
			elif ta==2:
				cb1.SetStringSelection('2 | Defensive')
			
			cb2 = wx.ComboBox(self.panel1, -1,choices=('1','2','3','4'),pos=(180, 90 + (i-1)*20),style=wx.CB_DROPDOWN|wx.CB_SORT)
			cb2.SetStringSelection(str(la))
		
			ltFaction=[]
			listOfFactions=Faction.getListOfFactions()
			currentFactionIndex=-1
			j=0
			for f in listOfFactions:
				if int(f)==int(fa):
					currentFactionIndex=j
				ltFaction.append(str(f) + " | " + str(listOfFactions[f]))
				j+=1
				
			cb3 = wx.ComboBox(self.panel1, -1,choices=ltFaction,pos=(220, 90 + (i-1)*20),style=wx.CB_DROPDOWN|wx.CB_SORT)
			cb3.SetSelection(currentFactionIndex)
			
			self.Bind(wx.EVT_COMBOBOX, lambda event,numAttitude=(i-1),inp1=cb1,inp2=cb2,inp3=cb3:self.changeAttitude(event,numAttitude,inp1,inp2,inp3), cb1)
			self.Bind(wx.EVT_COMBOBOX, lambda event,numAttitude=(i-1),inp1=cb1,inp2=cb2,inp3=cb3:self.changeAttitude(event,numAttitude,inp1,inp2,inp3), cb2)
			self.Bind(wx.EVT_COMBOBOX, lambda event,numAttitude=(i-1),inp1=cb1,inp2=cb2,inp3=cb3:self.changeAttitude(event,numAttitude,inp1,inp2,inp3), cb3)
			i+=1
		
		
	def changeAttitude(self,e,numAttitude,cb1,cb2,cb3):
		att=self.attitudes[numAttitude]
		ta=0
		if cb1.GetValue().find('|')>0:
			ta=cb1.GetValue().split('|')[0]
		fa=0
		if cb3.GetValue().find('|')>0:
			fa=cb3.GetValue().split('|')[0]
		la=0
		if cb2.GetValue()!="":
			la=cb2.GetValue()
		
		att.setProperties(ta,la,fa)
		self.showAttitudes()
		
	def deletePP(self,e,pp):
		self.patrolPoints.pop(pp)
		self.showPatrolPoints()
		
	def saveBehavior(self,e):
		if self.idBehavior==0:
			maxNum=0
			for fi in os.listdir(os.getcwd() + "\\datas\\behaviour\\zone" + str(self.idZone) +"\\"):
				num=int(fi.split('.')[0])
				if num > maxNum:
					maxNum=num
			query="insert into star063_behaviour_template (star064_num,star064_zone_star011)"
			query+=" values ('" + str(maxNum+1) + "','" + str(self.idZone) + "')"
			instanceDbConnector=shimDbConnector.getInstance()
			cursor=instanceDbConnector.getConnection().cursor()
			cursor.execute(query)
			self.idBehavior=maxNum+1
			cursor.close()
			instanceDbConnector.commit()
		docXml = xml.dom.minidom.Document()
		behavXml=docXml.createElement("behaviour")
		patrolsXml=docXml.createElement("patrol")
		for p in self.patrolPoints:
			patrolXml=docXml.createElement("patrolpoint")
			patrolXml.appendChild(docXml.createTextNode(str(p[0]) + "," + str(p[1]) + "," + str(p[2])))
			patrolsXml.appendChild(patrolXml)
		behavXml.appendChild(patrolsXml)
		
		#~ print self.attitudes
		for a in self.attitudes:
			attitudeXml=docXml.createElement("attitude")
			typeXml=docXml.createElement("typeattitude")
			ta,la,fa=a.getProperties()
			typeXml.appendChild(docXml.createTextNode(str(ta)))
			lvlXml=docXml.createElement("levelattitude")
			lvlXml.appendChild(docXml.createTextNode(str(la)))
			factionXml=docXml.createElement("faction")
			factionXml.appendChild(docXml.createTextNode(str(fa)))
			attitudeXml.appendChild(typeXml)
			attitudeXml.appendChild(lvlXml)
			attitudeXml.appendChild(factionXml)
			behavXml.appendChild(attitudeXml)
		docXml.appendChild(behavXml)
		fileHandle = open ("./datas/behaviour/zone"+str(self.idZone) + "/" + str(self.idBehavior) + ".xml", 'w' ) 
		fileHandle.write(docXml.toxml())
		fileHandle.close()
		
		self.prt.showBehavior()
		self.Destroy()
		
		
class ChooseBehaviorPanel(wx.MDIChildFrame):
	def __init__(self, parent,idZone,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Behavior Choice",size=(500,500),pos=(600,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500),pos=(0,0))
		
		self.prt=prt
		self.parent=parent
		self.idZone=idZone
		self.listBehavior=wx.ListBox(self.panel1, 26, pos=(10, 10), size=(200,350),style=wx.LB_SINGLE)
		self.showBehavior()
			
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseBehavior, self.listBehavior)		
		btn=wx.Button(self.panel1, -1, "Info", (200,200))
		self.Bind(wx.EVT_BUTTON, self.showInfo, btn)
		btn=wx.Button(self.panel1, -1, "New", (200,150))
		self.Bind(wx.EVT_BUTTON, self.onNew, btn)
		
	def onNew(self,e):
		BehaviorPanel(self.parent,self.idZone,0,self)
		
	def showBehavior(self):
		self.listBehavior.Clear()
		for fi in os.listdir(os.getcwd() + "\\datas\\behaviour\\zone" + str(self.idZone) +"\\"):
			self.listBehavior.Insert(fi,0)
	
	def onChooseBehavior(self,e):
		choice=self.listBehavior.GetStringSelection().split('.')[0]
		self.prt.behaviorInput.SetValue(choice)
		self.Destroy()
		
	def showInfo(self,e):
		BehaviorPanel(self.parent,self.idZone,self.listBehavior.GetStringSelection().split('.')[0],self)
		

class ChooseShipTemplatePanel(wx.MDIChildFrame):
	def __init__(self, parent,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "ShipTemplate",size=(500,500),pos=(600,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500),pos=(0,0))
		
		self.prt=prt
		self.parent=parent

		self.listItem=wx.ListBox(self.panel1, 26, pos=(10, 10), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseTplItem, self.listItem)		
		tabTempl=typeItem.getListOfItemByTypeItem(C_ITEM_SHIP)
		for t in tabTempl:
			it=ShimstarItem(0,t)
			self.listItem.Insert(str(t) + " | " + it.getTypeItemLabel()+ " | " + it.getName(),0)
			
		btn=wx.Button(self.panel1, -1, "Info", (200,200))
		self.Bind(wx.EVT_BUTTON, self.showInfo, btn)
			
	def onChooseTplItem(self,e):
		tab=self.listItem.GetStringSelection()
		self.prt.shipTemplateInput.SetValue(tab)
		self.Destroy()
		
	def showInfo(self,args):
		tab=self.listItem.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=ShimstarItem(0,idItem)
		ItemShipPanel(self.parent,0,idItem,0,None)

class NPCPanel(wx.MDIChildFrame):
	def __init__(self, parent,idNPCTemplate,prt=None,idZone=0):
		wx.MDIChildFrame.__init__(self,parent, -1, "NPC",size=(500,500),pos=(400,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500),pos=(0,0))
		
		self.prt=prt
		self.parent=parent
		self.idNPCTemplate=idNPCTemplate
		self.idZone=idZone
		
		self.NPC=NPC(self.idNPCTemplate)
		
		self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(10,15))
		self.editname = wx.TextCtrl(self.panel1, value=self.NPC.getName(), pos=(120, 10), size=(140,-1))
		
		self.lblShipTempalte=wx.StaticText(self.panel1, label="Ship Template :", pos=(10,40))
		templateShip=Ship(0,self.NPC.getTemplateShip())
		self.shipTemplateInput = wx.TextCtrl(self, value=str(templateShip.getTemplate()) + " | " + templateShip.getTypeItemLabel()+ " | " + templateShip.getName(), pos=(120, 40), size=(140,-1),style=wx.TE_READONLY)
		self.chooseShipTemplate=wx.Button(self.panel1, -1, "Choisir", (300,35))
		self.Bind(wx.EVT_BUTTON, self.onChooseShipTemplate, self.chooseShipTemplate)
		self.lblfaction = wx.StaticText(self.panel1, label="Faction :", pos=(10,95))
		
		indexCurrentFaction=-1
		listOfFaction=Faction.getListOfFactions()
		lt=[]
		lt.append("")
		i=1
		for f in listOfFaction:
			lt.append(str(f) + " | " + str(listOfFaction[f]))
			if int(self.NPC.getIdFaction())==int(f):
				indexCurrentFaction=i
			i+=1
		
		self.faction = wx.ComboBox(self.panel1, -1,choices=lt,pos=(120, 90 ),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.faction.SetSelection(indexCurrentFaction)
		self.lblBehaviour=wx.StaticText(self.panel1, label="Behavior Template :", pos=(10,65))
		
		self.behaviorInput = wx.TextCtrl(self, value=str(self.NPC.getIdBehavior()), pos=(120, 65), size=(140,-1))
		self.choosebehavior=wx.Button(self.panel1, -1, "Choisir", (300,60))
		self.Bind(wx.EVT_BUTTON, self.onChooseBehavior, self.choosebehavior)
		self.viewBehavior=wx.Button(self.panel1, -1, "Voir", (380,60))
		self.Bind(wx.EVT_BUTTON, self.onViewBehavior, self.viewBehavior)
		
		lt=[]
		indexCurrentZone=-1
		lt.append("")
		i=1
		listOfZone=Zone.getListOfZone()
		for l in listOfZone:
			t=Zone(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
			if int(l)==int(self.NPC.getIdZone()) or int(l)==self.idZone:
				indexCurrentZone=i
			i+=1
		
		self.lblZone=wx.StaticText(self.panel1, label="Zone :", pos=(10,120))
		self.cboxChoixZone = wx.ComboBox(self.panel1, -1,choices=lt,pos=(120, 120),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.cboxChoixZone.SetSelection(indexCurrentZone)
		
		self.saveNpc=wx.Button(self.panel1, -1, "Save", (30,180))
		self.Bind(wx.EVT_BUTTON, self.onSaveNpc, self.saveNpc)
		self.deleteNpc=wx.Button(self.panel1, -1, "Delete", (130,180))
		self.Bind(wx.EVT_BUTTON, self.onDeleteNpc, self.deleteNpc)
		
		
	def onDeleteNpc(self,e):
		if self.idNPCTemplate>0:
			NPCtemp=NPC(self.idNPCTemplate)
			NPCtemp.deleteFromBDD()
		self.prt.onChooseZone(None)
		self.Destroy()
		
	def onSaveNpc(self,e):
		NPCTemp=NPC(self.idNPCTemplate)
		shipTemplate=self.shipTemplateInput.GetValue()
		if shipTemplate.find('|')>0:
			shipTemplate=shipTemplate.split('|')[0]
		else:
			shipTemplate=0
		NPCTemp.setTemplateShip(shipTemplate)
		idBehav=self.behaviorInput.GetValue()
		if idBehav!="":
			idBehav=int(idBehav)
		else:
			idBehav=0
		NPCTemp.setIdBehavior(idBehav)
		idZone=self.cboxChoixZone.GetStringSelection()
		if idZone.find('|')>0:
			idZone=idZone.split('|')[0]
		else:
			idZone=0
		NPCTemp.setIdZone(idZone)
		NPCTemp.setName(self.editname.GetValue())
		idFaction=self.faction.GetStringSelection()
		if idFaction.find('|')>0:
			idFaction=idFaction.split('|')[0]
		else:
			idFaction=0
		
		NPCTemp.setIdFaction(idFaction)
		NPCTemp.saveToBDD()
		
		self.prt.onChooseZone(None)
		self.Destroy()
		
	def onChooseBehavior(self,e):
		idZone=self.cboxChoixZone.GetStringSelection()
		if idZone.find('|')>0:
			idZone=idZone.split('|')[0]
		else:
			idZone=0
		ChooseBehaviorPanel(self.parent,int(idZone),self)
	
	def onChooseShipTemplate(self,e):
		ChooseShipTemplatePanel(self.parent,self)
		
	def onViewBehavior(self,e):
		BehaviorPanel(self.parent,self.NPC.getIdZone(),self.NPC.getIdBehavior(),self)
		