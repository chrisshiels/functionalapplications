#!/usr/bin/env python


from __future__ import print_function


import string
import sys


def pipemaybe(l):
  def internal(v):
    return reduce(lambda a, e: e(a) if a is not None else a, l, v)
  return internal


def partial(f, *args):
  args1 = args
  def internal(*args):
    return f(*(args1 + args))
  return internal


def read(buffersize, f):
  while True:
    buf = f.read(buffersize)
    if buf == '':
      break
    yield buf


def expandendoflines(g):
  for buf in g:
    yield buf.replace('\n', '$\n')


def expandtabs(g):
  for buf in g:
    yield buf.replace('\t', '^I')


def expandnonprintables(g):
  for buf in g:
    yield ''.join(map(lambda e: e if \
                                e in string.printable else \
                                '^' + chr(ord('A') + ord(e) - 1),
                      list(buf)))


def write(f, g):
  for buf in g:
    print(buf, sep = '', end = '', file = f)


def parseargv(args, options):
  if not args:
    return args, options
  elif args[0][0] == '-':
    for c in list(args[0][1:]):
      options[c] = True
    return parseargv(args[1:], options)
  else:
    return args, options


def main(stdin, stdout, stderr, argv):
  args, options = parseargv(argv, {})

  ret = pipemaybe([
                    expandendoflines,
                    expandtabs,
                    expandnonprintables,
                    partial(write, stdout),
                  ])(read(512, stdin))

  return 0 if ret is not None else 1


if __name__ == '__main__':
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv))
