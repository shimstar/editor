import wx
from shimstar.zone.zone import *

class ZonePanel(wx.MDIChildFrame):
		def __init__(self, parent,idZone,prt=None):
			wx.MDIChildFrame.__init__(self,parent, -1, "Zone",size=(800,800),pos=(400,100))
			self.panel1 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300),pos=(0,0))
			self.panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300),pos=(320,0))
			self.panel3 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER,size=(300,300),pos=(320,320))
			self.prt=prt
			self.parent=parent
			self.idZone=idZone
			self.zone=Zone(self.idZone)
			self.panel1.Bind(wx.EVT_PAINT, self.on_paint) 
			
			
		def on_paint(self, event):
			dc = wx.PaintDC(self.panel1)
			dc.SetPen(wx.Pen('blue', 5))
			dc3 = wx.PaintDC(self.panel3)
			dc3.SetPen(wx.Pen('blue', 5))
			dc2 = wx.PaintDC(self.panel2)
			dc2.SetPen(wx.Pen('blue', 5))
			#~ dc.DrawCircle(10,10,1)
			listOfAster=self.zone.getListOfAsteroid()
			for a in listOfAster:
				ast=Asteroid(a)
				posX,posY,posZ=ast.getPos()
				dc.DrawCircle(posX/4+150,posY/4+150,1)
				dc2.DrawCircle(posY/4+150,posZ/4+150,1)
				dc3.DrawCircle(posX/4+150,posZ/4+150,1)
		
		