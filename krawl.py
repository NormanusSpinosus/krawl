#!/usr/bin/env python3
#
import curses
import random
import time
import sys

import krObject
import map


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


# Returns (dx, dy).
#
def decodeMovementKeys(k):
    if k == 'h': return -1,  0
    if k == 'j': return  0,  1
    if k == 'k': return  0, -1
    if k == 'l': return  1,  0
    if k == 'y': return -1, -1
    if k == 'u': return  1, -1
    if k == 'b': return -1,  1
    if k == 'n': return  1,  1

    return 0, 0


def clearAll(scr, fullRedraw):
    global playerObjs

    if fullRedraw: scr.clear()
    else:
      for o in [ playerObjs ]:
        for oo in o:
          oo.erase(scr)


# Draw all movables.  Floor markings first, then things, then NPCs and
# the player.
#
def drawAll(scr, fullRedraw):
    global m
    global playerObjs

    if fullRedraw:
      for j in range(m.ysize):
        for i in range(m.xsize):
          m.map[i][j].draw(scr, i, j)

    for o in [ playerObjs ]:
      for oo in o:
        oo.draw(scr)


def main(stdscr):
    random.seed()

    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh()

    global m
    global playerObjs
    global ROWS, COLS

    ROWS, COLS = curses.LINES, curses.COLS

    playerObjs = [ krObject.Object(int(COLS/2), int(ROWS/2), '@') ]
    m = map.Map(COLS, ROWS)
    m.initSolid()

    m.initMap(nRm=(5, 10), maxRm=20, aspect=(1, .5))

    clearAll(stdscr, True)
    drawAll(stdscr, True)
    stdscr.refresh()

    while True:

        k = stdscr.getkey()

        # 'x': exit.
        #
        if k == 'x': return 1

        clearAll(stdscr, False)

        dx, dy = decodeMovementKeys(k)

        if not m.map[playerObjs[0].x + dx][playerObjs[0].y + dy].blocked:
          playerObjs[0].x += dx
          playerObjs[0].y += dy

        drawAll(stdscr, False)
        stdscr.refresh()


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

x = curses.wrapper(main)
if x == 0: print("you've won")
if x == 1: print("meh")
if x == 2: print("you've not won")
