# renamebyexif

Script to generate mv commands to rename jpg images by exif DateTimeOriginal.
```
host$ sudo dnf -y install perl-Image-ExifTool ImageMagick

host$ make

host$ virtualenv virtualenv

host$ . virtualenv/bin/activate

(virtualenv) host$ pip install -r requirements.txt

(virtualenv) host$ pytest -v
============================= test session starts ==============================
platform linux2 -- Python 2.7.13, pytest-3.2.2, py-1.4.34, pluggy-0.4.0 -- /home/chris/chris/functionalapplications/renamebyexif/virtualenv/bin/python2
cachedir: .cache
rootdir: /home/chris/chris/functionalapplications/renamebyexif, inifile:
collected 5 items

test_renamebyexif.py::test_loadexif PASSED
test_renamebyexif.py::test_exifdatetime PASSED
test_renamebyexif.py::test_parsedatetime PASSED
test_renamebyexif.py::test_filedatetime PASSED
test_renamebyexif.py::test_main PASSED

=========================== 5 passed in 0.02 seconds ===========================

(virtualenv) host$ python renamebyexif.py *.jpg

(virtualenv) host$ python renamebyexif.py *.jpg | sh -x
```
