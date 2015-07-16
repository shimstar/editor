import wx
from shimstar.world.faction import *
from shimstar.gui.world.wxfaction import *

class FactionsPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "Factions",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		
		self.listFaction=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseFaction, self.listFaction)
		
		self.showAllFactions()
		
		self.createNew=wx.Button(self.panel1, -1, "Creer", (30,30))
		self.Bind(wx.EVT_BUTTON, self.onCreateNew, self.createNew)
		
	def onCreateNew(self,e):
		FactionPanel(self.parent,0,self)
		
	def showAllFactions(self):
		self.listFaction.Clear()
		listOfFaction=Faction.getListOfFactions()
		for l in listOfFaction:
			self.listFaction.Insert(str(l) + " | " + str(listOfFaction[l]),0)
		
	def onChooseFaction(self,e):
		FactionPanel(self.parent,self.listFaction.GetStringSelection().split('|')[0],self)
		
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			