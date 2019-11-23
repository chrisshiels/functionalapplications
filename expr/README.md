# expr

Parser combinator-based implementation of expr.
```
host$ virtualenv virtualenv

host$ . virtualenv/bin/activate

(virtualenv) host$ pip install -r requirements.txt

(virtualenv) host$ pytest -v

(virtualenv) host$ ./expr.py 4 + 4 \* 2
12
(virtualenv) host$ ./expr.py '4 + 4 * 2'
12
(virtualenv) host$ ./expr.py '4 + 4 + 4'
12
(virtualenv) host$ echo '(6 + 6) / (2 + 2)' | ./expr.py
3
```
