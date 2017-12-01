#!/usr/bin/env python

# 'wordfrequencies.py'.
# Chris Shiels.


import re
import sys


def pipemaybe(l):
  def internal(v):
    return reduce(lambda a, e: e(a) if a is not None else None, l, v)
  return internal


def partial(f, *args):
  args1 = args
  def internal(*args):
    return f(*(args1 + args))
  return internal


def removepossessives(s):
  return s.replace('\'s', '')


def rewritenonalphanumerics(s):
  return re.sub('\W', ' ', s)


def splitwords(s):
  return s.split()


def lowercasewords(l):
  return map(lambda e: e.lower(), l)


def dictfrequencies(l):
  def accumulate(a, e):
    if not e in a:
      a[e] = 1
    else:
      a[e] += 1
    return a
  return reduce(accumulate, l, {})


def listfrequencies(d):
  return reduce(lambda a, e: a + [ { 'word': e, 'count': d[e] } ],
                d.keys(),
                [])


def sortfrequencies(l):
  def compare(x, y):
    ret = cmp(x['count'], y['count']) * -1
    if ret == 0:
      ret = cmp(x['word'], y['word'])
    return ret
  return sorted(l, compare)


def outputfrequencies(stdout, l):
  for e in l:
    print >> stdout, \
             '%(count)s %(word)s' % { 'count': e['count'], 'word': e['word'] }
  return 0


def wordfrequencies(stdout, s):
  ret = pipemaybe([ removepossessives,
                    rewritenonalphanumerics,
                    splitwords,
                    lowercasewords,
                    dictfrequencies,
                    listfrequencies,
                    sortfrequencies,
                    partial(outputfrequencies, stdout)
                  ])(s)
  if ret != None:
    return ret
  else:
    return 1


def main(stdin, stdout, stderr, argv):
  if len(argv) == 0:
    return wordfrequencies(stdout, stdin.read())
  else:
    ret = 0
    for arg in argv:
      if len(argv) > 1:
          print "\n%(arg)s:" % { 'arg': arg }
      f = open(arg)
      ret = wordfrequencies(stdout, f.read())
      f.close()
      if ret != 0:
        break
    return ret


if __name__ == "__main__":
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv[1:]))
