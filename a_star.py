import pygame
import math
import time
import random

class Node: 
    def __init__(self, gameDisplay, x,y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.cameFrom = None
        self.wall = False

    def heuristic(self, end_x, end_y):

        dist = math.sqrt( (self.x-end_x)**2 + (self.y - end_y)**2 )
        self.h = dist
        return dist

    def add_neighbors(self, nodes):
        
        if not self.wall:
            if self.y < cols-1:
                self.neighbors.append(nodes[self.x][self.y+1])
            
            if self.y > 0:
                self.neighbors.append(nodes[self.x][self.y-1])
            
            if self.x < rows-1:
                self.neighbors.append(nodes[self.x+1][self.y])

            if self.x > 0:
                self.neighbors.append(nodes[self.x-1][self.y])

            if self.x < rows-1 and self.y < cols-1:
                self.neighbors.append(nodes[self.x+1][self.y+1])
            
            if self.x > 0 and self.y > 0:
                self.neighbors.append(nodes[self.x-1][self.y-1])

            if self.x < rows-1 and self.y > 0:
                self.neighbors.append(nodes[self.x+1][self.y-1])
            
            if self.x > 0 and self.y < cols-1:
                self.neighbors.append(nodes[self.x-1][self.y+1])


    def set_wall(self):
        
        if random.uniform(0,1) < 0.3:
            self.wall = True
        return self.wall



display = 500

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
FINISH = (0,255,255)
cols = 25
rows = 25
box = 10
line_width = 1

pygame.init()
pygame.display.set_caption('A* path finding')
font = pygame.font.SysFont("comicsansms", 20)


gameDisplay = pygame.display.set_mode((display,display))
gameDisplay.fill(WHITE)

gameExit = False

w, h = rows, cols;
nodes = [[0 for x in range(w)] for y in range(h)] 

openSet = []
closeSet = []

for i in range(rows):
    for j in range(cols):
        pygame.draw.rect(gameDisplay,BLACK,(i*display/cols,j*display/rows,display/rows,display/rows),line_width)
        nodes[i][j] = Node(gameDisplay, i,j)
        
walls = []  
for i in range(rows):
    for j in range(cols):
        wall_flag = nodes[i][j].set_wall()
        if wall_flag:
            if nodes[i][j] != nodes[rows-1][cols-1]:
                walls.append(nodes[i][j])


for i in range(len(walls)):
    pygame.draw.rect(gameDisplay,BLACK,(walls[i].x*display/cols,walls[i].y*display/rows,display/rows-2,display/rows-2))


for i in range(rows):
    for j in range(cols):
        nodes[i][j].add_neighbors(nodes)



startNode = nodes[0][0]
end = nodes[rows-1][cols-1]
pygame.draw.rect(gameDisplay,FINISH,(display-2*(box-1),display-2*(box-1),display,display))
openSet.append(startNode)

path = []
searchingForPath = True
while not gameExit:


    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            gameExit = True
            pygame.quit()
            quit()
    
    while searchingForPath:
        if len(openSet):

            winner = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[winner].f:
                    winner = i

            current = openSet[winner]
            openSet.pop(winner)
            closeSet.append(current)

            for neighbor in current.neighbors:

                if neighbor not in closeSet:
                    if neighbor not in openSet and not neighbor.wall:
                        neighbor.g += 1
                        neighbor.h = neighbor.heuristic(end.x,end.y)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.cameFrom = current
                        openSet.append(neighbor)        
                    else:
                        tempG = current.g + 1
                        if tempG < current.g: 
                        
                            neighbor.g += 1
                            neighbor.h = neighbor.heuristic(end.x,end.y)
                            neighbor.f = neighbor.g + neighbor.h
















            if current == end:

                temp = current
                path.append(temp)
                while temp.cameFrom:
                    path.append(temp.cameFrom)
                    temp = temp.cameFrom
                    
                searchingForPath = False
                print("Solution found ")





        else:

            searchingForPath = False
            print("There is no solution")





        for i in range(len(openSet)):
            pygame.draw.rect(gameDisplay,GREEN,(openSet[i].x*display/cols,openSet[i].y*display/rows,display/rows-2,display/rows-2))

        for i in range(len(closeSet)):
            pygame.draw.rect(gameDisplay,RED,(closeSet[i].x*display/cols,closeSet[i].y*display/rows,display/rows-2,display/rows-2))

        for i in range(len(path)):
            pygame.draw.rect(gameDisplay,BLUE,(path[i].x*display/cols,path[i].y*display/rows,display/rows-2,display/rows-2))

        pygame.display.update()
        time.sleep(0.1)