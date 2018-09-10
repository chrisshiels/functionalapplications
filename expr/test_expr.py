import StringIO


import pytest


import expr


@pytest.fixture
def stdin():
  return StringIO.StringIO()


@pytest.fixture
def stdout():
  return StringIO.StringIO()


@pytest.fixture
def stderr():
  return StringIO.StringIO()


def test_identity():
  assert expr.identity(None) is None
  assert expr.identity(1) == 1


def test_identitylist():
  assert expr.identitylist(None) == (None,)
  assert expr.identitylist(1) == (1,)
  assert expr.identitylist(1, 2) == (1, 2)
  assert expr.identitylist(1, 2, 3) == (1, 2, 3)


def test_token():
  assert expr.token('x')(' y') is None
  assert expr.token('x')(' x') == ('x', '')
  assert expr.token('x', len)(' x') == (1, '')
  assert expr.token('x+y')(' yxxxyy') is None
  assert expr.token('x+y')(' xxxyy') == ('xxxy', 'y')
  assert expr.token('x+y', len)(' xxxyy') == (4, 'y')


def test_end():
  assert expr.end()(' hello') is None
  assert expr.end()(' ') == ('', '')
  assert expr.end()('') == ('', '')


def test_then():
  def digit():
    def digit(s):
      return expr.token('\d')(s)
    return digit

  assert expr.then([ digit(), digit(), digit() ],
                   lambda x, y, z: int(x) + int(y) + int(z))('---') is None
  assert expr.then([ digit(), digit(), digit() ],
                   lambda x, y, z: int(x) + int(y) + int(z))('123') == (6, '')


def test_alt():
  def digit():
    def digit(s):
      return expr.token('\d')(s)
    return digit

  def letter():
    def letter(s):
      return expr.token('[a-z]')(s)
    return letter

  assert expr.alt([ digit(),
                    letter() ],
                   lambda x: x * 2)('---') is None
  assert expr.alt([ digit(),
                    letter() ],
                   lambda x: x * 2)('123') == ('11', '23')
  assert expr.alt([ digit(),
                    letter() ],
                   lambda x: x * 2)('abc') == ('aa', 'bc')


def test_add():
  assert expr.add()(' xxx') is None
  assert expr.add()(' +xxx') == ('+', 'xxx')


def test_subtract():
  assert expr.subtract()(' xxx') is None
  assert expr.subtract()(' -xxx') == ('-', 'xxx')


def test_multiply():
  assert expr.multiply()(' xxx') is None
  assert expr.multiply()(' *xxx') == ('*', 'xxx')


def test_divide():
  assert expr.divide()(' xxx') is None
  assert expr.divide()(' /xxx') == ('/', 'xxx')


def test_leftparen():
  assert expr.leftparen()(' xxx') is None
  assert expr.leftparen()(' (xxx') == ('(', 'xxx')


def test_rightparen():
  assert expr.rightparen()(' xxx') is None
  assert expr.rightparen()(' )xxx') == (')', 'xxx')


def test_expression():
  assert expr.expression()('  + 4xxx') is None
  assert expr.expression()('  4 + 4xxx') == (8, 'xxx')
  assert expr.expression()('  4 - 4xxx') == (0, 'xxx')


def test_term():
  assert expr.term()('  * 4xxx') is None
  assert expr.term()('  4 * 4xxx') == (16, 'xxx')
  assert expr.term()('  4 / 4xxx') == (1, 'xxx')


def test_primary():
  assert expr.primary()('  xxx') is None
  assert expr.primary()('  4xxx') == (4, 'xxx')
  assert expr.primary()('  ( 4 )xxx') == (4, 'xxx')


def test_integer():
  assert expr.integer()('  x44xxx') is None
  assert expr.integer()('  44xxx') == (44, 'xxx')


def test_main_singleargument(stdin, stdout, stderr):
  ret = expr.main(stdin, stdout, stderr, [ 'file.py',
                                           '4 + 4 * 2' ])
  assert ret == 0
  assert stdout.getvalue().rstrip() == '12'
  assert stderr.getvalue() == ''


def test_main_multiplearguments(stdin, stdout, stderr):
  ret = expr.main(stdin, stdout, stderr, [ 'file.py',
                                           '4',
                                           '+',
                                           '4',
                                           '*',
                                           '2' ])
  assert ret == 0
  assert stdout.getvalue().rstrip() == '12'
  assert stderr.getvalue() == ''


def test_main_stdin(stdout, stderr):
  stdin = StringIO.StringIO('(6 + 6) / (2 + 2)')
  ret = expr.main(stdin, stdout, stderr, [ 'file.py' ])
  assert ret == 0
  assert stdout.getvalue().rstrip() == '3'
  assert stderr.getvalue() == ''
