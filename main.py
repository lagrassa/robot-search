import obstacle, polygon
import becky, block
import pygame
import environment

other_vertex_list = [(0,50), (50,50), (50,0)]
reference_point = (50,50)
becky = becky.create_becky(reference_point)
block_vertices = [(200,200), (150,200), (200, 250), (120,80)]
color_list = [(0,0,255),(255,0,0),(0,255,0),(50,70,70),(80,90,50)]
block_list = []
for i in range(len(block_vertices)):
    new_block = block.block(block_vertices[i], color_list[i])
    block_list.append(new_block)

resolution = 10
#Can be BFS or DFS for blind_search, and "hill climbing" or "a star" for cost_based_search
algorithm = "hill climbing"
print "main start ", reference_point
basic_game = environment.Environment(reference_point, (300,300), block_list, becky, resolution, algorithm)
