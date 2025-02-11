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


def main(stdscr,*args,**kwargs):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    stdscr.addstr(0, 0, Menu)

    stdscr.refresh()
    stdscr.getkey()
    
curses.wrapper(main)