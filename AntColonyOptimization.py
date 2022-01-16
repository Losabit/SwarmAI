import pygame as pg
import random as r
from DrawerHelper import *

scale = 6

numAnts = 1000  # Number of Ants
eliteAntsPercentage = 5  # Percentage of elite Ants
initPheromone = 1.0  # Pheromone init value

# Food Variables
foodList = []
numFood = 4  # Amount of food
minFoodDistance = 20
maxFoodDistance = 100
foodAmounts = []
initialFoodAmount = 4

# Number of obstacles
numObstacles = 4000
freeSpace = 3  # Free space left around food & spawn

# Algorith parameters
alpha = 3  # Impact of pheromones
beta = 3  # Impact of the distance
q = 100  # Multiplier of the distance traveled
p = 0.0003  # local evaporation rate of pheromones
gp = 0.0007  # global evaporation rate of pheromones

dHelper = DrawerHelper("AntColonyOptimization Example", int(100 * scale), int(100 * scale))
clock = pg.time.Clock()
ants = []
matrix = []
spawnX, spawnY = 0, 0
iterations = 0


class Colony:
    def __init__(self):
        pass

    # Field initialization
    def initField(self):
        for i in range(100):
            matrix.append([])
            for j in range(100):
                matrix[i].append(initPheromone)
        global spawnX
        global spawnY
        spawnX = r.randint(0, 99)
        spawnY = r.randint(0, 99)
        matrix[spawnX][spawnY] = "spawn"

        global foodList
        for i in range(numFood):
            putFoodSuccess = False
            while not putFoodSuccess:
                foodX = r.randint(5, 94)
                foodY = r.randint(5, 94)
                foodXSuccess = (abs(foodX - spawnX) in range(minFoodDistance, maxFoodDistance)) and (
                        abs(foodY - spawnY) in range(0, maxFoodDistance))
                foodYSuccess = (abs(foodY - spawnY) in range(minFoodDistance, maxFoodDistance)) and (
                        abs(foodX - spawnX) in range(0, maxFoodDistance))
                if foodXSuccess or foodYSuccess:
                    if [foodX, foodY] not in foodList:
                        foodList.append([foodX, foodY])
                        foodAmounts.append(initialFoodAmount)
                        matrix[foodX][foodY] = "food"
                        putFoodSuccess = True

        for i in range(numObstacles):
            putObstacleSuccess = 0
            while putObstacleSuccess < numFood + 1:  # количество еды + точка спавна
                obstacleX = r.randint(0, 99)
                obstacleY = r.randint(0, 99)
                if not ((matrix[obstacleX][obstacleY] == "obstacle") and (matrix[obstacleX][obstacleY] == "food") and (
                        matrix[obstacleX][obstacleY] == "spawn")):
                    spawnXSuccess = (obstacleX <= spawnX - freeSpace) or (obstacleX >= spawnX + freeSpace)
                    spawnYSuccess = (obstacleY <= spawnY - freeSpace) or (obstacleY >= spawnY + freeSpace)
                    if spawnXSuccess or spawnYSuccess:
                        putObstacleSuccess += 1
                    else:
                        putObstacleSuccess = 0
                        continue
                    for i in range(numFood):
                        foodX = foodList[i][0]
                        foodY = foodList[i][1]
                        foodXSuccess = (obstacleX <= foodX - freeSpace) or (obstacleX >= foodX + freeSpace)
                        foodYSuccess = (obstacleY <= foodY - freeSpace) or (obstacleY >= foodY + freeSpace)
                        if foodXSuccess or foodYSuccess:
                            putObstacleSuccess += 1
                        else:
                            putObstacleSuccess = 0
                            continue
            matrix[obstacleX][obstacleY] = "obstacle"

    # отрисовка поля
    def drawField(self):
        dHelper.draw_background(dHelper.WHITE)
        for i in range(100):
            for j in range(100):
                if matrix[i][j] == "spawn":
                    dHelper.blit(dHelper.BLUE, 255, i, j, scale)
                elif matrix[i][j] == "food":
                    if initialFoodAmount > 0:
                        foodAlpha = foodAmounts[foodList.index([i, j])] / initialFoodAmount * 200 + 55
                    else:
                        foodAlpha = 255
                    dHelper.blit(dHelper.RED, foodAlpha, i, j, scale)

                elif matrix[i][j] == "obstacle":
                    dHelper.blit(dHelper.BLACK, 20, i, j, scale)
                else:
                    pheromoneGray = 255 - (matrix[i][j] - initPheromone) * 1.4
                    pheromoneGreen = 2 * pheromoneGray
                    if pheromoneGray > 255:
                        pheromoneGray = 255
                    if pheromoneGray < 0:
                        pheromoneGray = 0
                    if pheromoneGreen > 255:
                        pheromoneGreen = 255
                    if pheromoneGreen < 50:
                        pheromoneGreen = 50
                    dHelper.blit((pheromoneGray, pheromoneGreen, pheromoneGray), 255, i, j, scale)

    # Ants initialisation
    def createAnts(self):
        numLeet = int(eliteAntsPercentage / 100 * numAnts)  # Number of elite ants

        for i in range(numAnts):
            ants.append(Ant(spawnX, spawnY, False))

        # Election of elite ants
        while numLeet > 0:
            leetCandidate = r.choice(ants)
            if not leetCandidate.leet:
                leetCandidate.leet = True
                numLeet -= 1
                print("Ant: ", "%#10d" % leetCandidate.id, " became an elite !")

    # Moving & drawing the ants
    def drawAndMoveAnts(self, should_draw=True):
        for ant in ants:
            ant.turn()
            if should_draw:
                if not ant.leet:
                    dHelper.blit(dHelper.BLACK, 70, ant.x, ant.y, scale)
                else:
                    dHelper.blit(dHelper.TEAL, 127, ant.x, ant.y, scale)

    # Global evaporation of pheromones
    def globalEvaporate(self):
        for i in range(100):
            for j in range(100):
                if type(matrix[i][j]) == type(0.0):
                    matrix[i][j] *= (1 - gp);

    def noFood(self):
        if initialFoodAmount > 0:
            for i in foodAmounts:
                if i > 0:
                    return False
            return True
        else:
            return False

    def inc(self):
        global iterations
        iterations += 1


