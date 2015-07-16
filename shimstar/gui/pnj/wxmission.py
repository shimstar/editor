# -*- coding: iso-8859-1 -*-
import wx
from shimstar.pnj.mission import *
from shimstar.pnj.dialog import *
from shimstar.pnj.pnj import *
from shimstar.gui.pnj.wxdialogsearch import *
from shimstar.gui.pnj.wxpnjsearch import *
from shimstar.gui.pnj.wxmissionsearch import *
from shimstar.item.engine import *
from constantes import *
#~ .encode('iso-8859-1') 

class MissionPanel(wx.MDIChildFrame):
	def __init__(self, parent,pc,id):
		wx.MDIChildFrame.__init__(self,parent, -1, "Mission",size=(1000,600),pos=(400,100))
		self.parent=parent
		self.id=id
		self.pc=pc
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(1000,600))
		if id>0:
			self.mission=mission(int(id))
			self.edittxt= wx.TextCtrl(self.panel1, value=self.mission.getLabel(), pos=(15, 10), size=(340,-1))
			self.beginTxt= wx.StaticText(self.panel1, label="Depend de la mission :", pos=(15,40))
			idDepMission=self.mission.getDepMission()
			if idDepMission>0:
				depMission=mission(idDepMission)
				self.depMission= wx.TextCtrl(self, value=str(idDepMission) + "|" + depMission.getLabel(), pos=(115, 40), size=(200,-1))
			else:
				self.depMission= wx.TextCtrl(self, value="0", pos=(115, 40), size=(200,-1))
			self.changeDepMission=wx.Button(self.panel1, -1, "Changer", (330,35))
			self.Bind(wx.EVT_BUTTON, self.onChangeDepMission, self.changeDepMission)
			
			wx.StaticBox(self.panel1, -1, 'Dialogues', (5, 130), size=(420, 110))
			self.beginTxt= wx.StaticText(self.panel1, label="Dialogue de depart :", pos=(15,150))
			idBeginDiag=self.mission.getBeginDiag()
			if idBeginDiag>0:
				beginDiag=Dialog(idBeginDiag)
				self.beginDiag= wx.TextCtrl(self, value=str(idBeginDiag) + "|" + beginDiag.getText().replace('\\2n','\n \n').replace('\\1n','\n'), pos=(115, 150), size=(200,-1))
			else:
				self.beginDiag= wx.TextCtrl(self, value="", pos=(85, 150), size=(200,-1))
			self.changeBegin=wx.Button(self.panel1, -1, "Changer", (330,145))
			self.Bind(wx.EVT_BUTTON, self.onChangeBegin, self.changeBegin)
			self.currentTxt= wx.StaticText(self.panel1, label="Dialogue courant :", pos=(15,180))
			idCurrentDiag=self.mission.getCurrentDiag()
			if idCurrentDiag>0:
				currentDiag=Dialog(idCurrentDiag)
				self.currentDiag= wx.TextCtrl(self, value=str(idCurrentDiag) + "|" + currentDiag.getText().replace('\\2n','\n \n').replace('\\1n','\n'), pos=(115, 180), size=(200,-1))
			else:
				self.currentDiag= wx.TextCtrl(self, value="", pos=(85, 180), size=(200,-1))
			self.changeCurrent=wx.Button(self.panel1, -1, "Changer", (330,175))
			self.Bind(wx.EVT_BUTTON, self.onChangeCurrent, self.changeCurrent)
			
			self.EndTxt= wx.StaticText(self.panel1, label="Dialogue de fin :", pos=(15,210))
			idEndDiag=self.mission.getEndingDiag()
			if idEndDiag>0:
				endingDiag=Dialog(idEndDiag)
				self.endingDiag= wx.TextCtrl(self, value=str(idEndDiag) + "|" + endingDiag.getText().replace('\\2n','\n \n').replace('\\1n','\n'), pos=(115, 210), size=(200,-1))
			else:
				self.endingDiag= wx.TextCtrl(self, value="", pos=(85, 210), size=(200,-1))
			self.changeEnd=wx.Button(self.panel1, -1, "Changer", (330,205))
			self.Bind(wx.EVT_BUTTON, self.onChangeEnd, self.changeEnd)
			
			wx.StaticBox(self.panel1, -1, 'NPC', (5, 250), size=(420, 100))
			self.EndTxt= wx.StaticText(self.panel1, label="NPC donnant :", pos=(15,270))
			idBeginNPC=self.mission.getNPC()
			if idBeginNPC>0:
				beginNPC=PNJ(idBeginNPC)
				self.beginNPC= wx.TextCtrl(self, value=str(idBeginNPC) + " | " + beginNPC.getName().replace('\\2n','\n \n').replace('\\1n','\n'), pos=(115, 270), size=(200,-1))
			else:
				self.beginNPC= wx.TextCtrl(self, value="", pos=(85, 270), size=(200,-1))
			self.changeBeginNPC=wx.Button(self.panel1, -1, "Changer", (330,265))
			self.Bind(wx.EVT_BUTTON, self.onChangeBeginNPC, self.changeBeginNPC)
			
			self.EndTxt= wx.StaticText(self.panel1, label="NPC de fin :", pos=(15,300))
			idEndingNPC=self.mission.getEndingNPC()
			if idEndingNPC>0:
				endingNPC=PNJ(idEndingNPC)
				self.endingNPC= wx.TextCtrl(self, value=str(idEndingNPC) + " | " + endingNPC.getName().replace('\\2n','\n \n').replace('\\1n','\n'), pos=(115, 300), size=(200,-1))
			else:
				self.endingNPC= wx.TextCtrl(self, value="", pos=(85, 300), size=(200,-1))
			self.changeEndNPC=wx.Button(self.panel1, -1, "Changer", (330,295))
			self.Bind(wx.EVT_BUTTON, self.onChangeEndNPC, self.changeEndNPC)
			
			wx.StaticBox(self.panel1, -1, 'Objectifs', (450, 20), size=(480, 350))
			lt=Objectif.getListOfTypeObjectif()
			for o in self.mission.getObjectifs():
				wx.StaticText(self.panel1, label="Type :", pos=(465,45))
				self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(540, 40),style=wx.CB_DROPDOWN|wx.CB_SORT)
				self.Bind(wx.EVT_COMBOBOX, self.onChooseTypeObjectif, self.cboxChoixType)
				self.cboxChoixType.SetValue(Objectif.getTypeObjectifById(o.getIdType()))
				self.onChooseTypeObjectif(None)
			
		else:
			self.edittxt= wx.TextCtrl(self.panel1, value="", pos=(15, 10), size=(340,-1))
			wx.StaticBox(self.panel1, -1, 'Dialogues', (5, 130), size=(420, 110))
			self.beginTxt= wx.StaticText(self.panel1, label="Dialogue de depart :", pos=(15,150))
			self.beginDiag= wx.TextCtrl(self, value="", pos=(85, 150), size=(200,-1))
			self.changeBegin=wx.Button(self.panel1, -1, "Changer", (330,145))
			self.Bind(wx.EVT_BUTTON, self.onChangeBegin, self.changeBegin)
			self.currentTxt= wx.StaticText(self.panel1, label="Dialogue courant :", pos=(15,180))
			self.currentDiag= wx.TextCtrl(self, value="", pos=(85, 180), size=(200,-1))
			self.changeCurrent=wx.Button(self.panel1, -1, "Changer", (330,175))
			self.Bind(wx.EVT_BUTTON, self.onChangeCurrent, self.changeCurrent)
			
			self.EndTxt= wx.StaticText(self.panel1, label="Dialogue de fin :", pos=(15,210))
			self.endingDiag= wx.TextCtrl(self, value="", pos=(85, 210), size=(200,-1))
			self.changeEnd=wx.Button(self.panel1, -1, "Changer", (330,205))
			self.Bind(wx.EVT_BUTTON, self.onChangeEnd, self.changeEnd)
			
			wx.StaticBox(self.panel1, -1, 'NPC', (5, 250), size=(420, 100))
			self.EndTxt= wx.StaticText(self.panel1, label="NPC donnant :", pos=(15,270))
			self.beginNPC= wx.TextCtrl(self, value="", pos=(85, 270), size=(200,-1))
			self.changeBeginNPC=wx.Button(self.panel1, -1, "Changer", (330,265))
			self.Bind(wx.EVT_BUTTON, self.onChangeBeginNPC, self.changeBeginNPC)
			
			self.EndTxt= wx.StaticText(self.panel1, label="NPC de fin :", pos=(15,300))
			self.endingNPC= wx.TextCtrl(self, value="", pos=(85, 300), size=(200,-1))
			self.changeEndNPC=wx.Button(self.panel1, -1, "Changer", (330,295))
			self.Bind(wx.EVT_BUTTON, self.onChangeEndNPC, self.changeEndNPC)
			
			self.depMission= wx.TextCtrl(self, value="0", pos=(115, 40), size=(200,-1))
			self.changeDepMission=wx.Button(self.panel1, -1, "Changer", (330,35))
			self.Bind(wx.EVT_BUTTON, self.onChangeDepMission, self.changeDepMission)

			
		self.save=wx.Button(self.panel1, -1, "Save", (50,450))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (130,450))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
		
	def onChooseTypeObjectif(self,evt):
		tab=self.cboxChoixType.GetValue().split(" | ")
		if int(tab[0])==C_OBJECTIF_TRANSPORT:
			if self.mission!=None:
				preItem=self.mission.getPreItems()
				self.givenItemLbl=wx.StaticText(self.panel1, label="Objet donne à transporter :", pos=(465,70))
				self.givenItem=wx.TextCtrl(self, value="", pos=(620, 70), size=(200,-1))
				self.givenItemChange=wx.Button(self.panel1, -1, "Changer", (820,65))
				self.Bind(wx.EVT_BUTTON, self.onChangeGivenItem, self.givenItemChange)
				if len(preItem)>0:
					it=ShimstarItem(0,preItem[0])
					self.givenItem.SetValue(str(it.getTemplate()) + " | " + str(it.getName()))
		
	def onChangeGivenItem(self,evt):
		pass
	
	def onChangeBeginNPC(self,evt):
		PnjsearchPanel(self.parent,self.beginNPC)
	
	def onChangeEndNPC(self,evt):
		PnjsearchPanel(self.parent,self.endingNPC)
	
	def onChangeBegin(self,evt):
		DialogsearchPanel(self.parent,self.beginDiag)
		
	def onChangeCurrent(self,evt):
		DialogsearchPanel(self.parent,self.currentDiag)
	
	def onChangeEnd(self,evt):
		DialogsearchPanel(self.parent,self.endingDiag)
	
	def onChangeDepMission(self,evt):
		MissionSearchPanel(self.parent,self.depMission)
		
	def onSave(self,event):
		mis=mission(self.id)
		mis.setLabel(self.edittxt.GetValue())

		mis.setBeginDiag(self.beginDiag.GetValue().split("|")[0])
		mis.setCurrentDiag(self.currentDiag.GetValue().split("|")[0])
		mis.setEndingDiag(self.endingDiag.GetValue().split("|")[0])
		mis.setNpc(self.beginNPC.GetValue().split(" | ")[0])
		mis.setEndingNPC(self.endingNPC.GetValue().split(" | ")[0])
		mis.setDepMission(self.depMission.GetValue().split(" | ")[0])
		self.id=mis.saveToBDD()
		self.pc.showAllTemplate()
	
	def onDelete(self,event):
		mis=mission(self.id)
		mis.deleteFromBDD()
		self.pc.showAllTemplate()
		self.Destroy()
	