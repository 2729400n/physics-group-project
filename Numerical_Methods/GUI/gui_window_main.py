import tkinter as tk


class NumericalDisplay(tk.Tk):
    """
    Base class for numerical display GUI.
    """

    def __init__(self, master=None, baseName=None, className="Tk", useTk=True,
                 sync=False, use=None, **kw):
        super().__init__(master, baseName, className, useTk, sync, use, **kw)
        self.decorate_window()
        self.populate_window()

    def decorate_window(self):
        """Sets up the window title and appearance."""
        self.title('Electrostatic Project')

    def populate_window(self):
        """Placeholder for UI elements."""
        pass


class DefaultNumericalDisplay(NumericalDisplay):
    """
    Default GUI window with a menu bar.
    """

    def __init__(self, screenName=None, baseName=None, className="Tk",
                 useTk=True, sync=False, use=None, **kw):
        super().__init__(screenName, baseName, className, useTk, sync, use, **kw)
        self.setup_menu_bar()

    def setup_menu_bar(self):
        """Creates and configures the menu bar."""
        self.winfo_toplevel().option_add('*tearOff', False)
        self.mbar = tk.Menu(self)

        # File Menu
        self.file_menu = tk.Menu(self.mbar, name='file_menu')
        self.mbar.add_cascade(menu=self.file_menu, label='File')

        # Edit Menu
        self.edit_menu = tk.Menu(self.mbar, name='edit_menu')
        self.mbar.add_cascade(menu=self.edit_menu, label='Edit')

        # Assign to the root menu
        self.config(menu=self.mbar)


def test_prod():
    """
    Runs the GUI in standalone mode.
    """
    root = DefaultNumericalDisplay()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()


if __name__ == '__main__':
    test_prod()
