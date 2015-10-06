import numpy
import copy
import physical_object
import obstacle
def will_collide(state,robot, obstacle_list):
    robot_copy =  copy.deepcopy(robot)
    #based on state, update copy of robot's position
    robot_copy.move_to_point(state)
    for obstacle in obstacle_list:
        for obstacle_polygon in obstacle.polygon_list:
            for robot_copy_polygon in robot_copy.polygon_list:
                if not polygons_separate(robot_copy_polygon, obstacle_polygon):
                    return True #cannot go to that spot
    
    return False #All is fine

def polygons_separate(robot_polygon,  obstacle_polygon):
    isSeparated = False
    robot_polygon_normals = get_normals(robot_polygon)
    obstacle_polygon_normals = get_normals(obstacle_polygon)
    #Check each normal. If any one of these works, then you're good.
    for normal in robot_polygon_normals:
        projection_extremes_robot = get_min_max(robot_polygon, normal);
        projection_extremes_obstacle = get_min_max(obstacle_polygon, normal)
        if axes_separate(projection_extremes_robot, projection_extremes_obstacle):
            isSeparated = True
            break

    for normal in obstacle_polygon_normals:
        projection_extremes_obstacle = get_min_max(obstacle_polygon, normal);
        projection_extremes_robot = get_min_max(robot_polygon, normal)
        if axes_separate(projection_extremes_obstacle, projection_extremes_robot):
            isSeparated = True
            break
    if isSeparated:
        return True
    return False
    

def axes_separate(projection1, projection2):
    return projection1.max_proj < projection2.min_proj or projection2.max_proj < projection1.min_proj

def get_min_max(polygon, axis):
    projections = []
    origin = (0,0) 
    for i in range(0,len(polygon.all_vertices)):
        point_to = polygon.all_vertices[i]
        edge = (point_to[0]-origin[0], point_to[1]-origin[1])
        projection_scalar = (numpy.dot(axis,edge)/numpy.dot(axis,axis))
        projection = (projection_scalar * axis[0], projection_scalar * axis[1])
        projections.append(projection)
    minimum = min(projections, key = lambda p: numpy.linalg.norm(p))
    maximum = max(projections, key = lambda p: numpy.linalg.norm(p))
    return Projection_Extremes(minimum, maximum)


def get_normals(polygon):
    normals = []
    for i in range(0,len(polygon.all_vertices)):
        first_point = polygon.all_vertices[i-1]
        pointing_at = polygon.all_vertices[i]
        side_vector = (pointing_at[0]-first_point[0], pointing_at[1]-first_point[1])
        normal_vector =(-1*side_vector[1], side_vector[0])

        #normalizes
        normal_length = numpy.linalg.norm(normal_vector)
        normal_vector = [dim/normal_length for dim in normal_vector]
        normals.append(normal_vector)

    return normals

