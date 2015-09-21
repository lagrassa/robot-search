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
        self.main()

    def main(self):
        self.draw()
        print "thinking"
        time.sleep(5)
        movement_path = self.robot.plan(self.start, self.goal, self.obstacle_list, self.resolution, self.screen, self.algorithm)
        print self.start, "start"
        self.robot.current_state = (300,300)
        for state in movement_path:
            movement_vector = [self.robot.current_state[0]-state[0], self.robot.current_state[1]-state[1]]
            self.robot.move(movement_vector)
            self.robot.current_state = state
            time.sleep(0.05)
            self.draw()

        
        while True:
            self.draw()
            self.clock.tick(10)

    def draw(self):
        self.screen.fill(self.WHITE)
        self.robot.draw_parts(self.screen)
        for obstacle in self.obstacle_list:
            obstacle.draw_parts(self.screen)



