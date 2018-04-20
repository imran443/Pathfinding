from queue import PriorityQueue

class AStar():

   # The list which will hold the nodes as we go through.
    pq = PriorityQueue()
    vistedList = []
    goalNode = None

    def __init__(self, initNode, endNode):
        self.pq.put(initNode)
        self.goalNode = endNode

    def aStarAlgo(self, gameMapInternal, gameMap):
        counter = 0

        while (not self.pq.empty()):
            # Get the tuple with the smallest g value.
            priorityItem = self.pq.get()
            currentNode = priorityItem[2]
            currentNodeEdges = currentNode.getEgdes()
            currentNodeNeighbours = currentNode.getNeighbours()
            dist = currentNode.g
            
            # We have found the goal return the gameMap.
            if (self.goalNode in self.vistedList):
                updatedGameMap = self.tracePath(self.goalNode, gameMap)
                return updatedGameMap

            for i in range(len(currentNode.neighbours)):
                if (currentNodeNeighbours[i] not in self.vistedList):
                    alt = dist + currentNodeEdges[i]

                    if (alt < currentNodeNeighbours[i].g):
                        
                        currentNodeNeighbours[i].g = alt
                        
                        # Update the f value for the queue.
                        currentNodeNeighbours[i].f = alt + currentNodeNeighbours[i].h
                        currentNodeNeighbours[i].cameFrom = currentNode

                        # Add it to the priority queue as a tuple so that it can be kept organized.
                        self.pq.put((currentNodeNeighbours[i].f, counter, currentNodeNeighbours[i]))
                        counter+=1
            
            # Mark this node as visited
            self.vistedList.append(currentNode)
        
    def tracePath(self, node, gameMap):
        gameMap[node.i][node.j] = "x"
        prevNode = node.cameFrom
        while (prevNode != None):
            # Mark the current spot on the graph as visited.
            gameMap[prevNode.i][prevNode.j] = "x"
            prevNode = prevNode.cameFrom

        return gameMap

    

    