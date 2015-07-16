import wx
from shimstar.pnj.typedialog import *
from shimstar.pnj.dialog import *
from shimstar.gui.pnj.wxdialog import *

class DialogsPanel(wx.MDIChildFrame):
	def __init__(self, parent):		
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche de dialogues",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		listOfType=typeDialog.getListOfTypeDialogue()
		lt=[]
		for l in listOfType:
			t=typeDialog(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
		wx.StaticBox(self.panel1, -1, 'Type de dialogue', (0, 0), size=(240, 50))
		self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(10, 20),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.Bind(wx.EVT_COMBOBOX, self.onChooseTypeDialogue, self.cboxChoixType)
		wx.StaticBox(self.panel1, -1, 'Liste des Dialogues', pos=(0, 100), size=(240, 450))
		self.listDial=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseDial, self.listDial)
		self.addButton=wx.Button(self.panel1, -1, "Ajouter un nouveau dialogue", (10,490))
		self.Bind(wx.EVT_BUTTON, self.addDialog, self.addButton)
		self.SetAutoLayout(True)
		self.showAllTemplate()
		self.Layout()
		
	def addDialog(self,event):
		DialogPanel(self.parent,self,0)
		
	def showAllTemplate(self):
		tabTempl=typeDialog.getListOfDialogueByType(-1)
		self.listDial.Clear()
		for t in tabTempl:
			it=Dialog(int(t))
			self.listDial.Insert(str(t) + " | " + it.getText()[:40],0)
		
	def onChooseTypeDialogue(self,evt):
		if self.cboxChoixType.GetValue()!="":
			tab=self.cboxChoixType.GetValue().split(" | ")
			idTypeDial=int(tab[0])
		else:
			idTypeDial=-1
		tabTempl=typeDialog.getListOfDialogueByType(idTypeDial)
		self.listDial.Clear()
		for t in tabTempl:
			it=Dialog(int(t))
			self.listDial.Insert(str(t) + " | " + it.getText()[:40],0)
		
	def	onChooseDial(self,evt):
		tab=self.listDial.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=Dialog(idItem)
		DialogPanel(self.parent,self,idItem)
			
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			