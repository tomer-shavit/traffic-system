import os
import torch as T
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical


class ActorNetwork(nn.Module):
    # TODO need to run and see it saves in the new file properly
    def __init__(self, n_actions, input_dims, alpha, fc1_dim=256, fc2_dim=256, chkpt_dir='TrainedNetworks'):
        super(ActorNetwork, self).__init__()

        self.checkpoint_file = os.path.join(chkpt_dir, 'actor_torch_ppo')
        self.actor = nn.Sequential(
            nn.Linear(*input_dims, fc1_dim),
            nn.ReLU(),
            nn.Linear(fc1_dim, fc2_dim),
            nn.ReLU(),
            nn.Linear(fc2_dim, n_actions),
            nn.Softmax(dim=-1)
        )
        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        """
        Perform a forward pass through the network.
        :param state: The input state to the network.
        :return: A categorical distribution over actions.
        """
        dist = self.actor(state)
        dist = Categorical(dist)
        return dist

    def save_checkpoint(self):
        """Save the model's parameters to a checkpoint file."""
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        """Load the model's parameters from a checkpoint file."""
        self.load_state_dict(T.load(self.checkpoint_file))
