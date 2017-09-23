# 'Makefile'.
# Chris Shiels.


test: test.jpg


test.jpg:
	convert -size 1x1 canvas:purple test.jpg
	exiftool \
		-DateTimeOriginal='1970:01:01 00:00:00' -overwrite_original \
		test.jpg


clean:
	rm -f test.jpg
