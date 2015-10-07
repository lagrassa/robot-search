import obstacle, polygon
import becky, block
import pygame
import environment

other_vertex_list = [(0,50), (50,50), (50,0)]
reference_point = (50,50)
becky = becky.create_becky(reference_point)
block = block.block((200,200))
resolution = 10
#Can be BFS or DFS for blind_search, and "hill climbing" or "a star" for cost_based_search
algorithm = "hill climbing"
print "main start ", reference_point
basic_game = environment.Environment(reference_point, (300,300), [block], becky, resolution, algorithm)
