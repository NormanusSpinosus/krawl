import random


class Map:
  def __init__(self, xsize, ysize):
    # - 1 to avoid exception from trying to write to the last column.
    #
    self.xsize = xsize - 1
    self.ysize = ysize - 1

    self.map = [[Tile(False, "#")
                 for y in range(ysize) ]
                     for x in range(xsize) ]

    self.rooms = []


  def initSolid(self):
    for y in range(self.ysize):
      for x in range(self.xsize):
        self.map[x][y].blocked = True
        self.map[x][y].block_sight = True


  def initMap(self, nRm, maxRm, aspect=(1, 1)):
    r = Rect(self.xsize // 2 - 5,
                 self.ysize // 2 - 5, 15, 15)
    self.mkRoom(r)
    self.rooms.append(r)

    for i in range(random.randint(nRm[0], nRm[1])):
      w = random.randint(3, maxRm * aspect[0])
      h = random.randint(3, int(maxRm * aspect[1]))

      if (w > self.xsize - 2) | (h > self.ysize - 2): continue

      x = random.randint(0, self.xsize - w - 1)
      y = random.randint(0, self.ysize - h - 1)

      r = Rect(x, y, w, h)
      self.mkRoom(r)
      self.rooms.append(r)

    if len(self.rooms) < 2: return

    for i in range(1, len(self.rooms)):
      c1 = self.rooms[i-1].center()
      c2 = self.rooms[i].center()

      if(random.randint(0, 1)):
        self.mkHtunnel(c1[0], c2[0], c1[1])
        self.mkVtunnel(c1[1], c2[1], c2[0])
      else:
        self.mkVtunnel(c1[1], c2[1], c1[0])
        self.mkHtunnel(c1[0], c2[0], c1[1])


  def mkRoom(self, r):
    r.x1 = max(r.x1, 1)
    r.x2 = min(r.x2, self.xsize-2)
    r.y1 = max(r.y1, 1)
    r.y2 = min(r.y2, self.ysize-2)

    # range(a, b) returns numbers [a, b), so +1 here to make it [a, b].
    # Calculations above, on xsize/ysize, subtract one because size
    # counts from 1 but indices count from 0, and subtract one once
    # again, to make sure that there is a wall all around the map.
    #
    for x in range(r.x1, r.x2 + 1):
      for y in range(r.y1, r.y2 + 1):
        self.map[x][y].blocked = False
        self.map[x][y].block_sight = False
        self.map[x][y].display = ' '


  def mkHtunnel(self, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2)):
      self.map[x][y].blocked = False
      self.map[x][y].block_sight = False
      self.map[x][y].display = ' '


  def mkVtunnel(self, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2)):
      self.map[x][y].blocked = False
      self.map[x][y].block_sight = False
      self.map[x][y].display = ' '


  def getDims(self):
    return self.xsize, self.ysize



# A location in the world.
#
class Tile:
  def __init__(self, blocked, display, block_sight=None):
    self.blocked = blocked
    self.display = display

    if block_sight is None: block_sight = blocked
    self.block_sight = block_sight


  def draw(self, scr, x, y):
    scr.addch(y, x, self.display)


  def show(self):
    print("Tile, block %d vis %d disp %s" %
            (self.blocked, self.block_sight, self.display))



# Rectangles.  For rooms.
#
class Rect:
  def __init__(self, x, y, w, h):
    self.x1 = x
    self.y1 = y
    self.x2 = x + w
    self.y2 = y + h


  def center(self):
    return ((self.x1 + self.x2) // 2,
            (self.y1 + self.y2) // 2)
