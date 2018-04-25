from pygame.locals import *
import pygame, sys

class Display():
    gameMap = None

    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    BLOCK = '@'
    TILE = '.'
    PATH = 'x'

    colors = {
        BLOCK: BLACK,
        TILE: WHITE,
        PATH: GREEN
    }

    tileSize = 8
    mapWidth = None
    mapHeight = None

    displaySurface = None


    def __init__(self, gameMap):
        self.gameMap = gameMap
        self.mapWidth = gameMap.shape[0]
        self.mapHeight = gameMap.shape[1]
        pygame.init()
        self.displaySurface = pygame.display.set_mode([self.mapWidth * self.tileSize, self.mapHeight * self.tileSize])
    
    def createMap(self):
        
        self.displaySurface.fill(self.WHITE)

        while(True):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

            for row in range(self.mapHeight):
                for column in range(self.mapWidth):
                    pygame.draw.rect(self.displaySurface, self.colors[self.gameMap[row][column]], (column * self.tileSize, row * self.tileSize, self.tileSize, self.tileSize))
        
            pygame.display.update()

