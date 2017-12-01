# 'test_wordfrequencies.py'.
# Chris Shiels.


import StringIO

import wordfrequencies


def test_pipemaybe():
  def add1(x):
    return x + 1
  def addnone(x):
    return None
  assert wordfrequencies.pipemaybe([add1, add1, add1 ])(0) == \
         3
  assert wordfrequencies.pipemaybe([add1, addnone, add1 ])(0) == \
         None


def test_partial():
  def add(x, y):
    return x + y
  assert wordfrequencies.partial(add, 1)(1) == \
         2


def test_removepossessives():
  assert wordfrequencies.removepossessives('') == \
         ''
  assert wordfrequencies.removepossessives('File\'s contents') == \
         'File contents'


def test_rewritenonalphanumerics():
    assert wordfrequencies.rewritenonalphanumerics('a,b.c;d:e-f\'g"') == \
         'a b c d e f g '


def test_splitwords():
  assert wordfrequencies.splitwords('') == \
         []
  assert wordfrequencies.splitwords('aa') == \
         [ 'aa' ]
  assert wordfrequencies.splitwords('aa bb') == \
         [ 'aa', 'bb' ]
  assert wordfrequencies.splitwords('aa  bb') == \
         [ 'aa', 'bb' ]
  assert wordfrequencies.splitwords('aa bb cc') == \
         [ 'aa', 'bb', 'cc' ]
  assert wordfrequencies.splitwords('aa  bb  cc') == \
         [ 'aa', 'bb', 'cc' ]


def test_lowercasewords():
  assert wordfrequencies.lowercasewords([]) == \
         []
  assert wordfrequencies.lowercasewords([ 'aa' ]) == \
         [ 'aa' ]
  assert wordfrequencies.lowercasewords([ 'AA' ]) == \
         [ 'aa' ]
  assert wordfrequencies.lowercasewords([ 'aa', 'bb' ]) == \
         [ 'aa', 'bb' ]
  assert wordfrequencies.lowercasewords([ 'AA', 'BB' ]) == \
         [ 'aa', 'bb' ]


def test_dictfrequencies():
  assert wordfrequencies.dictfrequencies([]) == \
         {}
  assert wordfrequencies.dictfrequencies([ 'aa' ]) == \
         { 'aa': 1 }
  assert wordfrequencies.dictfrequencies([ 'aa', 'bb' ]) == \
         {
           'aa': 1,
           'bb': 1
         }
  assert wordfrequencies.dictfrequencies([ 'aa', 'bb', 'aa' ]) == \
         {
           'aa': 2,
           'bb': 1
         }
  assert wordfrequencies.dictfrequencies([ 'aa', 'bb', 'aa', 'bb' ]) == \
         {
           'aa': 2,
           'bb': 2
         }


def test_listfrequencies():
  assert wordfrequencies.listfrequencies({}) == \
         []
  assert wordfrequencies.listfrequencies({ 'aa': 1 }) == \
         [ { 'word': 'aa', 'count': 1 } ]
  assert wordfrequencies.listfrequencies({
                                           'aa': 1,
                                           'bb': 1
                                         }) == \
         [
           { 'word': 'aa', 'count': 1 },
           { 'word': 'bb', 'count': 1 }
         ]
  assert wordfrequencies.listfrequencies({
                                           'aa': 1,
                                           'bb': 2
                                         }) == \
         [
           { 'word': 'aa', 'count': 1 },
           { 'word': 'bb', 'count': 2 }
         ]


def test_sortfrequencies():
  assert wordfrequencies.sortfrequencies([]) == \
         []
  assert wordfrequencies.sortfrequencies([
                                           { 'word': 'aa', 'count': 1 },
                                           { 'word': 'bb', 'count': 2 }
                                         ]) == \
         [
           { 'word': 'bb', 'count': 2 },
           { 'word': 'aa', 'count': 1 }
         ]


def test_outputfrequencies():
  stdout = StringIO.StringIO()
  ret = wordfrequencies.outputfrequencies(stdout,
                                          [
                                            { 'word': 'bb', 'count': 2 },
                                            { 'word': 'aa', 'count': 1 }
                                          ])
  assert ret == 0
  assert stdout.getvalue() == """\
2 bb
1 aa
"""
  stdout.close()


def test_wordfrequencies():
  stdout = StringIO.StringIO()
  ret = wordfrequencies.wordfrequencies(stdout,
                                        'No hay mal que por bien no venga')
  assert ret == 0
  assert stdout.getvalue() == """\
2 no
1 bien
1 hay
1 mal
1 por
1 que
1 venga
"""
  stdout.close()
