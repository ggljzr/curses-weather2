import curses
import curses_gui as cg
import locale


if __name__ == '__main__':

    stdscr = cg.initCurses();

    window = cg.Window(10,10,10,10, 'wokno')
    #window = curses.newwin(10,10,10,10)
    #window.window.addstr(0,0,'test')
    stdscr.refresh()
    window.refresh()

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break

    cg.endCurses(stdscr)
