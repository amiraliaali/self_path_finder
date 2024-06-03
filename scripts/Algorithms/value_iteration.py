from maze import Maze, override
from maps import maze_map_1
import numpy as np

class MazeValueIteration(Maze):
    def state_values_init(self):
        self.state_values = np.full(
            self.maze_map.shape, 0.0
        )  # had to be initially filled with float numbers, otherwise later it would only get updated with integers
    
    def value_iteration(self, theta=1e-6, gamma=0.99):
        delta = float("inf")

        while delta > theta:
            delta = 0
            for row in range(self.state_values.shape[0]):
                for col in range(self.state_values.shape[1]):
                    old_state_value = self.state_values[(row, col)]
                    action_probs = None
                    max_action_return = float("-inf")

                    for action in range(4):
                        next_state, reward, _ = self.next_step((row, col), action)
                        action_return = reward + gamma * self.state_values[next_state]
                        if action_return > max_action_return:
                            max_action_return = action_return
                            action_probs = np.zeros(4)
                            action_probs[action] = 1.0

                    self.state_values[(row, col)] = max_action_return
                    self.policy_probs[(row, col)] = action_probs

                    delta = max(delta, abs(max_action_return - old_state_value))

        walls = np.where(self.maze_map == 1)
        for row, col in zip(list(walls[0]), list(walls[1])):
            self.state_values[(row, col)] = np.min(self.state_values)
            self.policy_probs[(row, col)] = np.full(4, 0.25)

    @override
    def run_maze(self, maze_map, draw_the_path, frame_width=500, frame_height=500):
        self.draw_path = draw_the_path
        self.generate_maze(maze_map, frame_width, frame_height)
        self.reward_map_init()
        self.policy_init()
        self.state_values_init()
        self.value_iteration()
        self.test_agent((0, 0))

if __name__ == "__main__":
    maze = MazeValueIteration()
    maze.run_maze(maze_map_1, True, 1500, 1500)