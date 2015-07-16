import wx
from shimstar.pnj.pnj import *
from shimstar.pnj.typenpc import *
from shimstar.zone.station import *
from shimstar.pnj.dialog import *
from shimstar.gui.pnj.wxdialog import *

class PnjPanel(wx.MDIChildFrame):
	def __init__(self, parent,idpnj,prt=None):
		wx.MDIChildFrame.__init__(self,parent, -1, "Pnj",size=(800,600),pos=(400,100))
		self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(800,600))
		self.prt=prt
		self.idpnj=idpnj
		self.parent=parent
		self.pnj=PNJ(idpnj)
		self.imgName=self.pnj.getFace()
		self.img = wx.BitmapButton(self.panel1, -1, wx.Bitmap("faces/" + self.pnj.getFace() + ".png"))
		self.Bind(wx.EVT_BUTTON, self.onChooseImg, self.img)
		self.lblname = wx.StaticText(self.panel1, label="Name :", pos=(150,15))
		self.editname = wx.TextCtrl(self.panel1,value=self.pnj.getName(), pos=(200, 10), size=(140,-1) )
		listOfTypePnj=TypeNPC.getListOfTypeNpc()
		lt=[]
		for l in listOfTypePnj:
			lt.append(str(l) + " | " + listOfTypePnj[l])
		self.lbltype = wx.StaticText(self.panel1, label="type :", pos=(150,55))
		self.cboxTypePNJ = wx.ComboBox(self.panel1, -1,choices=lt,style=wx.CB_DROPDOWN|wx.CB_SORT,pos=(200,50))
		typeNpc=TypeNPC(self.pnj.getTypeNPC())
		self.cboxTypePNJ.SetStringSelection(str(self.pnj.getTypeNPC()) + " | " + typeNpc.getName())
		listOfStation=station.getListOfStation()
		lt=[]
		lt.append("")
		indexActualStation=-1
		i=1
		for s in listOfStation:
			lt.append(str(s) + " | " + listOfStation[s])
			if s==self.pnj.getZone():
				indexActualStation=i
			i+=1
		self.lblStation = wx.StaticText(self.panel1, label="station :", pos=(150,85))
		self.cboxStation = wx.ComboBox(self.panel1, -1,choices=lt,style=wx.CB_DROPDOWN|wx.CB_SORT,pos=(200,80))
		self.cboxStation.Select(indexActualStation)
		
		self.listDial=wx.ListBox(self.panel1, 26, pos=(15, 180), size=(500,100),style=wx.LB_SINGLE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onChooseDial, self.listDial)
		self.showDialog()
		
	def	onChooseDial(self,evt):
		tab=self.listDial.GetStringSelection().split(' | ')
		idItem=int(tab[0])
		itemChoosed=Dialog(idItem)
		DialogPanel(self.parent,self,idItem)
		
	def showDialog(self):
		dialogs=self.pnj.getDialogs()
		for d in dialogs:
			temp=Dialog(d)
			self.listDial.Insert(str(d) + " | " + temp.getText(),0)
		
	def onChooseImg(self,event):
		dlg = wx.FileDialog(self, "Choose a file", "./faces", "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			filename = dlg.GetFilename()
			self.img.Destroy()
			self.img = wx.BitmapButton(self.panel1, -1, wx.Bitmap("faces/" + filename))
			self.imgName=filename
			self.Bind(wx.EVT_BUTTON, self.onChooseImg, self.img)
		dlg.Destroy()