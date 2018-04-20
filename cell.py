class Cell:
    i = None
    j = None
    
    # The distance from the source node to this node.
    # Note that this value will be only used for dijkstra's algorithm 
    # while for A* f,g,h will be used.
    f = None
    
    # The cost up to till this point
    g = None
    
    # The heuristic value
    h = None
    symbol = None
    cameFrom = None
    
    # The edges is the distance between each ndde connect to this node.
    edges = None
    
    # Stores the actual nodes
    neighbours = None
    # This value will be either 1 or 2. 1 repersents we came from a straigt line direction.
    # While 2 repersents we came in a diagonal direction.
    direction = None

    def __init__(self, i, j, g, f, symbol):
        self.i = i
        self.j = j
        self.g = g
        self.f = f
        self.symbol = symbol
        self.edges = []
        self.neighbours = []

    def addNeighbour(self, node):
        self.neighbours.append(node)

    def addEdge(self, val):
        self.edges.append(val)

    def getNeighbours(self):
        return self.neighbours

    def getEgdes(self):
        return self.edges
