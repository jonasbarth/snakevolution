from snake.env import SnakeEnv
from random import randint
from agents.random_agent import RandomAgent
import numpy as np

env = SnakeEnv(600, 600)
state, reward, done = env.reset()

action_space = np.array([0,1,2,3])

agent = RandomAgent(action_space)


while (not done):
    action = agent.get_action(state)
    state, reward, done = env.step(action)

env.wn.mainloop()
