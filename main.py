import obstacle, polygon
import becky, block
import pygame
import environment

other_vertex_list = [(0,50), (50,50), (50,0)]
reference_point = (50,50)
becky = becky.create_becky(reference_point)
block_vertices = [(200,700), (500,500), (600, 400), (320,80)]
color_list = [(0,0,255),(255,0,0),(0,255,0),(50,70,70),(80,90,50)]
block_list = []
for i in range(len(block_vertices)):
    new_block = block.block(block_vertices[i], color_list[i])
    shifted_vertex  = (block_vertices[i][0]+150, block_vertices[i][1]-20)
    new_complex_block = block.complex_block(shifted_vertex, color_list[i-1])
    block_list.append(new_block)
    block_list.append(new_complex_block)

resolution = 10
#Can be BFS or DFS for blind_search, and "hill climbing" or "a star" for cost_based_search
algorithm = "hill climbing"
goal = (700,700)
print "main start ", reference_point
basic_game = environment.Environment(reference_point, goal, block_list, becky, resolution, algorithm)
