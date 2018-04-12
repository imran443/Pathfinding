class Cell:
    i = None
    j = None
    f = None
    g = None
    h = None
    symbol = None
    cameFrom = None
    isWall = False
    neighbours = []
    
    def __init__(self, i, j, f, symbol, isWall):
        self.i = i
        self.j = j
        self.f = f
        self.symbol = symbol
        self.isWall = False
