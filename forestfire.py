import random
import matplotlib.pyplot as plt
#from drawnow import drawnow
import numpy as np
from matplotlib.colors import ListedColormap
import time


def CheckNN(x, y, listTrees, sizeGrid):
    toFill = set()
    toFill.add((x, y))
    #length = len(toFill)
    visited = set()
    while len(toFill) > 0:
        (x, y) = toFill.pop()
        visited.add((x, y))
        #length = len(toFill)
        if listTrees[x][y] == 1:
            listTrees[x][y] = 2
            if x == 0 and (sizeGrid - 1, y) not in visited:
                toFill.add((sizeGrid - 1, y))

            if x > 1 and (x - 1, y) not in visited:
                toFill.add((x - 1, y))

            if x == sizeGrid - 1 and (0, y) not in visited:
                toFill.add((0, y))

            if x < sizeGrid - 2 and (x + 1, y) not in visited:  # gdiva
                toFill.add((x + 1, y))

            if y == 0 and (x, sizeGrid - 1) not in visited:
                toFill.add((x, sizeGrid - 1))

            if y > 1 and (x, y - 1) not in visited:
                toFill.add((x, y - 1))

            if y == sizeGrid - 1 and (x, 0) not in visited:
                toFill.add((x, 0))

            if y < sizeGrid - 2 and (x, y + 1) not in visited:  # adfa
                toFill.add((x, y + 1))

        #length = len(toFill)


nRuns = 2001
sizeGrid = 128

pNewTree = float(1) / float(100)
pLightning = float(1) / float(1)
listTrees = [[0 for x in range(sizeGrid - 1)] for y in range(sizeGrid - 1)]
cmap = ListedColormap(['w', 'g', 'r'])
bounds = [0, 1, 2]
proportionBurnt = []
density = []

for t in range(0, nRuns):
    counterFire = 0
    nTrees = 0
    tmpDensity = 0
    strikeList = []
    proportion = 0
    for i in range(0, sizeGrid - 1):
        for j in range(0, sizeGrid - 1):
            if listTrees[i][j] == 0:
                r = random.uniform(0, 1)
                if r < pNewTree:
                    listTrees[i][j] = 1

    r = random.uniform(0, 1)
    if r < pLightning:
        xCoordStrike = np.random.randint(sizeGrid - 1)
        yCoordStrike = np.random.randint(sizeGrid - 1)
        CheckNN(xCoordStrike, yCoordStrike, listTrees, sizeGrid - 1)

    for i in range(0, sizeGrid - 1):
        for j in range(0, sizeGrid - 1):
            if listTrees[i][j] == 1:
                nTrees = nTrees + 1
            if listTrees[i][j] == 2:
                counterFire = counterFire + 1
                listTrees[i][j] = 0
    # print float(counter)/float(nTrees)
    if counterFire > 0:
        proportion = float(counterFire) / float(sizeGrid ** 2)
        tmpDensity = (float(nTrees) + float(counterFire)) / float(sizeGrid ** 2)
        density.append(tmpDensity)
        proportionBurnt.append(proportion)

    if t % 500 == 0:
        print ("Iteration ", t, "of ",nRuns,  "phase 1")

proportionBurnt.sort()
density.sort()
# proportionBurnt = proportionBurnt[::-1]



density2 = []
proportionBurnt2 = []
for t in range(0, len(density)):
    listTrees2 = [[0 for x in range(sizeGrid - 1)] for y in range(sizeGrid - 1)]
    counterFire2 = 0
    nTrees2 = float(0)
    tmpDensity2 = float(0)
    pNewTree2 = float(density[t])
    proportion2 = float(0)

    # Looping through the lists planting trees with probabilities pNewTree
    for i in range(0, sizeGrid - 1):
        for j in range(0, sizeGrid - 1):
            if listTrees2[i][j] == 0:
                r = random.uniform(0, 1)
                if r < pNewTree2:
                    listTrees2[i][j] = 1

    # Need to force a lignthing in a tree
    lightning_strike = 0
    while lightning_strike == 0:
        q = random.randint(0, sizeGrid - 2)
        w = random.randint(0, sizeGrid - 2)
        if listTrees2[q][w] == 1:
            CheckNN(q, w, listTrees2, sizeGrid - 1)
            lightning_strike = 1

    for i in range(0, sizeGrid - 1):
        for j in range(0, sizeGrid - 1):
            if listTrees2[i][j] == 1:
                nTrees2 = nTrees2 + 1
            if listTrees2[i][j] == 2:
                counterFire2 = counterFire2 + 1
                listTrees2[i][j] = 0

        proportion2 = float(counterFire2) / float(sizeGrid ** 2)

    tmpDensity2 = (float(nTrees2) + float(counterFire2)) / float(sizeGrid ** 2)
    density2.append(tmpDensity2)
    proportionBurnt2.append(proportion2)
    if t % 200 == 0:
        print("Iteration ", t, " of ", len(density), "phase 2")

proportionBurnt2.sort()
yVector = np.array(np.arange(0, len(density))) / float(len(density) - 1)
yVector2 = np.array(np.arange(0, len(density2))) / float(len(density2) - 1)
yVector = yVector[::-1]
yVector2 = yVector2[::-1]

# Now let's find a function that fits the first parts

startPoint = int(round(len(proportionBurnt)*0.05))
endPoint = int(round(len(proportionBurnt)*0.35))
xI = proportionBurnt[startPoint]
xF = proportionBurnt[endPoint]
yI = yVector[startPoint]
yF = yVector[endPoint]
tau = 1-(np.log(yF)-np.log(yI))/(np.log(xF)-np.log(xI))
print(tau)
xC = 0.7
yC = 1-tau*xC

powerLaw = []
uniformVector = []

for j in range(0,len(yVector)):
    w = random.uniform(0, 1)
    uniformVector.append(w)

uniformVector.sort()
#uniformVector= uniformVector[::-1]
for i in uniformVector:
    tmpVal = xI*(1-i)**(-1/(tau-1))
    #if tmpVal < 0.0001:
    #    tmpVal = 0.0001
    powerLaw.append(tmpVal)

print(np.amax(powerLaw))

plot3, = plt.loglog(powerLaw, yVector, 'orange')
#plt.plot([xI, xF, xC], [yI, yF, yC], 'r')
plot1, = plt.loglog(proportionBurnt, yVector2, 'g.')
#plot2, = plt.loglog(proportionBurnt2, yVector2, 'b')
plt.ylabel('i/N')
plt.xlabel('Relative fire size, ranked')
plt.legend([plot1, plot3], ['Simulated forest','Power law distribution'])
plt.axis((0.0001, 1, 0, 1))
plt.show()
n_fires_started = len(proportionBurnt2)
print('%d fires started' % n_fires_started)
