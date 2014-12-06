# Sean Tijmons
# 

from Field_visualization_2 import *
from heapq import heappush, heappop # for priority queue
import math
import time
import random
from itertools import repeat

chip = Field()

class node:
    xPos = 0 # x position
    yPos = 0 # y position
    zPos = 0
    distance = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate
    def __init__(self, xPos, yPos, zPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest, zDest):
        self.priority = self.distance + self.estimate(xDest, yDest, zDest) * 10 # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest, zDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        zd = zDest - self.zPos
        # Manhattan distance
        d = abs(xd) + abs(yd)
        return(d)

# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, zA, xB, yB, zB):
    closed_nodes_map = [[] for i in repeat(None, 8)]  # map of closed (tried-out) nodes
    open_nodes_map = [[] for i in repeat(None, 8)] # map of open (not-yet-tried) nodes
    dir_map = [[] for i in repeat(None, 8)] # map of dirs
    row = [0] * n
    for j in range(0, 8):
        for i in range(m): # create 2d arrays
            closed_nodes_map[j].append(list(row))
            open_nodes_map[j].append(list(row))
            dir_map[j].append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, zA, 0, 0)
    n0.updatePriority(xB, yB, zB)
    heappush(pq[pqi], n0)
    open_nodes_map[zA][yA][xA] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.zPos, n1.distance, n1.priority)
        x = n0.xPos
        y = n0.yPos
        z = n0.zPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[z][y][x] = 0
        closed_nodes_map[z][y][x] = 1 # mark it on the closed nodes map

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB and z == zB:
            # generate the path from finish to start
            # by following the dirs
            path = ''
            while not (x == xA and y == yA and z == zA):
                j = dir_map[z][y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
                x += dx[j]
                y += dy[j]
                z += dz[j]
            return path

        # generate moves (child nodes) in all possible dirs
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            zdz = z + dz[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1 or zdz < 0 or zdz > 7
                    or the_map[zdz][ydy][xdx] == 1 or the_map[zdz][ydy][xdx] == 5 or closed_nodes_map[zdz][ydy][xdx] == 1):
                # generate a child node
                m0 = node(xdx, ydy, zdz, n0.distance, n0.priority)
                m0.nextMove(dirs, i)
                m0.updatePriority(xB, yB, zB)
                # if it is not in the open list then add into that
                if open_nodes_map[zdz][ydy][xdx] == 0:
                    open_nodes_map[zdz][ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[zdz][ydy][xdx] = (i + dirs / 2) % dirs
                elif open_nodes_map[zdz][ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[zdz][ydy][xdx] = m0.priority
                    # update the parent direction
                    dir_map[zdz][ydy][xdx] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy and pq[pqi][0].zPos == zdz):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])       
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found, extra laag??

# MAIN-------------------------------------------------------------------------------

#def a_star_algorithm(gates, nets):

gates = chip.make_gate_list(chip.f_input_1)
nets = chip.make_net_list(chip.f_input1)

dirs = 6 # number of possible directions to move on the map
dx = [1, 0, 0, -1, 0, 0]
dy = [0, 1, 0, 0, -1, 0]
dz = [0, 0, 1, 0, 0, -1]

n = 18 # horizontal size of the map
m = 13 # vertical size of the map
the_map = [[] for i in repeat(None, 8)]
the_list = []

row = [0] * n
for j in range(0, 8):
    for i in range(m): # create empty map
        the_map[j].append(list(row))


coordinates_points = chip.net_coordinates(gates, nets)
priorityqueue = chip.sorted_list(coordinates_points)
print priorityqueue
lines = 0

for i in range(len(priorityqueue)):
    xA = priorityqueue[i][0][0]
    print xA
    yA = priorityqueue[i][0][1]
    print yA
    xB = priorityqueue[i][1][0]
    print xB
    yB = priorityqueue[i][1][1]
    print yB
    zA = 0
    zB = 0
    if len(gates)>0:
        for i in range(len(gates)):
            x = gates[i][1]
            y = gates[i][2]
            z = 0
            if (x == xA and y == yA and z == zA):
                the_map[z][y][x] = 2
            elif (x == xB and y == yB and z == zB):
                the_map[z][y][x] = 2
            else:
                the_map[z][y][x] = 5
    
    route = pathFind(the_map, n, m, dirs, dx, dy, xA, yA, zA, xB, yB, zB)
    print route
    begin_x = []
    end_x = []
    begin_y = []
    end_y = []
    begin_z = []
    end_z = []

    if len(route) > 0:
        x = xA
        y = yA
        z = zA
        print x,y,z
        the_map[z][y][x] = 5
        lines += 1
        begin_x.append(x)
        begin_y.append(y)
        begin_z.append(z)
        for i in range(len(route)):
            j = int(route[i])
            # k = int(route[i][j])
            x += dx[j]
            y += dy[j]
            z += dz[j]
            print x,y,z
            end_x.append(x)
            end_y.append(y)
            end_z.append(z)
            begin_x.append(x)
            begin_y.append(y)
            begin_z.append(z)
            the_map[z][y][x] = 1
        the_map[z][y][x] = 5
        end_x.append(x)
        end_y.append(y)
        end_z.append(z)

for i in range(0, 7):
    print the_map[i]
#uitleg: begin en eind coordinaten worden in the list gezipt, maar er moet ook nog een laag variabele toegevoegd worden,
# als die dus niet een lijn spant, kijk bij de return van de a_star algoritme.

begin_coordinates = zip(begin_x,begin_y, begin_z)
end_coordinates = zip(end_x, end_y, end_z)
the_list = zip(begin_coordinates,end_coordinates)

print the_list
#return the_list
counter = 0
# display the map with the route added
print 'Map:'
for z in range(0, 8):
    for y in range(m):
        for x in range(n):
            xyz = the_map[z][y][x]
            if xyz == 0:
                print '.', # space
            elif xyz == 1:
                print 'O', # obstacle
            elif xyz == 2:
                print 'G', # start
                counter+=1
            elif xyz == 3:
                print 'R', # route
            elif xyz == 4:
                print 'F', # finish
            elif xyz == 5:
                print 'G', # finish   
                counter+=1 
        print

print lines
print len(coordinates_points)
print counter
print the_list