import wx
from shimstar.npc.npc import *
from shimstar.zone.zone import *
from shimstar.gui.npc.wxnpc import *

class NPCsPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "NPCs",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		
		listOfZone=Zone.getListOfZone()
		lt=[]
		for l in listOfZone:
			t=Zone(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
		self.cboxChoixZone = wx.ComboBox(self.panel1, -1,choices=lt,pos=(10, 20),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.Bind(wx.EVT_COMBOBOX, self.onChooseZone, self.cboxChoixZone)
		
		self.listNpcTemplate=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseNPCTemplate, self.listNpcTemplate)
		
		btn=wx.Button(self.panel1, -1, "Nouveau", (120,20))
		self.Bind(wx.EVT_BUTTON, self.onCreateNew, btn)
		
	def onCreateNew(self,e):
		tab=self.cboxChoixZone.GetValue().split(" | ")
		idZone=int(tab[0])
		NPCPanel(self.parent,0,self,idZone)
		
	def onChooseNPCTemplate(self,e):
		tab=self.listNpcTemplate.GetStringSelection().split('|')
		idNPCTemplate=int(tab[0])
		
		NPCPanel(self.parent,idNPCTemplate,self)
		
	def onChooseZone(self,e):
		if self.cboxChoixZone.GetValue().index('|')>0:
			tab=self.cboxChoixZone.GetValue().split(" | ")
			idZone=int(tab[0])
			#~ zone=Zone(idZone)
			listOfNpc=NPC.getListOfNpcInZone(idZone)
			self.listNpcTemplate.Clear()
			for nt in listOfNpc:
				np=NPC(nt)
				self.listNpcTemplate.Insert(str(nt) + " | " + np.getName(),0)
		
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			