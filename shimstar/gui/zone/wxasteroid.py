import wx
from shimstar.zone.asteroid import *


class AsteroidPanel(wx.MDIChildFrame):
	def __init__(self, parent,pc,id):
		wx.MDIChildFrame.__init__(self,parent, -1, "keyword",size=(300,300),pos=(400,100))
		self.id=id
		self.pc=pc
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300))
		self.asteroid=None
		if id>0:
			self.asteroid=Asteroid(0,id)		
			self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(30,15))
			self.editname = wx.TextCtrl(self.panel1, value=str(self.asteroid.getName()), pos=(120, 10), size=(140,-1))
			self.lblegg = wx.StaticText(self.panel1, label="Egg :", pos=(30,45))
			self.editegg= wx.TextCtrl(self.panel1, value=str(self.asteroid.getEgg()), pos=(120, 40), size=(140,-1))
			self.lblmass = wx.StaticText(self.panel1, label="Masse :", pos=(30,75))
			self.editmass = wx.TextCtrl(self.panel1, value=str(self.asteroid.getMass()), pos=(120, 70), size=(140,-1))
			self.lbltext = wx.StaticText(self.panel1, label="Description :", pos=(30,105))
			self.edittext = wx.TextCtrl(self.panel1, value=str(self.asteroid.getText()), pos=(120, 100), size=(140,-1))
		else:
			self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(30,15))
			self.editname = wx.TextCtrl(self.panel1,value="", pos=(120, 10), size=(140,-1) )
			self.lblegg = wx.StaticText(self.panel1, label="Egg :", pos=(30,45))
			self.editegg= wx.TextCtrl(self.panel1, value="", pos=(120, 40), size=(140,-1))
			self.lblmass = wx.StaticText(self.panel1, label="Masse :", pos=(30,75))
			self.editmass = wx.TextCtrl(self.panel1, value="0", pos=(120, 70), size=(140,-1))
			self.lbltext = wx.StaticText(self.panel1, label="Description :", pos=(30,105))
			self.edittext = wx.TextCtrl(self.panel1, value="", pos=(120, 100), size=(140,-1))
			
		self.save=wx.Button(self.panel1, -1, "Save", (50,200))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (130,200))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
			
	def onSave(self,event):
		asteroid=Asteroid(0,self.id)
		asteroid.setName(self.editname.GetValue())
		asteroid.setEgg(self.editegg.GetValue())
		asteroid.setMass(self.editmass.GetValue())
		asteroid.setText(self.edittext.GetValue())
		self.id=asteroid.saveToBDD()
		self.pc.showAllAsteroids()
	
	def onDelete(self,event):
		asteroid=Asteroid(0,self.id)
		asteroid.deleteFromBDD()
		self.pc.showAllAsteroids()
		self.Destroy()