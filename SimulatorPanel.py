import wx

class MyPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.parent = parent
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.office = parent.office                 # alias for attached office object

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)

        font = self.dc.GetFont()
        font.SetPointSize(18)
        self.dc.SetFont(font)
        if self.office.hora != '' and self.office.minutos != '' and self.office.segundos != '':
            self.dc.DrawText(self.office.hora + ":" + self.office.minutos.zfill(2) + ":" + self.office.segundos.zfill(2), 120, 60)
        if self.office.ciclo != '':
            self.dc.DrawText("Ciclo: " + self.office.ciclo, 350, 60)

        font = self.dc.GetFont()
        font.SetPointSize(8)
        self.dc.SetFont(font)

        self.dc.SetPen(wx.Pen("black", style=wx.SOLID))
        self.dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
        self.dc.DrawRectangle(120, 100, 980, 500)

        for r in self.office.rooms:
            self.dc.SetPen(wx.Pen(self.getRoomBorderColor(r), style=wx.SOLID))
            self.dc.SetBrush(wx.Brush(self.getRoomFillColor(r), wx.SOLID))
            pos = self.getRoomPosition(r)
            self.dc.DrawRectangle(pos[0], pos[1], pos[2], pos[3])

            n_people = 0
            for i, p in enumerate(r.getPeople()):
                dispX = 0
                dispX_text = 0
                dispY = 30 * (n_people + 1)
                n_people += 1
                fill = self.getPersonFillColor(p)
                self.dc.SetPen(wx.Pen(self.getPersonBorderColor(p), style=wx.SOLID, width=3))
                self.dc.SetBrush(wx.Brush(fill, wx.SOLID))
                self.dc.DrawCircle(pos[0] + 30 + dispX, pos[1] + dispY, 8)
                self.dc.SetTextForeground(self.getPersonFontColor(p))
                self.dc.DrawText(p.getId(), pos[0] + 25 + dispX_text, pos[1] + dispY + 10)

        del self.dc

        text = self.office.getUpdatedText()
        if text != None:
            self.parent.OutputFrame.appendText(text)

    def getRoomPosition(self, room):
        if room.getId() == "Recepcion":
            return (120, 100, 180, 500)
        if room.getId() == "Pasillo":
            return (300, 300, 600, 100)
        if room.getId() == "Oficina1":
            return (300, 100, 120, 200)
        if room.getId() == "Oficina2":
            return (420, 100, 120, 200)
        if room.getId() == "Oficina3":
            return (540, 100, 120, 200)
        if room.getId() == "Oficina4":
            return (660, 100, 120, 200)
        if room.getId() == "Oficina5":
            return (780, 100, 120, 200)
        if room.getId() == "Gerencia":
            return (900, 100, 200, 250)
        if room.getId() == "OficinaDoble":
            return (900, 350, 200, 250)
        if room.getId() == "AseoHombres":
            return (300, 400, 240, 200)
        if room.getId() == "AseoMujeres":
            return (540, 400, 240, 200)
        if room.getId() == "Papeleria":
            return (780, 400, 120, 200)
        if room.getId() == 'Fuera':
            return (0, 100, 120, 500)
        return (0, 0, 100, 100)

    def getRoomBorderColor(self, room):
        if room.getId() == "Fuera":
            return "white"
        else:
            return "black"

    def getRoomFillColor(self, room):
        return "grey" if not room.light and not room.getId() == "Fuera" else "white"

    def getPersonBorderColor(self, person):
        id = person.getId()
        type = person.getType()
        tramite = person.getTramite()
        if tramite == "TG":
            return "blue"
        elif tramite == "TE":
            return "red"
        elif id == "Recepcionista":
            return "grey"
        else:
            return "green"

    def getPersonFillColor(self, person):
        id = person.getId()
        type = person.getType()
        tramite = person.getTramite()
        if type == "Usuario":
            return "white"
        else:
            return self.getPersonBorderColor(person)

    def getPersonFontColor(self, person):
        disp = person.getDisp()
        if disp == True:
            return "green"
        else:
            return "black"