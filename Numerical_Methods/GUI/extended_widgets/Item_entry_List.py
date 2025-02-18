import enum
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tk_const
from typing import Literal

import tkinter.simpledialog as tk_simpdiag
import tkinter.messagebox as msgbox

class ItemType(enum.StrEnum):
    STR = 'str'
    NUMBER = 'number'
    FLOAT = 'float'
    

def validateInt(new_str,d_str=None,*args):
    try:
        int(new_str)
    except:
        return False
    return True

def validateBool(new_str:str,d_str=None,*args):
    if (new_str.upper() in 'TRUE') or (new_str.upper() in 'TRUE'):
        return True
    else: return False

def validateDouble(new_str,d_str=None,*args):
    try:
        float(new_str)
    except:
        return False
    return True

class ItemList(tk.Frame):
    def __init__(self,master,):
        super().__init__(master)
        self.items=[]
        self.setupList()
        self.item_num = 0
        self.valInt=self.register(validateInt)
        self.valBool=self.register(validateBool)
        self.valDouble=self.register(validateDouble)
        self.validateDictionary = {'number':self.valInt,'float':self.valDouble,'bool':self.valBool,'str':''}
    
    def setupList(self):
        self._buttons_frame = ttk.Frame(self,)
        self.add_item_button = ttk.Button(self._buttons_frame,text="Add Item")
        self.add_item_button.pack(fill=tk.NONE,expand=True, side=tk.LEFT,padx=5,pady=5)
        
        self.remove_item_button = ttk.Button(self._buttons_frame,text="Remove")
        self.remove_item_button.pack(fill=tk.NONE,expand=True, side=tk.RIGHT,padx=5,pady=5)
        self._buttons_frame.pack(side=tk.TOP,fill=tk.X,expand=True)
        
        
        
    def add_item(self,evt:'tk.Event[tk.Button]',item_type: Literal['str','number','float','bool']=ItemType.STR):
        item_num = self.item_num
        
                
        new_item_section = ttk.Frame(master=self,)
        
        match item_type:
            case 'str':
                var = tk.StringVar(new_item_section,'')
            case 'bool':
                var = tk.BooleanVar(master=new_item_section,value=False)
            case 'float':
                var = tk.DoubleVar(master=new_item_section,value=0.0)
            case 'number':
                var = tk.IntVar(master=new_item_section,value=0)
            case _:
                var = tk.Variable(master=new_item_section,value=None)
        if item_type == 'bool':
            ttk.Checkbutton(master=new_item_section,variable=var).grid(column=1,row=0,sticky='ne',padx=5,pady=5)
        else:
            ttk.Entry(master=new_item_section,textvariable=var,validate='all',validatecommand=(self.validateDictionary[item_type],'%P')).grid(column=1,row=0,sticky='ne',padx=5,pady=5)
        ttk.Label(master=new_item_section,text=f'Item {item_num}:').grid(column=0,row=0,sticky='nw',padx=5,pady=5)
        new_item_section.pack(side=tk.TOP,padx=5,pady=5,before=self._buttons_frame)
        self.item_num+=1
        self._buttons_frame.pack()
        self.items += [[new_item_section,var]]
        self.update()
        return None
    
    def remove_item(self,evt):
        
        if(self.items!=[]):
            self.item_num-=1
            item = self.items.pop()
            frame:ttk.Frame = item[0]
            var:'tk.Variable' = item[1]
            frame.destroy()
            self._buttons_frame.pack()
        return None
    
    def get(self):
        vals = []
        for item in self.items:
            var:'tk.Variable' = item[1]
            vals += [var.get()]
        return vals
    
class TypedItemList(ItemList):
    def __init__(self,master,item_type:"Literal['str','number','float','bool']"):
        self.item_type = ItemType(item_type)
        super().__init__(master)
    def setupList(self):
        super().setupList()
        self.add_item_button.bind('<Button-1>', self.add_item)
        self.remove_item_button.bind('<Button-1>', self.remove_item)
    def add_item(self,evt):
        return super().add_item(evt,self.item_type.value)

def showStuff(*args):
    return f"{[i for i in args]}"


if __name__=='__main__':
    root=tk.Tk()




    mainFrame = ttk.Frame(root)
    typeList = TypedItemList(mainFrame,'number')
    typeList.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,anchor=tk.NW)
    typeList.propagate(True)

    def buttonCallBack(evt,):
        argd = typeList.get()
        print(argd)
        out = showStuff(*argd)
        o = msgbox.showinfo("Output",out)
        return None


    submitButton = ttk.Button(mainFrame,text='Submit')
    submitButton.bind('<Button-1>',buttonCallBack)
    submitButton.pack()

    mainFrame.pack(fill=tk.BOTH,expand=True, pady=5, padx=5 )

    root.mainloop()