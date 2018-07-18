# cat

Generator-based implementation of cat.
```
host$ virtualenv virtualenv

host$ . virtualenv/bin/activate

(virtualenv) host$ pip install -r requirements.txt

(virtualenv) host$ pytest -v

(virtualenv) host$ ./cat.py < ./cat.py
(virtualenv) host$ ./cat.py ./cat.py ./cat.py ./cat.py
(virtualenv) host$ ./cat.py -n ./cat.py
(virtualenv) host$ ./cat.py -n -vet ./cat.py
(virtualenv) host$ ./cat.py -n -vet -s ./cat.py
```
