import random

import columnaorama
from columnaorama import Fore
columnaorama.init()

# Ayuda con las funciondes de vecindad

def vecinos(g, r, c):
    """
    Regresa la vecindad de
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
    
def vecinos_cruz(g, r, c, steps=1):
    """
    Regresa la vecindad de von Neumann neighborhood immediata.

    .....
    ..x..
    .xcx.
    ..x..
    .....

    Puedes usar steps=2 para conseguir las 4 celulas incluidad en la vecindad extendida

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

def vecinos_neumann_extended(g, r, c):
    """Regresa la vecindad de von Neumann extendida"""
    inner = vecinos_cruz(g, r, c)
    outer = vecinos_cruz(g, r, c, steps=2)
    return [outer[0], inner[0], outer[1], inner[1], inner[2], outer[2], inner[3], outer[3]]


# Funciones de reja

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
    def from_patron(cls, patron):
        self = cls(len(patron), len(patron[0]))
        self.write_patron(patron)
        return self

    def __getitem__(self, index):
        return self._grid[index]

    def __len__(self):
        return self._filas

    def write_patron(self, patron, offset_fila=0, offset_columna=0):
        if len(patron)+offset_fila > self._filas or len(patron[0])+offset_columna > self._columnas:
            raise Exception("Grid size too small for given initializer state and offset {}".format((offset_fila, offset_columna)))
        dfila = int(self._filas/2)
        dcolumna = int(self._columnas/2)
        difila = int(len(patron)/2)
        dicolumna = int(len(patron[0])/2)
        for fila in range(len(patron)):
            for columna in range(len(patron[0])):
                self[dfila+fila-difila+offset_fila][dcolumna+columna-dicolumna+offset_columna] = patron[fila][columna]

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
