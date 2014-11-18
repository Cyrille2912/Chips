from Field_visualization import *

f_input_1 = csv.reader(open("gates_grid1.csv"))
f_input_2 = csv.reader(open("gates_grid2.csv"))
f_input1 = open("grid1_netlist1.txt", "r")

chip = Field()

grid = input("Choose Grid (1 or 2):")
while (grid != 1) and (grid != 2):
    grid = input("Choose Grid (1 or 2):")

if grid == 1:
    gate_list_1 = chip.make_gate_list(f_input_1)
    chip.grid_init(13,18,gate_list_1)
elif grid == 2:
    gate_list_2 = chip.make_gate_list(f_input_2)
    chip.grid_init(17,18,gate_list_2)

net_list1 = chip.make_net_list(f_input1)
net1 = chip.net_coordinates(gate_list_1, net_list1)
distance = chip.line_distance(net1)
chip.draw_line(distance,net1, gate_list_1)

