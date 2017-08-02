# 'test_life.py'.


import StringIO

import life


def test_reverse():
  assert life.reverse([]) == \
         []
  assert life.reverse([1]) == \
         [1]
  assert life.reverse([5, 4, 3, 2, 1]) == \
         [1, 2, 3, 4, 5]


def test_gridnew():
  g = life.gridnew(20, 20, lambda: 0)
  assert g['lenx'] == \
         20
  assert g['leny'] == \
         20
  assert len(g['cells']) == \
         20 * 20
  assert filter(lambda e: e != 0, g['cells']) == \
         []


def test_gridxytoindex():
  g = life.gridnew(20, 20)
  assert life.gridxytoindex(g, 0, 0) == \
         0
  assert life.gridxytoindex(g, 19, 0) == \
         19
  assert life.gridxytoindex(g, 0, 1) == \
         20
  assert life.gridxytoindex(g, 19, 19) == \
         20 * 20 - 1
  assert life.gridxytoindex(g, 20, 0) == \
         0
  assert life.gridxytoindex(g, 0, 20) == \
         0
  assert life.gridxytoindex(g, 20, 20) == \
         0


def test_gridindextoxy():
  g = life.gridnew(20, 20)
  assert life.gridindextoxy(g, 0) == \
         (0, 0)
  assert life.gridindextoxy(g, 19) == \
         (19, 0)
  assert life.gridindextoxy(g, 20) == \
         (0, 1)
  assert life.gridindextoxy(g, 20 * 20 - 1) == \
         (19, 19)
  assert life.gridindextoxy(g, 20 * 20) == \
         (0, 0)
  assert life.gridindextoxy(g, 20 * 20 + 1) == \
         (1, 0)
  assert life.gridindextoxy(g, 20 * 20 + 2) == \
         (2, 0)


def test_gridset():
  g = life.gridnew(20, 20)
  g = reduce(lambda a, e: life.gridset(a, e, e, 1), range(20), g)
  assert len(filter(lambda e: life.gridget(g, e, e) == 1, range(20))) == \
         20


def test_gridget():
  g = life.gridnew(20, 20)
  g = reduce(lambda a, e: life.gridset(a, e, e, 1), range(20), g)
  assert len(filter(lambda e: life.gridget(g, e, e) == 1, range(20))) == \
         len(filter(lambda e: g['cells'][e] == 1, range(20 * 20)))


def test_gridprint():
  f = StringIO.StringIO()
  g = life.gridnew(20, 20)
  g = reduce(lambda a, e: life.gridset(a, e, e, 1), range(20), g)
  life.gridprint(g, f)
  assert f.getvalue() == \
         reduce(lambda a, e: a +
                             ('. ' * e) + 'o ' + ('. ' * (20 - e - 1)) + "\n",
                life.reverse(range(20)),
                '')
  f.close()


def test_gridneighbours():
  g = life.gridnew(20, 20)
  g = reduce(lambda a, e: life.gridset(a, e, e, 1), range(20), g)
  assert life.gridneighbours(g, 0, 0) == \
         2
  assert life.gridneighbours(g, 1, 0) == \
         2
  assert life.gridneighbours(g, 2, 0) == \
         1
  assert life.gridneighbours(g, 3, 0) == \
         0


def test_gridtick():
  g = life.gridnew(20, 20)
  assert g['lenx'] == \
         20
  assert g['leny'] == \
         20
  assert len(g['cells']) == \
         20 * 20


def test_b3s23():
  assert life.b3s23(0, 3) == \
         1
  assert life.b3s23(1, 2) == \
         1
  assert life.b3s23(1, 3) == \
         1
  assert life.b3s23(5, 5) == \
         0


def test_gridload():
  g = life.gridload(life.gridnew(20, 20, lambda: 0), [], 0, 0)
  assert len(filter(lambda e: e != 0, g['cells'])) == 0


def test_glider():
  g = life.gridload(life.gridnew(20, 20), life.glider(), 0, 0)
  assert len(filter(lambda e: e != 0, g['cells'])) == 5


def test_pentadecathlon():
  g = life.gridload(life.gridnew(20, 20), life.pentadecathlon(), 0, 0)
  assert len(filter(lambda e: e != 0, g['cells'])) == 12
