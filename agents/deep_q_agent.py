import math

from rl.deep_q_network import DeepQNetwork
from util.replay_memory import ReplayMemory
import numpy as np
import torch as T



class DeepQAgent(object):
    def __init__(self, gamma, epsilon, learning_rate, input_dims, batch_size, learn_start, n_actions, max_mem_size=1000000, eps_end=0.01, eps_dec=5e-4):
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.n_actions = n_actions
        self.learn_start = learn_start
        self.batch_size = batch_size
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_mem_size
        self.mem_counter = 0
        self.policy_net = DeepQNetwork(learning_rate, input_dims, math.floor(input_dims[0] / 2), math.floor(input_dims[0] / 2), n_actions)
        self.target_net = DeepQNetwork(learning_rate, input_dims, math.floor(input_dims[0] / 2), math.floor(input_dims[0] / 2), n_actions)
        self.target_net.load_state_dict(self.target_net.state_dict())

        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool)


    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_counter % self.mem_size
        self.state_memory[index] = state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done
        self.new_state_memory[index] = state_
        self.mem_counter += 1

    def choose_action(self, observation):
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = T.tensor([observation]).to(self.policy_net.device)
            actions = self.policy_net.forward(state.float())
            action = T.argmax(actions).item()
        return action

    def update_target_net(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def learn(self):
        if self.mem_counter > self.learn_start:
            self.policy_net.optimiser.zero_grad()

            max_mem = min(self.mem_counter, self.mem_size)
            batch = np.random.choice(max_mem, self.batch_size, replace=False)

            batch_index = np.arange(self.batch_size, dtype=np.int32)
            state_batch = T.tensor(self.state_memory[batch]).to(self.policy_net.device)
            new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.policy_net.device)
            reward_batch = T.tensor(self.reward_memory[batch]).to(self.policy_net.device)
            terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.policy_net.device)
            action_batch = self.action_memory[batch]

            q_eval = self.policy_net.forward(state_batch)[batch_index, action_batch]
            q_next = self.policy_net.forward(new_state_batch)
            q_next[terminal_batch] = 0.0

            q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]

            loss = self.policy_net.loss(q_target, q_eval).to(self.policy_net.device)
            loss.backward()
            self.policy_net.optimiser.step()



            return loss

        return None

    def decay_epsilon(self):
        if self.mem_counter > self.learn_start:
            self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min \
                else self.eps_min
