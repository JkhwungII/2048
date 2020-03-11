import pygame
import copy
import random
pygame.init()
random.seed('foobar')


randerStartX = 76
randerStartY = 203
blcWidth = 119
vel = 1
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
theBG = pygame.Surface((1024, 768), pygame.SRCALPHA)

blc2 = pygame.image.load('pic\\blc2.png')
blc4 = pygame.image.load('pic\\blc4.png')
blc8 = pygame.image.load('pic\\blc8.png')
blc16 = pygame.image.load('pic\\blc16.png')
blc32 = pygame.image.load('pic\\blc32.png')
blc64 = pygame.image.load('pic\\blc64.png')
blc128 = pygame.image.load('pic\\blc128.png')
blc256 = pygame.image.load('pic\\blc256.png')
blc512 = pygame.image.load('pic\\blc512.png')
blc1024 = pygame.image.load('pic\\blc1024.png')
blc2048 = pygame.image.load('pic\\blc2048.png')
blcPic = [blc2, blc4, blc8, blc16, blc32, blc64, blc128, blc256, blc512, blc1024, blc2048]
gameover = pygame.image.load('pic\\gameover.png')
win = pygame.image.load('pic\\win.png')
bg = pygame.image.load('pic\\bg.jpg')
voltar = pygame.Rect(500, 508, 214, 43)
#----class section----
class Cord():
    def __init__(self, xIndex, yIndex):
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.CordPos = [self.xIndex*blcWidth+randerStartX, self.yIndex*blcWidth+randerStartY]
    def __eq__ (self, that):
        """if isinstance(that, self) == False:
            return False
        else:"""
        return that.xIndex == self.xIndex & that.yIndex == self.yIndex

class Grid():
    def __init__(self, row, col):
        self.screenSource = screen
        self.index = [row, col]
        self.gridCord = Cord(self.index[0], self.index[1])
        self.adjacentGrid = [None for i in range(4)]
        self.containBlc = None
        self.isMoving = False
        #self.movingTo: Cord
    def DOT_draw(self):
        pygame.draw.circle(self.screenSource, (255, 0, 0), self.position, 1)
    def addBlc(self, imgIndex):
        self.containBlc = Blc(imgIndex,self.gridCord.CordPos)
        self.containBlc.display()
    def hasBlc(self):
        if self.containBlc != None: return True
        else: return False
    def getBlc(self):
        return self.containedBlc
    def moveBlc(self, newPos):
        self.containBlc.display(newPos)
    def initAdjacentGrid(self, direction, addedGrid):
        self.adjacentGrid[direction] = addedGrid
    def getAdjacentGrid(self, direction):
        return self.adjacentGrid[direction]
        
class Blc():
    def __init__(self, imgIndex, Pos):
        self.xPos = Pos[0]
        self.yPos = Pos[1]
        self.imgIndex = imgIndex
    def __eq__ (self, that):
        if isinstance(that, self) == False:
            return False
        return self.imgIndex == that.imgIndex
    def getImgIndex(self):
        return self.imgIndex
    def display(self):
        screen.blit(blcPic[self.imgIndex], (self.xPos, self.yPos))
        pygame.display.update()
#----------------------

#----function section----
def initGrids(grids : list):
    for i in range(len(grids)):
        noTopGrid = False
        noBottomGrid = False
        if i - 1 < 0: noTopGrid = True
        if i + 1 >= len(grids): noBottomGrid = True
        for j in range(len(grids[i])):
            if noTopGrid == False: grids[i][j].initAdjacentGrid(0, grids[i-1][j])
            if noBottomGrid == False: grids[i][j].initAdjacentGrid(1, grids[i+1][j])
            if j - 1 > 0: grids[i][j].initAdjacentGrid(2, grids[i][j-1])
            if j + 1 < len(grids[i]): grids[i][j].initAdjacentGrid(3, grids[i][j+1])

