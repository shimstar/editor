import wx
from shimstar.character.user import *
from shimstar.gui.character.wxcharacter import *

class UserPanel(wx.MDIChildFrame):
	def __init__(self, parent,idUser,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "User",size=(600,300),pos=(400,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(600,300))
		self.prt=prt
		self.idUser=idUser
		self.parent=parent
		
		self.user=User(self.idUser)
		
		self.lblname = wx.StaticText(self, label="Name :", pos=(10,15))
		self.editname = wx.TextCtrl(self, value=self.user.getName(), pos=(120, 15), size=(140,-1))
		self.lbldateCreation = wx.StaticText(self, label="Cree le :", pos=(10,40))
		self.editCreation = wx.TextCtrl(self, value=self.user.getDateCreation(), pos=(120, 40), size=(140,-1))
		self.lblLastLogin = wx.StaticText(self, label="Derniere connexion :", pos=(10,65))
		self.editLastLogin = wx.TextCtrl(self, value=self.user.getLastLogin(), pos=(120, 65), size=(140,-1))
				
		self.listChar=wx.ListBox(self.panel1, 26, pos=(300, 10), size=(200,350),style=wx.LB_SINGLE)
		
		for c in self.user.getListOfCharacter():
			self.listChar.Insert(str(c.getId()) + " | " + str(c.getName()),0)
			
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseChar, self.listChar)
		
	def onChooseChar(self,e):
		idChar=self.listChar.GetStringSelection().split('|')[0]
		CharacterPanel(self.parent,self.idUser,idChar,self)