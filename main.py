import argparse
import curses

Options = []


def add_opt(func):
    if isinstance(func, str):
        func_name = func

        def add_named(definite_func: "function"):
            nonlocal func_name
            definite_func.__name__ = func_name
            Options += [definite_func]
            return definite_func

        return add_named
    else:
        global Options
        Options += [func]
        return func


@add_opt
def Open_GUI():
    import Numerical_Methods.GUI as gui
    gui.start()
    return




BANNER = r"""
##########################################################
#                                                        #
#  Greeting User.                                        #
#  Welcome to a Electrostatic boundary condition Solver  #
#                                                        #
##########################################################
"""

MENU = r''''''
def makeMenu():
    global MENU
    MENUBUILDER = ["####"]
    max_str = 0
    options_len = len(Options)
    for i in range(options_len):
        unit = "# " + f"{i+1}. {Options[i].__name__}"
        MENUBUILDER += [unit]
        unit_len = len(unit)
        if unit_len > max_str:
            max_str = unit_len
    MENUBUILDER += [MENUBUILDER[0]]
    MENU = "\r\n".join(
        [
            (
                f"{MENUBUILDER[i]}{' ' if (i!=0) and (i!=max(options_len+1,0)) else '#'}"
                + "#" * (max(max_str - len(MENUBUILDER[i]), 0)+1)
            )
            for i in range(options_len + 2)
        ]
    )
    return MENU


def showMenu():
    makeMenu()
    print(BANNER)
    print(MENU)#
    
showMenu()
