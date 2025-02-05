import tkinter.ttk as ttk

class MenuItem:
    def __init__(self, name=None, value=None):
        self.name=name
        self.value=value
        self.widget=None
    def _add_to_Menu(self,menu:'MenuBar'):
        if self.widget is None:
            self.widget = ttk.Button(menu,text=self.name)