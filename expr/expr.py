#!/usr/bin/env python


import re
import sys


def identity(v):
  return v


def identitylist(*v):
  return v


def token(r, f = identity):
  def token(s):
    match = re.match('\s+', s)
    if match:
      s = s[len(match.group(0)):]
    match = re.match(r, s)
    if match:
      return (f(match.group(0)), s[len(match.group(0)):])
    else:
      return None
  return token


def end(f = identity):
  def end(s):
    return token('$', f)(s)
  return end


def then(l, f = identitylist):
  def then(s):
    states = []
    for e in l:
      ret = e(s)
      if not ret:
        return None
      (state, s) = ret
      states += [ state ]
    return (f(*states), s)
  return then


def alt(l, f = identity):
  def alt(s):
    for e in l:
      ret = e(s)
      if ret:
        (state, s) = ret
        return (f(state), s)
    return None
  return alt


# Alternate monad pipeline implementation, though not as readable:
#def then(l, f = identitylist):
#  def bind(v, f):
#    if not v:
#      return None
#    (states, s) = v
#    ret = f(s)
#    if not ret:
#      return None
#    (state1, s1) = ret
#    return (states + [ state1 ], s1)
#
#  def unit(s):
#    return ([], s)
#
#  def then(s):
#    ret = reduce(bind, l, unit(s))
#    if not ret:
#      return None
#    (states, s) = ret
#    return (f(*states), s)
#  return then


# Alternate monad pipeline implementation, though not as readable:
#def alt(l, f = identity):
#  def bind(v, f):
#    (state, s) = v
#    if state is not None:
#      return v
#    ret = f(s)
#    if not ret:
#      return v
#    return ret
#
#  def unit(s):
#    return (None, s)
#
#  def alt(s):
#    ret = reduce(bind, l, unit(s))
#    (state, s) = ret
#    if state is None:
#      return None
#    return (f(state), s)
#  return alt


def add():
  def add(s):
    return token('\+')(s)
  return add


def subtract():
  def subtract(s):
    return token('-')(s)
  return subtract


def multiply():
  def multiply(s):
    return token('\*')(s)
  return multiply


def divide():
  def divide(s):
    return token('/')(s)
  return divide


def leftparen():
  def leftparen(s):
    return token('\(')(s)
  return leftparen


def rightparen():
  def rightparen(s):
    return token('\)')(s)
  return rightparen


# expression -> term '+' expression
#               term '-' expression
#               term
def expression():
  def internal(s):
    return alt([
                 then([ term(), add(), expression() ],
                      lambda a, _, b: a + b),
                 then([ term(), subtract(), expression() ],
                      lambda a, _, b: a - b),
                 term()
               ])(s)
  return internal


# term -> primary '*' term
#         primary '/' term
#         primary
def term():
  def internal(s):
    return alt([
                 then([ primary(), multiply(), term() ],
                      lambda a, _, b: a * b),
                 then([ primary(), divide(), term() ],
                      lambda a, _, b: a / b),
                 primary()
               ])(s)
  return internal


# primary -> integer
#            '(' expression ')'
def primary():
  def primary(s):
    return alt([
                 integer(),
                 then([ leftparen(), expression(), rightparen() ],
                      lambda _, a, __: a)
               ])(s)
  return primary


def integer():
  def integer(s):
    return token('\d+',
                 lambda a: int(a))(s)
  return integer


def parser():
  def parser(s):
    return then([ expression(), end() ],
                lambda a, _: a)(s)
  return parser


def parse(s, stdout, stderr):
  ret = parser()(s)
  if not ret:
    print >> stderr, 'Error'
    return 1
  else:
    (state, s) = ret
    print >> stdout, state
    return 0


def main(stdin, stdout, stderr, argv):
  if len(argv) == 1:
    for line in iter(stdin.readline, ''):
      parse(line.rstrip(), stdout, stderr)
    return 0
  else:
    return parse(' '.join(argv[1:]), stdout, stderr)


if __name__ == '__main__':
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv))
