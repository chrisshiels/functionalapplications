import meetingscheduler


def test_listcontains():
    assert meetingscheduler.listcontains([ 1, 2, 3, 4, 5 ], [ 3, 4 ]) is True
    assert meetingscheduler.listcontains([ 1, 2, 3, 4, 5 ], [ 3, 5 ]) is False


def test_listsubtract():
    assert list(meetingscheduler.listsubtract([ 1, 2, 3, 4, 5 ], [ 3, 4 ])) == \
           [1, 2, 5]

    assert list(meetingscheduler.listsubtract([ 1, 2, 3, 4, 5 ], [ 3, 5 ])) == \
           [1, 2, 4]


def test_parsetimes():
    assert meetingscheduler.parsetimes('9-11,12-13,16-18') == \
           [9, 10, 12, 16, 17]

    assert meetingscheduler.parsetimes('9-11') == \
           [9, 10]


def test_timesmatching():
    assert meetingscheduler.timesmatching(9, 18, 2, [ '9-11,12-13,16-18',
                                                      '9-13,16-17' ]) == \
           [13, 14]
    assert meetingscheduler.timesmatching(9, 18, 3, [ '9-11,12-13',
                                                      '9-13' ]) == \
           [13, 14, 15]


def test_parse():
    assert meetingscheduler.parse([ './meetingscheduler.py',
                                    '--start', '9',
                                    '--end', '18',
                                    '--duration', '2',
                                    '9-11,12-13', '9-13' ]) == \
           {
               'start': 9,
               'end': 18,
               'duration': 2,
               'timesbusys': [ '9-11,12-13', '9-13' ]
           }


def test_main(capsys):
    assert meetingscheduler.main([ './meetingscheduler.py',
                                   '--start', '9',
                                   '--end', '18',
                                   '--duration', '2',
                                   '9-11,12-13,16-18',
                                   '9-13,16-17' ]) == 0
    assert capsys.readouterr().out == '''\
13-15
14-16
'''

    assert meetingscheduler.main([ './meetingscheduler.py',
                                   '--start', '9',
                                   '--end', '18',
                                   '--duration', '3',
                                   '9-11,12-13',
                                   '9-13' ]) == 0
    assert capsys.readouterr().out == '''\
13-16
14-17
15-18
'''

    assert meetingscheduler.main([ './meetingscheduler.py',
                                   '--start', '9',
                                   '--end', '20',
                                   '--duration', '2',
                                   '9-10,10-11,12-13,16-18',
                                   '11-13,16-17',
                                   '9-10,11-12,16-18' ]) == 0
    assert capsys.readouterr().out == '''\
13-15
14-16
18-20
'''
