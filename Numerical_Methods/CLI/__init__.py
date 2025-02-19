import curses
import curses.ascii
import curses.panel
import curses.textpad


Menu='''1. Solve Task_1
2. Solve Task_2
3. Solve Task_3
4. Solve Task_4
5. Solve Task_Custom (will need to be passed the path to the file) 
'''


def main(stdscr:curses.window,*args,**kwargs):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    stdscr.addstr(0, 0, Menu)
    
    
    
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