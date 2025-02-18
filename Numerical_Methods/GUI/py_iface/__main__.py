from Numerical_Methods.GUI.py_iface import *

def printter(list_of :list = None):
    print(list_of)

bin_gui = gui_call_wrapper(list_of=list)(printter)

root = tk.Tk()
mainFraime = ttk.Frame(root,)
makeFunctionCallable(bin_gui,mainFraime)
mainFraime.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,side='top')
root.mainloop()