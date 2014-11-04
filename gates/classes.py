#
# Chips & Circuits
#
# File: classes.py
# Name: Cyrille Jones
# Date: 04/11/2014
#

import csv

# Open and read file 
f_input = csv.reader(open("gates-grid1.csv"))


def make_gate_list(filename):
    line = f_input.next()
    gate_name = []
    x_coordinates = []
    y_coordinates = []

    for line in f_input:
        gate_name.append(line[0])
        x_coordinates.append(int(line[1]))
        y_coordinates.append(int(line[2]))
        print line[0] + ":", int(line[1]), int(line[2])

    return zip(gate_name, x_coordinates, y_coordinates)

gate_list = make_gate_list(f_input)
print gate_list 
        
        





    




