from . import gui_window_main, tabbed_view, py_iface

def start():
    numericalScreen =gui_window_main.DefaultNumericalDisplay()
    tabbed_view.buildTab()
    numericalScreen.mainloop()