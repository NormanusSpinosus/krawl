#!/usr/bin/env python3
#
import curses

class Object:
  def __init__(self, x, y, display):
    self.x = x
    self.y = y
    self.display = display


  def move(self, dx, dy):
    self.x += dx
    self.y += dy


  def draw(self, scr):
    scr.addch(self.y, self.x, self.display)


  def erase(self, scr):
    scr.addch(self.y, self.x, ' ')
