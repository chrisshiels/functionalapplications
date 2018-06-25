import cat


def test_parseargv_noarguments():
  assert cat.parseargv([], {}) == \
                       ( [], {} )


def test_parseargv_combinedoptions():
  assert cat.parseargv([ '-v', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True }
                       )
  assert cat.parseargv([ '-ve', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True }
                       )
  assert cat.parseargv([ '-vet', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True, 't': True }
                       )


def test_parseargv_separateoptions():
  assert cat.parseargv([ '-v', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True }
                       )
  assert cat.parseargv([ '-v' , '-e', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True }
                       )
  assert cat.parseargv([ '-v', '-e', '-t', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True, 't': True }
                       )
