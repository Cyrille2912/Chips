#
# Chips & Circuits
#
# File: gate_lists.py
# Name: Cyrille Jones
# Date: 04/11/2014
#

import csv

# Open and read file 
f_input_1 = csv.reader(open("gates_grid1.csv"))


def make_gate_list(filename):
    line = filename.next()
    gate_name = []
    x_coordinates = []
    y_coordinates = []

    for line in filename:
        gate_name.append(line[0])
        y_coordinates.append(int(line[1]))
        x_coordinates.append(int(line[2]))
        # print line[0] + ":", int(line[1]), int(line[2])

    return zip(gate_name, x_coordinates, y_coordinates)

gate_list_1 = make_gate_list(f_input_1)

        
        





    




