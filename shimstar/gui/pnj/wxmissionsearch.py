import wx
from shimstar.pnj.mission import *


class MissionSearchPanel(wx.MDIChildFrame):
	def __init__(self, parent,editTxt):		
		self.editTxt=editTxt
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de Mission",size=(500,500),pos=(200,300))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500))
		self.parent=parent
		
		wx.StaticBox(self.panel1, -1, 'Liste des Missions', pos=(0, 100), size=(440, 450))
		self.listMission=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(400,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseMission, self.listMission)
		listOfMission=mission.getListOfMissions()
		for p in listOfMission:
			pn=mission(p)
			self.listMission.Insert(str(p) + " | " + pn.getLabel()[:40],0)
		
		self.SetAutoLayout(True)
		self.Layout()
		

	
	def	onChooseMission(self,evt):
		tab=self.listMission.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=mission(idItem)
		self.editTxt.SetValue(str(idItem) + " | " + itemChoosed.getLabel()[:40])
		self.Destroy()
			
			