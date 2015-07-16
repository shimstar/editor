import wx
from shimstar.pnj.typedialog import *
from shimstar.pnj.dialog import *
from shimstar.gui.character.wxskill import *
from shimstar.character.skill import *

class SkillsPanel(wx.MDIChildFrame):
	def __init__(self, parent):		
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de skills",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		listOfSkills=Skill.getListOfSkills()
		wx.StaticBox(self.panel1, -1, 'Liste des Skills', pos=(0, 100), size=(240, 450))
		self.listSkill=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		for s in listOfSkills:
			temp=Skill(s)
			self.listSkill.Insert(str(s) + " | " + temp.getName(),0)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseSkill, self.listSkill)
		self.addButton=wx.Button(self.panel1, -1, "Ajouter une nouvelle skill", (10,490))
		self.Bind(wx.EVT_BUTTON, self.addSkill, self.addButton)
		self.SetAutoLayout(True)
		self.Layout()
		
	def loadSkill(self):
		self.listSkill.Clear()
		listOfSkills=Skill.getListOfSkills()
		for s in listOfSkills:
			temp=Skill(s)
			self.listSkill.Insert(str(s) + " | " + temp.getName(),0)
		
	def addSkill(self,event):
		SkillPanel(self.parent,self,0)
		
	def	onChooseSkill(self,evt):
		tab=self.listSkill.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=Skill(idItem)
		SkillPanel(self.parent,self,idItem)
			
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			