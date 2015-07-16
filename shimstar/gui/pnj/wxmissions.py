import wx
from shimstar.pnj.mission import *
from shimstar.gui.pnj.wxmission import *

class MissionsPanel(wx.MDIChildFrame):
	def __init__(self, parent):		
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de mission",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		wx.StaticBox(self.panel1, -1, 'Liste des Missions', pos=(0, 100), size=(240, 450))
		self.listMissions=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseMission, self.listMissions)
		self.addButton=wx.Button(self.panel1, -1, "Ajouter une nouvelle mission", (10,490))
		self.Bind(wx.EVT_BUTTON, self.addMission, self.addButton)
		self.SetAutoLayout(True)
		self.showAllTemplate()
		self.Layout()
		
	def addMission(self,event):
		MissionPanel(self.parent,self,0)
		
	def showAllTemplate(self):		
		self.listMissions.Clear()
		tabTempl=mission.getListOfMissions()
		for t in tabTempl:
			it=mission(int(t))
			self.listMissions.Insert(str(t) + " | " + it.getLabel()[:40],0)
	
	def	onChooseMission(self,evt):
		tab=self.listMissions.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		MissionPanel(self.parent,self,idItem)
			
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			