from rl.deep_q_network import DeepQNetwork
from util.replay_memory import ReplayMemory
import numpy as np
import torch as T



class DeepQAgent(object):
    def __init__(self, gamma, epsilon, learning_rate, input_dims, batch_size, n_actions, max_mem_size=1000000, eps_end=0.01, eps_dec=0.996):
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_end = eps_end
        self.eps_dec = eps_dec
        self.n_actions = n_actions
        self.batch_size = batch_size
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_mem_size
        self.mem_counter = 0
        self.Q = DeepQNetwork(learning_rate, input_dims, 256, 256, n_actions)
        self.state_memory = np.zeros((self.mem_size, *input_dims))
        self.new_state_memory = np.zeros((self.mem_size, *input_dims))
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=np.uint8)
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.uint8)


    def store_transition(self, state, action, reward, state_, terminal):
        index = self.mem_counter % self.mem_size
        self.state_memory[index] = state
        actions = np.zeros(self.n_actions)
        actions[action] = 1.0
        self.action_memory[index] = actions
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - terminal
        self.new_state_memory[index] = state_
        self.mem_counter += 1

    def choose_action(self, observation):
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            actions = self.Q.forward(observation)
            action = T.argmax(actions).item()
        return action

    def learn(self):
        if self.mem_counter > self.batch_size:
            self.Q.optimiser.zero_grad()

            max_mem = self.mem_counter if self.mem_counter < self.mem_size \
                else self.mem_size
            batch = np.random.choice(max_mem, self.batch_size)
            state_batch = self.state_memory[batch]
            action_batch = self.action_memory[batch]
            action_values = np.array(self.action_space, dtype=np.uint8)
            action_indices = np.dot(action_batch, action_values)
            reward_batch = self.reward_memory[batch]
            terminal_batch = self.terminal_memory[batch]
            new_state_batch = self.new_state_memory[batch]

            reward_batch = T.Tensor(reward_batch).to(self.Q.device)
            terminal_batch = T.Tensor(terminal_batch).to(self.Q.device)

            Q = self.Q.forward(state_batch).to(self.Q.device)
            Q_target = self.Q.forward(state_batch).to(self.Q.device)
            Q_next = self.Q.forward(new_state_batch).to(self.Q.device)


            batch_index = np.arange(self.batch_size, dtype=np.int32)
            Q_target[action_batch] = reward_batch + self.gamma * T.max(Q_next, dim=1)[0] * terminal_batch

            self.epsilon = self.epsilon * self.eps_dec if self.epsilon > self.eps_end else self.eps_end

            loss = self.Q.loss(Q_target, Q).to(self.Q.device)
            loss.backward()
            self.Q.optimiser.step()
            return loss

        return None
