# 'test_renamebyexif.py'.
# Chris Shiels.


import datetime
import StringIO

import renamebyexif


def test_loadexif():
  exifdict = renamebyexif.loadexif('test.jpg')
  assert exifdict.__class__ == dict
  assert 'Exif' in exifdict
  assert 36867 in exifdict['Exif']


def test_exifdatetime():
  exifdatetimeoriginal = \
    renamebyexif.exifdatetime(renamebyexif.loadexif('test.jpg'))
  assert exifdatetimeoriginal == '1970:01:01 00:00:00'


def test_parsedatetime():
  dt = renamebyexif.parsedatetime('1970:01:01 00:00:00')
  assert dt.year == 1970
  assert dt.month == 1
  assert dt.day == 1
  assert dt.hour == 0
  assert dt.minute == 0
  assert dt.second == 0


def test_filedatetime():
  filedatetime = \
    renamebyexif.filedatetime(datetime.datetime(1970, 1, 1, 0, 0, 0))
  assert filedatetime == '19700101000000.jpg'


def test_main1():
  stdout = StringIO.StringIO()
  stderr = StringIO.StringIO()
  ret = renamebyexif.main(None, stdout, stderr, [])
  assert ret == 0
  assert stdout.getvalue() == ''
  assert stderr.getvalue() == 'Usage:  renamebyexif file.jpg ...\n'
  stdout.close()
  stderr.close()


def test_main2():
  stdout = StringIO.StringIO()
  stderr = StringIO.StringIO()
  ret = renamebyexif.main(None, stdout, stderr, [ 'test.jpg' ])
  assert ret == 0
  assert stdout.getvalue() == 'mv -n test.jpg 19700101000000.jpg\n'
  assert stderr.getvalue() == ''
  stdout.close()
  stderr.close()
