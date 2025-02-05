import tkinter.simpledialog as diag

def didItWorkAsIntended():
    return diag.askinteger(title='Satisfaction Prompt',prompt='On a scale of 0 to 10\n how well did the GUI work as intended?',initialvalue=5,minvalue=0,maxvalue=10,parent=None)

print(didItWorkAsIntended())
