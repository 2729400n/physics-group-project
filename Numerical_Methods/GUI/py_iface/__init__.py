from enum import Enum
import inspect, sys, functools
import lzma, linecache, gzip, zipfile, zlib, base64, binascii
import signal

import re

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tkconst
import tkinter.simpledialog as diag
import tkinter.messagebox as msgbox
from ...utils.naming import slugify_tk
import numpy as np
from .. import extended_widgets

class ArgsState(Enum):
    NOTARG = 'narg'
    ISARG = 'isarg'

typePattern = re.compile(r'[^\|\s]*(?=([.*])*)')
print(re.match(typePattern,"int | x").group())

class Bundler:
    def __init__(self,entry:'tk.StringVar|tk.BooleanVar|tk.IntVar|tk.DoubleVar',field:'ttk.Entry|ttk.Checkbutton',iframe:'tk.LabelFrame|ttk.Frame|tk.Frame'):
        pass

def toBytes(x:str):
    return x.encode('ascii','strict')


def validateInt(new_str,d_str=None,*args):
    if new_str=='':
        return  True
    try:
        int(new_str)
    except:
        return False
    return True

def validateBool(new_str:str,d_str=None,*args):
    if new_str=='':
        return True
    if (new_str.upper() in 'TRUE') or (new_str.upper() in 'FALSE'):
        return True
    else: return False

def validateDouble(new_str,d_str=None,*args):
    if new_str=='':
        return True
    try:
        float(new_str)
    except:
        return False
    return True
    
        
    

def argumentToTypeFactory(extras:dict = None):
    transTable = {bool:bool,int:int,float:float,list:list,
                  "bool":bool,"int":int,"float":float,"list":list,
                  str:str,"str":str, bytes:bytes, "bytes":bytes
                  }
    if extras is not None:
        transTable.update(**extras)
    def arguments(annot:'str|type'=None,val=None):
        nonlocal transTable
        # print('Annotation Type',type(annot))
        if val is None and annot is None:
            return str
        
        if isinstance(annot,type):
            if issubclass(annot,(str,bytes)):
                if issubclass(annot,(bytes)):
                    return bytes
                else: 
                    return str
            currtype = transTable.get(annot)
        elif isinstance(annot,str,bytes):
            currtype = transTable.get(re.match(typePattern,annot).group())
        else:
            currtype = None
        if(currtype is None):
            transTable.get(type(val))
        # print(currtype)
        return currtype
        
    return arguments

defaultArgsToTypes = argumentToTypeFactory()

def getArgsToType(func:'function',argumetMapper = defaultArgsToTypes,classType=False,instance=None):
    func_info = inspect.getfullargspec(func)
    arg_types = dict()
    for i in [*func_info.args,*func_info.kwonlyargs]:
        if(classType==True and i =='self'):continue
        arg_types[i]=argumetMapper(func_info.annotations.get(i),({**(func_info.kwonlydefaults or {})}).get(i))
    
    if (func_info.varargs) is not None:
        arg_types[func_info.varargs]=list
    return arg_types

def gui_call_wrapper(*positional_types,**kwargs_types):
    pos_types  = list(positional_types).copy()
    kw_types = kwargs_types.copy()
    def partial_decorator(func):
        nonlocal pos_types,kw_types
        arg2Type = getArgsToType(func)
        
        

        
        argspec = inspect.getfullargspec(func)
        posType_len = len(pos_types)
        for i in range(len(argspec.args)):
            if argspec.args[i] not in kw_types:
                kw_types.update(**{argspec.args[i]:arg2Type.get(argspec.args[i])})
                if len(pos_types)<=i:
                    ntype = arg2Type.get(argspec.args[i])
                    if ntype is not None:
                        pos_types+=[ntype]
        for i in argspec.kwonlyargs:
            if argspec.kwonlyargs[i] not in kw_types:
                kw_types.update(**{argspec.kwonlyargs[i]:arg2Type.get(argspec.kwonlyargs[i])})
        # print('pos_types',pos_types)
        # print('kw_types',kw_types)
        
        
        @functools.wraps(func)
        def arg_transform_wrapper(*args,**kwargs):
            nonlocal pos_types,kw_types,argspec
            # print(args,kwargs)
            
            for i in range(len(args)):
                if(isinstance(i,(tk.StringVar,tk.BooleanVar,tk.IntVar,tk.DoubleVar,extended_widgets.ItemList))):
                    args+=[pos_types[i](args[i].get()) ]
                    
            pos_args= [ *args]+ [ None for i in range(max(len(argspec.args) - len(args),0)) ]
            
            
            for i in kwargs:
                if(isinstance(i,(tk.StringVar,tk.BooleanVar,tk.IntVar,tk.DoubleVar,extended_widgets.ItemList))):
                    kwargs.update(**{i:kw_types[i](kwargs[i].get())})
            # print(args,kwargs)
            kargs={}
            for i in kwargs:
                index =argspec.args.index(i)
                if index!= -1:
                    pos_args[index]=kwargs[i]
                else:
                    kargs[i]=kwargs[i]
                    
            # print(pos_args,kargs)
            if len(kargs.keys())==0:
                return func(*pos_args)
            return func(*args,**kwargs)
        arg_transform_wrapper.__signature__  = inspect.signature(func)
        return arg_transform_wrapper
    return partial_decorator

