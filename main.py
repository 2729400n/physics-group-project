import tkinter.simpledialog as diag
import tkinter.messagebox as msg
import sys
import pathlib
import time

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


if __name__ == "__main__":
    
    # clear_cache  = check_user_approval.wouldYouLike(
    #     "Would you like to clear cached files in this Package?"
    # )
    # if clear_cache:
    #     numerical_methods_path =pathlib.Path(Numerical_Methods.__file__).resolve().absolute()
    #     if(numerical_methods_path.is_dir()):
    #         cachecleaner.clearPythonCaches(numerical_methods_path)
    #     else:
    #         cachecleaner.clearPythonCaches(numerical_methods_path.parent)
            
    
    caching = wouldYouLike(
        "Would you like to enable Python caching? It makes for speedy re runs!"
    )
    
    if caching:
        sys.dont_write_bytecode=False
    else:
        sys.dont_write_bytecode=True
    
    
    enable_rtloader = wouldYouLike(
        "Would you like to enable RTLoader?\nIt allows for real-time reloading of Python modules!"
    )
    
    
    import Numerical_Methods.GUI as gui
    import Numerical_Methods.utils.check_user_approval as check_user_approval
    import Numerical_Methods.utils.realtime as rtLoader
    import Numerical_Methods.utils.cleancaches as cachecleaner
    import Numerical_Methods
    

    if enable_rtloader:
        rtLoader.init_realtime_module()
        rtLoader.start_realtime_module()

    try:
        gui.start()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting gracefully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        if enable_rtloader:
            rtLoader.stop_realtime_module()
        raise
    finally:
        
        exit(0)
