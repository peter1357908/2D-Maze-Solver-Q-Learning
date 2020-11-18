import pygame

class MazeEnvironment:
    def __init__(self, move_penalty, wall_penalty, goal_reward):
        '''
        0: empty space
        1: wall
        2: goal
        '''
        self.maze = [
            [0,0,0,0,0,0],
            [0,1,1,0,1,1],
            [1,2,1,0,1,0],
            [0,0,1,0,0,0],
            [1,0,0,0,1,0],
            [0,0,1,0,1,0]
        ]
        self.num_rows = 6
        self.num_columns = 6
        self.num_actions = 4  # in the order of "up, down, left, right"
        self.agent_initial_x = 1
        self.agent_initial_y = 0
        self.agent_current_x = self.agent_initial_x
        self.agent_current_y = self.agent_initial_y
        self.canvas_width = 600
        self.canvas_height = 600
        self.block_width = self.canvas_width / self.num_columns
        self.block_height = self.canvas_height / self.num_rows

        self.move_penalty = move_penalty
        self.wall_penalty = wall_penalty
        self.goal_reward = goal_reward

        pygame.init()
        self.canvas = pygame.display.set_mode(
            (self.canvas_width, self.canvas_height))

    # also returns the initial state (x, y)
    def initialize(self):
        self.agent_current_x = self.agent_initial_x
        self.agent_current_y = self.agent_initial_y

        return (self.agent_current_x, self.agent_current_y)

    def draw_block(self, color, x, y):
        pygame.draw.rect(self.canvas, color,
                        (x*self.block_width, y*self.block_height, self.block_width, self.block_height))

    def draw_circle(self, color, x, y):
        pygame.draw.circle(self.canvas, color,
                           ((x+0.5)*self.block_width, (y+0.5)*self.block_height), min(self.block_width, self.block_height)*0.5)

    # returns (new_x, new_y, reward, isDone)
    def take_action(self, action):
        expected_x = self.agent_current_x
        expected_y = self.agent_current_y

        reward = 0
        isDone = False

        if action == 0:
            expected_y -= 1 # up   
        elif action == 1:
            expected_y += 1 # down
        elif action == 2:
            expected_x -= 1 # left
        elif action == 3:
            expected_x += 1 # right
        else:
            print(f'unexpected action: {action}')
        
        if not (0 <= expected_x < self.num_columns) or not (0 <= expected_y < self.num_rows):
            reward = reward - self.move_penalty - self.wall_penalty
        else:
            block_type = self.maze[expected_y][expected_x]
            if block_type == 0:
                reward = reward - self.move_penalty
                self.agent_current_x = expected_x
                self.agent_current_y = expected_y
            elif block_type == 1:
                reward = reward - self.move_penalty - self.wall_penalty
            elif block_type == 2:
                reward = reward - self.move_penalty + self.goal_reward
                self.agent_current_x = expected_x
                self.agent_current_y = expected_y
                isDone = True
            else:
                print(f'the agent ran into an unexpected block type at ({expected_x},{expected_y})')
                reward = reward - self.move_penalty
                isDone = True
        
        return (self.agent_current_x, self.agent_current_y, reward, isDone)


    def render(self):
        # render the maze
        # TODO: make the rendering more efficient
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                block_type = self.maze[y][x]
                
                if block_type == 0:
                    block_color = 'white'
                elif block_type == 1:
                    block_color = 'black'
                elif block_type == 2:
                    block_color = 'green'
                else:
                    block_color = None
                    print(f'unexpected block type in input maze at ({x}, {y})')
                
                if block_color != None:
                    self.draw_block(block_color, x, y)

        # render the agent
        self.draw_circle('blue', self.agent_current_x, self.agent_current_y)
        
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()



