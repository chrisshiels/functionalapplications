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


def read(f):
  for line in f:
    yield line


def removerepeatedemptylines(g):
  previousline = None
  for line in g:
    if line == '\n' and line == previousline:
      continue
    yield line
    previousline = line


def expandendoflines(g):
  for line in g:
    yield line[0:-1] + '$\n'


def expandtabs(g):
  for line in g:
    yield line.replace('\t', '^I')


def expandnonprintables(g):
  for line in g:
    yield ''.join(map(lambda e: e if \
                                e in string.printable else \
                                '^' + chr(ord('A') + ord(e) - 1),
                      list(line)))


def prependlinenumber(g):
  lineno = 0
  for line in g:
    lineno += 1
    yield '%6d\t%s' % ( lineno, line )


def write(f, g):
  for line in g:
    print(line, sep = '', end = '', file = f)


def parseargv(args, options):
  if not args:
    return args, options
  elif args[0][0] == '-':
    for c in list(args[0][1:]):
      options[c] = True
    return parseargv(args[1:], options)
  else:
    return args, options


def pipelineget(options, stdout):
  return filter(lambda e: e is not None,
                [
                  read,
                  removerepeatedemptylines \
                    if 's' in options \
                    else None,
                  expandendoflines \
                    if 'e' in options \
                    else None,
                  expandtabs \
                    if 't' in options \
                    else None,
                  expandnonprintables \
                    if 'e' in options or 't' in options or 'v' in options \
                    else None,
                  prependlinenumber \
                    if 'n' in options \
                    else None,
                  partial(write, stdout)
                ])


def main(stdin, stdout, stderr, argv):
  args, options = parseargv(argv[1:], {})

  pipeline = pipelineget(options, stdout)

  ret = pipemaybe(pipeline)(stdin)

  return 0 if ret is not None else 1


if __name__ == '__main__':
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv))
