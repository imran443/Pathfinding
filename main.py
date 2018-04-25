# Imran Qureshi, 5510631

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from random import randint
import math
import datetime
import csv

# My class imports
from cell import Cell
from dijkstra import Dijkstra
from astar import AStar
from jps import JPS
from display import Display

np.set_printoptions(threshold=np.nan)

# The edge value ranges.
minimum, max = 1, 1

# Indexes for starting and ending positions
startNodeXY = None
endNodeXY = None

fileName = "adaptive-depth-1"
# newFileName = fileName + "-results.txt"

# f = open(newFileName, 'w', newline="")

# Creates a cell object and stores it in a internal repersentation of the map.
def preProcessMap(gameMap, gameMapInternal, startNodeXY):
    
    for i in range(gameMap.shape[0]):
        for j in range(gameMap.shape[0]):
            
            if(gameMap[i][j] != '@'):
                # if initial node then set 
                if(i == startNodeXY[0] and j == startNodeXY[1]):
                    cell = Cell(i, j, 0, 0, gameMap[i][j])
                    gameMapInternal[i][j] = cell
                    continue

                cell = Cell(i, j, sys.maxsize, sys.maxsize, gameMap[i][j])
                gameMapInternal[i][j] = cell
            
            else:
                cell = Cell(i, j, 0, 0, gameMap[i][j])
                gameMapInternal[i][j] = cell
    
# This function finds neighbours of each node, and does not add walls as a neighbour.
def findNeighbours(gameMap, gameMapInternal):
    # For each node add all possible neighbours and corresponding edges.
    for i in range(gameMap.shape[0]):
        for j in range(gameMap.shape[0]):
            # If the current cell is not a wall then find it's neighbours.
            if (gameMap[i][j] != '@'):
                currentNode = gameMapInternal[i][j]
                
                # above
                if (i - 1 > 0 and gameMapInternal[i-1][j] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i-1][j])
                    currentNode.addEdge(randint(minimum, max))
                
                # right
                if (j + 1 < gameMap.shape[0] and gameMapInternal[i][j+1] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i][j+1])
                    currentNode.addEdge(randint(minimum, max))
                
                # below
                if (i + 1 < gameMap.shape[0] and gameMapInternal[i+1][j] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i+1][j])
                    currentNode.addEdge(randint(minimum, max))

                # left
                if(j - 1 > 0 and gameMapInternal[i][j-1] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i][j-1])
                    currentNode.addEdge(randint(minimum, max))

                # top right
                if (i - 1 > 0 and j + 1 < gameMap.shape[0] and gameMapInternal[i-1][j+1] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i-1][j+1])
                    currentNode.addEdge(randint(minimum, max))
                
                # bottom right
                if (i + 1 < gameMap.shape[0] and j + 1 < gameMap.shape[0] and gameMapInternal[i+1][j+1] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i+1][j+1])
                    currentNode.addEdge(randint(minimum, max))
                
                # bottom left
                if(i + 1 < gameMap.shape[0] and j - 1 > 0 and gameMapInternal[i+1][j-1] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i+1][j-1])
                    currentNode.addEdge(randint(minimum, max))
                
                # top left
                if(i - 1 > 0 and j - 1 > 0 and gameMapInternal[i-1][j-1] != '@'):
                    currentNode.addNeighbour(gameMapInternal[i-1][j-1])
                    currentNode.addEdge(randint(minimum, max))

# This method will set the heuristic value on each node in the graph. 
# This value will be the euclidean distance to the end node.
def setHeuristicVals(gameMapInternal, endNode):
    
    for i in range(gameMapInternal.shape[0]):
        for j in range(gameMapInternal.shape[0]):
            currentNode = gameMapInternal[i][j]
            currentNode.h = heuristic(currentNode.i, endNode.i, currentNode.j, endNode.j)

