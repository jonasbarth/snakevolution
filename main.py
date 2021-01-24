from snake.env import SnakeEnv
from random import randint
from agents.random_agent import RandomAgent

env = SnakeEnv(600, 600)
state, reward, done = env.reset()

agent = RandomAgent([0, 1, 2, 3])


while (not done):
    action = agent.get_action(state)
    state, reward, done = env.step(action)

env.wn.mainloop()
