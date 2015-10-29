import physical_object
import search_lib
import pygame
import time
import random
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
            if not self.not_in_C(possible_state, obstacle_list):
                safe_states.append(possible_state)
        return safe_states


    #Figures out whether or not there will be a collision from that state, then stores that in its memory
    #@param {Tuple} state 
    def not_in_C(self, state, obstacle_list):
        #Check for boundary
        width = self.screen.get_size()[0]
        height = self.screen.get_size()[1]
        x = state[0]
        y= state[1]
        if (x < 0 or x > width or y < 0 or y > height):
            return True 
        #Check for collision with obstacle
        if state in self.collision_memory and False:
            willCollide =  self.collision_memory[state]
        else:
            willCollide = collision_test.will_collide(state, self, obstacle_list)
            self.collision_memory[state] = willCollide 
        return willCollide
        
    #displays path on screen
    def display_path(self, path, obstacle_list, previous_path = [(0,0), (0, 0.5)]):
         BLACK = (0, 0, 0) 
         WHITE = (255, 255, 255)
         closed = False
         pygame.draw.lines(self.screen, BLACK, closed, path, 5)
         self.draw_parts(self.screen)
         for physical_object in self.obstacle_list:
             physical_object.draw_parts(self.screen)
         pygame.display.update()
         pygame.display.flip()
         #self.screen.fill(WHITE)

    #displays tree on screen
    def display_tree(self, tree1, tree2, obstacle_list, previous_path = [(0,0), (0, 0.5)]):
         if len(tree1.keys()) < 2 or len(tree2.keys()) < 2:
             return 
         for key in tree1.keys():
             path = tree1[key].path
         BLACK = (0, 0, 0) 
         WHITE = (255, 255, 255)
         closed = False
         pygame.draw.lines(self.screen, BLACK, closed, path1, 5)
         pygame.draw.lines(self.screen, BLACK, closed, path2, 5)
         self.draw_parts(self.screen)
         for physical_object in self.obstacle_list:
             physical_object.draw_parts(self.screen)
         pygame.display.update()
         pygame.display.flip()
         self.screen.fill(WHITE)

    def get_nearest_point(self,tree_points, end_point):
        nearest_point = min(tree_points, key = lambda x: self.heuristic(search_lib.Node(x), end_point))
        return nearest_point

    def rrt(self, start, goal, obstacle_list, resolution):
        self.obstacle_list = obstacle_list
        pathExists = False
        start_tree = {goal:search_lib.Node(goal)} #Both of these will hold search_lib.Nodes keyed on state
        goal_tree = {start:search_lib.Node(start)} 
        n = 0
        while(not pathExists):
            #switch trees
            n = (n+1) % 2
            expanding_tree = [start_tree, goal_tree][n]
            searched_for_tree = [start_tree, goal_tree][n-1]
            max_x, max_y = self.screen.get_size()[0], self.screen.get_size()[1]
            random_point = (random.randint(0,max_x), random.randint(0,max_y))
            #draw random point on screen
            nearest_random_point = self.get_nearest_point(expanding_tree.keys(), random_point)
            current_state = nearest_random_point
            if current_state in searched_for_tree:
                pathExists = True
                endState = current_state
                endNode = expanding_tree[endState]
                break;
            current_node = search_lib.Node(current_state)
            canExtend = True
            while (canExtend):
                extended_set = {}
                all_safe_states = self.successor(current_node, resolution, obstacle_list)
                possible_states = []
                for state in all_safe_states:
                    if state in extended_set.keys():
                        continue
                    else:
                        extended_set[state] = True
                        possible_states.append(state)
                nearest_state = self.get_nearest_point(possible_states, random_point)
                newNode = search_lib.Node(nearest_state, current_node)
                current_node.child = newNode
                self.display_path(newNode.path, obstacle_list)
                expanding_tree[nearest_state] = newNode
                current_node = newNode
                
                if len(possible_states) == 0 or current_node.state == nearest_state:
                    canExtend = False
                    extended_set = {}
                    break;
        print "RRT FINISHED"
        if pathExists:
            pathToStart = []
            pathToGoal = []
            if searched_for_tree == goal_tree:
                switch = False
            else:
                switch = True

            node = endNode
            pathToStart.append(node)
            while (node.parent is not None):
                pathToStart.append(node.parent)
                node = node.parent
            pathToStart.reverse()
            pathToGoal.append(endState)
            node = endNode
            while(node.child != None and node.child.state != goal):
                print "second loop"
                pathToGoal.append(node.child)
                node = node.child
            print "path to goal", pathToGoal
            print "pathToStart", pathToStart
            
            if switch:
                pathToStart, pathToGoal = pathToGoal, pathToStart

                return pathToStart + pathToGoal
                

            
    #plans path to move. Robot thinks about how to move, and when it's ready to move, it will move. 
    #@param start {tuple}
    #@param goal {tuple}
    #@param obstacle_list {list of Obstacle}
    #Draws the current paths in mind
    #returns a final path to the goal
    def blind_search(self, start, goal, obstacle_list, resolution, algorithm):
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
                if new_state not in explored:
                    explored[new_state] = True
                    new_node = search_lib.Node(new_state, nodeToExpand)
                    if (algorithm == "BFS"):
                        queue.insert(0,new_node)
                    elif (algorithm == "DFS"):
                        queue.append(new_node)
                    self.display_path(new_node.path, nodeToExpand, obstacle_list)
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

    def a_star(self, start, goal, obstacle_list, resolution, algorithm):
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
                if new_state not in explored: 
                    explored[new_state] = True
                    new_node = search_lib.Node(new_state, nodeToExpand)
                    new_node.cost = nodeToExpand.cost + self.distance(new_state, goal)
                    queue.append(new_node)
                    self.display_path(new_node.path,  nodeToExpand, obstacle_list)
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
    def plan(self, start, goal, obstacle_list, resolution,  algorithm):
        if algorithm == "rrt":
            path = self.rrt(start, goal, obstacle_list, resolution)
        elif (algorithm == "a star" or algorithm == "hill climbing"):
            path =  self.a_star(start, goal, obstacle_list, resolution,  algorithm)
        else:
            path =  self.blind_search(start, goal, obstacle_list, resolution,  algorithm)

        return path

        

        
                
                

 
