import polygon
import pygame
# class Physical Object
# @param {List} holding objects of type {Polygon} polygon_list - list of polygons that make up the object
class Physical_Object:
    def __init__(self, polygon_list):
        self.polygon_list = polygon_list

    #@param {Polygon} other_object - an object that could collide with this object
    #@returns boolean of whether robot can go there 
    def will_collide_with_object(self, other_object):
        pass
    #@param {List of Polygons} - list of potential objects that can collide with the object in question
    def check_for_collisions(self, object_list):
        pass
    
    #draws all the polygons in its list
    def draw_parts(self, screen):
        for polygon in self.polygon_list:
            polygon.draw(screen)
        #pygame.display.update()
        #pygame.display.flip()        



