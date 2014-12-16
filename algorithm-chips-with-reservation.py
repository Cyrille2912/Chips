# Sean Tijmons
# 

from Field_visualization_2 import *
from heapq import heappush, heappop # for priority queue
import math
import time
import random
from itertools import repeat
from netlists import *

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
        if dirs == 6 and (d == 2 or d == 5):
            self.distance += 10
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest, zDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        zd = zDest - self.zPos
        # Manhattan distance
        d = abs(xd) + abs(yd) + abs(zd)
        return(d)

# class line:
#     value = 0 # in the range of 0-6
#     xPos = 0
#     yPos = 0 # y position
#     zPos = 0
#     def __init__(self, xPos, yPos, zPos, value):
#         self.xPos = xPos
#         self.yPos = yPos
#         self.zPos = zPos
#         self.value = value
#     def     

# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, dz, xA, yA, zA, xB, yB, zB):
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
        #if n0.estimate(xB, yB) == 0:
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
                    or the_map[zdz][ydy][xdx] == 1 or the_map[zdz][ydy][xdx] == 5 or the_map[zdz][ydy][xdx] == 6 or closed_nodes_map[zdz][ydy][xdx] == 1 or closed_nodes_map[zdz][ydy][xdx] == 5 or closed_nodes_map[zdz][ydy][xdx] == 6):
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
def check_reserved(_tuple, _reserved):
    return _tuple in _reserved

