import Grid_visualisation
import gate_lists

grid = input("Choose Grid (1 or 2):")
while (grid != 1) and (grid != 2):
    grid = input("Choose Grid (1 or 2):")

if grid == 1:
    Grid_visualisation.grid_init(13,18,gate_lists.gate_list_1)
elif grid == 2:
    Grid_visualisation.grid_init(17,18,gate_lists.gate_list_2)
