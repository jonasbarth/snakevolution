from agents.deep_q_agent import DeepQAgent
from snake.env import SnakeEnv
from random import randint
from agents.random_agent import RandomAgent
import numpy as np

env = SnakeEnv(600, 600)


action_space = np.array([0,1,2,3])

agent = DeepQAgent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=4, input_dims=[6], learning_rate=0.003)
n_games = 10
score = 0


for i in range(n_games):
    print("Episode", i)
    score = 0
    state, reward, done = env.reset()

    while (not done):
        action = agent.choose_action(state)
        state_, reward, done = env.step(action)
        score += reward
        agent.store_transition(state, action, reward, state_, done)
        agent.learn()
        state = state_

    print("Score is", score)


env.wn.mainloop()
