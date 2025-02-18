import enum
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tk_const
from typing import Literal

class ItemType(enum.StrEnum):
    STR = 'str'
    

class ItemList(tk.Frame):
    def __init__(self,master,):
        super().__init__(master)
        self.setupList()
        self.item_num = 0
    
    def setupList(self):
        self.add_item_button = ttk.Button(self,text="Add Item")
        self.add_item_button.grid(column=0,row=0,sticky='ne',padx=5,pady=5)
    
    
        
    def add_item(self,item_type: Literal['str','number','float','bool']=ItemType.STR):
        item_num = self.item_num
        match item_type:
            case 'str':
                var = tk.StringVar(self,'')
            case 'bool':
                var = tk.BooleanVar(master=self,value=False)
            case 'float':
                var = tk.DoubleVar(master=self,value=0.0)
            case 'number':
                var = tk.IntVar(master=self,value=0)
            case _:
                var = tk.Variable(master=self,value=None)
                
        new_item_section = ttk.Frame(master=self,)
        if item_type == 'bool':
            ttk.Checkbutton(master=new_item_section).grid(column=1,row=0,sticky='ne',padx=5,pady=5)
        else:
            ttk.Entry(master=new_item_section).grid(column=1,row=0,sticky='ne',padx=5,pady=5)
        ttk.Label(master=new_item_section,text=f'Item {item_num}:').grid(column=0,row=0,sticky='nw',padx=5,pady=5)
        new_item_section.grid(column=0,row=item_num,sticky='nsew',padx=5,pady=5)
        self.update()
        
class TypedItemList(ItemList):
    def __init__(self,master,item_type:"Literal['str','number','float','bool']"):
        self.item_type = ItemType(item_type)
        super().__init__(master)
    
    def add_item(self,):
        return super().add_item(self.item_type.value)
        
root=tk.Tk()
typeList = TypedItemList(root,'str')
typeList.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,anchor=tk.NW)
typeList.propagate(True)
root.mainloop()