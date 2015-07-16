import wx
from shimstar.gui.item.wxitem import *
from shimstar.item.typeitem import *
from shimstar.item.engine import *
from shimstar.item.weapon import *
from shimstar.item.ship import *

class ItemEnginePanel(ItemPanel):
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
			#~ if itemChoosed.getTypeLabel()=="ENGINE":
				#~ self.item=engine(idItem,idTemplate)
			self.item=ShimstarItem(idItem,idTemplate)
			#~ print self.item
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
				
				self.showEngine()
					
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
			
			self.showEngine()
			
		self.save=wx.Button(self.panel1, -1, "Save", (100,230))
		self.Bind(wx.EVT_BUTTON, self.onSave, self.save)
		self.delete=wx.Button(self.panel1, -1, "Delete", (200,230))
		self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete)
		
	def onDelete(self,args):
		if self.item!=None:
			listOfItemInstanciated=ShimstarItem.getListOfInstanciedObject(self.item.getTemplate())
			if len(listOfItemInstanciated)==0:
				eng=engine(self.item.getTemplate(),self.item.getSpecific())
				eng.delete()
				self.prt.showAllTemplate()
				self.Destroy()
			else:
				dlg = wx.MessageDialog(self.parent, "Il existe des objets lies a ce template, vous ne pouvez pas supprimer le template", "No", wx.OK | wx.ICON_INFORMATION)
				dlg.ShowModal()
				dlg.Destroy()
								
			
	def showEngine(self):		
		self.lblAcceleration=self.lblname = wx.StaticText(self.panel1, label="Acceleration :", pos=(10,100))
		self.acceleration= wx.TextCtrl(self.panel1,value="", pos=(120, 100), size=(60,-1) )
		self.lblSpeed= wx.StaticText(self.panel1, label="Vitesse :", pos=(10,120))
		self.speed= wx.TextCtrl(self.panel1,value="", pos=(120, 120), size=(60,-1) )
		
		if self.item!=None:
			eng=engine(self.item.getTemplate(),self.item.getSpecific())
			self.speed.SetValue(str(eng.getSpeedMax()))
			self.acceleration.SetValue(str(eng.getAcceleration()))
			
	def onSave(self,event):
		if self.item==None:
			itemToSave=engine(0,0,True)		
		else:
			itemToSave=engine(self.item.getTemplate(),self.item.getSpecific())
		itemToSave.setName(self.editname.GetValue())
		tab=self.cboxChoixType.GetValue().split(" | ")
		if len(tab)>0:
			itemToSave.setTypeItem(int(tab[0]))

		itemToSave.setImg(self.imgName.split('.')[0])
		itemToSave.setSpeedMax(self.speed.GetValue())
		itemToSave.setAcceleration(self.acceleration.GetValue())
		itemToSave.saveToBDD()
		self.prt.showAllTemplate()
		self.Destroy()
	
	