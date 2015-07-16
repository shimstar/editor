import wx
from shimstar.pnj.skeyword import *


class KeywordPanel(wx.MDIChildFrame):
	def __init__(self, parent,pc,id):
		wx.MDIChildFrame.__init__(self,parent, -1, "keyword",size=(300,100),pos=(400,100))
		self.id=id
		self.pc=pc
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,100))
		self.keyword=None
		if id>0:
			self.keyword=Keyword(id)		
			self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(80,15))
			self.editname = wx.TextCtrl(self.panel1, value=self.keyword.getName(), pos=(120, 10), size=(140,-1))
		else:
			self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(80,15))
			self.editname = wx.TextCtrl(self.panel1,value="", pos=(120, 10), size=(140,-1) )
			
		self.save=wx.Button(self.panel1, -1, "Save", (50,50))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (130,50))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
			
	def onSave(self,event):
		keyword=Keyword(self.id)
		keyword.setName(self.editname.GetValue())
		self.id=keyword.saveToBDD()
		self.pc.showAllKeywords()
	
	def onDelete(self,event):
		keyword=Keyword(self.id)
		keyword.deleteFromBDD()
		self.pc.showAllKeywords()
		self.Destroy()