import wx
from shimstar.character.skill import *

class skillsearchPanel(wx.MDIChildFrame):
	def __init__(self, parent,editTxt):		
		self.editTxt=editTxt
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de skill",size=(500,500),pos=(200,300))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(500,500))
		self.parent=parent
		listOfSkills=Skill.getListOfSkills()
		wx.StaticBox(self.panel1, -1, 'Liste des skills', pos=(0, 100), size=(440, 450))
		self.listSkills=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(400,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseSkills, self.listSkills)
		self.listSkills.Clear()
		for t in listOfSkills:
			it=Skill(int(t))
			self.listSkills.Insert(str(t) + " | " + it.getName()[:40],0)
		self.SetAutoLayout(True)
		self.Layout()
	
	def	onChooseSkills(self,evt):
		tab=self.listSkills.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=Skill(idItem)
		self.editTxt.SetValue(str(idItem) + " | " + itemChoosed.getName())
		self.Destroy()
			
			