def doPathing(startingPoints : list, direction: int):
    pathingProgess = 0
    while pathingProgess < 4:
        for i in range(4):
            #isDone = False
            currentGrid = startingPoints[i]
            nextGrid = currentGrid.getAdjacentGrid(direction)
            blcRepeatCounter = 1
            addedMove = 0
            if currentGrid.hasBlc == False: 
                currentGrid = currentGrid.getAdjacentGrid(direction)
            while nextGrid != None:
                if nextGrid.hasBlc == False: addedMove += 1
                elif nextGrid.getBlc == currentGrid: blcRepeatCounter += 1
                elif nextGrid.getBlc != currentGrid.getBlc:
                    if blcRepeatCounter > 1:
                        addedMove = blcRepeatCounter / 2
                        blcRepeatCounter = 1
                currentGrid = nextGrid
            if blcRepeatCounter > 1:
                        addedMove = blcRepeatCounter / 2
                        blcRepeatCounter = 1
            


"""def setBlcPath(direction):
    loop1Start: int
    loop1End: int
    loop2Start: int
    loop2End: int
    for i in range(loop1Start, loop1End):
        for j in range(loop2Start,loop2End):
            countMoves = 0
            for k in range(j + 1, loop2End):
                if gridList[i][k].used == False: countMoves += 1
                elif gridList[i][j].getBlc == gridList[i][k].getBlc: countMoves += 1
                else: pass
            if isinstance(gridList[i][j].getBlc, blcs): 
                gridList[i][j].getBlc.addMoves(countMoves)
            countMoves = 0         
def blockCreate(maxInput1, numbers1, listIndex):
    a = 1
    if maxInput1 < 16:
        while a == 1:
            Rand = random.choice(numbers1)
            indexRand = random.randint(0,1)
            if maxInput1 > 15:
                a = 0
            elif blockSpace[Rand].used == False:
                blockSpace[Rand].used = True
                blockSpace[Rand].blcID = indexRand
                blocks.append(blcs(blockSpace[Rand].xPosition, blockSpace[Rand].yPosition, indexRand, listIndex))
                blockSpace[Rand].blcIndex = listIndex
                a = 0
    if maxInput1 >= 16:
        screen.blit(gameover, (0, 0))"""

"""def movingBlc(fromGrid:Grid,toGrid:Grid):
    isDone = False
    moveDest = 238
    nowPos = copy.deepcopy(toGrid.gridCord.CordPos)
    destPos = fromGrid.gridCord.CordPos
    while nowPos[0] != destPos[0]:
        if nowPos[0] < destPos[0]:
            if (destPos[0] - nowPos[0]) > moveDest:
                nowPos[0] += moveDest
                screen.blit(bg, (0,0))
                aGrid.containBlc.display(nowPos)
                pygame.display.update()
            else:
                nowPos[0] = destPos[0]
                screen.blit(bg, (0,0))
                aGrid.containBlc.display(destPos)
                pygame.display.update()  
        elif nowPos[0] > destPos[0]:
            if (nowPos[0] - destPos[0]) > moveDest:
                nowPos[0] -= moveDest
                screen.blit(bg, (0,0))
                aGrid.containBlc.display(nowPos)
                pygame.display.update()
            else:
                nowPos[0] = destPos[0]
                screen.blit(bg, (0,0))
                aGrid.containBlc.display(destPos)
                pygame.display.update()
    destPos = None
    aGrid = None
    return"""
#------------------------

#----running section----
GridList = [[Grid(i, j) for i in range(4)] for j in range(4)]
initGrids(GridList)
screen.blit(bg, (0,0))
pygame.display.update()
GridList[0][3].addBlc(10)
pygame.display.update()
running = True
isClicked = False
i = 0
while running:
    keys = pygame.key.get_pressed()
    pygame.time.delay(100)
    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.QUIT:
            running = False      
    if keys[pygame.K_LEFT]:
        True
        #movingBlc(GridList[0][0], GridList[0][3])
    if keys[pygame.K_RIGHT]:
        True
        #movingBlc(GridList[0][0],GridList[0][3])

#------------------------
pygame.quit()