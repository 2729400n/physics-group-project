if __name__ == '__main__':
    from . import *

    import tkinter.messagebox


    def printter(list_of :list):
        tkinter.messagebox.showinfo("Printter",f"{list_of}")
        return 

    bin_gui = gui_call_wrapper()(printter)

    root = tk.Tk()
    mainFraime = ttk.Frame(root,)
    makeFunctionCallable(bin_gui,mainFraime)
    mainFraime.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,side='top')
    root.mainloop()