def a_star_algorithm(priorityqueue, reserverd_queue=[((),())]):

    #print gates
    mastercounter = []
    for i in range(1):
        plaats = i
        #print 'run: ', plaats
        
        #print gates
        
        #print len(nets)

        dirs = 6 # number of possible directions to move on the map
        dx = [1, 0, 0, -1, 0, 0]
        dy = [0, 1, 0, 0, -1, 0]
        dz = [0, 0, 1, 0, 0, -1]

        fx = [1, 0, -1, 0]
        fy = [0, 1, 0, -1]

        n = 18 # horizontal size of the map
        m = 13 # vertical size of the map
        the_map = [[] for i in repeat(None, 8)]
        the_list = []

        row = [0] * n
        for j in range(0, 8):
            for i in range(m): # create empty map
                the_map[j].append(list(row))


        
        # priorityqueue_temp = chip.sorted_list(coordinates_points)

        # priorityqueue = []
        # for i in range(len(priorityqueue_temp)):
        #     priorityqueue.append(priorityqueue_temp[i][0])

        # print 'prior' ,priorityqueue
        # begining_of_queue= [((11, 5), (6, 3)), ((10, 12), (16, 15)), ((6, 1), (7, 12)), ((4, 12), (10, 6)), ((6, 9), (10, 1)), ((6, 9), (16, 7)), ((14, 2), (9, 10)), ((6, 8), (15, 12)), ((7, 12), (10, 1)), ((4, 5), (8, 15)), ((1, 15), (12, 11)), ((1, 15), (9, 8)), ((15, 1), (4, 5)), ((12, 6), (4, 14)), ((10, 12), (1, 3)), ((8, 15), (1, 1))]

        # for el in begining_of_queue:
        #     priorityqueue.remove(el)
        #     priorityqueue.insert(0,el)

        # print len(priorityqueue)

        #print superqueue

        # aanpassen priorityqueue = superqueue
        # priorityqueue = []
        # for i in range(len(superqueue)):
        #     priorityqueue.append(random.choice(superqueue))
        #     superqueue.remove(priorityqueue[i])

        #print priorityqueue    

        lines = 0

        begin_x = []
        end_x = []
        begin_y = []
        end_y = []
        begin_z = []
        end_z = []
        route_main = []
        drawn = []
        not_drawn = []
        for i in range(len(priorityqueue)):
            xA = priorityqueue[i][0][0]
            #print xA
            yA = priorityqueue[i][0][1]
            #print xA, yA
            xB = priorityqueue[i][1][0]
            #print xB
            yB = priorityqueue[i][1][1]
            #print xB, yB
            zA = 0
            zB = 0
            
            reserved_x = reserverd_queue[:len(reserverd_queue)/2]
            reserved_y = reserverd_queue[len(reserverd_queue)/2:]
            _reserved_x = []
            _reserved_y = []
            for item in reserved_x:
                _reserved_x.append(item[0])
                _reserved_x.append(item[1])

            for item in reserved_y:
                _reserved_y.append(item[0])
                _reserved_y.append(item[1])


            if len(gates)>0:
                for zf in range(1):
                    for i in range(len(reserved_x)):
                        for j in range(4):
                            z = zf
                            y = reserved_x[i][0][1] + fx[j]
                            x = reserved_x[i][0][0] + fy[j]                     
                            if the_map[z][y][x] != 1:
                                 the_map[z][y][x] = 6
                for z in range(0, 8):
                    if z in range(3):
                        if (xA,yA) in _reserved_x:
                            for j in range(4):
                                if the_map[z][yA][xA +fx[j]] != 1:
                                     the_map[z][yA][xA +fx[j]] = 0
                        if (xB,yB) in _reserved_x:
                            for j in range(4):
                                if the_map[z][yB][xB +fx[j]] != 1:
                                    the_map[z][yB][xB +fx[j]] = 0

                        if (xA,yA) in _reserved_y:
                            for j in range(4):
                                if the_map[z][yA + fy[j]][xA] != 1:
                                    the_map[z][yA +fy[j]][xA] = 0 
                        if (xB,yB) in _reserved_y:
                            for j in range(4):
                                if the_map[z][yB + fy[j]][xB] != 1:
                                    the_map[z][yB +fy[j]][xB] = 0


                    for i in range(len(gates)):
                        x = gates[i][1]
                        y = gates[i][2]
                        # if (z==0):
                        xyz = the_map[z][y][x]
                        if (x == xA and y == yA and z==0):
                            the_map[z][y][x] = 2
                        elif (x == xB and y == yB and z==0):
                            the_map[z][y][x] = 2
                        elif (x == xA and y == yA and xyz != 1):
                            the_map[z][yA][xA] = 2    
                        elif (x == xB and y == yB and xyz != 1):
                            the_map[z][yB][xB] = 2
                        elif (x != xA or xB and y != yA or yB):
                            if (z==0 or z==1):
                                if (xyz != 1):
                                    the_map[z][y][x] = 5
                        




                        # elif (x != xA or xB and y != yA or yB and z == 2 and xyz != 1):    
                        #     the_map[2][y][x] = 5       
                        # elif (x != xA or xB and y != yA or yB and z == 3 and xyz != 1):    
                        #     the_map[3][y][x] = 5                          
                        # else:
                        #     if (the_map[z][y][x] != 1):
                        #         the_map[z][y][x] = 5
                        # else:
                        #     if (the_map[z][yA][xA] != 1):
                        #         the_map[z][yA][xA] = 0
                        #     elif (the_map[z][yB][xB] != 1):
                        #         the_map[z][yB][xB] = 0    
                        # #elif not (x == xA and y == yA or x == xB and y == yB):
                        #     else:    
                        #         the_map[z][y][x] = 5 
            
            #path tester
            #print 'Map:'
            # for z in range(0, 8):
            #     for y in range(m):
            #         for x in range(n):
            #             xyz = the_map[z][y][x]
            #             if xyz == 0:
            #                 print '.', # space
            #             elif xyz == 1:
            #                 print 'O', # obstacle
            #             elif xyz == 2:
            #                 print 'S', # start
            #             elif xyz == 3:
            #                 print 'R', # route
            #             elif xyz == 4:
            #                 print 'F', # finish
            #             elif xyz == 5:
            #                 print 'G', # finish 
            #             elif xyz == 6:
            #                 print 'R', # finish      
            #         print
            #     print '\n'


            route = pathFind(the_map, n, m, dirs, dx, dy, dz, xA, yA, zA, xB, yB, zB)
            #print route
            route_main.append(route)
            for i in range(1,8):
                begin = the_map[i][yA][xA]
                if (begin != 1):
                    the_map[i][yA][xA] = 0
                end = the_map[i][yB][xB]    
                if (end != 1):
                    the_map[i][yB][xB] = 0    

            if len(route) == 0:
                not_drawn.append(((xA,yA),(xB,yB)))

            elif len(route) > 0:
                # begin_x = []
                # end_x = []
                # begin_y = []
                # end_y = []
                # begin_z = []
                # end_z = []
                drawn.append(((xA,yA),(xB,yB)))
                routes = len(route)
                x = xA
                y = yA
                z = zA
                # print x,y,z
                the_map[z][y][x] = 5
                
                lines += 1
                
                
                begin_x.append(x)
                begin_y.append(y)
                begin_z.append(z)
                for i in range(len(route)):
                    j = int(route[i])
                    x += dx[j]
                    y += dy[j]
                    z += dz[j]
                    # print x,y,z
                    if routes > 1:
                        end_x.append(x)
                        end_y.append(y)
                        end_z.append(z)
                        begin_x.append(x)
                        begin_y.append(y)
                        begin_z.append(z)
                        routes -= 1
                    
                    elif routes == 1:
                        end_x.append(x)
                        end_y.append(y)
                        end_z.append(z)
                        routes -= 1
                    the_map[z][y][x] = 1
                the_map[z][y][x] = 5
                
                # print 'Map:'
                # for z in range(0, 8):
                #     for y in range(m):
                #         for x in range(n):
                #             xyz = the_map[z][y][x]
                #             if xyz == 0:
                #                 print '.', # space
                #             elif xyz == 1:
                #                 print 'O', # obstacle
                #             elif xyz == 2:
                #                 print 'G', # start
                #             elif xyz == 3:
                #                 print 'R', # route
                #             elif xyz == 4:
                #                 print 'F', # finish
                #             elif xyz == 5:
                #                 print 'G', # finish 
                #             elif xyz == 6:
                #                 print 'R', # finish   
                #         print
                #     print '\n'
                

                # print begin_x
                # print begin_y
                # print begin_z
               
                begin_coordinates = zip(begin_x,begin_y, begin_z)
                #print begin_coordinates
                end_coordinates = zip(end_x, end_y, end_z)
                #print end_coordinates
                the_list = zip(begin_coordinates, end_coordinates)
                #the_list.append(temp)

        # print the_list
        #display the map with the route added
        
        # print 'Map:'
        # for z in range(0, 8):
        #     for y in range(m):
        #         for x in range(n):
        #             xyz = the_map[z][y][x]
        #             if xyz == 0:
        #                 print '.', # space
        #             elif xyz == 1:
        #                 print 'O', # obstacle
        #             elif xyz == 2:
        #                 print 'G', # start
        #             elif xyz == 3:
        #                 print 'R', # route
        #             elif xyz == 4:
        #                 print 'F', # finish
        #             elif xyz == 5:
        #                 print 'G', # finish 
        #             elif xyz == 6:
        #                 print 'R', # finish   
        #         print
        #     print '\n'

        # layers_number = 0
        # for i in range(len(the_list)):
        #     if the_list[i][0][2] >= layers_number:
        #         layers_number +=1

        # print 'Grid 1 - Netlist 3'
        # print 'Number of layers used:  ', layers_number
        # print 'Number of drawn lines: ', lines
        # # print 'Number of total lines: ', len(coordinates_points)
        # print 'Number of nets:        ', len(nets)
        # # print 'Number of gates:       ', len(gates)
        # print 'Number of nodes:      ',len(the_list)
        print the_list
        nodes_count = len(the_list)
        mastercounter.append(lines)
        # print lines
        # print route_main

        test = []
        name = range(0,50)
        test = zip(name, priorityqueue, route_main)
        # print test
    maximum = max(mastercounter)
    #print 'Largest Number of drawn lines' ,maximum

    return not_drawn, drawn, nodes_count

    # print 'Not drawn list: ', not_drawn
    # print 'Drawn list: ', drawn

