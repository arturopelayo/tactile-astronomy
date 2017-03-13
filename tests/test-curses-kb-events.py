import curses
import time

def main(stdscr):
    curses.noecho()
    curses.cbreak()

    stdscr.keypad(True)


    event = None
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Waiting for event")
        if event:
            stdscr.addstr(1, 0, str(event))
        stdscr.refresh()
        event = stdscr.getkey()

curses.wrapper(main)
