#!/usr/bin/env python

# 'renamebyexif.py'.
# Chris Shiels.


import datetime
import sys

import piexif


def loadexif(filename):
  return piexif.load(filename)


def exifdatetime(exifdict):
  return exifdict['Exif'][piexif.ExifIFD.DateTimeOriginal]


def parsedatetime(exifdatetimeoriginal):
  return datetime.datetime.strptime(exifdatetimeoriginal, '%Y:%m:%d %H:%M:%S')


def filedatetime(dt):
  return dt.strftime('%Y%m%d%H%M%S.jpg')


def usage(stdin, stdout, stderr):
  print >> stderr, 'Usage:  renamebyexif file.jpg ...'
  return 0


def renamebyexif(stdin, stdout, stderr, argv):
  for arg in argv:
    arg1 = reduce(lambda a, e: e(a),
                  [ loadexif, exifdatetime, parsedatetime, filedatetime ],
                  arg)
    print >> stdout, 'mv -n {arg} {arg1}'.format(arg = arg, arg1 = arg1)
  return 0


def main(stdin, stdout, stderr, argv):
  if argv == []:
    return usage(stdin, stdout, stderr)
  else:
    return renamebyexif(stdin, stdout, stderr, argv)


if __name__ == "__main__":
  sys.exit(main(sys.stdin, sys.stdout, sys.stderr, sys.argv[1:]))
