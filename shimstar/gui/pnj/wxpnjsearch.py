import wx
from shimstar.pnj.pnj import *


class PnjsearchPanel(wx.MDIChildFrame):
	def __init__(self, parent,editTxt):		
		self.editTxt=editTxt
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de Pnj",size=(500,500),pos=(200,300))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500))
		self.parent=parent
		
		wx.StaticBox(self.panel1, -1, 'Liste des Pnjs', pos=(0, 100), size=(440, 450))
		self.listPnj=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(400,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChoosePnj, self.listPnj)
		listOfPnj=PNJ.getListOfPNJ()
		for p in listOfPnj:
			pn=PNJ(p)
			self.listPnj.Insert(str(p) + " | " + pn.getName(),0)
		
		self.SetAutoLayout(True)
		self.Layout()
		
	
	def	onChoosePnj(self,evt):
		tab=self.listPnj.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=PNJ(idItem)
		self.editTxt.SetValue(str(idItem) + " | " + itemChoosed.getName())
		self.Destroy()
			
			