#--------------------------------------MAIN----------------------------------------------------------------------------#


net_lists = NetLists()
gates = chip.make_gate_list(chip.f_input_1)
nets = net_lists.netlist_2
coordinates_points = chip.net_coordinates(gates, nets)
temp = chip.sorted_list(coordinates_points)
priorityqueue = []

for el in temp:
    priorityqueue.append(el[0])
# print priorityqueue
board = a_star_algorithm(priorityqueue)
# print board[0]
print 'Number of drawn lines', len(board[1])
print 'Number of total lines', len(nets) 
winning = []
winning_linesteps = []
winning_numberNodes = []
for i in range(3000):
    priorityqueue = []
    board_temp = []
    end_temp = []
    reserverd_queue = []
    for el in board[0]:
        priorityqueue.append(el)
    for el in board[1]:
        board_temp.append(el)
    picker = random.choice(range(2))

    for i in range(picker): 
        choice = random.choice(board_temp)
        board_temp.remove(choice)
        end_temp.append(choice) 
    reserverd_queue = end_temp[:]   
    priorityqueue = priorityqueue+end_temp+board_temp
    # print priorityqueue
    board = a_star_algorithm(priorityqueue, reserverd_queue)
    print 'Random choices', picker    
    print 'Number of drawn lines', len(board[1])
    print 'Number of total lines', len(nets)
    winning.append(len(board[1]))
    winning_linesteps.append(board[2])
for i in range(len(winning_linesteps)):
    if winning[i] >= 37:
        winning_numberNodes.append(winning_linesteps[i])
 
print 'Winning', max(winning)
print 'Winning Nodes', winning_numberNodes

