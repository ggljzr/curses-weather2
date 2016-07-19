# -*- coding: utf-8 -*-

import curses
import locale
import subprocess
import sys

import pytoml as toml

# curses color pairs
PAIR_RED = 1
PAIR_GREEN = 2
PAIR_BLUE = 3
PAIR_YELLOW = 4
PAIR_CYAN = 5
PAIR_WHITE = 6
PAIR_BLACK = 7

PAIR_BLUE_RED = 8

MIN_ROWS = 26
MIN_COLS = 70

def initCurses():

    locale.setlocale(locale.LC_ALL, '')

    # init curses interface
    stdscr = curses.initscr()

    # colors
    curses.start_color()
    curses.init_pair(PAIR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(PAIR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(PAIR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(PAIR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(PAIR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(PAIR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(PAIR_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)  # no cursor

    return stdscr


def endCurses(stdscr):
    # terminate curses application
    curses.nocbreak()
    curses.echo()
    stdscr.keypad(0)
    curses.endwin()

class Window(object):
    
    def __init__(self, size_rows, size_columns, x, y, window_name):
        self.rows = size_rows
        self.columns = size_columns
        self.x = x
        self.y = y
        self.window_name = window_name
        self.window = curses.newwin(size_rows, size_columns, y, x)
        self.drawWindowBorder()


    def drawHLine(self, row, col, length, color):
        for i in range(col, col + length):
            try:
                self.window.addch(row, i, curses.ACS_HLINE,
                             curses.A_BOLD | curses.color_pair(color))
            except curses.error:
                pass

    def drawVLineCorners(self, row, col, length, color, right):

        upperCorner = curses.ACS_ULCORNER
        lowerCorner = curses.ACS_LLCORNER

        if right == True:
            upperCorner = curses.ACS_URCORNER
            lowerCorner = curses.ACS_LRCORNER

        try:
            self.window.addch(row, col, upperCorner,
                         curses.A_BOLD | curses.color_pair(color))
            self.window.addch(row + length - 1, col, lowerCorner,
                         curses.A_BOLD | curses.color_pair(color))
        except curses.error:
            pass

        for i in range(row + 1, row + length - 1):
            try:
                self.window.addch(i, col, curses.ACS_VLINE,
                             curses.A_BOLD | curses.color_pair(color))
            except curses.error:
                pass

    def drawName(self):
        self.window.addstr(0,0,self.window_name, curses.A_BOLD | curses.color_pair(PAIR_BLUE))

    def drawWindowBorder(self):
        self.drawHLine(0, 0, self.columns, PAIR_RED)
        self.drawHLine(self.rows - 1, 0, self.columns,PAIR_RED)

        self.drawVLineCorners(0, self.columns - 1, self.rows,PAIR_RED, True)
        self.drawVLineCorners(0, 0, self.rows, PAIR_RED, False)
        self.drawName()

    def refresh(self):
        self.window.refresh()







