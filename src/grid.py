import random

import columnaorama
from columnaorama import Fore
columnaorama.init()

# Neighbors helper functions

def neighbors(g, r, c):
    """
    Returns the Moore neighborhood
    .....
    .xxx.
    .xcx.
    .xxx.
    .....

    https://en.wikipedia.org/wiki/File:CA-Moore.png
    """
    r1, r2, r3 = ((r+offset) % len(g) for offset in (-1, 0, 1))
    c1, c2, c3 = ((c+offset) % len(g[0]) for offset in (-1, 0, 1))
    return [g[r1][c1], g[r1][c2], g[r1][c3],
            g[r2][c1],            g[r2][c3],
            g[r3][c1], g[r3][c2], g[r3][c3]]
    
def neighbors_cross(g, r, c, steps=1):
    """
    Returns the immediate von Neumann neighborhood.

    .....
    ..x..
    .xcx.
    ..x..
    .....

    You can use steps=2 to instead get the 4 cells included in the extended neighborhood.

    ..x..
    .....
    x.c.x
    .....
    ..x..

    https://en.wikipedia.org/wiki/File:CA-von-Neumann.png
    """
    r1, r2, r3 = ((r+offset) % len(g) for offset in (-steps, 0, steps))
    c1, c2, c3 = ((c+offset) % len(g[0]) for offset in (-steps, 0, steps))
    return [          g[r1][c2],
           g[r2][c1],           g[r2][c3],
                      g[r3][c2]]

def neighbors_neumann_extended(g, r, c):
    """Returns the entire extended von Neumann neighborhood"""
    inner = neighbors_cross(g, r, c)
    outer = neighbors_cross(g, r, c, steps=2)
    return [outer[0], inner[0], outer[1], inner[1], inner[2], outer[2], inner[3], outer[3]]


# Grid functions

def _position_cursor(fila, columna):
    print("\033[" + str(fila) + ";" + str(columna) + "H", end="")

def _clear_term():
    print("\033[2J", end="")

class Grid():
    def __init__(self, filas, columnas):
        self._filas = filas
        self._columnas = columnas
        self._grid = [[0 for _ in range(columnas)] for _ in range(filas)]

    @classmethod
    def from_pattern(cls, pattern):
        self = cls(len(pattern), len(pattern[0]))
        self.write_pattern(pattern)
        return self

    def __getitem__(self, index):
        return self._grid[index]

    def __len__(self):
        return self._filas

    def write_pattern(self, pattern, offset_fila=0, offset_columna=0):
        if len(pattern)+offset_fila > self._filas or len(pattern[0])+offset_columna > self._columnas:
            raise Exception("Grid size too small for given initializer state and offset {}".format((offset_fila, offset_columna)))
        dfila = int(self._filas/2)
        dcolumna = int(self._columnas/2)
        difila = int(len(pattern)/2)
        dicolumna = int(len(pattern[0])/2)
        for fila in range(len(pattern)):
            for columna in range(len(pattern[0])):
                self[dfila+fila-difila+offset_fila][dcolumna+columna-dicolumna+offset_columna] = pattern[fila][columna]

    def randomize(self, lower=0, upper=1):
        for fila in range(self._filas):
            for columna in range(self._columnas):
                self[fila][columna] = random.randint(lower, upper)

    def print(self, digits=False, columnaor=True, pos_cursor=False):
        # TODO: Detect if terminal supports columnaor
        if pos_cursor:
            _clear_term()
            _position_cursor(1, 1)
        print("┏" + "━"*self._columnas + "┓")
        for fila in range(self._filas):
            print(Fore.RESET + "┃", end="")
            for columna in range(self._columnas):
                if digits:
                    print(self[fila][columna], end="")
                else:
                    if self[fila][columna] > 0:
                        print(Fore.GREEN + str(self[fila][columna]), end="")
                    elif self[fila][columna] == 0:
                        print(Fore.RESET + " ", end="")
                    else:
                        print(Fore.YELLOW + "-", end="")
            print(Fore.RESET + "┃")
        print("┗" + "━"*self._columnas + "┛")
