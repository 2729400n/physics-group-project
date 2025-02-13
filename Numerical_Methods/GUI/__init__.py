from . import gui_window_main, tabbed_view, py_iface

import os, os.path as pth
__base__ = pth.abspath(pth.dirname(__file__))


def start():
    numericalScreen =gui_window_main.DefaultNumericalDisplay()
    tabs=tabbed_view.TabbedView(numericalScreen)
    tabs.buildTab(pth.abspath(pth.join(__base__,'./scenes')))
    tabs.pack()
    numericalScreen.mainloop()