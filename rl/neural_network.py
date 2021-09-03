import torch as T
import torch.nn as nn
import torch.nn.functional as F

class NeuralNetwork(nn.Module):

    def __init__(self, input_dims, hidden_dims, output_dims):
        super().__init__()
        self.fc1 = nn.Linear(input_dims, hidden_dims)
        self.fc2 = nn.Linear(hidden_dims, output_dims)

    def forward(self, input):
        state = T.Tensor(input).to(self.device)
        x = F.relu(self.fc1(state))
        x = self.fc1(x)

        return x

    def weights(self):
        return [self.fc1, self.fc2]