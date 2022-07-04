# meetingscheduler


```
host$ # Setup.
host$ virtualenv virtualenv
host$ . virtualenv/bin/activate
(virtualenv) host$ pip install -r ./requirements.txt


(virtualenv) host$ # Run tests.
(virtualenv) host$ pytest -v --cov
============================= test session starts ==============================
platform linux -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0 -- /home/chris/functionalapplications/meetingscheduler/virtualenv/bin/python
cachedir: .pytest_cache
rootdir: /home/chris/functionalapplications/meetingscheduler
plugins: cov-3.0.0
collected 6 items

test_meetingscheduler.py::test_listcontains PASSED                       [ 16%]
test_meetingscheduler.py::test_listsubtract PASSED                       [ 33%]
test_meetingscheduler.py::test_parsetimes PASSED                         [ 50%]
test_meetingscheduler.py::test_timesmatching PASSED                      [ 66%]
test_meetingscheduler.py::test_parse PASSED                              [ 83%]
test_meetingscheduler.py::test_main PASSED                               [100%]

---------- coverage: platform linux, python 3.10.5-final-0 -----------
Name                       Stmts   Miss  Cover
----------------------------------------------
meetingscheduler.py           36      0   100%
test_meetingscheduler.py      22      0   100%
----------------------------------------------
TOTAL                         58      0   100%


============================== 6 passed in 0.05s ===============================


(virtualenv) host$ # Schedule a meeting between 09:00 and 18:00 for two hours
(virtualenv) host$ # for two people where
(virtualenv) host$ # person 1 is busy through 09:00-11:00,12:00-13:00,16:00-18:00 and
(virtualenv) host$ # person 2 is busy through 09:00-13:00,16:00-17:00.
(virtualenv) host$ ./meetingscheduler.py --start 9 --end 18 --duration 2 \
        9-11,12-13,16-18 9-13,16-17
13-15
14-16


(virtualenv) host$ # Schedule a meeting between 09:00 and 18:00 for three hours
(virtualenv) host$ # for two people where
(virtualenv) host$ # person 1 is busy through 09:00-11:00,12:00-13:00 and
(virtualenv) host$ # person 2 is busy through 09:00-13:00.
(virtualenv) host$ ./meetingscheduler.py --start 9 --end 18 --duration 3 \
        9-11,12-13 9-13
13-16
14-17
15-18


(virtualenv) host$ # Schedule a meeting between 09:00 and 20:00 for two hours
(virtualenv) host$ # for three people where
(virtualenv) host$ # person 1 is busy through 09:00-10:00,10:00-11:00,12:00-13:00,16:00-18:00 and
(virtualenv) host$ # person 2 is busy through 11:00-13:00,16:00-17:00 and
(virtualenv) host$ # person 3 is busy through 09:00-10:00,11:00-12:00,16:00-18:00.
(virtualenv) host$ ./meetingscheduler.py --start 9 --end 20 --duration 2 \
        9-10,10-11,12-13,16-18 11-13,16-17 9-10,11-12,16-18
13-15
14-16
18-20
```
