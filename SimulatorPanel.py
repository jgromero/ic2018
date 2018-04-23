import wx

class MyPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.office = parent.office                 # alias for attached office object

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)

        font = self.dc.GetFont()
        font.SetPointSize(8)
        self.dc.SetFont(font)

        self.dc.SetPen(wx.Pen("black", style=wx.SOLID))
        self.dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
        self.dc.DrawRectangle(100, 100, 1000, 500)

        for r in self.office.rooms:
            self.dc.SetPen(wx.Pen(r.getBorderColor(), style=wx.SOLID))
            self.dc.SetBrush(wx.Brush(r.getFillColor(), wx.SOLID))
            pos = r.getPosition()
            self.dc.DrawRectangle(pos[0], pos[1], pos[2], pos[3])

            for i, p in enumerate(r.getEmployees()):
                self.dc.SetPen(wx.Pen(p.getBorderColor(), style=wx.SOLID))
                self.dc.SetBrush(wx.Brush(p.getFillColor(), wx.SOLID))
                self.dc.DrawCircle(pos[0] + 30, pos[1] + (30*(i+1)), 10)
                self.dc.SetPen(wx.Pen("black", style=wx.SOLID))
                self.dc.DrawText(p.getId(), pos[0] + 25, pos[1] + (30*(i+1)+10))

            for i, p in enumerate(r.getCustomers()):
                self.dc.SetPen(wx.Pen(p.getBorderColor(), style=wx.SOLID))
                self.dc.SetBrush(wx.Brush("white", wx.SOLID))
                self.dc.DrawCircle(pos[0] + 30 + 30, pos[1] + (30 * (i + 1)), 10)
                self.dc.SetPen(wx.Pen("black", style=wx.SOLID))
                self.dc.DrawText(p.getId(), pos[0] + 30 + 25, pos[1] + (30*(i + 1)+10))

        del self.dc