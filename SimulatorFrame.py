import wx
import os
import clips

from SimulatorPanel import MyPanel
from Office import Office

class SimulatorFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (1200, 800) )
        self.dirname = ''
        self.filename = ''
        self.clipsFile = ''

        # create office object
        self.office = Office()

        # create a panel in the frame
        self.pnl = MyPanel(self, -1)

        # and put some text with a larger bold font on it
        # st = wx.StaticText(self.pnl, label="Oficina Inteligente", pos=(100, 60))
        # font = st.GetFont()
        # font.PointSize += 10
        # font = font.Bold()
        # st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Oficina inteligente 0.1")

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        loadItem = fileMenu.Append(-1, "&Cargar...\tCtrl-L", "Cargar fichero .clp")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        clipsMenu = wx.Menu()
        resetItem = clipsMenu.Append(-1, "Re&set\tCtrl-S", "Reset")
        runItem   = clipsMenu.Append(-1, "&Run\tCtrl-R", "Run")

        oficinaMenu = wx.Menu()
        solicitudTGItem = oficinaMenu.Append(-1, "&Nueva solicitud TG\tCtrl-G", "Nueva solicitud TG")
        solicitudTEItem = oficinaMenu.Append(-1, "&Nueva solicitud TE\tCtrl-E", "Nueva solicitud TE")
        disponibleE1 = oficinaMenu.Append(-1, "Disponible E1", "Disponible E1")
        disponibleE2 = oficinaMenu.Append(-1, "Disponible E2", "Disponible E2")
        disponibleG1 = oficinaMenu.Append(-1, "Disponible G1", "Disponible G1")
        disponibleG2 = oficinaMenu.Append(-1, "Disponible G2", "Disponible G2")
        disponibleG3 = oficinaMenu.Append(-1, "Disponible G3", "Disponible G3")
        disponibleG4 = oficinaMenu.Append(-1, "Disponible G4", "Disponible G4")
        disponibleG5 = oficinaMenu.Append(-1, "Disponible G5", "Disponible G5")

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&Archivo")
        # menuBar.Append(clipsMenu, "&CLIPS")
        menuBar.Append(oficinaMenu, "&Oficina")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen,  loadItem)

        self.Bind(wx.EVT_MENU, self.OnReset, resetItem)
        self.Bind(wx.EVT_MENU, self.OnRun,   runItem)

        self.Bind(wx.EVT_MENU, self.OnSolicitudTG, solicitudTGItem)
        self.Bind(wx.EVT_MENU, self.OnSolicitudTE, solicitudTEItem)
        self.Bind(wx.EVT_MENU, self.OnDisponibleE1, disponibleE1)
        self.Bind(wx.EVT_MENU, self.OnDisponibleE2, disponibleE2)
        self.Bind(wx.EVT_MENU, self.OnDisponibleG1, disponibleG1)
        self.Bind(wx.EVT_MENU, self.OnDisponibleG2, disponibleG2)
        self.Bind(wx.EVT_MENU, self.OnDisponibleG3, disponibleG3)
        self.Bind(wx.EVT_MENU, self.OnDisponibleG4, disponibleG4)
        self.Bind(wx.EVT_MENU, self.OnDisponibleG5, disponibleG5)

        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)


    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Selecciona archivo", self.dirname, "", "*.clp", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
        self.dirname = dlg.GetDirectory()
        if(self.filename != ""):
            self.clipsFile = os.path.join(self.dirname, self.filename)
            clips.BatchStar(self.clipsFile)
            clips.Reset()
            clips.Run()
            self.SetStatusText(self.clipsFile)
            self.office.updatePeopleLocation()
            self.Refresh()
        dlg.Destroy()

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Oficina inteligente 0.1.",
                      "Acerca de Oficina Inteligente",
                      wx.OK|wx.ICON_INFORMATION)

    def OnReset(self, event):
        """Reset"""
        if self.clipsFile != "":
            clips.Reset()
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en RESET", wx.OK)
            dlg.ShowModal()

    def OnRun(self, event):
        """Run"""
        if self.clipsFile != "":
            clips.Run()
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en RUN", wx.OK)
            dlg.ShowModal()

    def OnSolicitudTG(self, event):
        """TramitesGenerales"""
        if self.clipsFile != "":
            clips.Assert("(Solicitud TramitesGenerales)")
            clips.Run()
            self.office.updatePeopleLocation()
            self.Refresh()
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en ASSERT", wx.OK)
            dlg.ShowModal()

    def OnSolicitudTE(self, event):
        """TramitesEspeciales"""
        if self.clipsFile != "":
            clips.Assert("(Solicitud TramitesEspeciales)")
            clips.Run()
            self.office.updatePeopleLocation()
            self.Refresh()
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en ASSERT", wx.OK)
            dlg.ShowModal()

    def OnDisponibleE1(self, event):
        self.ProcessAssertDisponible("E1")

    def OnDisponibleE2(self, event):
        self.ProcessAssertDisponible("E2")

    def OnDisponibleG1(self, event):
        self.ProcessAssertDisponible("G1")

    def OnDisponibleG2(self, event):
        self.ProcessAssertDisponible("G2")

    def OnDisponibleG3(self, event):
        self.ProcessAssertDisponible("G3")

    def OnDisponibleG4(self, event):
        self.ProcessAssertDisponible("G4")

    def OnDisponibleG5(self, event):
        self.ProcessAssertDisponible("G5")

    def ProcessAssertDisponible(self, who):
        if self.clipsFile != "":
            fact = "(Disponible " + who + ")"
            clips.Assert(fact)
            clips.Run()
            self.office.updatePeopleLocation()
            self.Refresh()
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en ASSERT", wx.OK)
            dlg.ShowModal()
