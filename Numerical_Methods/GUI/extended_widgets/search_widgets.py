import collections.abc
import tkinter as tk
import tkinter.ttk as ttk
import re
import symtable
import types, typing, collections.abc as abc
import collections

class SearchField(tk.Frame):
     
    def __init__(self,master=None,*args,**kwargs):
        
        super().__init__(master,*args,class_ = "FrameSearchField",**kwargs)
        self.setup()
    
    def setup(self):
        self.pattern = tk.StringVar(self,"","search_query")
        self.search_entry  = ttk.Entry(self,)
    def search(self,hayStack,regex=False,single = False):
        queryString = self.pattern.get()
        if isinstance(hayStack,(abc.Iterable,typing.Iterable)):
            if isinstance(hayStack,dict):
                stacks = {i:i for i in hayStack}
            else:
                stacks = {hayStack[i]:i for i in range(len(hayStack))}
            allowed = []
            if regex:
                for hay in stacks:
                    express =re.compile(pattern=queryString)
                    if re.match(express,hay):
                        allowed.append(stacks[hay])
            else:
                for hay in stacks:
                    if (queryString in hay):
                        allowed.append(stacks[hay])
            return allowed
        elif isinstance(hayStack,str):
            if regex:
                express =re.compile(pattern=queryString)
                places = [i.pos for i in re.findall(express,hayStack) if isinstance(i,re.Match) and (i is not None)] 
            else:
                places = []
                pos0 = 0
                queryString_len = len(queryString)
                while True:
                    try:
                        pos0 = hayStack.find(queryString,pos0)
                        if pos0 == -1:
                            break
                        places.append(pos0)
                        pos0 += queryString_len
                    except:
                        break
            return places
                

sfield = SearchField()
sfield.pattern.set('test')
print(sfield.search({'test':0,'test2':1,'none':4,' some': 42}))
# sfield.pack(file=tk.BOTH,expand=True)
# tk.mainloop()