# Sets the heuristic value up for each node in the array.
def heuristic(x1, x2, y1, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def printMap(map):
    temp = np.ndarray.tolist(map)
    str2 = ''
    for line in temp:
        str1=''.join(line)
        str2 += str1 + '\n'
    print(str2)

def createMap():
    global startNodeXY
    global endNodeXY

    tempMap = np.genfromtxt(sys.path[0] + "\\adaptiveDepth\\" + fileName + ".txt", skip_header=4, dtype=str, delimiter='\n')
    gameMap = np.empty((tempMap.shape[0], tempMap.shape[0]), dtype=str)
    
    for i in range(tempMap.shape[0]):
        for j in range(tempMap.shape[0]):
            gameMap[i][j] = tempMap[i][j]
    
    # Holds the array of objects which repersent the gameMap.
    gameMapInternal = np.empty((gameMap.shape[0], gameMap.shape[0]), dtype=np.object)
    
    # The index for starting node and ending node
    startNodeXY = [1, 1]
    endNodeXY = [gameMap.shape[0]-2, gameMap.shape[0]-2]

    preProcessMap(gameMap, gameMapInternal, startNodeXY)
    findNeighbours(gameMap, gameMapInternal)
    
    return gameMap, gameMapInternal
    
    
def main():
    continueProcessing = 'Y'
    
    while (continueProcessing == 'y' or continueProcessing == 'Y'):
        # Creates and return the string and object repersentation of the map.
        gameMap, gameMapInternal = createMap()

        # The actual start and end nodes.
        startNode = gameMapInternal[startNodeXY[0]][startNodeXY[1]]
        endNode = gameMapInternal[endNodeXY[0]][endNodeXY[1]]

        algoChoice = input("Choose which algorithm to run? (D - Dijkstra, A - A Star, J - Jump Point Search): ")
        
        # Used for recording time for each algorithm run.
        startTime = datetime.datetime.now()
        
        nodesExpanded = 0
        displayGame = None

        if (algoChoice == 'D' or algoChoice == 'd'):
            # Each tuple added to the queue will have a second value as a counter to break ties.
            dijkstra = Dijkstra((startNode.f, 0, startNode), endNode)
            dijkstraMap, nodesExpanded = dijkstra.dijkstraAlgo(gameMapInternal, gameMap)
            displayPath = Display(dijkstraMap)
            displayPath.createMap()
            printMap(dijkstraMap)
            
            # Prints results to file.
            # f.write("Dijkstra: \n")
            # f.write("Beginning position: " + str(startNodeXY[0]) + "," + str(startNodeXY[1]) + " Ending position: " + str(endNodeXY[0]) + ", " + str(endNodeXY[1]) + "\n")
            # f.write("Running on file: " + fileName + "\n")

        elif (algoChoice == 'A' or algoChoice == 'a'):
            # This sets up the heuristic values for AStar.
            setHeuristicVals(gameMapInternal, endNode)
            aStar = AStar((startNode.h, 0, startNode), endNode)
            aStarMap, nodesExpanded = aStar.aStarAlgo(gameMapInternal, gameMap)
            displayPath = Display(aStarMap)
            displayPath.createMap()
            printMap(aStarMap)

            # f.write("A-Star: \n")
            # f.write("Beginning position: " + str(startNodeXY[0]) + "," + str(startNodeXY[1]) + " Ending position: " + str(endNodeXY[0]) + ", " + str(endNodeXY[1]) + "\n")
            # f.write("Running on file: " + fileName + "\n")


        elif (algoChoice == 'J' or algoChoice == 'j'):
            jps = JPS(startNode, endNode)
            jpsMap, nodesExpanded = jps.JPSAlgo(gameMapInternal, gameMap)
            displayPath = Display(jpsMap)
            displayPath.createMap()
            printMap(jpsMap)
            # f.write("JPS: \n")
            # f.write("Beginning position: " + str(startNodeXY[0]) + "," + str(startNodeXY[1]) + " Ending position: " + str(endNodeXY[0]) + ", " + str(endNodeXY[1]) + "\n")
            # f.write("Running on file: " + fileName + "\n")

        
        endTime = datetime.datetime.now()
        
        timeElapsed = endTime - startTime
        
        print("Time: ", timeElapsed)
        # f.write("Time: " + str(timeElapsed) + "\n")

        print("Nodes searched: ", nodesExpanded)
        # f.write("Nodes searched: " + str(nodesExpanded) + "\n")
        # f.write("------------------------------------------------------------------ \n")

        continueProcessing = input("Would you like to continue? (Y or N): ")
    
    # f.close()

if __name__ == '__main__':
    main()