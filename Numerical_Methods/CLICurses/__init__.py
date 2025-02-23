import curses
import curses.ascii
import curses.panel
import curses.textpad


MainWindow :curses.window = None
Menu='''1. Solve Task_1
 2. Solve Task_2
 3. Solve Task_3
 4. Solve Task_4
 5. Solve Task_Custom (will need to be passed the path to the file) 
'''


def main(stdscr:curses.window,*args,**kwargs):
    global MainWindow
    # Clear screen
    MainWindow = stdscr
    stdscr.clear()
    
    
    stdscr.addstr(1, 1, Menu)
    stdscr.box()
    
    
    stdscr.refresh()
    opt = stdscr.getch()
    match opt:
        case 0x31:
            pass
        case 0x32:
            pass
        case 0x33:
            pass
        case 0x34:
            pass
        case 0x35:
            pass
        case 0x36:
            pass
        case 0x37:
            pass
        case 0x38:
            pass
        case 0x39:
            pass
def main_cli():
    curses.wrapper(main)

if __name__ == '__main__':
    main_cli()