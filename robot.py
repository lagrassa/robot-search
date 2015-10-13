import physical_object
import search_lib
import pygame
import time
import collision_test

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

    def in_bounds(self, new_state):
        return True
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
        clock = pygame.time.Clock()
        while len(queue) > 0:
            clock.tick(0.05);
            nodeToExpand = queue.pop()
            if (nodeToExpand.state == goal):
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
    def cost_plus_heuristic(self, node, goal):
        cost = node.cost
        heuristic = self.distance(node.state, goal)
        return cost + heuristic
    def heuristic(self, node, goal):
        heuristic = self.distance(node.state, goal)
        return  heuristic

    def distance(self, state1, state2):
        return ((state1[0]-state2[0])**2+(state1[1]-state2[1])**2)**0.5

    def a_star(self, start, goal, obstacle_list, resolution, screen, algorithm):
        self.obstacle_list  = obstacle_list #stored in robot's memory
        explored = {}
        start_node = search_lib.Node(start)
        start_node.cost = 0
        queue = [start_node]        
        while len(queue) > 0:
            if algorithm == "a star":
                queue = sorted(queue, key = lambda node: self.cost_plus_heuristic(node, goal))
            else:
                queue = sorted(queue, key = lambda node: self.heuristic(node, goal))
            nodeToExpand = queue.pop(0)
            if (nodeToExpand.state == goal):
                return nodeToExpand.path
            
            new_state_list = self.successor(nodeToExpand, resolution, obstacle_list)
            for new_state in new_state_list:
                if new_state not in explored and self.in_bounds(new_state):
                    explored[new_state] = True
                    new_node = search_lib.Node(new_state, nodeToExpand)
                    new_node.cost = nodeToExpand.cost + self.distance(new_state, goal)
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
        if (algorithm == "a star" or algorithm == "hill climbing"):
            path =  self.a_star(start, goal, obstacle_list, resolution, screen, algorithm)
        else:
            path =  self.blind_search(start, goal, obstacle_list, resolution, screen, algorithm)

        return path

        

        
                
                

 
