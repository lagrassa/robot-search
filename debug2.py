import pygame
import time
#Environment sets up a game where a robot must find its way to the finish. Useful for testing
#
#
#Written by lagrassa 
#
#

#@param start {tuple} start location of robot
#@param finish {tuple} end location of robot
#@param obstacles {list of Obstacle} list of obstacles robot must manuever around
#@param robot {Robot} Robot that must get from point A to point B
#@return {Environment} Returns a game that can render itself
class Environment:
    def __init__(self, start, goal, obstacle_list, robot, resolution, algorithm):
        self.start = start
        self.goal = goal
        self.obstacle_list = obstacle_list
        self.robot = robot
        self.resolution = resolution
        pygame.init()
        self.SIZE = [400,400]
        self.screen = pygame.display.set_mode(self.SIZE)
        self.WHITE = (255,255,255)
        self.screen.fill(self.WHITE)
        self.clock = pygame.time.Clock()
        self.algorithm = algorithm
        self.robot.move_to_point(self.start)
        self.robot.current_state = self.start
        self.main()

    def main(self):
        print "environment start", self.start
        self.draw()
        print "thinking"
        #movement_path = self.robot.plan(self.start, self.goal, self.obstacle_list, self.resolution, self.screen, self.algorithm)
        movement_path = [self.start]
        for i in range(400):
            movement_path.append(tuple([movement_path[i-1][0],movement_path[i-1][1]+1]))
        #print "this is the found start by the plan", movement_path[0]
        #print "this is the last part of the plan", movement_path[-1]
        for state in movement_path:
            movement_vector = [state[0]-self.robot.current_state[0], state[1]-self.robot.current_state[1]]
            self.robot.move(movement_vector)
            self.robot.current_state = state
            print "movement_vector perceieved: ", movement_vector

            time.sleep(2)
            #self.robot.display_path(movement_path, self.screen, self.obstacle_list)
            self.draw()
        
        while True:
            self.draw()
            self.clock.tick(10)

    def draw(self):
        self.screen.fill(self.WHITE)
        self.robot.draw_parts(self.screen)
        for obstacle in self.obstacle_list:
            obstacle.draw_parts(self.screen)



