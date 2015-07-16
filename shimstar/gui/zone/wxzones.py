import wx
from shimstar.zone.zone import *
from shimstar.gui.zone.wxzone import *

class ZonesPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de zone",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		
		listOfZone=Zone.getListOfZone()
		lt=[]
		for l in listOfZone:
			t=Zone(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
		self.cboxChoixZone = wx.ComboBox(self.panel1, -1,choices=lt,pos=(10, 20),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.Bind(wx.EVT_COMBOBOX, self.onChooseZone, self.cboxChoixZone)
		
	def onChooseZone(self,e):
		tab=self.cboxChoixZone.GetValue().split(" | ")
		idZone=int(tab[0])
		ZonePanel(self.parent,idZone,self)
		
	