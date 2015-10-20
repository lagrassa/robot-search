import pygame
import time
import collision_test
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
        self.resolution = resolution
        pygame.init()
        self.SIZE = [1000,1000]
        self.screen = pygame.display.set_mode(self.SIZE)
        self.WHITE = (255,255,255)
        self.screen.fill(self.WHITE)
        self.clock = pygame.time.Clock()
        self.algorithm = algorithm
        self.robot = robot
        self.robot.screen = self.screen
        self.robot.move_to_point(self.start)
        self.robot.current_state = self.start
        self.main()

    def main(self):
        self.draw()
        print "thinking"
        movement_path = self.robot.plan(self.start, self.goal, self.obstacle_list, self.resolution, self.algorithm)
        for state in movement_path:
            assert(not(collision_test.will_collide(state, self.robot, self.obstacle_list)))
        for state in movement_path:
            movement_vector = [state[0]-self.robot.current_state[0], state[1]-self.robot.current_state[1]]
            self.robot.move(movement_vector)
            self.robot.current_state = state
            time.sleep(0.05)
            #self.robot.display_path(movement_path, self.screen, self.obstacle_list)
            self.draw()
            

        
        while True:
            self.draw()
            self.clock.tick(1)

    def draw(self):
        self.screen.fill(self.WHITE)
        self.robot.draw_parts(self.screen)
        for obstacle in self.obstacle_list:
            obstacle.draw_parts(self.screen)
        pygame.display.flip()



