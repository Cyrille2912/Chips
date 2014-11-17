from Tkinter import *
import csv

class Field(object):
    def grid_init(self, m , n, list_tpl_nodes):

        unit_length = 40
        # half size of nodes
        sq_hsize = 10

        x_list = []
        y_list = []

        for i in range(n):
            x_list.append((i + 1) * unit_length)

        for i in range(m):
            y_list.append((i + 1) * unit_length)

        root.wm_title('Chips & Circuits') = Tk()
        root.geometry("1000x1000")

        canvas_1 = Canvas(root, height = (m + 2) * unit_length,
                          width = (n + 2) * unit_length, bg="white")
        for i in x_list:
            canvas_1.create_line(i, y_list[0], i, y_list[m - 1])

        for j in y_list:
            canvas_1.create_line(x_list[0], j, x_list[n - 1], j)
            
        for node in list_tpl_nodes:
            x_node = (node[1] + 1) * unit_length
            y_node = (node[2] + 1) * unit_length
            canvas_1.create_rectangle(x_node - sq_hsize, y_node - sq_hsize,
                                      x_node + sq_hsize, y_node + sq_hsize,
                                      fill="red", outline = "red")


        canvas_1.pack()
        root.mainloop()


    def make_gate_list(self, filename):
        """
        Returns a list with the gates's name and its coordinates (x, y).
        """
        line = filename.next()
        gate_name = []
        x_coordinates = []
        y_coordinates = []

        for line in filename:
            gate_name.append(int(line[0]))
            y_coordinates.append(int(line[1]))
            x_coordinates.append(int(line[2]))

        return zip(gate_name, x_coordinates, y_coordinates)

    #gate_list_1 = make_gate_list(f_input_1)
    #gate_list_2 = make_gate_list(f_input_2)

    # Open and read file 
    f_input1 = open("grid1_netlist1.txt", "r")
    f_input2 = open("grid1_netlist2.txt", "r")
    f_input3 = open("grid1_netlist3.txt", "r")


    def make_net_list(self, filename):
        """
        Returns a list of connections between 
        gates.
        """
        line = filename.next()
        gates1 = []
        gates2 = []

        for line in filename:
            for i in range(len(line) - 1):
                if line[i] == ',':
                    gates2.append(int(line[:i]))
                if line[i] == ' ':
                    gates1.append(int(line[i+1:]))

        return zip(gates1, gates2)

    #net_list1 = make_net_list(f_input1)
    #net_list2 = make_net_list(f_input2)
    #net_list3 = make_net_list(f_input3)


    def net_coordinates(self, gates, nets):
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

    #net1 = net_coordinates(gate_list_1, net_list1)

    def connect_gates(self, netlists):
        """
        Connects the gates according to the net list.
        """
        for coordinates in netlists:
            
