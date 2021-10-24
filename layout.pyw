import wx, wx.aui
import codecs
import math

from layout_reader import Layouts

class Key:
	def __init__(self, pos, ki, is_tall = False, is_tri = False):
		self.pos     = pos
				
		self.w = 50
		self.h = 75 if is_tall else 50
		self.rr = 8
		self.rect = wx.Rect(0, 0, self.w, self.h)
		self.rect.SetPosition(pos)
		
		self.is_tri = is_tri
		if is_tri:
			self.w = 105
			self.h = 60
		self.ki = ki
			
	def draw(self, context):
		if self.is_tri:
			shape = [	[self.pos[0], self.pos[1] + self.h],
						[self.pos[0], self.pos[1] + self.h // 2],
						[self.pos[0] + self.w // 2, self.pos[1]],
						[self.pos[0] + self.w, self.pos[1] + self.h // 2],
						[self.pos[0] + self.w, self.pos[1] + self.h],
						]
			context.DrawLines(shape)
		else:
			context.DrawRoundedRectangle(self.pos[0], self.pos[1], self.w, self.h, self.rr)
		
		dleft, dtop = (15, 10) if self.is_tri else (0, 0)
		for name, info in self.ki.items():
			ddleft = 3 * (len(name) - 1) if not self.is_tri else 0
			left = info["pos"][0] + dleft - ddleft
			left_limit = 30 if self.is_tri else 5
			if left < left_limit: left = left_limit
			pos = self.pos[0] + left, self.pos[1] + info["pos"][1] + dtop
			context.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_NORMAL, False), wx.Colour(info["rgb"]))
			context.DrawText(name, *pos)


class KeyPanelBig:
	def __init__(self, kset, ltr = True):
		self.keys = []
		self.tops = [20, 20, 10, 0, 10, 20, 20]
		left  = 10
		top   = 10
		sz    = 50
		pad   = 5
		nkeys = 7
		side  = 0 if ltr else 1
		for i in range(5):
			if i > 2: nkeys -= 1
			tops_ = self.tops[:nkeys]
			for nk, t in enumerate(tops_):
				
				left_ = left if ltr else 900 - left
				ksym = nk if ltr else -nk - 1
				ki = kset.get_key_info(side, i, ksym)
				self.keys.append(Key((left_, t + top), ki))
								
				left += sz + pad
			left = 10
			top += sz + pad
	
	def draw(self, context):
		for k in self.keys:
			k.draw(context)
	
class KeyPanelSmall:
	def __init__(self, kset, ltr = True):
		self.keys = []
		self.ltr = ltr
		left = 0
		top  = 0
		sz   = 50
		pad  = 5
		
		side = 0 if self.ltr else 1
		ki = kset.get_key_info(side, 5, 0)
		if self.ltr:
			self.keys.append(Key((left, top), ki, is_tall = True, is_tri = True))
		else:
			self.keys.append(Key((left + 55, top), ki, is_tall = True, is_tri = True))
		top += self.keys[-1].h + pad
		for i in range(3):
			ki = kset.get_key_info(side, 6, i)
			self.keys.append(Key((left, top), ki, is_tall = True))
			left += sz + pad
	
	def draw(self, context):
		if self.ltr:
			dx, dy, angle = 420, 0, math.pi / 6.0
		else:
			dx, dy, angle = 240, 475, -math.pi / 6.0
		for k in self.keys:
			context.Rotate(angle)
			context.Translate(dx, dy)
			k.draw(context)
			context.Translate(-dx, -dy)
			context.Rotate(-angle)

	
class TestPanel(wx.Panel):
	def __init__(self, parent, kbd):
		wx.Panel.__init__(self, parent, -1)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		
		self.left_panel_big   = KeyPanelBig  (kbd)
		self.left_panel_small = KeyPanelSmall(kbd)
		
		self.right_panel_big   = KeyPanelBig  (kbd, ltr = False)
		self.right_panel_small = KeyPanelSmall(kbd, ltr = False)
		
		# Drawing the keyboard into a bitmap
		self.bmp = wx.Bitmap(978, 485)
		dc = wx.MemoryDC()
		dc.SelectObject(self.bmp)
		dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, wx.ALPHA_OPAQUE)))
		dc.Clear()
		dc = wx.GraphicsContext.Create(dc)
		rgb = (200, 200, 200)
		dc.SetPen(wx.Pen(wx.Colour(*rgb, wx.ALPHA_OPAQUE)))
		dc.SetBrush(wx.Brush(wx.Colour(*rgb, 128)))

		self.left_panel_big.draw(dc)
		self.left_panel_small.draw(dc)
		
		self.right_panel_big.draw(dc)
		self.right_panel_small.draw(dc)
		
		
	def OnPaint(self, evt):
		pdc = wx.PaintDC(self)
		pdc.DrawBitmap(self.bmp, 0, 0)


class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
		
		self.control = wx.aui.AuiNotebook(self)
		
		lts = Layouts()
		lts.read("all_layouts.txt")
		
		for k, v in lts.sets.items():
			self.control.AddPage(TestPanel(self.control, v), k)
		
		self.windowSizer = wx.BoxSizer()
		self.windowSizer.Add(self.control, 1, wx.ALL|wx.EXPAND)
		
		self.SetSizer(self.windowSizer)
		self.SetSize(wx.Size((978, 485)))

app = wx.App()

frame = MainWindow(None, -1, "Window")
frame.Show(1)
app.MainLoop()
