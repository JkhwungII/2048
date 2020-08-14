import pygame
import copy
import random
pygame.init()
random.seed('foobar')
pygame.display.set_caption("2048")

BlockWidth = 119
width, height = 1024, 768
randerStartX ,randerStartY= 76, 203
#win = pygame.image.load('pic\\win.png')
bg = pygame.image.load('pic\\bg.jpg')
gameover = pygame.image.load('pic\\gameover.png')
screen = pygame.display.set_mode((width, height))
blcPic= []
for i in range(1,12):
    blcPic.append(pygame.image.load('pic\\blc'+ str(pow(2, i))+'.png'))
voltar = pygame.Rect(500, 508, 214, 43)
#----class section----
class Cord():
    def __init__(self, xIndex, yIndex):
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.CordPos = [self.xIndex*BlockWidth+randerStartX - 5, self.yIndex*BlockWidth+randerStartY - 1]
    def __eq__ (self, that):
        if isinstance(that, Cord) == False:
            return False
        else:
            return that.xIndex == self.xIndex & that.yIndex == self.yIndex
        
class Block():
    def __init__(self, value, Pos):
        self.xPos = Pos[0]
        self.yPos = Pos[1]
        self.imgIndex = value
    def __eq__ (self, that):
        if isinstance(that, Block) == False:
            return False
        return self.imgIndex == that.imgIndex
    def getImgIndex(self):
        return self.imgIndex
    def movingUpdate(self, xMovingDist, yMovingDist):
        if xMovingDist != 0:
            self.xPos += xMovingDist
        if yMovingDist != 0:
            self.yPos += yMovingDist
        screen.blit(blcPic[self.imgIndex], (self.xPos, self.yPos))
        pygame.display.update()

class Grid():
    def __init__(self, row, col):
        self.index = [row, col]
        self.gridCord = Cord(self.index[0], self.index[1])
        # 0:up, 1:down, 2:left, 3:right
        self.adjacentGrid = [None for i in range(4)]
        self.containBlock = None
        self.isMerging = False
        self.movingStepsCount = 0
        self.movingTo = None
        #self.movingBuffer : Block
    def addBlock(self, value):
        self.containBlock = Block(value,self.gridCord.CordPos)
        self.containBlock.movingUpdate(0, 0)
        pygame.display.update()
    def hasBlock(self):
        return self.containBlock != None
    def getBlock(self):
        return self.containBlock
    def connectAdjacentGrid(self, direction, addedGrid):
        self.adjacentGrid[direction] = addedGrid
    def getAdjacentGrid(self, direction):
        return self.adjacentGrid[direction]
    def setPath(self, distance, direction):
        self.movingStepsCount = distance
        self.movingTo = self
        for i in range(distance):
            self.movingTo = self.movingTo.adjacentGrid[direction]
    def getMovingSteps(self):
        return self.movingStepsCount
    def getMovingTo(self):
        return self.movingTo
    def clearContainBlock(self):
        self.containBlock = None
    def postSlidingAdjust(self, newBlock: Block):
        self.movingStepsCount = 0
        self.movingTo.containBlock = newBlock
        self.movingTo = None

