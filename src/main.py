from time import sleep
import sys
import argparse

from .grid import *
from .patrons import *
from .rules import *

from . import examples


def patron_from_stdin():
    # TODO: Habilita la elecion de regla
    patron = sys.stdin.read()
    patron = string_to_patron(patron)
    grid = Grid.from_patron(patron)
    while True:
        grid.print(pos_cursor=True)
        grid = apply_rule(grid, rule_conway)
        sleep(0.1)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--example', dest='example',
                        help='specify an example to run')
    parser.add_argument('--from-stdin', dest='from_stdin', action='store_const',
                        const=True, default=False,
                        help='load patron from stdin')

    args = parser.parse_args()

    if args.example:
        examples.run_example(args.example)
    elif args.from_stdin:
        patron_from_stdin()
    else:
        examples.glider_gun()


if __name__ == "__main__":
    main()
