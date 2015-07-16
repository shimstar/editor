import wx
from shimstar.character.user import *
from shimstar.gui.character.wxuser import *

class UsersPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "NPCs",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		
		listOfUsers=User.getListOfUsers()
		self.listUser=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		lt=[]
		for l in listOfUsers:
			self.listUser.Insert(str(l) + " | "   + listOfUsers[l],0)
		
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseUser, self.listUser)
		
		btn=wx.Button(self.panel1, -1, "Nouveau", (120,20))
		#~ self.Bind(wx.EVT_BUTTON, self.onCreateNew, btn)
		
	#~ def onCreateNew(self,e):
		#~ NPCPanel(self.parent,0,self)
		
	def onChooseUser(self,e):
		tab=self.listUser.GetStringSelection().split('|')
		idUser=int(tab[0])
		
		UserPanel(self.parent,idUser,self)
		
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			