import numpy as np


class PPOMemory:
    def __init__(self, batch_size):
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.batch_size = batch_size

    def generate_batches(self):
        """
        Generate random batches from stored experiences.
        :return: Arrays of stored states, actions, probabilities, values, rewards, dones, and the generated batches.
        """
        n_states = len(self.states)
        batch_start = np.arange(0, n_states, self.batch_size)
        indices = np.arange(n_states, dtype=np.int64)
        np.random.shuffle(indices)
        batches = [indices[i:i + self.batch_size] for i in batch_start]

        return np.array(self.states), \
            np.array(self.actions), \
            np.array(self.probs), \
            np.array(self.vals), \
            np.array(self.rewards), \
            np.array(self.dones), \
            batches

    def store_memory(self, state, action, prob, val, reward, done):
        """
        Store an experience in memory.
        :param state: The observed state.
        :param action: The action taken.
        :param prob: The probability of the taken action.
        :param val: The value estimate of the state.
        :param reward: The reward received.
        :param done: Boolean indicating whether the episode is finished.
        """
        self.states.append(state)
        self.probs.append(prob)
        self.actions.append(action)
        self.vals.append(val)
        self.rewards.append(reward)
        self.dones.append(done)

    def clear_memory(self):
        """
        Clear all stored experiences from memory.
        """
        self.states.clear()
        self.probs.clear()
        self.actions.clear()
        self.rewards.clear()
        self.dones.clear()
        self.vals.clear()
