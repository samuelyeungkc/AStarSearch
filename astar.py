import Queue
import math

def rowInRange(x):
    if (x >= 0 and x < getTotalRow()):
        return True
    else:
        return False
    
def colInRange(y):
    if (y >= 0 and y < getTotalCol()):
        return True
    else:
        return False
       
def canGo(posX, posY, visited):
    if not rowInRange(posX):
        return False
    if not colInRange(posY):
        return False
    if map[posX][posY] == -1:
        return False
    if visited[posX][posY]:
        return False
    return True

def removeNoise(line):
	line = line.replace("\n", "")
	line = line.replace(" ", "")
	return line

def getTotalRow():
	TOTALROW = 18
#	TOTALROW = 6 
	return TOTALROW

def getTotalCol():
	TOTALCOL = 32
#	TOTALCOL = 9
	return TOTALCOL

def getMap():
	TOTALROW = getTotalRow()
	TOTALCOL = getTotalCol()

	map = [[-1 for x in range(TOTALCOL)] for x in range(TOTALROW)] 

	currentRow = TOTALROW - 1 
	currentCol = 0
	f = open('map', 'r')
	line = f.readline()
	while line != "":
		line = removeNoise(line)
		for x in range(len(line)):
			ch = line[x]
			if (ch == 'X'):
				map[currentRow][x] = -1
			elif (ch == '.'):
				map[currentRow][x] = 0
			else:
				map[currentRow][x] = ch
		currentRow -= 1
		line = f.readline()

	return map

# return the location of the character : A, B, or C
def getLocation(map,ch):
	for x in range(getTotalRow()):
		for y in range(getTotalCol()):
			if (map[x][y] == ch):
				xLoc = x
				yLoc = y
				
	return (xLoc,yLoc)

# return the distance of two points using admissible heuristic function
# pos,des - a tuple in (x,y) format
def getAdmissibleDistance(pos, des):
	posX = pos[0]
	posY = pos[1]
	desX = des[0]	
	desY = des[1]	
	xDiff = (desX - posX) ** 2
	yDiff = (desY - posY) ** 2
	diff = xDiff + yDiff
	diff = math.pow(diff, 0.5)
	return diff

def getNonAdmissibleDistance(pos, des):
	posX = pos[0]
	posY = pos[1]
	desX = des[0]	
	desY = des[1]	
	xDiff = math.fabs(desX - posX)
	yDiff = math.fabs(desY - posY) 
	diff = xDiff + yDiff
	return diff

def computeDistance(func,pos,des):
	return func(pos,des)

# test the condition and put the node 
# put the node into the queue if possible
# i.e. there is such a node, the node free (not -1)
# and the node is not visited before
def testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited):
	neighbour = (posX, posY)
	if (canGo(posX, posY, visited)):
		prio = func(neighbour,des)
		member = (prio, neighbour, posX, posY)
		que.put(member)

def aStar(pos, des, path, func):
	
	map = getMap()
	
	currentX = pos[0]
	currentY = pos[1]

	que = Queue.PriorityQueue()
	member = (0, pos, -1, -1)
	que.put(member)
	visited = [[False for x in range(getTotalCol())] for x in range(getTotalRow())] 

	# 2D array to hold where the path comes from
	# ex. 2-5-8, 2 is 5 parent and 5 is 8 parent
	parent = [[(-2,-2) for x in range(getTotalCol())] for x in range(getTotalRow())] 

	while (1):
	
		element = que.get()
		pos = element[1] # second element is the current position (prio,pos)
		posX = int(pos[0])
		posY = int(pos[1])


		# do no visit again visted node
		if (visited[posX][posY]):
			continue

		path = path + str(pos)
		visited[posX][posY] = True
		parentX = element[2]
		parentY = element[3]
		parent[posX][posY] = (parentX, parentY)

		if ( (posX,posY) == des ):
			print parent
			return path

					
		# compute bottom left
		posX = int(pos[0]) - 1
		posY = int(pos[1]) - 1
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)
		

		# compute central left
		posX = int(pos[0]) - 1
		posY = int(pos[1])
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		# compute top left
		posX = int(pos[0]) - 1
		posY = int(pos[1]) + 1
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		# compute bottom 
		posX = int(pos[0])
		posY = int(pos[1]) - 1
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		# compute top 
		posX = int(pos[0])
		posY = int(pos[1]) + 1
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		# compute bottom right
		posX = int(pos[0]) + 1
		posY = int(pos[1]) - 1
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		# compute central right
		posX = int(pos[0]) + 1
		posY = int(pos[1])
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		# compute top right
		posX = int(pos[0]) + 1
		posY = int(pos[1]) + 1
		testAndPutIntoQueueIfPossible(posX, posY, des, func, que, visited)

		if (que.empty()):
			return "No Path\n" + "Path so far: " + path

	return "Error"

map = getMap()
bLoc = getLocation(map,'B')
aLoc = getLocation(map, 'A')
cLoc = getLocation(map, 'C')
#print "A location: " + str(aLoc)
print "C location: " + str(cLoc)
ACAdmi = getAdmissibleDistance(aLoc,cLoc)
ACNonAdmi = getNonAdmissibleDistance(aLoc,cLoc)
# A-C Admissible 28.0
# A-C Non-Admissible 39.0

result = aStar(aLoc, cLoc,"",getAdmissibleDistance)
#result = aStar(aLoc, bLoc,"",getAdmissibleDistance)
#result = aStar(aLoc, bLoc,"",getNonAdmissibleDistance)
#result = aStar(aLoc, cLoc,"",getNonAdmissibleDistance)
#result = aStar(aLoc, cLoc,"",getAdmissibleDistance)
print "Result : "
print result
