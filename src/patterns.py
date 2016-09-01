def _char_to_cell(char):
    if char == ".":
        return 0
    elif char == "x":
        return 1
    elif char in "0123456789":
        return int(char)
    else:
        raise Exception("Unknown cell value")

def _lista_to_patron(lista):
    patron = []
    for fila in lista:
        patron.append([])
        for char in fila:
            patron[-1].append(_char_to_cell(char))
    return patron

def string_to_patron(string):
    lista = string.split("\n")
    if lista[-1] == "":
        lista = lista[:-1]
    for fila in lista[1:]:
        assert len(fila) == len(lista[0])
    return _lista_to_patron(lista)

def patron(f, *args, **kwargs):
    """patron decorator"""
    return _lista_to_patron(f(*args, **kwargs))

@patron
def GLIDER():
    return [".x.",
            "x..",
            "xxx"]
            
@patron
def GLIDER_GUN():
    return ["..........................................",
            "...........................x..............",
            ".........................x.x..............",
            "...............xx......xx............xx...",
            "..............x...x....xx............xx...",
            "...xx........x.....x...xx.................",
            "...xx........x...x.xx....x.x..............",
            ".............x.....x.......x..............",
            "..............x...x.......................",
            "...............xx.........................",
            "..........................................",
            "..........................................",
            "..........................................",
            "...........xxxxxxxxx..........x...........",
            ".............................xxx..........",
            "..............................x...........",
            ".........................................."]

@patron
def WIREWORLD_TRACK():
    return ["...........",
            "..1111111..",
            ".1.......1.",
            "..1111111..",
            "..........."]

@patron
def WIREWORLD_DIODE():
    return ["11........11",
            ".....11.....",
            "111111.11111",
            ".....11.....",
            "11........11"]

@patron
def HIGHLIFE_REPLICATOR():
    return ["xx...xx",
            "...xxx.",
            "..x..x.",
            ".x...x.",
            ".x..x..",
            ".xxx...",
            "xx....xx"]
