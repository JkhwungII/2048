import pygame
import copy
import random

pygame.init()
random.seed()
pygame.display.set_caption("2048")

clock = pygame.time.Clock()
BlockWidth = 119
width, height = 1024, 768
randerStartX, randerStartY = 76, 203
# win = pygame.image.load('pic\\win.png')
bg = pygame.image.load('pic\\bg.jpg')
gameover = pygame.image.load('pic\\gameover.png')
win = pygame.image.load('pic\\win.png')
screen = pygame.display.set_mode((width, height))
blcPic = []
for i in range(1, 12):
    blcPic.append(pygame.image.load('pic\\blc' + str(pow(2, i)) + '.png'))
voltar = pygame.Rect(500, 508, 214, 43)


# ----class section----
class Cord:
    def __init__(self, xIndex, yIndex):
        self.xIndex = xIndex
        self.yIndex = yIndex
        self.CordPos = [self.xIndex * BlockWidth + randerStartX - 5, self.yIndex * BlockWidth + randerStartY - 1]

    def __eq__(self, that):
        if not isinstance(that, Cord):
            return False
        else:
            return that.xIndex == self.xIndex & that.yIndex == self.yIndex


class Block:
    def __init__(self, value, Pos):
        self.xPos = Pos[0]
        self.yPos = Pos[1]
        self.imgIndex = value

    def __eq__(self, that):
        if not isinstance(that, Block):
            return False
        return self.imgIndex == that.imgIndex

    def getImgIndex(self):
        return self.imgIndex

    def blockUpgrade(self):
        self.imgIndex += 1
        return self.imgIndex

    def blockUpdate(self, xMovingDist, yMovingDist):
        if xMovingDist != 0:
            self.xPos += xMovingDist
        if yMovingDist != 0:
            self.yPos += yMovingDist
    def paintBlock(self):
        screen.blit(blcPic[self.imgIndex], (self.xPos, self.yPos))


class Grid:
    def __init__(self, row, col):
        self.index = [row, col]
        self.gridCord = Cord(self.index[0], self.index[1])
        # 0:up, 1:down, 2:left, 3:right
        self.adjacentGrid = [None for i in range(4)]
        self.containBlock = None
        self.beingMerged = False
        self.movingStepsCount = 0
        self.movingTo = None
        # self.movingBuffer : Block

    def addBlock(self, value):
        self.containBlock = Block(value, self.gridCord.CordPos)
        self.containBlock.paintBlock()
        pygame.display.update()
        #pygame.display.update()

    def removeBlock(self):
        del self.containBlock
        self.containBlock = None
        self.beingMerged = False

    def hasBlock(self):
        return self.containBlock is not None

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
        if not self.beingMerged:
            self.movingStepsCount = 0
            self.movingTo.containBlock = newBlock
            self.movingTo = None


