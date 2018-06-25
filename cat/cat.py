#!/usr/bin/env python


import string
import sys


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
    print >> f, buf,


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

  write(stdout,
        expandnonprintables(expandtabs(expandendoflines(read(512, stdin)))))

  return 0


if __name__ == '__main__':
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv))
