import wx
from shimstar.pnj.trigger import *
from shimstar.pnj.mission import *
from shimstar.zone.zone import *
from shimstar.pnj.event import *

class TriggerPanel(wx.MDIChildFrame):
	def __init__(self, parent,pc,id,mission):
		wx.MDIChildFrame.__init__(self,parent, -1, "keyword",size=(750,500),pos=(400,100))
		self.id=id
		self.missio=mission
		self.pc=pc
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(750,500))
		self.trigger=None
		
		wx.StaticText(self.panel1, label="Type :", pos=(15,30))
		listOfTypeTrigger=Trigger.getTypeTrigger()
		lt=[]
		for id in listOfTypeTrigger:
			lt.append(str(id) + "|" + str(listOfTypeTrigger[id]))
		self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(80, 30),style=wx.CB_DROPDOWN|wx.CB_SORT)
		listOfZone=Zone.getListOfZone()
		lt=[]
		for l in listOfZone:
			t=Zone(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
		wx.StaticText(self.panel1, label="Zone :", pos=(15,60))
		self.cboxChoixZone = wx.ComboBox(self.panel1, -1,choices=lt,pos=(80, 65),style=wx.CB_DROPDOWN|wx.CB_SORT)
		
		wx.StaticBox(self.panel1, -1, 'Declencheur', (5, 5), size=(300, 200))
		wx.StaticBox(self.panel1, -1, 'Evenement', (305, 5), size=(400, 200))
		
		listOfTypeEvent=Event.getTypeEvent()
		lt=[]
		for l in listOfTypeEvent:
			lt.append(str(l) + " | "   + listOfTypeEvent[l])
		wx.StaticText(self.panel1, label="Type :", pos=(320,30))
		self.cboxChoixTypeEvent = wx.ComboBox(self.panel1, -1,choices=lt,pos=(380, 35),style=wx.CB_DROPDOWN|wx.CB_SORT)
		
		if id>0:
			self.trigger=Trigger(id)		
			
		#~ self.save=wx.Button(self.panel1, -1, "Save", (50,50))
		#~ self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		#~ self.delete=wx.Button(self.panel1, -1, "Delete", (130,50))
		#~ self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
			
	def onSave(self,event):
		self.trigger=Trigger(self.id)
		self.trigger.setName(self.editname.GetValue())
		self.id=self.trigger.saveToBDD()
		#~ self.pc.showAllKeywords()
		
	
	def onDelete(self,event):
		self.trigger=Trigger(self.id)
		self.trigger.deleteFromBDD()
		#~ self.pc.showAllKeywords()
		self.Destroy()