class Table:
    def __init__(self):
        self.gameState = True
        self.GridList = [[Grid(i, j) for i in range(4)] for j in range(4)]
        self.GridsWithBlock = []
        self.GridsMoving = []
        self.GridsBeingUpgrade = []
        self.GridsBeingMerge = []
        self.direction: int
        self.totalMoves = 0
        for i in range(len(self.GridList)):
            noTopGrid = False
            noBottomGrid = False
            if i - 1 < 0: noTopGrid = True
            if i + 1 >= len(self.GridList): noBottomGrid = True
            for j in range(len(self.GridList[i])):
                if not noTopGrid:
                    self.GridList[i][j].connectAdjacentGrid(0, self.GridList[i - 1][j])
                if not noBottomGrid:
                    self.GridList[i][j].connectAdjacentGrid(1, self.GridList[i + 1][j])
                if j - 1 >= 0:
                    self.GridList[i][j].connectAdjacentGrid(2, self.GridList[i][j - 1])
                if j + 1 < len(self.GridList[i]):
                    self.GridList[i][j].connectAdjacentGrid(3, self.GridList[i][j + 1])

    def doPathing(self):
        lengthOfGWB = len(self.GridsWithBlock)
        for i in range(lengthOfGWB):
            currentGrid:Grid
            nextGrid:Grid
            passCount = 0
            isMerging = False
            currentGrid = self.GridsWithBlock[i]
            nextGrid = currentGrid.getAdjacentGrid(self.direction)
            BlockRepeatCounter = 1
            addedMove = 0
            while 1:
                if nextGrid is None:
                    break
                else:
                    currentBlock = currentGrid.getBlock()
                    nextBlock = nextGrid.getBlock()
                    if nextBlock is None:
                        addedMove += 1
                        nextGrid = nextGrid.getAdjacentGrid(self.direction)
                    else:
                        if currentBlock == nextBlock:
                            BlockRepeatCounter += 1
                            if passCount == 0:
                                isMerging = True
                        passCount += 1
                        currentGrid = nextGrid
                        nextGrid = currentGrid.getAdjacentGrid(self.direction)
            if BlockRepeatCounter % 2 == 0 and isMerging:
                self.GridsBeingUpgrade.append(self.GridsWithBlock[i])
                nextMergingGrid = self.findNextBlock(self.GridsWithBlock[i])
                self.GridsBeingMerge.append(nextMergingGrid)
                nextMergingGrid.beingMerged = True
            addedMove += (BlockRepeatCounter // 2)
            if addedMove > 0:
                self.GridsWithBlock[i].setPath(addedMove, self.direction)
                self.GridsMoving.append(self.GridsWithBlock[i])
            self.totalMoves += addedMove
        for i in range(lengthOfGWB):
            if not self.GridsWithBlock[i].beingMerged:
                destGrid = self.GridsWithBlock[i].getMovingTo()
                if destGrid:
                    self.GridsWithBlock.append(destGrid)
                else:
                    self.GridsWithBlock.append(self.GridsWithBlock[i])
        for i in range(lengthOfGWB):
            del self.GridsWithBlock[:1]
            
            
    def checkPathing(self,direction: int):
        lengthOfGWB = len(self.GridsWithBlock)
        for i in range(lengthOfGWB):
            currentGrid:Grid
            nextGrid:Grid
            passCount = 0
            isMerging = False
            currentGrid = self.GridsWithBlock[i]
            nextGrid = currentGrid.getAdjacentGrid(direction)
            BlockRepeatCounter = 1
            addedMove = 0
            while 1:
                if nextGrid is None:
                    break
                else:
                    currentBlock = currentGrid.getBlock()
                    nextBlock = nextGrid.getBlock()
                    if nextBlock is None:
                        addedMove += 1
                        nextGrid = nextGrid.getAdjacentGrid(direction)
                    else:
                        if currentBlock == nextBlock:
                            BlockRepeatCounter += 1
                            if passCount == 0:
                                isMerging = True
                        passCount += 1
                        currentGrid = nextGrid
                        nextGrid = currentGrid.getAdjacentGrid(direction)
            addedMove += (BlockRepeatCounter // 2)
        return addedMove

    def doMerging(self):
        if len(self.GridsBeingMerge) > 0:
            upgradingGrid: Grid
            upgradingBlock: Block
            mergingGrid: Grid
            for k in range(len(self.GridsBeingMerge)):
                upgradingGrid = self.GridsBeingUpgrade[k]
                mergingGrid = self.GridsBeingMerge[k]
                upgradingBlock = upgradingGrid.getBlock()
                currentLV = upgradingBlock.blockUpgrade()
                upgradingBlock.paintBlock
                mergingGrid.removeBlock()
                mergingGrid.movingStepsCount = 0
                mergingGrid.movingTo = None
            self.displayOldBlocks()
            self.GridsBeingMerge.clear()
            self.GridsBeingUpgrade.clear()
            if currentLV==11:
                self.gameState = False
                screen.blit(win,(0,0))
                pygame.display.update()

    def displayOldBlocks(self):
        oldBlock: Block
        for grid in self.GridsMoving:
            movingBlock = grid.getBlock()
            if movingBlock is not None:
                movingBlock.paintBlock()
        for grid in self.GridsWithBlock:
            oldBlock = grid.getBlock()
            if oldBlock is not None:
                oldBlock.paintBlock()
        pygame.display.update()

    def insertNewBlock(self,Starting=False):
        if len(self.GridsWithBlock) < 16 and self.gameState:
            if self.totalMoves > 0 or Starting:
                self.totalMoves = 0
                isDrawing = True
                while isDrawing:
                    drawnNumber = random.randint(0, 15)
                    drawnColumn = drawnNumber // 4
                    drawnRow = drawnNumber % 4
                    if not self.GridList[drawnColumn][drawnRow].hasBlock():
                        blockValue = random.randint(0, 1)
                        self.GridList[drawnColumn][drawnRow].addBlock(blockValue)
                        self.GridsWithBlock.append(self.GridList[drawnColumn][drawnRow])
                        isDrawing = False
        else:
            self.gameState = False
            screen.blit(gameover,(0,0))
            pygame.display.update()
            

    def findNextBlock(self,startingGrid:Grid):
        while 1:
            startingGrid = startingGrid.getAdjacentGrid(self.direction)
            if startingGrid.hasBlock():
                return startingGrid

    # 0:up, 1:down, 2:left, 3:right
    def doSliding(self, direction: int):
        movedLength = 0
        movingdist = 5
        blockMovingBuffer = []
        removeList = []
        if self.gameState:
            self.direction = direction
            self.doPathing()
            if self.totalMoves>0:
                while movedLength < 119:
                    clock.tick(30)
                    screen.blit(bg, (0, 0))
                    pygame.display.update()
                    for MovingGrid in self.GridsMoving:
                        currentBlock = MovingGrid.containBlock
                        currentMovingDist = movingdist * (MovingGrid.getMovingSteps())
                        if currentMovingDist > 0:
                            # move block======
                            if direction == 0:
                                currentBlock.blockUpdate(0, -1 * currentMovingDist)
                            elif direction == 1:
                                currentBlock.blockUpdate(0, currentMovingDist)
                            elif direction == 2:
                                currentBlock.blockUpdate(-1 * currentMovingDist, 0)
                            elif direction == 3:
                                currentBlock.blockUpdate(currentMovingDist, 0)
                            # ========================
                        else:
                            continue
                    self.displayOldBlocks()
                    movedLength += movingdist        
                self.doMerging()
                for MovingGrid in self.GridsMoving:
                    if MovingGrid.hasBlock():
                        blockMovingBuffer.append(MovingGrid.getBlock())
                for MovingGrid in self.GridsMoving:
                    if MovingGrid.hasBlock():
                        MovingGrid.clearContainBlock()
                    else:
                        removeList.append(MovingGrid)
                for i in removeList:
                    self.GridsMoving.remove(i)
                for i in range(len(self.GridsMoving)):
                    self.GridsMoving[i].postSlidingAdjust(blockMovingBuffer[i])        
                self.GridsMoving.clear()
                self.insertNewBlock()
            elif len(self.GridsWithBlock) == 16:
                possibleMoves = 0
                for i in range(4):
                    possibleMoves += self.checkPathing(i)
                if possibleMoves < 1:
                    self.gameState = False
                    screen.blit(gameover,(0,0))
                    pygame.display.update()
        return True

# ----------------------

# ----running section----
def main():
    running = True
    playingTable = Table()
    screen.blit(bg, (0, 0))
    playingTable.insertNewBlock(True)


    while running:
        
        # 0:up, 1:down, 2:left, 3:right
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_UP:
                    playingTable.doSliding(0)
                elif event.key==pygame.K_DOWN:
                    playingTable.doSliding(1)
                elif event.key==pygame.K_LEFT:
                    playingTable.doSliding(2)
                elif event.key==pygame.K_RIGHT:
                    playingTable.doSliding(3)
         
    ''' if keys[pygame.K_UP] and finished:
            finished= False
            finished=playingTable.doSliding(0)
        if keys[pygame.K_DOWN] and finished:
            finished= False
            finished=playingTable.doSliding(1)
        if keys[pygame.K_LEFT] and finished:
            finished= False
            finished=playingTable.doSliding(2)
        if keys[pygame.K_RIGHT] and finished:
            finished= False
            finished=playingTable.doSliding(3)
        keys = None'''
       
    pygame.quit()
# ------------------------
if __name__ == '__main__':
    main()