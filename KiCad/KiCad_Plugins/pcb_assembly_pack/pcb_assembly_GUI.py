# PCB assembly GUI
import wx
import wx.xrc


class PCBAssemblyGUI ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"PCB Assembly Pack", pos = wx.DefaultPosition, size = wx.Size( 224,159 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Select Assembly sides:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.chkbox_top = wx.CheckBox( self, wx.ID_ANY, u"TOP Assembly", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chkbox_top.SetValue(True) 
		bSizer4.Add( self.chkbox_top, 0, wx.ALL, 5 )
		
		self.chkbox_bottom = wx.CheckBox( self, wx.ID_ANY, u"BOTTOM Assembly", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chkbox_bottom.SetValue(True) 
		bSizer4.Add( self.chkbox_bottom, 0, wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button3 = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

