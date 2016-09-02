from time import sleep

from .grid import *
from .rules import *
from .patrons import *


_examples = {}

def example(f):
    """A decorador que registra una función como un ejemplo"""
    _examples[f.__name__] = f
    return f

@example
def glider_gun():
    filas = 30
    columnas = 60
    grid = Grid(filas, columnas)
    grid.write_patron(GLIDER_GUN)
    while True:
        grid.print(pos_cursor=True)
        grid = apply_rule(grid, rule_conway)
        sleep(0.1)

@example
def wireworld():
    filas = 5
    columnas = 15
    grid = Grid(filas, columnas)
    grid.write_patron(WIREWORLD_TRACK)
    grid[1][4] = 2
    grid[1][5] = 3
    while True:
        grid.print(pos_cursor=True)
        grid = apply_rule(grid, rule_wireworld)
        sleep(0.1)

@example
def wireworld_diodes():
    filas = 9
    columnas = 12
    grid = Grid(filas, columnas)

    # Dibuja un diodo con la entrada en la realización de dirección
    grid.write_patron(WIREWORLD_DIODE, offset_fila = -2)
    grid[2][3] = 3
    grid[2][4] = 2

    # Escribe diodo con el aporte de diodo anterior en el aislamiento de dirección
    grid.write_patron(WIREWORLD_DIODE, offset_fila = 2)
    grid[6][11] = 0
    for i in range(3, 6):
        grid[i][10] = 1

    while True:
        grid.print(pos_cursor=True)
        grid = apply_rule(grid, rule_wireworld)
        sleep(0.1)

@example
def highlife_replicator():
    filas = 40
    columnas = 40
    grid = Grid(filas, columnas)
    grid.write_patron(HIGHLIFE_REPLICATOR)
    while True:
        grid.print(pos_cursor=True)
        grid = apply_rule(grid, rule_highlife)
        sleep(0.1)

def run_example(name):
    _examples[name]()
