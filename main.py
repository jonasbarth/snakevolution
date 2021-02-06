from agents.deep_q_agent import DeepQAgent
from agents.human_agent import HumanAgent
from snake.env import SnakeEnv
from random import randint
from agents.random_agent import RandomAgent
import numpy as np
from torch.utils.tensorboard import SummaryWriter
import torch

writer = SummaryWriter()
env = SnakeEnv(600, 600)


action_space = np.array([0,1,2,3])

agent = HumanAgent(env)
agent.play()
"""
agent = DeepQAgent(gamma=0.99, epsilon=1.0, batch_size=64, learn_start=50000, n_actions=4, input_dims=[6], learning_rate=0.0005)
n_games = 0
score = 0
global_step = 0


for i in range(n_games):
    score = 0
    state, reward, done = env.reset()

    while not done:

        action = agent.choose_action(state)
        state_, reward, done = env.step(action)
        score += reward
        agent.store_transition(state, action, reward, state_, done)
        loss = agent.learn()
        state = state_
        if (loss):
            writer.add_scalar("Loss", loss, global_step=global_step)

        writer.add_scalar("Reward", reward, global_step=global_step)
        global_step += 1

    writer.add_scalar("Episode score", score, global_step=i)
    writer.add_scalar("Moves per episode", env.n_moves, global_step=i)


env.wn.mainloop()
"""