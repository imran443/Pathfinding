import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from cell import Cell
from random import randint

np.set_printoptions(threshold=np.nan)
gameMapInternal = np.empty((100, 100), dtype=np.object)

# Coordinates for the start node and end node.
startNode = [1, 1]
endNode = [98, 98]

# Creates a cell object and stores it in a internal repersentation of the map.
def preProcessMap(gameMap):
    for i in range(gameMap.shape[0]):
        for j in range(gameMap.shape[0]):
            if(gameMap[i][j] != '@'):
                cell = Cell(i, j, randint(1,10), gameMap[i][j], False)
                gameMapInternal[i][j] = cell
            else:
                cell = Cell(i, j, randint(1,10), gameMap[i][j], True)
                gameMapInternal[i][j] = cell
    return

def main():
    gameMap = np.genfromtxt(sys.path[0] + r'\adaptiveDepth\adaptive-depth-1.txt', skip_header=4, dtype=str, delimiter='\n' )
    preProcessMap(gameMap)
    print(gameMapInternal[98][98].symbol)
    
    return

if __name__ == '__main__':
    main()