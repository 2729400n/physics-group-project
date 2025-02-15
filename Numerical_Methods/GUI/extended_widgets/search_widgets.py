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
        self.search_entry  = ttk.Entry(self,name='searchbox',textvariable=self.pattern,validate='all',class_="Searchbox")
        self.search_entry.bind_class('Searchbox','<Return>',SearchField._search)
        self.search_entry.pack(fill=tk.BOTH,expand=True)
        
    @staticmethod
    def _search(evt:'tk.Event[tk.Entry]'):
        searhVar = evt.widget.cget('textvariable')
        queryString = searhVar.get()
        evt.widget.event_generate('<<Search>>')
        
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
                

if __name__ == '__main__':
    root = tk.Tk()
    sfield = SearchField(root)
    sfield.pattern.set('test')
    print(sfield.search({'test':0,'test2':1,'none':4,' some': 42}))
    sfield.pack(fill=tk.BOTH,expand=True)
    root.wm_geometry('640x480+0+0')
    root.mainloop()
# sfield.pack(file=tk.BOTH,expand=True)
# tk.mainloop()