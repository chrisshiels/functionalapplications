#!/usr/bin/env python

# 'life.py'.


import sys


def reverse(l):
  return reduce(lambda a, e: [ e ] + a,
                l,
                [])


def gridnew(lenx, leny, f = lambda: 0):
  return { 'lenx': lenx,
           'leny': leny,
           'cells': map(lambda i: f(), range(lenx * leny))
         }


def gridxytoindex(grid, x, y):
  return y % grid['leny'] * grid['lenx'] + x % grid['lenx']


def gridindextoxy(grid, i):
  i %= grid['leny'] * grid['lenx']
  return (i % grid['leny'], i / grid['lenx'])


def gridset(grid, x, y, v):
  grid['cells'][gridxytoindex(grid, x, y)] = v
  return grid


def gridget(grid, x, y):
  return grid['cells'][gridxytoindex(grid, x, y)]


def gridprint(grid, file):
  for y in reverse(range(grid['leny'])):
    for x in range(grid['lenx']):
      print >> file, 'o' if gridget(grid, x, y) == 1 else '.',
    print >> file, ''
  return grid


def gridneighbours(grid, x, y):
  sum = 0
  for xoffset in [ -1, 0, 1 ]:
    for yoffset in [ -1, 0, 1 ]:
      if not (xoffset == 0 and yoffset == 0):
        sum += gridget(grid, x + xoffset, y + yoffset)
  return sum


def gridtick(grid, f):
  return {
    'lenx': grid['lenx'],
    'leny': grid['leny'],
    'cells': map(lambda i: f(grid['cells'][i],
                             gridneighbours(grid,
                                            i % grid['lenx'],
                                            i / grid['lenx'])),
                 range(grid['lenx'] * grid['leny']))
  }


def b3s23(current, n):
  if current == 0 and n == 3:
    return 1
  elif current == 1 and (n == 2 or n == 3):
    return 1
  else:
    return 0


def gridload(grid, l, x, y):
  return reduce(lambda a, e: gridset(a, x + e[0], y + e[1], 1), l, grid)


def glider():
  return [
           [ 0, 0 ],
           [ 1, 0 ],
           [ 1, 1 ],
           [ 2, 1 ],
           [ 0, 2 ]
         ]


def pentadecathlon():
  return [
           [ 5, 10 ],
           [ 6, 10 ],
           [ 7, 9 ],
           [ 7, 11 ],
           [ 8, 10 ],
           [ 9, 10 ],
           [ 10, 10 ],
           [ 11, 10 ],
           [ 12, 9 ],
           [ 12, 11 ],
           [ 13, 10 ],
           [ 14, 10 ]
         ]


def main(stdin, stdout, stderr, argv):
  g = gridload(gridnew(20, 20), pentadecathlon(), 0, 0)
  gridprint(g, stdout)

  while True:
    raw_input()
    g = gridtick(g, b3s23)
    gridprint(g, stdout)


if __name__ == "__main__":
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv[1:]))


# To do:
# - argv lenx, leny, initial.
# - stringtogrid().
