import wx
from shimstar.item.typeitem import *
from shimstar.item.engine import *
from shimstar.item.weapon import *
from shimstar.item.ship import *
from shimstar.gui.item.wxitem import *

class ItemWeaponPanel(ItemPanel):
	def __init__(self, parent,idItem,idTemplate,tpItem=0,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Item",size=(300,300),pos=(400,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300))
		self.prt=prt
		self.item=None
		self.parent=parent
		
		#~ face = wx.BitmapButton(self.panel1, -1, wx.Bitmap("faces/" + pnjChoosed.getFace() + ".png"))
		if idItem>0 or idTemplate>0:
			print "itempanel " + str(idItem) + "/" + str(idTemplate)
			itemChoosed=ShimstarItem(idItem,idTemplate)
			self.item=None
			self.item=ShimstarItem(idItem,idTemplate)
			if self.item!=None:
				self.img = wx.BitmapButton(self.panel1, -1, wx.Bitmap("items/" + self.item.getImg() + ".png"))
				self.imgName=self.item.getImg() + ".png"
				self.Bind(wx.EVT_BUTTON, self.onChooseImg, self.img)
				self.lblname = wx.StaticText(self, label="Name :", pos=(80,15))
				self.editname = wx.TextCtrl(self, value=self.item.getName(), pos=(120, 10), size=(140,-1))
				self.typeNamelbl = wx.StaticText(self, label="Type :", pos=(80,40))
				self.listOfType=typeItem.getListOfTypeItem()
				lt=[]
				selected=""
				for l in self.listOfType:
					t=typeItem(l)
					lt.append(str(t.getId()) + " | "   + t.getName())
				self.cboxChoixType = wx.ComboBox(self.panel1, -1,choices=lt,pos=(120,35),style=wx.CB_DROPDOWN|wx.CB_SORT)
				self.cboxChoixType.SetStringSelection(str(self.item.getTypeItem()) + " | " + self.item.getTypeLabel())
				
				self.showWeapon()
					
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
			
			self.showWeapon()
			
		self.save=wx.Button(self.panel1, -1, "Save", (100,230))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (200,230))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
		
	def onDelete(self,args):
		if self.item!=None:
			listOfItemInstanciated=ShimstarItem.getListOfInstanciedObject(self.item.getTemplate())
			if len(listOfItemInstanciated)==0:
				wea=Weapon(self.item.getTemplate(),self.item.getSpecific())
				wea.delete()
				self.prt.showAllTemplate()
				self.Destroy()
			else:
				dlg = wx.MessageDialog(self.parent, "Il existe des objets lies a ce template, vous ne pouvez pas supprimer le template", "No", wx.OK | wx.ICON_INFORMATION)
				dlg.ShowModal()
				dlg.Destroy()
				
			
	def showWeapon(self):
		self.lblDamage=self.lblname = wx.StaticText(self.panel1, label="Dommage :", pos=(10,100))
		self.damage= wx.TextCtrl(self.panel1,value="", pos=(80, 100), size=(60,-1) )
		self.lblRange= wx.StaticText(self.panel1, label="Portee :", pos=(10,120))
		self.range= wx.TextCtrl(self.panel1,value="", pos=(80, 120), size=(60,-1) )
		self.lblCadence= wx.StaticText(self.panel1, label="Cadence :", pos=(10,140))
		self.cadence= wx.TextCtrl(self.panel1,value="", pos=(80, 140), size=(60,-1) )
		self.lblSpeed= wx.StaticText(self.panel1, label="Vitesse :", pos=(10,160))
		self.speed= wx.TextCtrl(self.panel1,value="", pos=(80, 160), size=(60,-1) )
		self.lblEgg= wx.StaticText(self.panel1, label="Egg :", pos=(10,180))
		self.egg= wx.TextCtrl(self.panel1,value="", pos=(80, 180), size=(120,-1) )
		self.chooseEgg=wx.Button(self.panel1, -1, "Choisir", (200,180))
		self.Bind(wx.EVT_BUTTON, self.chooseEggDlg, self.chooseEgg)
		if self.item!=None:
			wea=Weapon(self.item.getTemplate(),self.item.getSpecific())
			self.damage.SetValue(str(wea.getDamage()))
			self.range.SetValue(str(wea.getRange()))
			self.cadence.SetValue(str(wea.getCadence()))
			self.speed.SetValue(str(wea.getSpeed()))
			self.egg.SetValue(str(wea.getEgg()))
			
			
	def onSave(self,event):
		if self.item==None:
			tab=self.cboxChoixType.GetValue().split(" | ")
			itemToSave=Weapon(0,0,True)
		else:
			itemToSave=Weapon(self.item.getTemplate(),self.item.getSpecific())
		itemToSave.setName(self.editname.GetValue())
		tab=self.cboxChoixType.GetValue().split(" | ")
		if len(tab)>0:
			itemToSave.setTypeItem(int(tab[0]))
		itemToSave.setImg(self.imgName.split('.')[0])
		itemToSave.setSpeed(self.speed.GetValue())
		itemToSave.setRange(self.range.GetValue())
		itemToSave.setCadence(self.cadence.GetValue())
		itemToSave.setDamage(self.damage.GetValue())
		itemToSave.setEgg(self.egg.GetValue())
		
		itemToSave.saveToBDD()
		self.prt.showAllTemplate()
		self.Destroy()
	
	