class Ant:
    global spawnX
    global spawnY

    def __init__(self, x, y, leet):
        self.x = x
        self.y = y
        self.tabooList = []
        self.putPheromone = False
        self.l0 = 0
        self.tabooListIndex = 0
        self.leet = leet
        self.id = r.randint(10000000, 99999999)

    def move(self, dir):
        if [self.x, self.y] not in self.tabooList:
            self.tabooList.append([self.x, self.y])
        dx, dy = 0, 0

        if dir == 0:
            dy = -1
        if dir == 1:
            dy = -1
            dx = 1
        if dir == 2:
            dx = 1
        if dir == 3:
            dx = 1
            dy = 1
        if dir == 4:
            dy = 1
        if dir == 5:
            dy = 1
            dx = -1
        if dir == 6:
            dx = -1
        if dir == 7:
            dx = -1
            dy = -1

        self.x += dx
        self.y += dy

        if [self.x, self.y] not in self.tabooList:
            self.tabooList.append([self.x, self.y])

        if dx * dy == 0:
            self.l0 += 1
        else:
            self.l0 += 2 ** .5

    def tryMove(self, dir):
        if dir == 0:
            return [self.x, self.y - 1]
        if dir == 1:
            return [self.x + 1, self.y - 1]
        if dir == 2:
            return [self.x + 1, self.y]
        if dir == 3:
            return [self.x + 1, self.y + 1]
        if dir == 4:
            return [self.x, self.y + 1]
        if dir == 5:
            return [self.x - 1, self.y + 1]
        if dir == 6:
            return [self.x - 1, self.y]
        if dir == 7:
            return [self.x - 1, self.y - 1]

    # Get the amount of pheromones on neighboring cells
    def getPheromone(self, dir):
        pheromoneX = self.x
        pheromoneY = self.y
        if dir == 0:
            pheromoneY = self.y - 1
        if dir == 1:
            pheromoneY = self.y - 1
            pheromoneX = self.x + 1
        if dir == 2:
            pheromoneX = self.x + 1
        if dir == 3:
            pheromoneX = self.x + 1
            pheromoneY = self.y + 1
        if dir == 4:
            pheromoneY = self.y + 1
        if dir == 5:
            pheromoneY = self.y + 1
            pheromoneX = self.x - 1
        if dir == 6:
            pheromoneX = self.x - 1
        if dir == 7:
            pheromoneX = self.x - 1
            pheromoneY = self.y - 1

        if type(matrix[pheromoneX][pheromoneY]) == type(0.0):
            return matrix[pheromoneX][pheromoneY]
        else:
            return initPheromone * 10000

    # Function to return the inverse of the distance
    def getInverseDistance(self, dir):
        if (dir == 0) or (dir == 2) or (dir == 4) or (dir == 6):
            return 1.0  # Straight line, distance == 1
        else:
            return float(1 / 2 ** .5)  # Diagonal distance

    # Determine possible moves
    possibleTurns = []

    def addPossibleTurns(self, arr):
        self.possibleTurns = []
        for i in arr:
            pp = self.tryMove(i)
            if not (pp in self.tabooList) and (pp[0] in range(0, 100)) and (pp[1] in range(0, 100)) and (
                    matrix[pp[0]][pp[1]] != "obstacle"):
                self.possibleTurns.append(i)

    # Resetting the ants when it's lost
    def respawn(self):
        self.x = spawnX
        self.y = spawnY
        self.tabooList = []
        self.putPheromone = False
        self.tabooListIndex = 0
        self.l0 = 0
        print("Ant: ", self.id, " respawned !")

    # Choose next point of interest and move there
    def turn(self):
        if not self.putPheromone:

            # Set possible directions
            if (self.x == 0) and (self.y == 0):
                self.addPossibleTurns([2, 3, 4])
            if (self.x == 0) and (self.y == 99):
                self.addPossibleTurns([0, 1, 2])
            if (self.x == 99) and (self.y == 0):
                self.addPossibleTurns([4, 5, 6])
            if (self.x == 99) and (self.y == 99):
                self.addPossibleTurns([6, 7, 0])
            if (self.x == 0) and (self.y in range(1, 99)):
                self.addPossibleTurns([0, 1, 2, 3, 4])
            if (self.x == 99) and (self.y in range(1, 99)):
                self.addPossibleTurns([0, 4, 5, 6, 7])
            if (self.y == 0) and (self.x in range(1, 99)):
                self.addPossibleTurns([2, 3, 4, 5, 6])
            if (self.y == 99) and (self.x in range(1, 99)):
                self.addPossibleTurns([6, 7, 0, 1, 2])
            if (self.x in range(1, 99)) and (self.y in range(1, 99)):
                self.addPossibleTurns([0, 1, 2, 3, 4, 5, 6, 7])

            # Calculate the prob of a move
            sum_ = 0
            probabilities = []
            for i in self.possibleTurns:
                sum_ += self.getInverseDistance(i) ** beta * self.getPheromone(i) ** alpha
            for i in self.possibleTurns:
                probabilities.append(self.getInverseDistance(i) ** beta * self.getPheromone(i) ** alpha / sum_)

            if not self.leet:
                # Function to calculate the sum of the first elements of the array
                def sumFirstElements(arr, end):
                    summ = 0
                    if end >= len(arr):
                        end = len(arr) - 1
                    for i in range(0, end):
                        summ += arr[i]
                    return summ

                # Randomly choosing the direction
                probRange = []
                for i in range(0, len(probabilities)):
                    probRange.append(sumFirstElements(probabilities, i))

                def selectDir():
                    if len(self.possibleTurns) > 0:
                        rand = r.random()
                        for i in range(len(probRange) - 1):
                            if (rand >= probRange[i]) and (rand < probRange[i + 1]):
                                return self.possibleTurns[i]
                        if rand >= probRange[-1]:
                            return self.possibleTurns[-1]
                    else:
                        self.respawn()
            else:
                def selectDir():
                    if len(self.possibleTurns) > 0:
                        maxProb = max(probabilities)
                        maxIndexes = [i for i, j in enumerate(probabilities) if j == maxProb]
                        return self.possibleTurns[r.choice(maxIndexes)]
                    else:
                        self.respawn()

            newDir = selectDir()
            self.move(newDir)

            if matrix[self.x][self.y] == "food":
                antStr = "Ant:"
                if self.leet:
                    antStr = "Elite Ant:"
                print(antStr, self.id, " found", "%#3d" % foodAmounts[foodList.index([self.x, self.y])],
                      "food units at coordinate :", self.x, self.y, "in", "%#10f" % self.l0, "steps")
                self.putPheromone = True

                if initialFoodAmount != 0:
                    foodAmounts[foodList.index([self.x, self.y])] -= 1
                    if foodAmounts[foodList.index([self.x, self.y])] == 0:
                        matrix[self.x][self.y] = initPheromone
                        self.putPheromone = False
                        print("The food at : ", self.x, self.y, " is finished but the pheromones remains.")

        else:  # if putFeromone
            self.tabooListIndex += 1
            self.x = self.tabooList[-self.tabooListIndex][0]
            self.y = self.tabooList[-self.tabooListIndex][1]

            if type(matrix[self.x][self.y]) == type(0.0):
                newTau = (1 - p) * matrix[self.x][self.y] + q / self.l0
                matrix[self.x][self.y] = newTau

            if matrix[self.x][self.y] == "spawn":
                self.respawn()
        return


def main():
    ant_colony = Colony()
    ant_colony.initField()
    ant_colony.createAnts()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        ant_colony.drawField()
        ant_colony.drawAndMoveAnts()
        pg.display.flip()
        clock.tick()
        ant_colony.globalEvaporate()
        ant_colony.inc()
        if ant_colony.noFood():
            print("Ants have eaten all the food in : ", iterations, "iterations.")
    pg.quit()


if __name__ == "__main__":
    main()
