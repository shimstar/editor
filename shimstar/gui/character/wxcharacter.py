import wx
from shimstar.character.user import *
from shimstar.character.character import *
from shimstar.world.faction import *
from shimstar.zone.zone import *
from shimstar.zone.station import *

class InfoShipTabPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		#~ self.parent=parent
		#~ self.prt=prt
		#~ self.idChar=char

		sizer = wx.BoxSizer(wx.VERTICAL)
		txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
		txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(txtOne, 0, wx.ALL, 5)
		sizer.Add(txtTwo, 0, wx.ALL, 5)

		self.SetSizer(sizer)
		
class InfoCharTabPanel(wx.Panel):
	def __init__(self, parent,idChar):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		self.character=Character(idChar)
		self.img = wx.BitmapButton(self, -1, wx.Bitmap("faces/" + self.character.getFace() + ".png"))
		self.lblname = wx.StaticText(self, label="Name :", pos=(150,15))
		self.editname = wx.TextCtrl(self,value=self.character.getName(), pos=(250, 10), size=(140,-1) )
		self.lblzone = wx.StaticText(self, label="Zone :", pos=(150,40))
		zone=Zone(self.character.getIdZone())
		self.editzone = wx.TextCtrl(self,value=str(zone.getId()) + ' | ' + zone.getName(), pos=(250, 40), size=(140,-1) )
		self.lbllaststation = wx.StaticText(self, label="Last Station :", pos=(150,65))
		st=station(self.character.getLastStation())
		self.editlaststation = wx.TextCtrl(self,value=str(self.character.getLastStation()) + " | " + st.getName(), pos=(250, 65), size=(140,-1) )
		self.lblfaction = wx.StaticText(self, label="Faction :", pos=(150,90))
		fa=Faction(self.character.getIdFaction())
		self.edifaction = wx.TextCtrl(self,value=str(fa.getId()) + " | " + fa.getName(), pos=(250, 90), size=(140,-1) )
	

class CharacterNotebook(wx.Notebook):
	def __init__(self, parent,idChar,prt,panel1):
		wx.Notebook.__init__(self, panel1, id=wx.ID_ANY, style=wx.BK_DEFAULT)
		self.parent=parent
		self.prt=prt
		self.idChar=idChar
		
		tabOne = InfoCharTabPanel(self,idChar)
		
		self.AddPage(tabOne, "Infos")        
		
		tabTwo = InfoShipTabPanel(self)
		self.AddPage(tabTwo, "Vaisseau")

	

class CharacterPanel(wx.MDIChildFrame):
	def __init__(self, parent,idUser,idCharacter,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Character",size=(600,300),pos=(200,50))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(600,300))
		self.prt=prt
		self.idUser=idUser
		self.idCharacter=idCharacter
		self.parent=parent
		
		notebook = CharacterNotebook(self.parent,idCharacter,prt,self.panel1)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
		self.panel1.SetSizer(sizer)
		