from Tkinter import *

import gate_lists
##   n = 17
##   m = 12 


def grid_init(m , n, list_tpl_nodes):


    line_length = 40
    # half size of nodes
    sq_hsize = 10

    x_list = []
    y_list = []

    for i in range(n):
        x_list.append((i + 1) * line_length)

    for i in range(m):
        y_list.append((i + 1) * line_length)

    root = Tk()
    root.geometry("1000x650")

    canvas_1 = Canvas(root, height = (m + 2) * line_length,
                      width = (n + 2) * line_length, bg="white")
    for i in x_list:
        canvas_1.create_line(i, y_list[0], i, y_list[m - 1])

    for j in y_list:
        canvas_1.create_line(x_list[0], j, x_list[n - 1], j)
        
    for node in list_tpl_nodes:
        x_node = (node[1] + 1) * line_length
        y_node = (node[2] + 1) * line_length
        canvas_1.create_rectangle(x_node - sq_hsize, y_node - sq_hsize,
                                  x_node + sq_hsize, y_node + sq_hsize,
                                  fill="red", outline = "red")


    canvas_1.pack()
    root.mainloop()
