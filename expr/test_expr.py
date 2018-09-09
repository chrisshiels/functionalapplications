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
