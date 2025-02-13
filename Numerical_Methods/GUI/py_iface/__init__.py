import inspect, sys, functools

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tkconst

def toBytes(x:str):
    return x.encode('ascii','strict')
    

def argumentToTypeFactory(extras = None):
    if extras == None:
        extras = {bool:bool,int:int,float:float,list:list,
                  "bool":bool,"int":int,"float":float,"list":list,
                  str:str,"str":str, bytes:bytes, "bytes":bytes
                  }
    def arguments(annot:'str|type'=None,val=None):
        nonlocal extras
        if val is None and annot is None:
            return str
        if isinstance(annot,type):
            if issubclass(annot,(str,bytes)):
                if issubclass(annot,(bytes)):
                    return bytes
                else: 
                    return str
        currtype = extras.get(annot)
        if(currtype is None):
            extras.get(val.__class__)
        if currtype is None:
            return str
        return currtype
        
    return arguments

defaultArgsToTypes = argumentToTypeFactory()

def getArgsToType(func:'function',argumetMapper = defaultArgsToTypes):
    func_info = inspect.getfullargspec(func)
    arg_types = {i:argumetMapper(func_info.annotations.get(i),(func_info.kwonlydefaults or {}).get(i)) for i in [*func_info.args,*func_info.kwonlyargs,func_info.varargs]}
    return arg_types

def  add_Field_Var(master, field_name, field_type,field_value=None):
    varname =f'val_{field_name}'
    innerFrame =tk.LabelFrame(master,text=field_name)
    if(field_type==bool):
        entry= tk.BooleanVar(master, value=field_value, name=varname)
        entry_field = ttk.Checkbutton(innerFrame,name=field_name,text=field_name, variable=entry)
    if(field_type==str):
        entry= tk.StringVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    if(field_type==int):
        entry= tk.IntVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame, name=field_name,text=field_name, validate='all',validatecommand=lambda x: x.isnumeric(), textvariable=entry)
    if(field_type==float):
        entry= tk.BooleanVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all',validatecommand=lambda x: x.isdecimal(), textvariable=entry)
    return entry,entry_field,innerFrame
def callFunc(ev:'tk.Event[ttk.Button]',func:'function',*args, **kwargs):
    form = ev.widget.master
    for i in kwargs:
        print(i,kwargs[i].get())
    return None

if __name__ == '__main__':
    
    argMapping=getArgsToType(print)
    root=tk.Tk()
    wmain=ttk.Labelframe(root,width=640,height=480, text=print.__name__)
    stores = {}
    for i in  argMapping:
        store,field, iframe =add_Field_Var(wmain,i,argMapping[i])
        field.grid()
        iframe.grid()
        stores.setdefault(i,store)
    btn=ttk.Button(wmain,text="Submit", class_='Submit', name='submit_button')
    btn.bind_class('Submit','<Button-1>',lambda ev:callFunc(ev,print,**stores))
    btn.grid()
    
    wmain.grid()
    root.mainloop()