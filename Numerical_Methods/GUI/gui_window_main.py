import tkinter as tk


class NumericalDisplay(tk.Tk):

    def decorateWindow(self):
        self.title('Eletrostatic Project')

    def populateWindow(self):
        pass

    def __init__(self, master=None, baseName=None, className="Tk", useTk=True,
                 sync=False, use=None, **kw):

        tk.Tk.__init__(self, None, baseName, className=className,
                       useTk=useTk, sync=sync, use=use, **kw)
        self.decorateWindow()
        self.populateWindow()
        self.propagate(True)


class DefaultNumericalDisplay(NumericalDisplay):
    def __init__(self, screenName=None, baseName=None, className="Tk",
                 useTk=True, sync=False, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

    def setupMenuBar(self):
        self.winfo_toplevel().option_add('*tearOff', False)
        self.mbar = tk.Menu(self)

        # A File Menu
        self.file_menu = tk.Menu(self.mbar, name='file_menu')
        self.mbar.add_cascade(menu=self.file_menu, label='File')
        self.mbar.add_separator()

        self.edit_menu = tk.Menu(self.mbar, name='edit_menu')
        self.mbar.add_cascade(menu=self.edit_menu, label='Edit')
        self['menu'] = self.mbar

    def populateWindow(self):
        self.setupMenuBar()


def testProd():
    # import sys

    root = DefaultNumericalDisplay()

    root.wm_protocol("WM_DELETE_WINDOW", lambda: root.destroy())

    root.mainloop()


if __name__ == '__main__':
    testProd()
