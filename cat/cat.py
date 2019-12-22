#!/usr/bin/env python


from __future__ import print_function


import string
import sys


def pipe(l):
  def internal(v):
    return reduce(lambda a, e: e(a), l, v)
  return internal


def partial(f, *args1):
  def internal(*args2):
    return f(*(args1 + args2))
  return internal


def read(f):
  for line in f:
    yield line


def removerepeatedemptylines(g):
  previousline = None
  for line in g:
    if line == '\n' and previousline == '\n':
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


def prependlinenumbers(g):
  lineno = 0
  for line in g:
    lineno += 1
    yield '%6d\t%s' % ( lineno, line )


def write(f, g):
  for line in g:
    print(line, sep = '', end = '', file = f)
  return 0


def cat(pipeline, stdin, args):
  if not args:
    return pipe(pipeline)(stdin)
  else:
    for arg in args:
      f = open(arg)
      ret = pipe(pipeline)(f)
      f.close()
      if ret != 0:
        break
    return ret


def parseargs(options, args):
  if not args:
    return options, args
  elif args[0][0] == '-':
    for c in list(args[0][1:]):
      options[c] = True
    return parseargs(options, args[1:])
  else:
    return options, args


def checkargs(options):
  return len(filter(lambda e: e not in [ 'e', 'n', 's', 't', 'v' ],
                    options.keys())) == 0


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
                  prependlinenumbers \
                    if 'n' in options \
                    else None,
                  partial(write, stdout)
                ])


def usage(f, exitcode):
  print('''\
Usage: cat [ options ] [ file ... ]

.
.
''',
        file = f)
  return exitcode


def main(stdin, stdout, stderr, argv):
  if len(argv) == 2 and argv[1] in ('-h', '--help'):
    return usage(stdout, 0)

  options, args = parseargs({}, argv[1:])
  if not checkargs(options):
    return usage(stderr, 1)

  pipeline = pipelineget(options, stdout)
  return cat(pipeline, stdin, args)


if __name__ == '__main__':
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv))
