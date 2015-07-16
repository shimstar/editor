import wx
from constantes import *
from shimstar.item.typeitem import *
from shimstar.item.engine import *
from shimstar.gui.item.wxitem import *
from shimstar.gui.item.wxitemengine import *
from shimstar.gui.item.wxitemweapon import *
from shimstar.gui.item.wxitemship import *

class ItemsPanel(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self,parent, -1, "Recherche d'items",size=(300,800))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,800))
		self.parent=parent
		listOfType=typeItem.getListOfTypeItem()
		lt=[]
		for l in listOfType:
			t=typeItem(l)
			lt.append(str(t.getId()) + " | "   + t.getName())
		wx.StaticBox(self.panel1, -1, 'Type d''objets', (0, 0), size=(240, 50))
		self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(10, 20),style=wx.CB_DROPDOWN|wx.CB_SORT)
		self.createNew=wx.Button(self.panel1, -1, "Creer", (120,20))
		self.Bind(wx.EVT_BUTTON, self.onCreateNew, self.createNew)
		self.Bind(wx.EVT_COMBOBOX, self.onChooseTypeItem, self.cboxChoixType)
		wx.StaticBox(self.panel1, -1, 'Recherche', pos=(0, 50), size=(240, 50))
		self.search = wx.TextCtrl(self, -1, '', pos= (10, 70), style=wx.TE_RIGHT)
		wx.StaticBox(self.panel1, -1, 'Liste des templates', pos=(0, 100), size=(240, 450))
		self.listItem=wx.ListBox(self.panel1, 26, pos=(10, 120), size=(200,350),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseTplItem, self.listItem)
		
		self.SetAutoLayout(True)
		self.showAllTemplate()
		self.Layout()
		
	def onCreateNew(self,evt):
		tab=self.cboxChoixType.GetValue().split(" | ")
		idTypeItem=int(tab[0])
		if idTypeItem==C_ITEM_ENGINE:
			ItemEnginePanel(self.parent,0,0,idTypeItem,self)
		elif idTypeItem==C_ITEM_WEAPON:
			ItemWeaponPanel(self.parent,0,0,idTypeItem,self)
		elif idTypeItem==C_ITEM_SHIP:
			ItemShipPanel(self.parent,0,0,idTypeItem,self)
		else:
			ItemPanel(self.parent,0,0,idTypeItem,self)
			
	
	def showAllTemplate(self):
		tabTempl=typeItem.getListOfItemByTypeItem(-1)
		self.listItem.Clear()
		for t in tabTempl:
			it=ShimstarItem(0,int(t))
			self.listItem.Insert(str(t) + " | " + it.getTypeItemLabel()+ " | " + it.getName(),0)
			
		
	def onChooseTypeItem(self,evt):
		tab=self.cboxChoixType.GetValue().split(" | ")
		idTypeItem=int(tab[0])
		tabTempl=typeItem.getListOfItemByTypeItem(idTypeItem)
		self.listItem.Clear()
		for t in tabTempl:
			it=ShimstarItem(0,t)
			self.listItem.Insert(str(t) + " | " + it.getTypeItemLabel()+ " | " + it.getName(),0)
				
		
	def	onChooseTplItem(self,evt):
		tab=self.listItem.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=ShimstarItem(0,idItem)
		if itemChoosed.getTypeItem()==C_ITEM_ENGINE:
			ItemEnginePanel(self.parent,0,idItem,0,self)
		elif itemChoosed.getTypeItem()==C_ITEM_WEAPON:
			ItemWeaponPanel(self.parent,0,idItem,0,self)
		elif itemChoosed.getTypeItem()==C_ITEM_SHIP:
			ItemShipPanel(self.parent,0,idItem,0,self)
		else:
			ItemPanel(self.parent,0,idItem,0,self)
	
	def Destroy(self,evt):
		self.parent.activeWindows.remove(self)
		evt.Skip()
			