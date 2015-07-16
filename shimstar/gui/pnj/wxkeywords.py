# -*- coding: utf-8 -*- 
import wx
from shimstar.pnj.skeyword import *
from shimstar.gui.pnj.wxkeyword import *

class KeywordsPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de keyword",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		
		wx.StaticBox(self.panel1, -1, 'Creer', pos=(0, 50), size=(240, 50))
		self.newKeyword=wx.Button(self.panel1, -1, "Creer un nouveau keyword", (10,70))
		self.Bind(wx.EVT_BUTTON, self.onNewKeyword, self.newKeyword)
		wx.StaticBox(self.panel1, -1, 'Liste des Keywords', pos=(0, 100), size=(240, 450))
		self.listItem=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseKeyword, self.listItem)
		
		self.SetAutoLayout(True)
		self.showAllKeywords()
		self.Layout()
		
	def showAllKeywords(self):
		tabTempl=Keyword.getListOfKeyword()
		self.listItem.Clear()
		for t in tabTempl:
			k=Keyword(t)
			self.listItem.Insert(str(t) + " | " + k.getName(),0)
		
	def onChooseKeyword(self,evt):
		tab=self.listItem.GetStringSelection().split(" | ")
		idKeyword=int(tab[0])
		KeywordPanel(self.parent,self,idKeyword)
	
	def onNewKeyword(self,e):
		KeywordPanel(self.parent,self,0)
	
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			