from agents.deep_q_agent import DeepQAgent
import numpy as np
from torch.utils.tensorboard import SummaryWriter

from rl.snake import SnakeMDP

writer = SummaryWriter()

env = SnakeMDP(False)


action_space = np.array([0,1,2])
n_games = 10000
score = 0
global_step = 0
eps_dec = 1 / (n_games * 0.8)
target_update = 10


agent = DeepQAgent(gamma=0.99, epsilon=1.0, batch_size=64, learn_start=10000, n_actions=3, input_dims=[11], learning_rate=0.0005, eps_dec=eps_dec)



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
            writer.add_scalar("Epsilon", agent.epsilon, global_step=global_step)

        writer.add_scalar("Reward", reward, global_step=global_step)
        global_step += 1

    if i % target_update == 0:
        agent.update_target_net()


    agent.decay_epsilon()
    writer.add_scalar("Episode score", score, global_step=i)
    writer.add_scalar("Moves per episode", env.n_steps(), global_step=i)