import pygame
# class Polygon
# @param tuple, reference_vertex
# @param list of tuples, other_vertices -other vertices of polygon with respect to reference_vertex
#
class Polygon:
    def __init__(self, reference_vertex, other_vertices):
        self.reference_vertex = reference_vertex
        self.other_vertices = other_vertices
        self.all_vertices = self.get_relative_vertices()
        self.color = (255, 0, 0)

    def get_relative_vertices(self):
        relative_vertex_list = [self.reference_vertex]
        for other_vertex in self.other_vertices:
            # list comprehension to allow multi dimensional reference points
            relative_vertex = [other_vertex[dimension]+self.reference_vertex[dimension] for dimension in range(len(self.reference_vertex))]
            relative_vertex_list.append(relative_vertex)
        relative_vertex_tuple = tuple(relative_vertex_list) # for performance
        return relative_vertex_tuple
    #Use pygame to draw polygon and fill it in with
    #tests if self has collided with obstacles
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.all_vertices)

