# -*- coding: iso-8859-1 -*-
import wx
from shimstar.character.skill import *
#~ import array
from shimstar.gui.character.wxskillsearch import *
#~ .encode('iso-8859-1') 

class SkillPanel(wx.MDIChildFrame):
	def __init__(self, parent,pc,id):
		wx.MDIChildFrame.__init__(self,parent, -1, "skill",size=(800,600),pos=(400,100))
		self.parent=parent
		self.id=id
		self.pc=pc
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(800,600))
		print "IIINNNNIIIT"
		self.entPar=[]
		self.cbPar=[]
		self.chbPar=[]
		self.supPar=[]
		self.stPar=[]
		
		if id>0:
			tempSkill=Skill(id)
			self.lblName= wx.StaticText(self.panel1, label="Nom :", pos=(5,15))
			self.editName= wx.TextCtrl(self.panel1, value=tempSkill.getName(), pos=(50, 10))
			self.lblDes= wx.StaticText(self.panel1, label="Description :", pos=(5,70))
			self.editDes= wx.TextCtrl(self.panel1, value=tempSkill.getText(), pos=(50, 90), size=(340,100),style=wx.TE_MULTILINE)
			self.cbBase = wx.CheckBox(self.panel1, label=': Compétence de base',pos=(5,40))
			self.cbBase.SetValue(tempSkill.getBase())
			wx.StaticBox(self.panel1, -1, 'Dependances', (5, 200), size=(600, 200))
			self.loadParents()
		else:
			self.lblName= wx.StaticText(self.panel1, label="Nom :", pos=(5,15))
			self.editName= wx.TextCtrl(self.panel1, value="", pos=(50, 10))
			self.lblDes= wx.StaticText(self.panel1, label="Description :", pos=(5,70))
			self.editDes= wx.TextCtrl(self.panel1, value="", pos=(50, 90), size=(340,100),style=wx.TE_MULTILINE)
			self.cbBase = wx.CheckBox(self.panel1, label=': Compétence de base',pos=(5,40))
			wx.StaticBox(self.panel1, -1, 'Dependances', (5, 200), size=(400, 200))
		
		self.addParent=wx.Button(self.panel1, -1, "Ajouter", (15,220))
		self.Bind(wx.EVT_BUTTON, self.onAddParent, self.addParent)
		
		self.save=wx.Button(self.panel1, -1, "Save", (50,450))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (130,450))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
		
	def loadParents(self):
		for a in self.entPar:
			a.Hide()
			a.Destroy()
		for a in self.cbPar:			
			a.Hide()
			a.Destroy()
		for a in self.chbPar:
			a.Hide()
			a.Destroy()
		for a in self.supPar:
			a.Hide()
			a.Destroy()
		for a in self.stPar:
			a.Hide()
			a.Destroy()
		tempSkill=Skill(self.id)
		i=0
		for s in tempSkill.getParents():
			self.entPar.append(wx.TextCtrl(self.panel1, value=str(s.getId()) + " | " + s.getName(), pos=(10, 250+i*30)))
			temp=wx.StaticText(self.panel1, label="Niveau :", pos=(120,255+i*30))
			self.stPar.append(temp)
			cb=wx.ComboBox(self.panel1, -1,choices=['1','2','3','4','5'],pos=(170, 250+i*30),style=wx.CB_DROPDOWN|wx.CB_SORT)
			cb.SetValue(str(s.getLevel()))
			self.cbPar.append(cb)
			ck=wx.CheckBox(self.panel1, label=': primaire',pos=(210,255+i*30))
			self.chbPar.append(ck)
			ck.SetValue(s.getIsPrimary())
			removeParentButton=wx.Button(self.panel1, -1, "Supprimer", (300,245+i*30))
			self.Bind(wx.EVT_BUTTON, lambda event: self.onRemoveParent(event, i), removeParentButton)
			self.supPar.append(removeParentButton)
		self.panel1.Refresh()
		
	def onAddParent(self,event):
		i=len(self.entPar)
		text=wx.TextCtrl(self.panel1, value="", pos=(10, 250+i*30))
		skillsearchPanel(self.parent,text)
		self.entPar.append(text)
		temp=wx.StaticText(self.panel1, label="Niveau :", pos=(120,255+i*30))
		cb=wx.ComboBox(self.panel1, -1,choices=['1','2','3','4','5'],pos=(170, 250+i*30),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.cbPar.append(cb)
		ck=wx.CheckBox(self.panel1, label=': primaire',pos=(210,255+i*30))
		self.chbPar.append(ck)
		removeParentButton=wx.Button(self.panel1, -1, "Supprimer", (300,245+i*30))
		self.Bind(wx.EVT_BUTTON, lambda event: self.onRemoveParent(event, i), removeParentButton)
		self.supPar.append(removeParentButton)
		
	def onRemoveParent(self,event,i):
		id=int(self.entPar[i].GetValue().split(" | ")[0])
		tempSkill=Skill(self.id)
		tempSkill.removeParent(id)
		self.loadParents()
		#~ itSelected=self.listSkill.GetSelection()
		#~ if itSelected!=-1:
			#~ self.listSkill.Delete(itSelected)
		
	def onChangeDep(self,event):
		DialogsearchPanel(self.parent,self.deptxt)
			
	def onSave(self,event):
		tempSkill=Skill(self.id)
		tempSkill.setName(self.editName.GetValue())
		tempSkill.setText(self.editDes.GetValue().replace('\n','\\\\1n'))
		if self.cbBase.GetValue():
			tempSkill.setBase(1)
		else:
			tempSkill.setBase(0)
			
		parents=[]
		for i in self.listSkill.GetItems():
			keyTab=i.split(" | ")
			par=Skill(int(keyTab[0]))
			parents.append(par)
			
		tempSkill.setParents(parents)
		
		tempSkill.saveToBDD()
		self.id=tempSkill.getId()
		self.pc.loadSkill()
		#~ dial=Dialog(self.id)
		#~ dial.setText(self.edittxt.GetValue().replace('\n','\\\\1n'))
		#~ dial.setProba(int(self.editproba.GetValue()))
		#~ if self.cbReadonce.GetValue():
			#~ dial.setReadOnce(1)
		#~ else:
			#~ dial.setReadOnce(0)
			
		#~ typeDiag=self.cboxChoixType.GetValue()
		#~ if typeDiag!="":
			#~ tabType=typeDiag.split(" | ")
			#~ idType=tabType[0]
			#~ dial.setTypeDialogue(int(idType))
			
		#~ dep=self.deptxt.GetValue()
		#~ if dep!="":
			#~ tabDep=dep.split(" | ")
			#~ idDiag=tabDep[0]
			#~ dial.setRefDialogue(int(idDiag))
			
		#~ dial.clearKeywords()
		#~ for i in self.listkeyw.GetItems():
			#~ keyTab=i.split(" | ")
			#~ dial.appendKeywords(int(keyTab[0]))
		
		#~ dial.saveToBDD()
		#~ self.id=dial.getId()
		#~ self.pc.onChooseTypeDialogue(None)
		
	
	def onDelete(self,event):
		pass
		#~ dial=Dialog(self.id)
		#~ dial.deleteFromBDD()
		#~ self.pc.onChooseTypeDialogue(None)
		#~ self.pc.showAllTemplate()
		#~ self.Destroy()
		