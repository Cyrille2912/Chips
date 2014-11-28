## Work on Chip visualisation through class window with Tkinter
## George Goultidis 

import gate_lists

from Tkinter import *
from ttk import *
import random


class window:
	
	def __init__(self, master, window_width = 800, window_height = 600, delay = 0.2):
		# in seconds for animation
		self.delay = delay

		self.width = window_width
		self.height = window_height
		self.master = master

		self.notebook = Notebook(self.master)

		self.canvas_1 = Canvas(self.notebook, height = self.height, width = self.width)
		self.canvas_2 = Canvas(self.notebook, height = self.height, width = self.width)
		self.canvas_3 = Canvas(self.notebook, height = self.height, width = self.width)
		self.canvas_4 = Canvas(self.notebook, height = self.height, width = self.width)
		self.canvas_5 = Canvas(self.notebook, height = self.height, width = self.width)
		self.canvas_6 = Canvas(self.notebook, height = self.height, width = self.width)
		self.canvas_7 = Canvas(self.notebook, height = self.height, width = self.width)

		self.notebook.add(self.canvas_1, text = "Layer 1")
		self.notebook.add(self.canvas_2, text = "Layer 2")
		self.notebook.add(self.canvas_3, text = "Layer 3")
		self.notebook.add(self.canvas_4, text = "Layer 4")
		self.notebook.add(self.canvas_5, text = "Layer 5")
		self.notebook.add(self.canvas_6, text = "Layer 6")
		self.notebook.add(self.canvas_7, text = "Layer 7")

		self.notebook.pack(side= LEFT)

		self.button_frame = Frame(self.master, height = self.height,
			width = 100)
		self.button_frame.pack(side = RIGHT)
		
		self.listbox1 = Listbox(self.button_frame, width = 10)
		self.listbox1.pack(side = TOP)
		
		self.quit = Button(self.button_frame, text = "Quit",
			command = self.button_frame.master.destroy, width = 10)
		self.quit.pack(side = BOTTOM)
	

		for Grid_Net in ["Grid1: Net1", "Grid1: Net2", "Grid1: Net3", "Grid2: Net1",
		"Grid2: Net2", "Grid2: Net3"]:
			self.listbox1.insert(END,Grid_Net)
		self.listbox1.selection_set(first=0)
		self.currently_sel = self.listbox1.curselection()
		self.poll()


	def poll(self):
		sel = self.listbox1.curselection()
		if sel != self.currently_sel:
			self.currently_sel = sel
			for canvas in [self.canvas_1, self.canvas_2, self.canvas_3,
			self.canvas_4, self.canvas_5, self.canvas_6, self.canvas_7]:
				canvas.delete("all")

	    	if int(self.currently_sel[0]) in [0, 1, 2]:
	    		self.draw_grid(13,18,gate_lists.gate_list_1)
	    	elif int(self.currently_sel[0]) in [3, 4, 5]:
	    		self.draw_grid(17,18,gate_lists.gate_list_2)
		self.master.after(500, self.poll)


	def draw_grid(self, m , n, list_tpl_nodes):

		min_dim = min(m, n)
		min_side = min(self.height, self.width)

		unit_length = (min_side - 40) / min_dim

		# half size of nodes
		sq_hsize = unit_length / 5

		x_list = []
		y_list = []

		for i in range(n):
			x_list.append((i + 1) * unit_length)

		for i in range(m):
			y_list.append((i + 1) * unit_length)

		for canvas in [self.canvas_1, self.canvas_2, self.canvas_3,
		self.canvas_4, self.canvas_5, self.canvas_6, self.canvas_7]:
			for i in x_list:
				canvas.create_line(i, y_list[0], i, y_list[m - 1])

			for j in y_list:
				canvas.create_line(x_list[0], j, x_list[n - 1], j)
			    
			for node in list_tpl_nodes:
				x_node = (node[1] + 1) * unit_length
				y_node = (node[2] + 1) * unit_length
				canvas.create_rectangle(x_node - sq_hsize, y_node - sq_hsize, 
					x_node + sq_hsize, y_node + sq_hsize, fill="red", outline = "red")


root = Tk()

win = window(root)

win.poll()
root.mainloop()

