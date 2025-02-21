import tkinter.simpledialog as diag
import tkinter.messagebox as msg


def didItWorkAsIntendedScale():
    return diag.askinteger(title='Satisfaction Prompt',prompt='On a scale of 0 to 10\n how well did the GUI work as intended?',initialvalue=5,minvalue=0,maxvalue=10,parent=None)

def didItWorkAsIntended():
    dialog = diag.SimpleDialog(None,"Did it work as intended",["Yes","No"],0,1,"Did it work?")
    opt = dialog.go()
    return opt

def wouldYouLike(msg_:str="Would you like this",title="Physics Solver",):
    try:
        opt= msg.askyesno(title,msg_)
    except:
        opt = False
    return opt

