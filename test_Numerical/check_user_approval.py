import tkinter.simpledialog as diag

def didItWorkAsIntendedScale():
    return diag.askinteger(title='Satisfaction Prompt',prompt='On a scale of 0 to 10\n how well did the GUI work as intended?',initialvalue=5,minvalue=0,maxvalue=10,parent=None)

def didItWorkAsIntended():
    dialog = diag.SimpleDialog(None,"Did it work as intended",["Yes","No"],0,5,"Did it work?")
    opt = dialog.go()
    return opt

didItWorkAsIntended()