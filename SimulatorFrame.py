import wx
import os
import clips
import time

from SimulatorPanel import MyPanel
from Office import Office

class SimulatorFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (1200, 800) )
        self.dirname = ''
        self.filename = ''
        self.clipsFile = ''
        self.simClipsFile = ''
        self.simEventsFile = ''

        # create office object
        self.office = Office()

        # create a panel in the frame
        self.pnl = MyPanel(self, -1)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Oficina inteligente 0.1")

        # output text frame
        self.OutputFrame = OutputFrame(self, "Salidas")
        self.OutputFrame.Show()


    def makeMenuBar(self):
        fileMenu = wx.Menu()
        loadItem = fileMenu.Append(-1, "Cargar...\tCtrl-L", "Cargar fichero .clp")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        oficinaMenu = wx.Menu()
        nuevoCicloItem = oficinaMenu.Append(-1, "Increme&ntar ciclo\tCtrl-N", "Nuevo ciclo")
        lanzarSimulacionItem = oficinaMenu.Append(-1, "Lanzar &simulacion\tCtrl-S", "Simulacion completa")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&Archivo")
        menuBar.Append(oficinaMenu, "&Oficina")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnOpen,  loadItem)
        self.Bind(wx.EVT_MENU, self.OnNuevoCiclo, nuevoCicloItem)
        self.Bind(wx.EVT_MENU, self.OnLanzarSimulacion, lanzarSimulacionItem)

    def OnExit(self, event):
        self.Close(True)

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Selecciona archivo", self.dirname, "", "*.clp", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
        self.dirname = dlg.GetDirectory()
        if(self.filename != ""):
            self.clipsFile = os.path.join(self.dirname, self.filename)
            self.simClipsFile = os.path.join(self.dirname, 'simulacionoficina.bin')
            self.simEventsFile = os.path.join(self.dirname, 'Simulacion.txt')
            clips.Clear()
            clips.BatchStar(self.clipsFile)
            clips.BatchStar(self.simClipsFile)
            clips.Reset()
            f = open(self.simEventsFile)
            events_lines = f.read().splitlines()
            for e in events_lines:
                if not ";" in e:
                    clips.Assert(e)
            f.close()
            clips.Assert("(ciclo 0)")

            # clips.PrintFacts()
            # clips.PrintRules()
            clips.Run()
            self.SetStatusText(self.clipsFile)
            self.office.updatePeopleLocation()
            self.Refresh()

            self.OutputFrame.box.Clear()
            self.OutputFrame.appendText("[sys] Iniciar simulacion " + time.strftime("%c"))
        dlg.Destroy()


    def OnNuevoCiclo(self, event):
        """Incrementar ciclo de la simulacion"""
        if self.clipsFile != "":
            clips.Assert("(Seguir S)")
            clips.Run()
            self.office.updatePeopleLocation()
            self.Refresh()
            error = clips.ErrorStream.Read()
            if error != None:
                print(error)
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en ASSERT", wx.OK)
            dlg.ShowModal()

    def OnLanzarSimulacion(self, event):
        """Lanzar toda la simulacion"""
        if self.clipsFile != "":
            for i in range(50):
                clips.Assert("(Seguir S)")
                clips.Run()
                self.office.updatePeopleLocation()
                self.Refresh()
        else:
            dlg = wx.MessageDialog(self, "No se ha cargado fichero .clp", "Error en ASSERT", wx.OK)
            dlg.ShowModal()

class OutputFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size = (400, 300) )
        self.box = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE, size = (400, 300))

    def appendText(self, text):
        for line in text.split('\n'):
            if "[sys]" in line:
                self.box.SetDefaultStyle(wx.TextAttr(wx.LIGHT_GREY))
                self.box.AppendText(line.strip() + "\n")
            elif len(line) >= 1:
                self.box.SetDefaultStyle(wx.TextAttr(wx.BLACK))
                self.box.AppendText(line.strip() + "\n")