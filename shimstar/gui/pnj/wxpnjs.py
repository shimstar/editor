import wx
from shimstar.pnj.pnj import *
from shimstar.gui.pnj.wxpnj import *

class PNJsPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche d'items",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		listOfPnj=PNJ.getListOfPNJ()
		lt=[]
		for l in listOfPnj:
			t=PNJ(l)
			lt.append(str(t.getId()) + " | " + t.getName())
		self.cbox = wx.ComboBox(self.panel1, -1,choices=lt,style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.Bind(wx.EVT_COMBOBOX, self.onChoosePNJ, self.cbox)

		
	def onChoosePNJ(self,evt):
		tab=self.cbox.GetValue().split(" | ")
		idPnj=int(tab[0])
		if idPnj>0:
			#~ pnjChoosed=PNJ(idPnj)
			#~ face = wx.BitmapButton(self.panel2, -1, wx.Bitmap("faces/" + pnjChoosed.getFace() + ".png"))
			PnjPanel(self.parent,idPnj,self)
		
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			