class Table():
    def __init__(self):
        self.GridList = [[Grid(i, j) for i in range(4)] for j in range(4)]
        self.GridsWithBlock = []
        self.GridsMoving = []
        self.GridsBeingMerge = []
        self.direction: int
        for i in range(len(self.GridList)):
            noTopGrid = False
            noBottomGrid = False
            if i - 1 < 0: noTopGrid = True
            if i + 1 >= len(self.GridList): noBottomGrid = True
            for j in range(len(self.GridList[i])):
                if not noTopGrid: 
                    self.GridList[i][j].connectAdjacentGrid(0, self.GridList[i-1][j])
                if not noBottomGrid: 
                    self.GridList[i][j].connectAdjacentGrid(1, self.GridList[i+1][j])
                if j - 1 >= 0: 
                    self.GridList[i][j].connectAdjacentGrid(2, self.GridList[i][j-1])
                if j + 1 < len(self.GridList[i]): 
                    self.GridList[i][j].connectAdjacentGrid(3, self.GridList[i][j+1])
    

    def doPathing(self):
        lengthOfGWB = len(self.GridsWithBlock)
        for i in range(lengthOfGWB):
            currentGrid = self.GridsWithBlock[i]
            BlockRepeatCounter = 1
            addedMove = 0
            while 1:
                nextGrid = currentGrid.getAdjacentGrid(self.direction)
                if nextGrid is None:
                    break
                elif nextGrid.hasBlock() == False: 
                    addedMove += 1
                else:
                    if nextGrid.getBlock() == currentGrid.getBlock() and not currentGrid.isMerging:
                        nextGrid.isMerging = True
                        self.GridsBeingMerge.append(nextGrid)
                        addedMove += 1
                currentGrid = nextGrid
            if addedMove > 0:          
                self.GridsWithBlock[i].setPath(addedMove, self.direction)
                self.GridsMoving.append(self.GridsWithBlock[i])
        for i in range(lengthOfGWB):
            if not self.GridsWithBlock[i].isMerging:
                destGrid = self.GridsWithBlock[i].getMovingTo()
                if destGrid:
                    self.GridsWithBlock.append(destGrid)
                else:
                    self.GridsWithBlock.append(self.GridsWithBlock[i])
        for i in range(lengthOfGWB):
            del self.GridsWithBlock[:1]
            
    def doMerging(self):
        True


    def insertNewBlock(self):
        if len(self.GridsWithBlock) < 16:
          isDrawing = True
          while isDrawing:
                drawnNumber = random.randint(0,15)
                drawnColumn = drawnNumber // 4
                drawnRow = drawnNumber % 4
                if not self.GridList[drawnColumn][drawnRow].hasBlock():
                    blockValue = random.randint(0,1)
                    self.GridList[drawnColumn][drawnRow].addBlock(blockValue)
                    self.GridsWithBlock.append(self.GridList[drawnColumn][drawnRow])
                    isDrawing = False
                    
    # 0:up, 1:down, 2:left, 3:right
    def doSliding(self, direction: int):
        self.direction = direction
        self.doPathing()
        movedLength = 0
        movingdist = 5
        blockMovingBuffer = []
        while movedLength < 119:
            screen.blit(bg, (0,0))
            for MovingGrid in self.GridsMoving:
                currentBlock = MovingGrid.containBlock
                currentMovingDist = movingdist * (MovingGrid.getMovingSteps())
                if currentMovingDist > 0:
                    if direction == 0:
                        currentBlock.movingUpdate(0, -1 * currentMovingDist)
                    elif direction == 1:
                        currentBlock.movingUpdate(0, currentMovingDist)
                    elif direction == 2:
                        currentBlock.movingUpdate(-1 * currentMovingDist, 0)
                    elif direction == 3:
                        currentBlock.movingUpdate(currentMovingDist, 0)
                    pygame.display.update()
                else:
                    continue
            movedLength += movingdist
        for MovingGrid in self.GridsMoving:
            blockMovingBuffer.append(MovingGrid.getBlock())
        for MovingGrid in self.GridsMoving:
            MovingGrid.clearContainBlock()
        for i in range(len(self.GridsMoving)):
            self.GridsMoving[i].postSlidingAdjust(blockMovingBuffer[i])
        self.GridsMoving.clear()
        self.insertNewBlock()

        
        for i in range(len(self.GridList)):
            for j in range(len(self.GridList[i])):
                if self.GridList[i][j].hasBlock():
                    if j == len(self.GridList[i]) - 1:
                        print(self.GridList[i][j].getBlock().getImgIndex(), end='  ')
                        print('\n')
                    else:
                        print(self.GridList[i][j].getBlock().getImgIndex(), end='  ')
                else:
                    if j == len(self.GridList[i]) - 1:
                        print('#', end='  ')
                        print('\n')
                    else:
                        print('#', end='  ')
        
        print('===================')
#----------------------


#----running section----
running = True
playingTable = Table()
screen.blit(bg, (0,0))
pygame.display.update()
playingTable.insertNewBlock()
#isClicked = False
i = 0
while running:
    # 0:up, 1:down, 2:left, 3:right
    keys = pygame.key.get_pressed()
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_UP]:
        playingTable.doSliding(0)
    if keys[pygame.K_DOWN]:
        playingTable.doSliding(1)
    if keys[pygame.K_LEFT]:
        playingTable.doSliding(2)
    if keys[pygame.K_RIGHT]:
        playingTable.doSliding(3)

#------------------------
pygame.quit()