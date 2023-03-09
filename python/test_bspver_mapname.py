# This is only a local test
# allows a user to test all maps in a folder for their bsp version
# to determine the game and then enter into the sheet
# i don't want to automate it so here it is



import os
import bsp_tool

folder_path = "G:/surf/bsptest"
map_files = os.listdir(folder_path)

for map_file in map_files:
    if map_file.endswith(".bsp"):
        map_path = os.path.join(folder_path, map_file)
        bsp = bsp_tool.load_bsp(map_path)
        print(f"BSP version {bsp.bsp_version} map file {map_file}:")