class Robot(physical_object.Physical_Object):
    def __init__ (self, polygon_list, current_location):
        physical_object.Physical_Object.__init__(self, polygon_list)
        self.collision_memory = {}
        self.current_location = current_location
   
    #moves the robot part to a new location
    #@param {Polygon} part - part of the robot that's moving
    #@param {tuple}movement_vector - list of changes in position, of form (deltaX, deltaY, deltaZ.......)
    def move_part(self, part, movement_vector):
        new_vertex_locations = []
        for vertex in part.all_vertices:
            vertex = (vertex[0]+movement_vector[0], vertex[1]+movement_vector[1])
            #vertex = tuple([vertex[dimension] + movement_vector[dimension] for dimension in range(len(movement_vector))])
            new_vertex_locations.append(vertex)
        part.all_vertices = new_vertex_locations
        return part

    # moves entire robot, part by part to a new location
    #@param {tuple}movement_vector - list of changes in position, of form (deltaX, deltaY, deltaZ.......)
    def move(self, movement_vector):
        for body_part in self.polygon_list:
            self.body_part = self.move_part(body_part, movement_vector)

    def move_to_point(self, point):
        deltaX = point[0]-self.current_location[0]
        deltaY = point[1]-self.current_location[1]
        self.move([deltaX, deltaY])

    #finds all possible places robot can move to 
    #@param {Node}nodeToExpand
    #@param {resolution} spaces on grid on which robot may move
    #currently only supports 2 dimensions
    def successor(self, nodeToExpand, resolution, obstacle_list):
        state = nodeToExpand.state
        x = state[0]
        y = state[1]
        d = resolution
        all_possible_states = [(x+d, y), (x-d, y), (x, y+d), (x, y-d)]
        safe_states = []
        for possible_state in all_possible_states:
            #if not(self.collision_check(possible_state, obstacle_list)):
            if not self.collision_check(possible_state, obstacle_list):
                assert(possible_state != (200,200))
                safe_states.append(possible_state)
        return safe_states

    #@param {Obstacle} obstacle robot can collide with
    #@returns {Boolean} true if the robot will collide with said obstacle at that point
    def will_collide_with_obstacle(self, obstacle):
        for body_part in self.polygon_list:
            for obstacle_part in obstacle.polygon_list:
                if self.parts_will_collide(body_part, obstacle_part):
                    return True
        return False
    #Determines whether two parts share points
    #@param {Polygon} body_part
    #@param {Polygon} obstacle
    #@returns{Boolean} 

    def parts_will_collide(self, body_part, obstacle):
        for vertex in body_part.all_vertices:
            for other_vertex in obstacle.all_vertices:
                if vertex == other_vertex:
                    return True
        return False

    #Figures out whether or not there will be a collision from that state, then stores that in its memory
    #@param {Tuple} state 
    def collision_check(self, state, obstacle_list):
        if state in self.collision_memory and False:
            willCollide =  self.collision_memory[state]
        else:
            willCollide = collision_test.will_collide(state, self, obstacle_list)
            self.collision_memory[state] = willCollide 
        return willCollide
        
    #displays path on screen
    def display_path(self, path, screen, obstacle_list, previous_path = [(0,0), (0, 0.5)]):
         BLACK = (0, 0, 0) 
         WHITE = (255, 255, 255)
         closed = False
         pygame.draw.lines(screen, BLACK, closed, path, 5)
         self.draw_parts(screen)
         for physical_object in self.obstacle_list:
             physical_object.draw_parts(screen)
         pygame.display.update()
         pygame.display.flip()
         screen.fill(WHITE)
         time.sleep(0.000001)

    def in_bounds(self, new_state):
        return new_state[0] < 400 and new_state[0] > 0 and new_state[1] < 400 and new_state[1] > 0
    #plans path to move. Robot thinks about how to move, and when it's ready to move, it will move. 
    #@param start {tuple}
    #@param goal {tuple}
    #@param obstacle_list {list of Obstacle}
    #Draws the current paths in mind
    #returns a final path to the goal
    def blind_search(self, start, goal, obstacle_list, resolution, screen, algorithm):
        self.obstacle_list  = obstacle_list #stored in robot's memory
        explored = {}
        start_node = search_lib.Node(start)
        queue = [start_node]        
        
        while len(queue) > 0:
            nodeToExpand = queue.pop()
            if nodeToExpand.state == goal:
                return nodeToExpand.path

            new_state_list = self.successor(nodeToExpand, resolution, obstacle_list)
            for new_state in new_state_list:
                if new_state not in explored and self.in_bounds(new_state):
                    explored[new_state] = True
                    new_node = search_lib.Node(new_state, nodeToExpand)
                    if (algorithm == "BFS"):
                        queue.insert(0,new_node)
                    elif (algorithm == "DFS"):
                        queue.append(new_node)
                    self.display_path(new_node.path, screen, nodeToExpand, obstacle_list)
                else:
                    continue
        print "found nothing"
        return None
    #Currently only supports 2 dimensions for simplicity
    #@param startnode
    #@param goal node
    #@param {Obstacle} obstacle_list
    #@param {int} resolution of grid
    #@param {Surface} screen to display paths on
    def plan(self, start, goal, obstacle_list, resolution, screen, algorithm):
        path =  self.blind_search(start, goal, obstacle_list, resolution, screen, algorithm)
        return path


class Projection_Extremes:

    def __init__(self, min_proj, max_proj):
        self.min_proj = min_proj
        self.max_proj = max_proj
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
'''
reference_point = (200,250)
other_vertex_list = [(0,50), (50,50), (50,0)]
square = Polygon(reference_point, other_vertex_list)
triangle_reference_point = (reference_point[0], reference_point[1]-50)
triangle_other_vertex_list = [(0,50),(50,50)]
triangle = Polygon(triangle_reference_point, triangle_other_vertex_list)
triangle.color = (0, 0, 255)

becky = Robot([square, triangle], reference_point)

other_vertex_list = [(0,50), (50,50), (50,0)]
reference_point = (200,200)
square = Polygon(reference_point, other_vertex_list)
import pygame
block = obstacle.Obstacle([square])
pygame.init()
screen = pygame.display.set_mode([400,400])
screen.fill((255,255,255))
becky.draw_parts(screen)
block.draw_parts(screen)
clock = pygame.time.Clock() 
while True:
    clock.tick(5)
    print polygons_separate(becky.polygon_list[1], block.polygon_list[0])
    print becky.polygon_list[1].all_vertices
    #print will_collide((0,0), becky, [block])
'''

