# -*- coding: utf-8 -*- 
import wx
from shimstar.zone.asteroid import *
from shimstar.gui.zone.wxasteroid import *

class AsteroidsPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche d'ateroid",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		
		wx.StaticBox(self.panel1, -1, 'Creer', pos=(0, 50), size=(240, 50))
		self.newAst=wx.Button(self.panel1, -1, "Creer un nouvel asteroid", (10,70))
		self.Bind(wx.EVT_BUTTON, self.onNewAst, self.newAst)
		wx.StaticBox(self.panel1, -1, 'Liste des Asteroids', pos=(0, 100), size=(240, 450))
		self.listItem=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseAsteroid, self.listItem)
		
		self.SetAutoLayout(True)
		self.showAllAsteroids()
		self.Layout()
		
	def showAllAsteroids(self):
		tabTempl=Asteroid.getListOfAsteroidTemplate()
		self.listItem.Clear()
		for t in tabTempl:
			k=Asteroid(0,t)
			self.listItem.Insert(str(t) + " | " + k.getName(),0)
		
	def onChooseAsteroid(self,evt):
		tab=self.listItem.GetStringSelection().split(" | ")
		id=int(tab[0])
		AsteroidPanel(self.parent,self,id)
	
	def onNewAst(self,e):
		AsteroidPanel(self.parent,self,0)
	
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			