fieldToWidget = {}
def  add_Field_Var(master:'tk.Widget', field_name, field_type,field_value=None,field_label=None):
    varname =f'val_{field_name}'
    if field_label is None:
        field_label=field_name
    innerFrame =tk.LabelFrame(master,text=field_label)
    if(field_type==bool):
        entry= tk.BooleanVar(master, value=field_value, name=varname)
        entry_field = ttk.Checkbutton(innerFrame,name=field_name,text=field_name, variable=entry)
    elif(field_type==str):
        entry= tk.StringVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    elif(field_type==int):
        valInt=innerFrame.register(validateInt)
        entry= tk.IntVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame, name=field_name,text=field_name, validate='all',validatecommand=(valInt,'%P'), textvariable=entry)
    elif(field_type==float):
        valNum=innerFrame.register(validateDouble)
        entry= tk.DoubleVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all',validatecommand=(valNum,'%P'), textvariable=entry)
    elif(issubclass(field_type,list)):
        entry_field = extended_widgets.TypedItemList(innerFrame,item_type='float')
        entry= entry_field
    else:
        entry= tk.Variable(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    return entry,entry_field,innerFrame


# Calling Function that begin call
def callFunc(ev:'tk.Event[ttk.Button]',func:'function',*args, **kwargs):
    form = ev.widget.master
    
    # print(args,kwargs)
    for i in kwargs:
        
        if isinstance(kwargs[i],(tk.Variable,tk.StringVar,tk.BooleanVar,tk.IntVar,tk.DoubleVar,extended_widgets.ItemList)):
            arg = kwargs[i].get()
            if  isinstance(kwargs[i],tk.Variable):
                try:
                    if arg.strip() =='True':
                        argz=True
                    elif arg.strip() =='False':
                        argz=False
                    else:
                        raise ValueError()

                except:
                    try:
                        if  isinstance(kwargs[i],tk.DoubleVar):
                            raise ValueError('Double')
                        argz=int(arg)
                        print(kwargs[i],argz,type(kwargs[i]))
                    except:
                        # print('not int')
                        try:
                            argz=np.float64(arg)
                        except:
                            # print('not float')
                            try:
                                argz=str(arg).encode('utf-8').decode('unicode_escape')
                            except:
                                argz=str(arg)
            # print('callFunc before Storing:',arg,type(arg))
            arg=argz
            kwargs[i]=arg
    try:
        returnValue=func(**kwargs)
        # print(func)
        if returnValue is not None:
            msgbox.showinfo(title=func.__name__,message=f"{returnValue}")
    except Exception as ex:
        msgbox.showerror(title=func.__name__,message=f"{ex}")
    return None

def getDefault(arg,func):
    func_sig=inspect.signature(func)
    param=func_sig.parameters.get(arg)
    if param is None:
        return ArgsState.NOTARG,None
    print(param.default)
    return ArgsState.ISARG,param.default

def makeFunctionCallable(func:'function',master=None,classType=False,instance=None,direction='left',max_rows=4):
    argMapping=getArgsToType(func,classType=classType)
    mroot = ttk.Labelframe(master=master,width=640,height=480, text=func.__name__)
    wmain_outer= ttk.Frame(mroot)
    
    # wmain = ttk.Frame(wmain_outer)
    
    stores = {}
    count = 0
    for i in  argMapping:
        if count%max_rows==0:
            wmain = ttk.Frame(wmain_outer)
            wmain.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,side=direction,anchor=tk.NW)
        defarg = getDefault(i,func)
        if defarg[1] == inspect._empty:
            defarg = (defarg[0],None)
        store,field, iframe =add_Field_Var(master=wmain,field_name=slugify_tk(i),field_type=argMapping[i],field_value=defarg[1] if defarg[0]==ArgsState.ISARG else None,field_label=i)
        field.grid(sticky='w')
        iframe.grid(sticky='w')
        stores.update(**{i:store})
        count+=1
        
    btn=ttk.Button(mroot,text="Submit", class_='Submit', name='submit_button')
    # print(stores)
    btn.bind('<Button-1>',lambda ev:callFunc(ev,func,**stores))
    # btn.pack(side='bottom',anchor=tk.S,fill=tk.NONE,expand=False,padx=5,pady=5)
    
    # root.wm_geometry('640x480')
    # wmain.master.wm_geometry('640x480')
    wmain_outer.grid(row=0,column=0)
    wmain_outer.propagate(True)
    btn.grid(row=1,column=0)
    mroot.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,side=direction,anchor=tk.NW)
    mroot.propagate(True)
    return stores


    
    
