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
