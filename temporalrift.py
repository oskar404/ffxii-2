#!/usr/bin/env python3
"""
Final Fantasy XII-2 Temporal rift clock puzzle solver
"""

import argparse


class Node:
    def __init__(self, position, parent = None):
        self.pos = position
        self.parent = parent
        self.left = None
        self.right = None

    def has_node(self, position):
        if self.pos == position:
            return True
        elif self.parent:
            return self.parent.has_node(position)
        return False


def create_path(node, clock):
    result = []
    while node:
        result.append((node.pos, clock[node.pos]))
        node = node.parent
    result.reverse()
    return result


def search(start, clock):
    paths = []
    rflag = True

    clock_size = len(clock)
    node = Node(start)

    # iterate all branches of tree
    while node:

        # add nodes to left branch as many as possible
        while not node.left:
            rflag = True
            pos_l = node.pos - clock[node.pos]
            if pos_l < 0:
                pos_l = clock_size + pos_l
            if node.has_node(pos_l):
                break
            parent = node
            node = Node(pos_l, parent)
            parent.left = node

        # add one node to right branch
        pos_r = (node.pos + clock[node.pos]) % clock_size
        if node.has_node(pos_r):
            if rflag:
                paths.append(create_path(node, clock))
                rflag = False
            node = node.parent
        else:
            if node.right:
                node = node.parent
            else:
                rflag = True
                parent = node
                node = Node(pos_r, parent)
                parent.right = node

    # remove duplicates .. set does not work for these

    result = []
    for path in paths:
        if path not in result:
            result.append(path)
    return result


def solve(args):
    if args.verbose > 0:
        print(f'Clock: {args.clock}')
    # Brute force solving. search all possible solutions
    for start_point in range(len(args.clock)):
        paths = search(start_point, args.clock)
        for path in paths:
            is_solution = len(path) == len(args.clock)
            if args.verbose > 0 or is_solution:
                solution = ''
                if is_solution and args.verbose > 0:
                    solution = ' SOLUTION'
                human_path = [ f"{pos+1}({step})" for pos, step in path]
                print(f"path: {' > '.join(human_path)}{solution}")


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
