import sys
import os
import os.path as pth
import tkinter as tk

from . import gui_window_main, tabbed_view, py_iface

# Define the base directory
BASE_DIR = pth.abspath(pth.dirname(__file__))


def start():
    """
    Initializes and starts the numerical GUI application.
    """
    # Create the main numerical display window
    numerical_screen = gui_window_main.DefaultNumericalDisplay()

    # Create the tabbed view and add scenes
    tabs = tabbed_view.TabbedView(numerical_screen)
    tabs.buildTab(pth.join(BASE_DIR, "scenes"))
    tabs.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

    # Ensure window properly closes on user exit
    numerical_screen.wm_protocol("WM_DELETE_WINDOW", lambda: close_application(numerical_screen))

    # Start the Tkinter main loop
    numerical_screen.mainloop()


def close_application(window):
    """
    Handles the GUI window closing event.
    """
    print("Called Destroy")
    window.destroy()

