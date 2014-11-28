## Work on Chip visualisation through class Window with Tkinter
## George Goultidis 

import gate_lists
import algorithms

from Tkinter import *
from ttk import *
import random


class Window:
    
    def __init__(self, master, window_width = 600, window_height = 600,layer_depth = 8,\
    delay = 0.2):
        """
        """

        # in seconds for animation
        self.delay = delay

        self.width = window_width
        self.height = window_height
        self.master = master

        self.button_width = 15

        self.layer_depth = layer_depth

        # noteboo for layers
        self.notebook = Notebook(self.master)
        
        # one canvas per layer  
        self.canvas_list = [Canvas(self.notebook, height = self.height, width = self.width)\
        for i in range(self.layer_depth)]
        
        # one layer per page
        for i in range(self.layer_depth):
            self.notebook.add(self.canvas_list[i], text = "Layer %d" %(i))

        self.notebook.pack(side= LEFT)

        # frame containing all buttons on the right
        self.button_frame = Frame(self.master, height = self.height)
        self.button_frame.pack(side = RIGHT)
        
        # initialize the listbox
        self.grid_listbox = Listbox(self.button_frame, width = self.button_width,\
            height = 7)
        self.grid_listbox.pack(side = TOP)

        for Grid_Net in ["Grid1: Net1", "Grid1: Net2", "Grid1: Net3", "Grid2: Net1",
        "Grid2: Net2", "Grid2: Net3"]:
            self.grid_listbox.insert(END,Grid_Net)
        self.grid_listbox.selection_set(first=0)
        self.currently_sel_listbox = -1
        self.poll()

        # algorithm buttons
        self.random_c_r_alg_button = Button(self.button_frame, text = "Random C Relax alg",\
            command = lambda : self.combine_grid_connections(algorithms.random_constraint_relaxation_algorithm()),\
            width = self.button_width)
        self.random_c_r_alg_button.pack(side = TOP)

        self.random_alg_button = Button(self.button_frame, text = "Random alg",\
            command = lambda : self.combine_grid_connections(algorithms.random_algorithm()),\
            width = self.button_width)
        self.random_alg_button.pack(side = TOP)

        self.a_star_alg_button = Button(self.button_frame, text = "A* alg",\
            command = lambda : self.combine_grid_connections(algorithms.a_star_algorithm()),\
            width = self.button_width)
        self.a_star_alg_button.pack(side = TOP)

        self.quit_button = Button(self.button_frame, text = "Quit",
            command = self.button_frame.master.destroy, width = self.button_width)
        self.quit_button.pack(side = BOTTOM)
    

    def combine_grid_connections(self, list_tpl_connections):
        if int(self.currently_sel_listbox[0]) in [0, 1, 2]:
            self.draw_grid(13,18,gate_lists.gate_list_1)
        elif int(self.currently_sel_listbox[0]) in [3, 4, 5]:
            self.draw_grid(17,18,gate_lists.gate_list_2) 

        self.draw_connections(list_tpl_connections)


    def poll(self):
        """
        A method that checks the user selection of the grid_listbox and the constaint_relaxation_checkbox
        every 500ms. If the selection has changed, it calls draw_grid and (ALGORITHM HERE) respectively
        for the new selection.
        """
        # check for grid_listbox selection
        sel = self.grid_listbox.curselection()
        if sel != self.currently_sel_listbox:
            #### print sel, self.currently_sel_listbox
            self.currently_sel_listbox = sel
            
            if int(self.currently_sel_listbox[0]) in [0, 1, 2]:
                self.draw_grid(13,18,gate_lists.gate_list_1)
            elif int(self.currently_sel_listbox[0]) in [3, 4, 5]:
                self.draw_grid(17,18,gate_lists.gate_list_2)        
            
            
        self.master.after(500, self.poll)


    def draw_grid(self, m , n, list_tpl_nodes):
        """
        Gets the dimentions m (y-axis) and n (x-axis) and a list of tuples containing the information 
        of each node. The tuples are of the type (node_no, x-position, y-position).
        First deletes what was previously drawn, then draws all layers.
        """
        # initializing dimensions of the canvas (NEEDS ELABORATION)
        min_dim = max(m, n)
        min_side = min(self.height, self.width)

        unit_length = (min_side - 40) / min_dim

        # half size of nodes
        sq_hsize = unit_length / 5

        # lists with positions of lines
        x_list = []
        y_list = []

        for i in range(n):
            x_list.append((i + 1) * unit_length)
        for i in range(m):
            y_list.append((i + 1) * unit_length)

        for canvas in self.canvas_list:
            # delete what was previously there
            canvas.delete("all")

            # draw the lines for each layer
            for i in x_list:
                canvas.create_line(i, y_list[0], i, y_list[m - 1])
            for j in y_list:
                canvas.create_line(x_list[0], j, x_list[n - 1], j)
            
            # Layer 0 has red nodes, all other have blue   
            if canvas == self.canvas_list[0]:
                color = "red"
            else:
                color = "blue"

            # draw the nodes on each layer
            for node in list_tpl_nodes:
                x_node = (node[1] + 1) * unit_length
                y_node = (node[2] + 1) * unit_length
                canvas.create_rectangle(x_node - sq_hsize, y_node - sq_hsize, 
                    x_node + sq_hsize, y_node + sq_hsize, fill=color, outline = color)


    def draw_connections(self, list_tpl_connections):
        """
        Gets a list of tuples of the type ((x_0,y_0), (x_1,y_1), layer_no) from algorithms.py and
        draws a lines connecting the two points of each tuple on the corresponding layer
        """
        for tpl in list_tpl_connections:
            self.canvas_list[tpl[2]].create_line(tpl[0][0],tpl[0][1], tpl[1][0],tpl[1][1])


if __name__ == "__main__":
    root = Tk()

    win = Window(root)

    root.mainloop()