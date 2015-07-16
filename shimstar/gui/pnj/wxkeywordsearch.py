import wx
from shimstar.pnj.skeyword import *

class keywordsearchPanel(wx.MDIChildFrame):
	def __init__(self, parent,editTxt):		
		self.editTxt=editTxt
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de keyword",size=(500,500),pos=(200,300))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500))
		self.parent=parent
		listOfKeywords=Keyword.getListOfKeyword()
		wx.StaticBox(self.panel1, -1, 'Liste des Keywords', pos=(0, 100), size=(440, 450))
		self.listkeyw=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(400,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseKeyw, self.listkeyw)
		self.listkeyw.Clear()
		for t in listOfKeywords:
			it=Keyword(int(t))
			self.listkeyw.Insert(str(t) + " | " + it.getName()[:40],0)
		self.SetAutoLayout(True)
		self.Layout()
	
	def	onChooseKeyw(self,evt):
		tab=self.listkeyw.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=Keyword(idItem)
		#~ DialogPanel(self.parent,0,idItem)
		self.editTxt.Insert(str(idItem) + " | " + itemChoosed.getName(),0)
		self.Destroy()
			
			