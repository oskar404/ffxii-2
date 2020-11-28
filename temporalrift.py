#!/usr/bin/env python3
"""
Final Fantasy XII-2 Temporal rift clock puzzle solver
"""

import argparse


def search(start, clock):
    steps = []
    size = len(clock)
    pos = start
    visited = [False for _ in range(len(clock))]
    while not visited[pos]:
        visited[pos] = True
        step = clock[pos]
        steps.append((pos+1, step))
        pos = (pos + step) % size
    return [steps]


def solve(args):
    if args.verbose > 0:
        print(f'Clock: {args.clock}')
    # Brute force solving. search all possible solutions
    for start_point in range(len(args.clock)):
        paths = search(start_point, args.clock)
        for p in paths:
            is_solution = len(p) == len(args.clock)
            if args.verbose > 0 or is_solution:
                solution = ''
                if is_solution and args.verbose > 0:
                    solution = ' SOLUTION'
                print(f'path: {p} (start: {start_point+1}){solution}')


def validate(clock):
    assert len(clock) <= 12, 'Maximum number of elements in clock is 12'
    invalid = [x for x in clock if x > 6 or x < 1]
    assert len(invalid) == 0, 'Supported numbers are from 1 to 6'


def create_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'clock',
        help=('Number describing how to jump to next position. '
              ' Supported numbers from 1 to 6. Maximum list size is 12'),
        metavar='NUMBER',
        type=int,
        nargs='+')
    parser.add_argument(
        '-v', '--verbose',
        help='Add verbosity i.e print more than just solutions',
        action='count',
        default=0)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    validate(args.clock)
    solve(args)


if __name__ == "__main__":
    main()
