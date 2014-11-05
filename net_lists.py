#
# Chips & Circuits
#
# File: net_lists.py
# Name: Cyrille Jones
# Date: 04/11/2014
#

# Open and read file 
f_input1 = open("grid1_netlist1.txt", "r")
f_input2 = open("grid1_netlist2.txt", "r")
f_input3 = open("grid1_netlist3.txt", "r")


def make_net_list(filename):
    line = filename.next()
    x_coordinates = []
    y_coordinates = []

    for line in filename:
        for i in range(len(line) - 1):
            if line[i] == ',':
                y_coordinates.append(int(line[:i]))
            if line[i] == ' ':
                x_coordinates.append(int(line[i+1:]))

    return zip(x_coordinates, y_coordinates)

net_list1 = make_net_list(f_input1)
print net_list1
# net_list2 = make_net_list(f_input2)
# net_list3 = make_net_list(f_input3)

        
        





    




