import wx
from shimstar.item.typeitem import *
from shimstar.item.engine import *
from shimstar.item.weapon import *
from shimstar.item.ship import *
from shimstar.gui.item.wxitem import *
from shimstar.gui.item.wxitemengine import *
from shimstar.gui.item.wxitemweapon import *

class ChooseItemSlotPanel(wx.MDIChildFrame):
		def __init__(self, parent,idSlot,listOfType,prt=None):
			wx.MDIChildFrame.__init__(self,parent, -1, "Item",size=(300,300),pos=(400,100))
			self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300))
			self.prt=prt
			self.parent=parent
			self.slot=Slot(idSlot,0,False)
			self.listItem=wx.ListBox(self.panel1, 26, pos=(10, 50), size=(200,200),style=wx.LB_SINGLE)
			listOfItem=ShimstarItem.getListOfItemTemplatesByType(listOfType)
			
			for l in listOfItem:
				t=ShimstarItem(0,int(l))
				typei=t.getTypeItem()
				ti=typeItem(typei)
				self.listItem.Insert(str(ti.getName()) + " | "   + t.getName() + " | " + str(t.getTemplate()),0)
				
			self.Bind(wx.EVT_LISTBOX_DCLICK, self.chooseItem, self.listItem)
			
			btn=wx.Button(self.panel1, -1, "Info", (200,200))
			self.Bind(wx.EVT_BUTTON, self.showInfo, btn)
			
		def chooseItem(self,args):
			tab=self.listItem.GetStringSelection().split(' | ')
			itSlot=self.slot.getItem()
			changeItemSlot=False
			if itSlot!=None:
				if itSlot.getTemplate()!=int(tab[2]):
					changeItemSlot=True
			else:
				changeItemSlot=True
			if changeItemSlot==True:
				t=ShimstarItem(0,int(tab[2]))
				t.saveInstance()
				#~ print "#####" + str(t.getId())
				self.slot.setItem(t)
				self.slot.saveToBDD()
				self.prt.loadSlots()
			self.Destroy()
			
			
		def showInfo(self,args):
			tab=self.listItem.GetStringSelection().split(' | ')
			idItem=int(tab[2])
			itemChoosed=ShimstarItem(0,idItem)
			if itemChoosed.getTypeItem()==C_ITEM_ENGINE:
				ItemEnginePanel(self.parent,0,idItem,0,self)
			elif itemChoosed.getTypeItem()==C_ITEM_WEAPON:
				ItemWeaponPanel(self.parent,0,idItem,0,self)
			elif itemChoosed.getTypeItem()==C_ITEM_SHIP:
				ItemShipPanel(self.parent,0,idItem,0,self)
			else:
				ItemPanel(self.parent,0,idItem,0,self)
				

class ChooseTypeSlotPanel(wx.MDIChildFrame):
		def __init__(self, parent,idSlot,prt=None):
			wx.MDIChildFrame.__init__(self,parent, -1, "Item",size=(300,300),pos=(400,100))
			self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300))
			self.prt=prt
			self.parent=parent
			listOfType=typeItem.getListOfTypeItem()
			lt=[]
			self.listItem=wx.ListBox(self.panel1, 26, pos=(10, 50), size=(200,200),style=wx.LB_MULTIPLE)
			self.listItem.Clear()
			for l in listOfType:
				t=typeItem(l)
				self.listItem.Insert(str(t.getId()) + " | "   + t.getName(),0)
			self.chooseTypes=wx.Button(self.panel1, -1, "Choisir", (200,200))
			self.Bind(wx.EVT_BUTTON, self.chooseTypeAction, self.chooseTypes)
			self.slot=Slot(idSlot,0,False)
			
		def chooseTypeAction(self,args):
			li=self.listItem.GetSelections() 
			for i in li:
				tab=self.listItem.GetString(i).split('|')
				self.slot.addType(tab[0])
			self.prt.loadSlots()
			self.Destroy()
				
			
