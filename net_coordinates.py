#
# Chips & Circuits
#
# File: net_coordinates.py
# Name: Cyrille Jones & Sean Tijmons
# Date: 04/11/2014
#
from gate_lists import *
from net_lists import *

def net_coordinates(gates, nets):
    """
    Links the gate coordinates with the gates's 
    number in the net list. Returns a list a tuples with,
    in each tuple, the start coordinates and the end coordinates 
    of each net.
    """
    gate_coordinates_from = []
    gate_coordinates_to = []

    for connections in nets:
            for coordinates in gates:
                    if connections[0] == coordinates[0]:
                            gate_coordinates_from.append(coordinates[1:])
                    if connections[1] == coordinates[0]:
                            gate_coordinates_to.append(coordinates[1:])
                            
    return zip(gate_coordinates_from, gate_coordinates_to)

net1 = net_coordinates(gate_list_1, net_list1)



