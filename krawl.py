#!/usr/bin/env python3
#
import curses
import random
import time


def move(x, y, dx, dy):
    newx = x + dx
    newy = y + dy

    # addch will raise an exception after writing to the
    # lower right corner, because it will then attempt to
    # advance the cursor (and fail).  So give the right
    # edge a char's extra space.  Give the bottom some
    # space as well, so a status display can go in there
    # at some point.
    #
    if newx >= COLS-1: newx = COLS-2
    elif newx < 0: newx = 0

    if newy >= ROWS-1: newy = ROWS-2
    elif newy < 0: newy = 0

    return newx, newy


def decodeMovementKeys(k, x, y):
    newX, newY = x, y

    if k == 'h': newX, newY = move(x, y, -1, 0)
    if k == 'j': newX, newY = move(x, y, 0, 1)
    if k == 'k': newX, newY = move(x, y, 0, -1)
    if k == 'l': newX, newY = move(x, y, 1, 0)
    if k == 'y': newX, newY = move(x, y, -1, -1)
    if k == 'u': newX, newY = move(x, y, 1, -1)
    if k == 'b': newX, newY = move(x, y, -1, 1)
    if k == 'n': newX, newY = move(x, y, 1, 1)

    return newX, newY


def main(stdscr):
    random.seed()

    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh()

    global ROWS, COLS
    global meX, meY

    ROWS, COLS = curses.LINES, curses.COLS
    meX = int(COLS / 2)
    meY = int(ROWS / 2)

    stdscr.addch(meY, meX, '@')

    while True:
        k = stdscr.getkey()

        # 'x': exit.
        #
        if k == 'x': return 1

        stdscr.addch(meY, meX, ' ')
        meX, meY = decodeMovementKeys(k, meX, meY)
        stdscr.addch(meY, meX, '@')


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

x = curses.wrapper(main)
if x == 0: print("you've won")
if x == 1: print("meh")
if x == 2: print("you've not won")
