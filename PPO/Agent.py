import numpy as np
import torch as T
from PPO.ActorNetwork import ActorNetwork
from PPO.CriticNetwork import CriticNetwork
from PPO.PPOMemory import PPOMemory

C1 = 0.5


class Agent:
    def __init__(self, input_dims, n_actions, gamma=0.99, alpha=0.0003, gae_lambda=0.95,
                 policy_clip=0.2, batch_size=64, n_epoch=10):
        self.gamma = gamma
        self.policy_clip = policy_clip
        self.n_epochs = n_epoch
        self.gae_lambda = gae_lambda

        self.actor = ActorNetwork(n_actions, input_dims, alpha)
        self.critic = CriticNetwork(input_dims, alpha)
        self.memory = PPOMemory(batch_size)

    def remember(self, state, action, prob, val, reward, done):
        """
        Store experience in memory for later use during training.
        :param state: The state observed.
        :param action: The action taken.
        :param prob: The probability of the taken action.
        :param val: The value estimate of the state.
        :param reward: The reward received.
        :param done: Boolean indicating whether the episode is finished.
        """
        self.memory.store_memory(state, action, prob, val, reward, done)

    def save_models(self):
        """
        Save the models' parameters to checkpoint files.
        """
        print("... Saving Models ...")
        self.actor.save_checkpoint()
        self.critic.save_checkpoint()

    def load_models(self):
        """
        Load the models' parameters from checkpoint files.
        """
        print("... Loading Models ...")
        self.actor.load_checkpoint()
        self.critic.load_checkpoint()

    def choose_action(self, observation):
        """
        Choose an action based on the current observation of the environment.
        :param observation: The current state of the environment.
        :return: The selected action, log probability of the action, and value estimate of the state.
        """
        state = T.tensor([observation], dtype=T.float).to(self.actor.device)
        dist = self.actor(state)
        value = self.critic(state)
        action = dist.sample()

        probs = T.squeeze(dist.log_prob(action)).item()
        action = T.squeeze(action).item()
        value = T.squeeze(value).item()

        return action, probs, value

    def learn(self):
        """
        Perform learning by updating the actor and critic networks using the collected experiences.
        """
        for _ in range(self.n_epochs):
            state_arr, action_arr, old_probs_arr, vals_arr, reword_arr, done_arr, batches = \
                self.memory.generate_batches()

            values = vals_arr
            advantages = self.generate_advantages(done_arr, reword_arr, values)
            values = T.tensor(values).to(self.actor.device)

            for batch in batches:
                states = T.tensor(state_arr[batch], dtype=T.float).to(self.actor.device)
                old_probs = T.tensor(old_probs_arr[batch], dtype=T.float).to(self.actor.device)
                actions = T.tensor(action_arr[batch], dtype=T.float).to(self.actor.device)

                dist = self.actor(states)
                critic_value = self.critic(states)
                critic_value = T.squeeze(critic_value)

                new_probs = dist.log_prob(actions)
                prob_ratio = new_probs.exp() / old_probs.exp()
                weighted_probs = advantages[batch] * prob_ratio
                weighted_clipped_probs = T.clamp(prob_ratio, 1-self.policy_clip, 1+self.policy_clip)*advantages[batch]
                actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()

                returns = advantages[batch] + values[batch]
                critic_loss = ((returns-critic_value)**2).mean()

                total_loss = actor_loss + C1 * critic_loss
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step()

        self.memory.clear_memory()

    def generate_advantages(self, done_arr, reword_arr, values):
        """
        Calculate the advantage estimates used for policy updates.
        :param done_arr: Array indicating whether an episode has finished.
        :param reword_arr: Array of received rewards.
        :param values: Array of value estimates from the critic network.
        :return: Tensor containing the calculated advantages.
        """
        advantage = np.zeros(len(reword_arr), dtype=np.float32)
        for t in range(len(reword_arr) - 1):
            discount = 1
            a_t = 0
            for k in range(t, len(reword_arr) - 1):
                a_t = discount * (reword_arr[k] + self.gamma * values[k + 1] * (1 - int(done_arr[k])) - values[k])
                discount *= self.gamma * self.gae_lambda

            advantage[t] = a_t
        return T.tensor(advantage).to(self.actor.device)
