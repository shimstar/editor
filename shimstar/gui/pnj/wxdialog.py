# -*- coding: iso-8859-1 -*-
import wx
from shimstar.pnj.dialog import *
from shimstar.gui.pnj.wxdialogsearch import *
from shimstar.pnj.typedialog import *
from shimstar.pnj.skeyword import *
from shimstar.gui.pnj.wxkeywordsearch import *
#~ .encode('iso-8859-1') 

class DialogPanel(wx.MDIChildFrame):
	def __init__(self, parent,pc,id):
		wx.MDIChildFrame.__init__(self,parent, -1, "dialogue",size=(800,600),pos=(400,100))
		self.parent=parent
		self.id=id
		self.pc=pc
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(800,600))
		self.keyword=None
		listOfType=typeDialog.getListOfTypeDialogue()
		lt=[]
		
		for l in listOfType:
			t=typeDialog(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
		if id>0:
			self.dial=Dialog(id)		
			self.lbltxt= wx.StaticText(self.panel1, label="Texte :", pos=(5,205))
			self.edittxt= wx.TextCtrl(self.panel1, value=self.dial.getText().replace('\\2n','\n \n').replace('\\1n','\n'), pos=(420, 10), size=(340,500),style=wx.TE_MULTILINE)
			wx.StaticBox(self.panel1, -1, 'Parametres', (5, 0), size=(400, 120))
			self.lblproba= wx.StaticText(self.panel1, label="Probabilite :", pos=(15,30))
			self.editproba= wx.TextCtrl(self.panel1, value=str(self.dial.getProba()), pos=(75, 25), size=(40,-1))
			self.cbReadonce = wx.CheckBox(self.panel1, label=': Lu une fois',pos=(15,55))
			self.cbReadonce.SetValue(self.dial.getReadOnce())
			wx.StaticText(self.panel1, label="Type :", pos=(15,85))
			self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(65, 80),style=wx.CB_DROPDOWN|wx.CB_SORT)
			typeDiag=typeDialog(self.dial.getTypeDialogue())
			self.cboxChoixType.SetValue(str(typeDiag.getId()) + " | " + typeDiag.getName())
			wx.StaticBox(self.panel1, -1, 'Dependance', (5, 130), size=(400, 50))
			self.lbldep= wx.StaticText(self.panel1, label="Dependance :", pos=(15,150))
			idDep=self.dial.getRefDialogue()
			if idDep>0:
				objDep=Dialog(idDep)
				self.deptxt= wx.TextCtrl(self, value=str(idDep) + "|" + objDep.getText(), pos=(85, 150), size=(200,-1))
			else:
				self.deptxt= wx.TextCtrl(self, value="", pos=(85, 150), size=(200,-1))
				
			wx.StaticBox(self.panel1, -1, 'Keywords', (5, 190), size=(400, 150))
			self.listkeyw=wx.ListBox(self.panel1, 26, pos=(10, 220), size=(200,100),style=wx.LB_SINGLE)
			for k in self.dial.getKeywords():
				tempK=Keyword(k)
				self.listkeyw.Insert(str(tempK.getId()) + " | " + tempK.getName(),0)
		else:
			#~ self.lbltxt= wx.StaticText(self.panel1, label="Texte :", pos=(5,195))
			#~ self.edittxt= wx.TextCtrl(self.panel1, value="", pos=(420, 10), size=(340,500),style=wx.TE_MULTILINE)
			#~ wx.StaticBox(self.panel1, -1, 'Parametres', (5, 0), size=(400, 100))
			#~ self.lblproba= wx.StaticText(self.panel1, label="Probabilite :", pos=(15,25))
			#~ self.editproba= wx.TextCtrl(self.panel1, value="100", pos=(75, 20), size=(40,-1))
			#~ self.cbReadonce = wx.CheckBox(self.panel1, label=': Lu une fois',pos=(15,60))
			#~ wx.StaticText(self.panel1, label="Type :", pos=(15,85))
			#~ self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(65, 80),style=wx.CB_DROPDOWN|wx.CB_SORT)
			#~ wx.StaticBox(self.panel1, -1, 'Dependance', (5, 110), size=(400, 50))
			#~ self.lbldep= wx.StaticText(self.panel1, label="Dependance :", pos=(15,130))
			#~ self.deptxt= wx.TextCtrl(self, value="", pos=(85, 130), size=(200,-1))
			#~ self.listkeyw=wx.ListBox(self.panel1, 26, pos=(10, 220), size=(200,100),style=wx.LB_SINGLE)
			self.edittxt= wx.TextCtrl(self.panel1, value="", pos=(420, 10), size=(340,500),style=wx.TE_MULTILINE)
			wx.StaticBox(self.panel1, -1, 'Parametres', (5, 0), size=(400, 120))
			self.lblproba= wx.StaticText(self.panel1, label="Probabilite :", pos=(15,30))
			self.editproba= wx.TextCtrl(self.panel1, value="100", pos=(75, 25), size=(40,-1))
			self.cbReadonce = wx.CheckBox(self.panel1, label=': Lu une fois',pos=(15,55))
			#~ self.cbReadonce.SetValue(self.dial.getReadOnce())
			wx.StaticText(self.panel1, label="Type :", pos=(15,85))
			self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(65, 80),style=wx.CB_DROPDOWN|wx.CB_SORT)
			#~ typeDiag=typeDialog(self.dial.getTypeDialogue())
			#~ self.cboxChoixType.SetValue(str(typeDiag.getId()) + " | " + typeDiag.getName())
			wx.StaticBox(self.panel1, -1, 'Dependance', (5, 130), size=(400, 50))
			self.lbldep= wx.StaticText(self.panel1, label="Dependance :", pos=(15,150))
			self.deptxt= wx.TextCtrl(self, value="", pos=(85, 150), size=(200,-1))
			wx.StaticBox(self.panel1, -1, 'Keywords', (5, 190), size=(400, 150))
			self.listkeyw=wx.ListBox(self.panel1, 26, pos=(10, 220), size=(200,100),style=wx.LB_SINGLE)
			
		self.changeDep=wx.Button(self.panel1, -1, "Dependance", (300,145))
		self.Bind(wx.EVT_BUTTON, self.onChangeDep, self.changeDep)
		
		self.addKeyword=wx.Button(self.panel1, -1, "Ajouter", (280,240))
		self.Bind(wx.EVT_BUTTON, self.onAddKeyword, self.addKeyword)
		
		self.deleteKeyword=wx.Button(self.panel1, -1, "Supprimer", (280,280))
		self.Bind(wx.EVT_BUTTON, self.onDeleteKeyword, self.deleteKeyword)
			
		self.save=wx.Button(self.panel1, -1, "Save", (50,450))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (130,450))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
		
	def onAddKeyword(self,evt):
		keywordsearchPanel(self.parent,self.listkeyw)
		
	def onDeleteKeyword(self,evt):
		itSelected=self.listkeyw.GetSelection()
		if itSelected!=-1:
			self.listkeyw.Delete(itSelected)
		
		
	def onChangeDep(self,event):
		DialogsearchPanel(self.parent,self.deptxt)
			
	def onSave(self,event):
		dial=Dialog(self.id)
		dial.setText(self.edittxt.GetValue().replace('\n','\\\\2n'))
		dial.setProba(int(self.editproba.GetValue()))
		if self.cbReadonce.GetValue():
			dial.setReadOnce(1)
		else:
			dial.setReadOnce(0)
			
		typeDiag=self.cboxChoixType.GetValue()
		if typeDiag!="":
			tabType=typeDiag.split(" | ")
			idType=tabType[0]
			dial.setTypeDialogue(int(idType))
			
		dep=self.deptxt.GetValue()
		if dep!="":
			tabDep=dep.split(" | ")
			idDiag=tabDep[0]
			dial.setRefDialogue(int(idDiag))
			
		dial.clearKeywords()
		for i in self.listkeyw.GetItems():
			keyTab=i.split(" | ")
			dial.appendKeywords(int(keyTab[0]))
		
		dial.saveToBDD()
		self.id=dial.getId()
		self.pc.onChooseTypeDialogue(None)
		
	
	def onDelete(self,event):
		dial=Dialog(self.id)
		dial.deleteFromBDD()
		self.pc.onChooseTypeDialogue(None)
		#~ self.pc.showAllTemplate()
		self.Destroy()