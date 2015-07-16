import os,sys
import wx
import xml.dom.minidom
from shimstar.world.faction import *


class FactionPanel(wx.MDIChildFrame):
	def __init__(self, parent,idFaction,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Faction Description",size=(300,300),pos=(300,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300),pos=(0,0))
		
		self.prt=prt
		self.parent=parent
		self.idFaction=idFaction
		
		btn=wx.Button(self.panel1, -1, "Save", (10,200 ))
		self.Bind(wx.EVT_BUTTON, self.saveFaction, btn)
		btn=wx.Button(self.panel1, -1, "Delete", (120,200 ))
		self.Bind(wx.EVT_BUTTON, self.deleteFaction, btn)
		lbl=wx.StaticText(self.panel1, label="Nom : "  , pos=(50,50 ))
		self.input1= wx.TextCtrl(self.panel1,value="", pos=(100, 50 ), size=(100,-1) )
		if self.idFaction>0:
			fa=Faction(self.idFaction)
			self.input1.SetValue(fa.getName())
		
	def saveFaction(self,e):
		fa=Faction(self.idFaction)
		fa.setName(self.input1.GetValue())
		fa.saveToBDD()
		self.prt.showAllFactions()
		self.Destroy()
	
	def deleteFaction(self,e):
		if self.idFaction>0:
			fa=Faction(self.idFaction)
			fa.deleteFromBDD()
		self.prt.showAllFactions()
		self.Destroy()