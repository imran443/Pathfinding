from queue import PriorityQueue

class JPS():
    
    class FoundPath(Exception):
        pass

   # The list which will hold the nodes as we go through.
    pq = None
    vistedList = []
    goalNode = None
    gameMapInternal = None
    counter = 0

    def __init__(self, initNode, endNode):
        self.pq = PriorityQueue()
        self.pq.put((0, self.counter, initNode))
        self.goalNode = endNode
        

    def JPSAlgo(self, gameMapInternal, gameMap):
        self.gameMapInternal = gameMapInternal

        while(not self.pq.empty()):
            # Get the tuple with the smallest distance to the goal node value.
            priorityItem = self.pq.get()
            currentNode = priorityItem[2]
            currentNodeX = currentNode.i
            currentNodeY = currentNode.j
            if(currentNode not in self.vistedList):
                self.vistedList.append(currentNode)
            
            # Check all cardinal directions first then all diagonals.
            try:
                self.addJumpPointToQueue(self.checkCardinalDirection(currentNodeX, currentNodeY, -1, 0), self.counter)
                self.addJumpPointToQueue(self.checkCardinalDirection(currentNodeX, currentNodeY, 0, 1), self.counter)
                self.addJumpPointToQueue(self.checkCardinalDirection(currentNodeX, currentNodeY, 1, 0), self.counter)
                self.addJumpPointToQueue(self.checkCardinalDirection(currentNodeX, currentNodeY, 0, -1), self.counter)

                self.addJumpPointToQueue(self.checkDiagonalDirection(currentNodeX, currentNodeY, -1, 1), self.counter)
                self.addJumpPointToQueue(self.checkDiagonalDirection(currentNodeX, currentNodeY, 1, 1), self.counter)
                self.addJumpPointToQueue(self.checkDiagonalDirection(currentNodeX, currentNodeY, 1, -1), self.counter)
                self.addJumpPointToQueue(self.checkDiagonalDirection(currentNodeX, currentNodeY, -1, -1), self.counter)
            
            # Throw this exception when the goal node has been found.
            except self.FoundPath:
                updatedGameMap = self.tracePath(self.goalNode, gameMap)
                return updatedGameMap, self.counter
            
    # A general method for checking all directions north/south etc.
    def checkCardinalDirection(self, startX, startY, directionX, directionY):
        currentX, currentY = startX, startY
        curStepCost = self.gameMapInternal[currentX][currentY].g

        while(True):
            
            currentX += directionX
            currentY += directionY
            selectedNode = self.gameMapInternal[currentX][currentY]
            curStepCost += 1
            # If the selected node is not a wall and has not been previously visted and not the goal node. 
            # Then modify it with the current cost and where it came from.
            if (selectedNode.symbol != "@" and selectedNode not in self.vistedList and selectedNode != self.goalNode):
                selectedNode.g = curStepCost
                selectedNode.cameFrom = self.gameMapInternal[currentX - directionX][currentY - directionY]
                self.vistedList.append(selectedNode)

            elif (selectedNode == self.goalNode):
                self.goalNode.cameFrom = self.gameMapInternal[currentX - directionX][currentY - directionY]
                raise self.FoundPath()

            else:
                return None
            
            # Checks for jump points and returns immeadiatly if one is found.
            if directionX == 0: 
                if self.gameMapInternal [currentX + 1] [currentY].symbol == "@" and self.gameMapInternal [currentX + 1] [currentY + directionY].symbol != "@":
                    return selectedNode
                if self.gameMapInternal [currentX - 1] [currentY].symbol == "@" and self.gameMapInternal [currentX - 1] [currentY + directionY].symbol != "@":
                    return selectedNode
            elif directionY == 0:
                if self.gameMapInternal [currentX] [currentY + 1].symbol == "@" and self.gameMapInternal [currentX + directionX] [currentY + 1].symbol != "@":
                    return selectedNode
                if self.gameMapInternal [currentX] [currentY - 1].symbol == "@" and self.gameMapInternal [currentX + directionX] [currentY - 1].symbol != "@":
                    return selectedNode

    # This method checks all diagonal directions
    def checkDiagonalDirection(self, startX, startY, directionX, directionY):
        currentX, currentY = startX, startY
        curStepCost = self.gameMapInternal[currentX][currentY].g

        while(True):
            currentX += directionX
            currentY += directionY
            selectedNode = self.gameMapInternal[currentX][currentY]
            curStepCost += 1

            if (selectedNode.symbol != "@" and selectedNode not in self.vistedList and selectedNode != self.goalNode):
                selectedNode.g = curStepCost
                selectedNode.cameFrom = self.gameMapInternal[currentX - directionX][currentY - directionY]
                self.vistedList.append(selectedNode)

            elif (selectedNode == self.goalNode):
                self.goalNode.cameFrom = self.gameMapInternal[currentX - directionX][currentY - directionY]
                raise self.FoundPath()

            else:
                return None

            # If a jump point is found, 
            if self.gameMapInternal [currentX + directionX] [currentY].symbol == "@" and self.gameMapInternal [currentX + directionX] [currentY + directionY].symbol != "@":
                return selectedNode
            
            else: # Otherwise, extend a horizontal "tendril" to probe the self.gameMapInternal.
                self.addJumpPointToQueue(self.checkCardinalDirection (currentX, currentY, directionX, 0), self.counter)

            if self.gameMapInternal [currentX] [currentY + directionY].symbol == "@" and self.gameMapInternal [currentX + directionX] [currentY + directionY].symbol != "@":
                return selectedNode
            
            else: # Extend a vertical search to look for anything else
                self.addJumpPointToQueue(self.checkCardinalDirection (currentX, currentY, 0, directionY), self.counter)
    
    # A simple method to add to the priority queue.
    # The priority is based on how far the current node is to the end node.
    def addJumpPointToQueue(self, node, counter):
        if node is not None:
            self.pq.put((node.g + max(abs(node.i - self.goalNode.i), abs(node.j - self.goalNode.j)), counter, node))
            self.counter += 1
    
    # Pritns the path out on the game map
    def tracePath(self, node, gameMap):
        gameMap[node.i][node.j] = "x"
        prevNode = node.cameFrom
        while (prevNode != None):
            # Mark the current spot on the graph as visited.
            gameMap[prevNode.i][prevNode.j] = "x"
            prevNode = prevNode.cameFrom

        return gameMap