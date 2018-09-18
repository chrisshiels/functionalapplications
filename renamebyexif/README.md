# renamebyexif

Pipeline-based jpg image renamer using exif DateTimeOriginal.
```
host$ sudo dnf -y install perl-Image-ExifTool ImageMagick

host$ make

host$ virtualenv virtualenv

host$ . virtualenv/bin/activate

(virtualenv) host$ pip install -r requirements.txt

(virtualenv) host$ pytest -v

(virtualenv) host$ python renamebyexif.py *.jpg

(virtualenv) host$ python renamebyexif.py *.jpg | sh -x
```
