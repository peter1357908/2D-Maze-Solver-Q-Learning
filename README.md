# Q-learning Solver for Simple 2D Maze

## Dependent Libraries

PyGame 2.0.0, NumPy 1.19.4

## How to Run

Make sure you have installed all the dependent libraries, then simply run `python ./maze_q_learning_solver.py` in the root directory of this project.

## Expected Behavior

There are various parameters for the Q-learning algorithm that can be set in [maze_q_learning_solver.py](maze_q_learning_solver.py). By default, the agent trains for 2000 episodes, displaying the training process every 50 episodes; after training for 2000 episodes, the agent starts to exclusively exploit the previously learned Q-table, pausing a bit after reaching goal each time.

In the rendered graphics, the agent is the blue ball, with the black blocks being insurmountable walls and the green block being the goal. You can observe the agent seemingly aimlessly wondering the maze in the first few rendered episodes, and become gradually more efficiently in solving the maze.

With the default maze and parameters, the agent starts to consistently take the shortest route to the goal after a few rendered episodes (as the number of episodes increases, the agent is more biased toward exploiting learned Q-table rather than exploring randomly, showing that the Q-learning algorithm is properly implemented).

## Algorithm

The [basic Q-learning algorithm](https://en.wikipedia.org/wiki/Q-learning#Algorithm) is used to help the agent train itself and ultimately solve a given maze (the maze can be configured in [maze_environment.py](maze_environment.py)). The core algorithm is explained in the link and will not be reiterated here. This section of the README will mainly talk about some tweaks done to facilitate the training process.

The agent starts with a Q-table randomized with uniformly distributed float values in a certain range. During each episode, the agent tries to reach the goal one step at a time. The direction in which to take the step is either determined by the current Q-table ("exploitation") or randomly chosen ("exploration"). Whether to explore or to exploit is determined randomly based a value denoted as "epsilon"; the higher the epsilon, the more likely the agent would explore instead of exploit, and the epsilon value would decrease as episodes go by. After taking each step, the Q-table is updated - the Q-value for the state-action pair is modified based on the reward decided by the environment (along with other modifiers like the learning rate factor and the discount factor).

## Implementation

This section will talk about some design choices regarding the maze environment as well as the general code structure.

By default, an episode does not end until the agent reaches the goal; as a result, together with the effect of the epsilon (see "Algorithm" above), the first episode will likely be the longest episode (the most steps taken).

Each step by the agent incurs a "move penalty" (small in value), and running into a wall (or the boundary) in a step will additionally incur a "wall penalty" (moderate in value). Reaching the goal will result in a "goal reward" (great in value).

The code consists of two modules - the maze environment class, and the solver as the driver of that class. It is modularized so that it is also easy to write a program that allows the maze to be played as a game, or write a different algorithm that solves the maze.

There are also some statistics collection code commented out in [maze_q_learning_solver.py](maze_q_learning_solver.py). Uncomment them to have the stats printed to the console as the training goes on; you can also add in some `Matplotlib` code to draw some graphs (as an example, see [my other Q-learning implementation](https://github.com/peter1357908/RL-Solvers/blob/master/MountainCar-v0_Q-table_Analyzed.py))

## Resources Used

I referenced [my own past implementation of q-learning](https://github.com/peter1357908/RL-Solvers/blob/master/MountainCar-v0_Q-table_Analyzed.py) and took some inpiration (mainly the idea of using Q-learning to solve 2D mazes; no code borrowed) from [this web article on using q-learning to solve 2D mazes](https://becominghuman.ai/q-learning-a-maneuver-of-mazes-885137e957e4).

## Data Used

Since we are talking about Q-learning, which is a form of reinforcement learning, there really is no "data" per se. Instead, what matters is the design of the environment, which can be found in [maze_environment.py](maze_environment.py). Specifically, I hard-coded a solvable 6-by-6 2D maze, and set up the reward mechanism as described in the "Implementation" section.

## Conclusion

It worked! The agent eventually learns to navigate the maze to reach the goal, taking the shortest route possible. The basic observation is discussed in "Expected Behavior" section. Based on a few test runs, the number of episodes may be turned way down and still have the agent construct a Q-table that prompts the "shortest route to goal" behavior.

As hinted above, the training parameters are not optimized - we may either manually optimize them by looking at the stats (see "Implementation" section) while adjusting them, or, better, use another machine learning algorithm!

Q-learning is a very basic reinforcement learning algorithm and has limited application - it is best used for environments with discrete states, discrete actions, and very few state-action pairs (the small 2D maze used for this project is a prime example). For a less optimal use of the Q-learning algorithm, refer to [my other implementation](https://github.com/peter1357908/RL-Solvers/blob/master/MountainCar-v0_Q-table_Analyzed.py), where the environment has discrete actions but continuous states (I had to "discretize" the states by partitioning the state space).
