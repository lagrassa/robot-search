import physical_object
import search_lib
import pygame
import time

class Robot(physical_object.Physical_Object):
    def __init__ (self, polygon_list):
        physical_object.Physical_Object.__init__(self, polygon_list)
        self.collision_memory = {}
   
    #moves the robot part to a new location
    #@param {Polygon} part - part of the robot that's moving
    #@param {tuple}movement_vector - list of changes in position, of form (deltaX, deltaY, deltaZ.......)
    def move_part(self, part, movement_vector):
        new_vertex_locations = []
        for vertex in part.all_vertices:
            vertex = tuple([vertex[dimension] + movement_vector[dimension] for dimension in range(len(movement_vector))])
            new_vertex_locations.append(vertex)
        part.all_vertices = new_vertex_locations
        return part

    # moves entire robot, part by part to a new location
    #@param {tuple}movement_vector - list of changes in position, of form (deltaX, deltaY, deltaZ.......)
    def move(self, movement_vector):
        for body_part in self.polygon_list:
            self.body_part = self.move_part(body_part, movement_vector)

    #finds all possible places robot can move to 
    #@param {Node}nodeToExpand
    #@param {resolution} spaces on grid on which robot may move
    #currently only supports 2 dimensions
    def successor(self, nodeToExpand, resolution):
        state = nodeToExpand.state
        x = state[0]
        y = state[1]
        d = resolution
        all_possible_states = [(x+d, y), (x-d, y), (x, y+d), (x, y-d)]
        safe_states = []
        for possible_state in all_possible_states:
            if not self.collision_test(possible_state):
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
    def collision_test(self, state):
        if state in self.collision_memory:
            return self.collision_memory[state]
        else:
            #Check each obstacle to see if it is safe
            for obstacle in self.obstacle_list:
                if self.will_collide_with_obstacle(obstacle):
                    return False
            else:
                isSafe = True
            
            self.collision_memory[state] = isSafe
        
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
         time.sleep(0.01)

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

            new_state_list = self.successor(nodeToExpand, resolution)

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

        

        
                
                

 