class ItemShipPanel(ItemPanel):
	def __init__(self, parent,idItem,idTemplate,tpItem=0,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Item",size=(300,300),pos=(400,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300))
		self.prt=prt
		self.item=None
		self.parent=parent
		self.slotsLbl=[]
		self.slotsInput=[]
		self.slotsBtn=[]
		self.slotsCb=[]
		self.slotsAddBtn=[]
		if idItem>0 or idTemplate>0:

			itemChoosed=ShimstarItem(idItem,idTemplate)
			self.item=None
			self.item=ShimstarItem(idItem,idTemplate)
			if self.item!=None:
				self.img = wx.BitmapButton(self.panel1, -1, wx.Bitmap("items/" + self.item.getImg() + ".png"))
				self.imgName=self.item.getImg() + ".png"
				self.Bind(wx.EVT_BUTTON, self.onChooseImg, self.img)
				self.lblname = wx.StaticText(self, label="Name :", pos=(80,15))
				self.editname = wx.TextCtrl(self.panel1, value=self.item.getName(), pos=(120, 10), size=(140,-1))
				self.typeNamelbl = wx.StaticText(self, label="Type :", pos=(80,40))
				self.listOfType=typeItem.getListOfTypeItem()
				lt=[]
				selected=""
				for l in self.listOfType:
					t=typeItem(l)
					lt.append(str(t.getId()) + " | "   + t.getName())
				self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(120,35),style=wx.CB_DROPDOWN|wx.CB_SORT)
				self.cboxChoixType.SetStringSelection(str(self.item.getTypeItem()) + " | " + self.item.getTypeLabel())
				self.showShip()
					
		else:
			self.img = wx.BitmapButton(self.panel1, -1, wx.Bitmap("items/blank.png"))
			self.Bind(wx.EVT_BUTTON, self.onChooseImg, self.img)
			self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(80,15))
			self.editname = wx.TextCtrl(self.panel1,value="", pos=(120, 10), size=(140,-1) )
			self.typeNamelbl = wx.StaticText(self.panel1, label="Type :", pos=(80,40))
			listOfType=typeItem.getListOfTypeItem()
			lt=[]
			selected=""
			for l in listOfType:
				t=typeItem(l)
				lt.append(str(t.getId()) + " | "   + t.getName())
			tItem=typeItem(tpItem)
			self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(120,35),style=wx.CB_DROPDOWN|wx.CB_SORT)
			self.cboxChoixType.SetStringSelection(str(tItem.getId()) + " | "   + tItem.getName())
			
			self.showShip()
		
		self.save=wx.Button(self.panel1, -1, "Save", (100,230))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (200,230))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
		
	def onDelete(self,args):
		if self.item!=None:
			listOfItemInstanciated=ShimstarItem.getListOfInstanciedObject(self.item.getTemplate())
			if len(listOfItemInstanciated)==0:
				sh=Ship(self.item.getTemplate(),self.item.getSpecific())
				sh.delete()
				self.prt.showAllTemplate()
				self.Destroy()
			else:
				dlg = wx.MessageDialog(self.parent, "Il existe des objets lies a ce template, vous ne pouvez pas supprimer le template", "No", wx.OK | wx.ICON_INFORMATION)
				dlg.ShowModal()
				dlg.Destroy()
				
	def chooseItemSlot(self,evt,idSlot,tempType):
		ChooseItemSlotPanel(self.parent,idSlot,tempType,self)
		
	def chooseTypeItemSlot(self,evt,idSlot):
		ChooseTypeSlotPanel(self.parent,idSlot,self)
				
	def showShip(self):
		self.SetSize((800,300))
		self.panel1.SetSize((800,300))
		self.lblHull= wx.StaticText(self.panel1, label="Coque :", pos=(10,100))
		self.hull= wx.TextCtrl(self.panel1,value="", pos=(120, 100), size=(60,-1) )
		self.lblMass= wx.StaticText(self.panel1, label="Mass :", pos=(10,120))
		self.masse= wx.TextCtrl(self.panel1,value="", pos=(120, 120), size=(60,-1) )
		self.lblTorque= wx.StaticText(self.panel1, label="Torque :", pos=(10,140))
		self.torque= wx.TextCtrl(self.panel1,value="", pos=(120, 140), size=(60,-1) )
		self.lblFAngular= wx.StaticText(self.panel1, label="Friction Angulaire:", pos=(10,160))
		self.FAngular= wx.TextCtrl(self.panel1,value="", pos=(120, 160), size=(60,-1) )
		self.lblFVelocity= wx.StaticText(self.panel1, label="Friction Vitesse:", pos=(10,180))
		self.FVelocity= wx.TextCtrl(self.panel1,value="", pos=(120, 180), size=(60,-1) )
		self.lblEgg= wx.StaticText(self.panel1, label="Egg :", pos=(10,200))
		self.egg= wx.TextCtrl(self.panel1,value="", pos=(80, 200), size=(120,-1) )
		self.chooseEgg=wx.Button(self.panel1, -1, "Choisir", (200,200))
		self.Bind(wx.EVT_BUTTON, self.chooseEggDlg, self.chooseEgg)
		if self.item!=None:
			ship=Ship(self.item.getTemplate(),self.item.getSpecific())
			self.hull.SetValue(str(ship.getHull()))
			self.masse.SetValue(str(ship.getMasse()))
			self.torque.SetValue(str(ship.getTorque()))
			self.FAngular.SetValue(str(ship.getFrictionAngular()))
			self.FVelocity.SetValue(str(ship.getFrictionVelocity()))
			self.egg.SetValue(str(ship.getEgg()))
			self.loadSlots()
				
	def loadSlots(self):
		ship=Ship(self.item.getTemplate(),self.item.getSpecific())
		#~ if len(self.slotsLbl)>0:
			#~ for s in self.slotsLbl:
				#~ s.Delete()
				
		slots=ship.getSlots()
		for s in self.slotsLbl:
			s.Destroy()
		self.slotsLbl=[]
		for s in self.slotsInput:
			s.Destroy()
		self.slotsInput=[]
		for s in self.slotsBtn:
			s.Destroy()
		self.slotsBtn=[]
		for s in self.slotsCb:
			s.Destroy()
		self.slotsCb=[]
		for s in self.slotsAddBtn:
			s.Destroy()
		self.slotsAddBtn=[]
		btn=wx.Button(self.panel1, -1, "Add Slot", (320,10))
		self.Bind(wx.EVT_BUTTON, self.addSlot, btn)
		i=1
		for s in slots:
			lbl=wx.StaticText(self.panel1, label="Slot "+ str(i) + " :", pos=(320,100 + (i-1)*20))
			self.slotsLbl.append(lbl)
			input= wx.TextCtrl(self.panel1,value="", pos=(580, 100 + (i-1)*20), size=(100,-1) )
			self.slotsInput.append(input)
			btn=wx.Button(self.panel1, -1, "Choisir", (700,100 + (i-1)*20))
			self.slotsBtn.append(btn)
			self.Bind(wx.EVT_BUTTON, lambda event,temp=s.getId(),tempType=s.getTypes():self.chooseItemSlot(event,temp,tempType), btn)
			btnAdd=wx.Button(self.panel1, -1, "Add", (480,100 + (i-1)*20))
			self.slotsAddBtn.append(btnAdd)
			self.Bind(wx.EVT_BUTTON, lambda event,temp=s.getId():self.chooseTypeItemSlot(event,temp), btnAdd)
			typesSlot=s.getTypes()
			
			#~ print typesSlot
			lt=[]
			for l in self.listOfType:
				if l in typesSlot:
					t=typeItem(l)
					lt.append(str(t.getId()) + " | "   + t.getName())
			cb = wx.ComboBox(self.panel1, -1,choices=lt,pos=(380,100 + (i-1)*20),style=wx.CB_DROPDOWN|wx.CB_SORT)
			self.slotsCb.append(cb)
			itemSlot=s.getItem()
			if itemSlot!=None:
				input.SetValue(str(itemSlot.getName()))
				cb.SetStringSelection(str(itemSlot.getTypeItem()) + " | " + itemSlot.getTypeLabel())
			i+=1
			
					
	def addSlot(self,args):
		slotToAdd=Slot(0,0,True)
		slotToAdd.setShip(self.item.getSpecific())
		ship=Ship(self.item.getTemplate(),self.item.getSpecific())
		ship.addSlot(slotToAdd)
		slotToAdd.saveToBDD()
		self.loadSlots()
	
	def onSave(self,event):
		if self.item==None:
			tab=self.cboxChoixType.GetValue().split(" | ")
			itemToSave=Ship(0,0,True)			
		else:
			itemToSave=Ship(self.item.getTemplate(),self.item.getSpecific())
		itemToSave.setTorque(self.torque.GetValue())
		itemToSave.setFrictionAngular(self.FAngular.GetValue())
		itemToSave.setFrictionVelocity(self.FVelocity.GetValue())
		itemToSave.setMasse(self.masse.GetValue())
		itemToSave.setHull(self.hull.GetValue())
		itemToSave.setEgg(self.egg.GetValue())
		itemToSave.setName(self.editname.GetValue())
		tab=self.cboxChoixType.GetValue().split(" | ")
		if len(tab)>0:
			itemToSave.setTypeItem(int(tab[0]))
		itemToSave.setImg(self.imgName.split('.')[0])
		itemToSave.saveToBDD()
		if self.prt!=None:
			self.prt.showAllTemplate()
		self.Destroy()
	
	def onChooseImg(self,event):
		dlg = wx.FileDialog(self, "Choose a file", "./images", "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
				filename = dlg.GetFilename()
				self.img.Destroy()
				self.img = wx.BitmapButton(self.panel1, -1, wx.Bitmap("items/" + filename))
				self.imgName=filename
				self.Bind(wx.EVT_BUTTON, self.onChooseImg, self.img)
		dlg.Destroy()
		
