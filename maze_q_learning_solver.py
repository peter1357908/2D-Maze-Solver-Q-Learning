# Author: Shengsong Gao
# Date: 11/17/2020
#
# Final Project For Dartmouth COSC 16 Computational Neuroscience

from maze_environment import MazeEnvironment
import pygame
import numpy as np
import time

LEARNING_RATE = 0.3
DISCOUNT_RATE = 0.9
NUM_EPISODES = 2000
RENDER_INTERVAL = 50

epsilon = 0.7  # determines whether to explore or exploit; decays over time
EPSILON_DECAY_START = 1
EPSILON_DECAY_END = NUM_EPISODES // 2
EPSILON_DECREMENT = epsilon / (EPSILON_DECAY_END - EPSILON_DECAY_START)

# create the environment and make a Q-table

maze = MazeEnvironment(move_penalty=0.1, wall_penalty=1, goal_reward=10)
q_table = np.random.uniform(
    low=-2, high=0, size=(maze.num_columns, maze.num_rows, maze.num_actions))

# uncomment to satiate the stats nerds - part 1
# ep_rewards = []
# aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

# training
for episode in range(NUM_EPISODES):
    episode_reward = 0
    curr_x, curr_y = maze.initialize()
    if episode % RENDER_INTERVAL == 0:  # shows the first but not the last episode
        rendering = True
    else:
        rendering = False

    isDone = False
    while not isDone:
        if rendering:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rendering = False
            time.sleep(0.05)
            maze.render()

        if np.random.random() > epsilon:
            action = np.argmax(q_table[curr_x][curr_y])
        else:
            action = np.random.randint(0, maze.num_actions)

        new_x, new_y, reward, isDone = maze.take_action(action)
        episode_reward += reward

        max_future_q = np.max(q_table[new_x][new_y])
        current_q = q_table[curr_x][curr_y][action]
        new_q = (1 - LEARNING_RATE) * current_q + \
            LEARNING_RATE * (reward + DISCOUNT_RATE * max_future_q)
        q_table[curr_x][curr_y][action] = new_q

        if not isDone:    
            curr_x = new_x
            curr_y = new_y

    if EPSILON_DECAY_END >= episode >= EPSILON_DECAY_START:
        epsilon -= EPSILON_DECREMENT

    # uncomment to satiate the stats nerds - part 2
    # ep_rewards.append(episode_reward)

    # if episode % RENDER_INTERVAL == 0:
    #     average_reward = sum(
    #         ep_rewards[-RENDER_INTERVAL:]) / len(ep_rewards[-RENDER_INTERVAL:])
    #     aggr_ep_rewards['ep'].append(episode)
    #     aggr_ep_rewards['avg'].append(average_reward)
    #     aggr_ep_rewards['min'].append(min(ep_rewards[-RENDER_INTERVAL:]))
    #     aggr_ep_rewards['max'].append(max(ep_rewards[-RENDER_INTERVAL:]))
    
    # print(
    #     f'Episode: {episode}, average reward: {average_reward}, min: {min(ep_rewards[-RENDER_INTERVAL:])}, max: {max(ep_rewards[-RENDER_INTERVAL:])}')

# post training - pure exploitation of the Q-table

rendering = True
curr_x, curr_y = maze.initialize()
maze.render()

while rendering:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rendering = False

    time.sleep(0.05)
    action = np.argmax(q_table[curr_x][curr_y])
    curr_x, curr_y, reward, isDone = maze.take_action(action)
    maze.render()

    if isDone:
        time.sleep(2)
        curr_x, curr_y = maze.initialize()
        maze.render()

maze.cleanup()
