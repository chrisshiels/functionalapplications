import StringIO
import sys


import pytest


import cat


@pytest.fixture
def helloworldfile(tmpdir):
  f = tmpdir.mkdir('fixtures').join('helloworld.txt')
  f.write('''\
Hello
World
''')
  return f


@pytest.fixture
def stdin():
  return StringIO.StringIO()


@pytest.fixture
def stdout():
  return StringIO.StringIO()


@pytest.fixture
def stderr():
  return StringIO.StringIO()


def test_pipe():
  def adda(l):
    return l + [ 'a' ]

  def addb(l):
    return l + [ 'b' ]

  def addc(l):
    return l + [ 'c' ]

  assert cat.pipe([ adda, addb, addc ])([]) == [ 'a', 'b', 'c' ]


def test_partial():
  def add(x, y):
    return x + y

  add1 = cat.partial(add, 1)

  assert add1(1) == 2


def test_read():
  f = StringIO.StringIO('''\
Line 1
Line 2
Line 3
''')
  g = cat.read(f)
  assert g.next() == 'Line 1\n'
  assert g.next() == 'Line 2\n'
  assert g.next() == 'Line 3\n'
  with pytest.raises(StopIteration):
    g.next()


def test_removerepeatedemptylines():
  g = cat.removerepeatedemptylines([ 'huey\n',
                                     '\n',
                                     '\n',
                                     'dewey\n',
                                     '\n',
                                     '\n',
                                     '\n',
                                     '\n',
                                     'louie\n' ])
  assert g.next() == 'huey\n'
  assert g.next() == '\n'
  assert g.next() == 'dewey\n'
  assert g.next() == '\n'
  assert g.next() == 'louie\n'
  with pytest.raises(StopIteration):
    g.next()


def test_expandendoflines():
  g = cat.expandendoflines([ 'huey\n',
                             'dewey\n',
                             'louie\n' ])
  assert g.next() == 'huey$\n'
  assert g.next() == 'dewey$\n'
  assert g.next() == 'louie$\n'
  with pytest.raises(StopIteration):
    g.next()


def test_expandtabs():
  g = cat.expandtabs([ 'huey\tdewey\n',
                       '\t\tlouie\n' ])
  assert g.next() == 'huey^Idewey\n'
  assert g.next() == '^I^Ilouie\n'
  with pytest.raises(StopIteration):
    g.next()


def test_expandnonprintables():
  g = cat.expandnonprintables([ 'huey\001dewey\n',
                                '\002\003louie\n' ])
  assert g.next() == 'huey^Adewey\n'
  assert g.next() == '^B^Clouie\n'
  with pytest.raises(StopIteration):
    g.next()


def test_prependlinenumbers():
  g = cat.prependlinenumbers([ 'huey\n',
                               'dewey\n',
                               'louie\n' ])
  assert g.next() == '     1\thuey\n'
  assert g.next() == '     2\tdewey\n'
  assert g.next() == '     3\tlouie\n'
  with pytest.raises(StopIteration):
    g.next()


def test_write():
  f = StringIO.StringIO()
  ret = cat.write(f, [ 'huey\n',
                       'dewey\n',
                       'louie\n' ])
  assert ret == 0
  assert f.getvalue() == 'huey\ndewey\nlouie\n'


def test_cat():
  ret = cat.cat([], 0, [])
  assert ret == 0


def test_parseargs_noarguments():
  assert cat.parseargs({}, []) == \
                       ( {}, [] )


def test_parseargs_combinedoptions():
  assert cat.parseargs({}, [ '-v', 'filename' ]) == \
                       (
                         { 'v': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-ve', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-vet', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True, 't': True },
                         [ 'filename' ]
                       )


def test_parseargs_separateoptions():
  assert cat.parseargs({}, [ '-v', 'filename' ]) == \
                       (
                         { 'v': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-v' , '-e', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-v', '-e', '-t', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True, 't': True },
                         [ 'filename' ]
                       )


def test_checkargs():
  assert cat.checkargs({ 'e': True }) == True
  assert cat.checkargs({ 'x': True }) == False


def test_pipelineget():
  assert cat.expandendoflines not in cat.pipelineget({}, sys.stdout)
  assert cat.expandendoflines in cat.pipelineget({ 'e': True },
                                                 sys.stdout)

  assert cat.prependlinenumbers not in cat.pipelineget({}, sys.stdout)
  assert cat.prependlinenumbers in cat.pipelineget({ 'n': True },
                                                   sys.stdout)

  assert cat.removerepeatedemptylines not in cat.pipelineget({}, sys.stdout)
  assert cat.removerepeatedemptylines in cat.pipelineget({ 's': True },
                                                         sys.stdout)

  assert cat.expandtabs not in cat.pipelineget({}, sys.stdout)
  assert cat.expandtabs in cat.pipelineget({ 't': True },
                                           sys.stdout)

  assert cat.expandnonprintables not in cat.pipelineget({}, sys.stdout)
  assert cat.expandnonprintables in cat.pipelineget({ 'e': True },
                                                    sys.stdout)
  assert cat.expandnonprintables in cat.pipelineget({ 't': True },
                                                    sys.stdout)
  assert cat.expandnonprintables in cat.pipelineget({ 'v': True },
                                                    sys.stdout)


def test_main_singlefile(helloworldfile, stdin, stdout, stderr):
  ret = cat.main(stdin, stdout, stderr, [ 'file.py',
                                          str(helloworldfile) ])
  assert ret == 0
  assert stdout.getvalue() == '''\
Hello
World
'''
  assert stderr.getvalue() == ''


def test_main_multiplefiles(helloworldfile, stdin, stdout, stderr):
  ret = cat.main(stdin, stdout, stderr, [ 'file.py',
                                          str(helloworldfile),
                                          str(helloworldfile),
                                          str(helloworldfile) ])
  assert ret == 0
  assert stdout.getvalue() == '''\
Hello
World
Hello
World
Hello
World
'''
  assert stderr.getvalue() == ''


def test_usage(stdout):
  ret = cat.usage(stdout, 0)
