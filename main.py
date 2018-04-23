import wx
from SimulatorFrame import SimulatorFrame

import clips

def run():
    # Required:
    # Python 2.7
    # pip install - U wxPython

    app = wx.App()
    frm = SimulatorFrame(None, "Oficina Inteligente")
    frm.Show()
    app.MainLoop()

if __name__ == "__main__":
    run()