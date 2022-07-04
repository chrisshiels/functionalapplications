#!/usr/bin/env python


import argparse
import functools
import sys


def listcontains(l1, l2):
    """
    listcontains([ 1, 2, 3, 4, 5 ], [ 3, 4 ])
    # => True

    listcontains([ 1, 2, 3, 4, 5 ], [ 3, 5 ])
    # => False
    """
    for i in range(len(l1) - len(l2)):
        if l1[i:i + len(l2)] == l2:
            return True
    return False


def listsubtract(l1, l2):
    """
    list(listsubtract([ 1, 2, 3, 4, 5 ], [ 3, 4 ]))
    # => [1, 2, 5]

    list(listsubtract([ 1, 2, 3, 4, 5 ], [ 3, 5 ]))
    # => [1, 2, 4]
    """
    return filter(lambda e: e not in l2, l1)


def parsetimes(times):
    """
    parsetimes('9-11,12-13,16-18')
    # => [9, 10, 12, 16, 17]

    parsetimes('9-11')
    # => [9, 10]
    """
    ret = []
    for time in times.split(','):
        (start, end) = time.split('-')
        ret += range(int(start), int(end))
    return ret


def timesmatching(start, end, duration, timesbusys):
    """
    timesmatching(9, 18, 2, [ '9-11,12-13,16-18',
                              '9-13,16-17' ])
    # => [13, 14]

    timesmatching(9, 18, 3, [ '9-11,12-13',
                              '9-13' ])
    # => [13, 14, 15]
    """
    timesall = list(range(start, end + 1))
    timesbusysparsed = list(map(parsetimes, timesbusys))
    timesavailable = \
        list(functools.reduce(listsubtract, timesbusysparsed, timesall))
    timesmatching = \
        list(filter(lambda e: listcontains(timesavailable,
                                           list(range(e, e + duration))),
                    timesavailable))
    return timesmatching


def parse(argv):
    """
    parse([ './meetingscheduler.py',
            '--start', '9',
            '--end', '18',
            '--duration', '2',
            '9-11,12-13', '9-13' ])
    # => {
             'start': 9,
             'end': 18,
             'duration': 2,
             'timesbusys': [ '9-11,12-13', '9-13' ]
         }
    """
    argumentparser = argparse.ArgumentParser(description = 'Meeting scheduler')
    argumentparser.add_argument('--start',
                                type = int,
                                required = True,
                                help = 'Start of the day, e.g. 9')
    argumentparser.add_argument('--end',
                                type = int,
                                required = True,
                                help = 'End of the day, e.g. 18')
    argumentparser.add_argument('--duration',
                                type = int,
                                required = True,
                                help = 'Meeting duration, e.g. 2')
    argumentparser.add_argument('timesbusys',
                                type = str,
                                nargs = '+',
                                help = 'Busy times, e.g. 9-11,12-13 9-13')
    args = argumentparser.parse_args(argv[1:])
    return vars(args)


def main(argv):
    args = parse(argv)
    for timematching in timesmatching(args['start'],
                                      args['end'],
                                      args['duration'],
                                      args['timesbusys']):
        print('%d-%d' % (timematching, timematching + args['duration']))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))  # pragma: nocover


# host$ ./meetingscheduler.py --start 9 --end 18 --duration 2 \
#         9-11,12-13,16-18 9-13,16-17
# 13-15
# 14-16
#
# host$ ./meetingscheduler.py --start 9 --end 18 --duration 3 \
#         9-11,12-13 9-13
# 13-16
# 14-17
# 15-18
#
# host$ ./meetingscheduler.py --start 9 --end 20 --duration 2 \
#         9-10,10-11,12-13,16-18 11-13,16-17 9-10,11-12,16-18
# 13-15
# 14-16
# 18-20
