import numpy as np
import random

ACTIONS = ["AutoRespond", "Escalate", "Ignore"]

class ModerationEnv:
    """Tiny synthetic environment for moderation decisions.

    State index encodes:
        0-9: low risk
        10-19: medium risk
        20-29: high risk
    """

    def __init__(self):
        self.state = 0

    def reset(self):
        self.state = random.randint(0, 29)
        return self.state

    def step(self, action_idx):
        state = self.state
        action = ACTIONS[action_idx]

        if state < 10:
            risk = "low"
        elif state < 20:
            risk = "medium"
        else:
            risk = "high"

        reward = 0

       
        if risk == "high":
            if action == "Escalate":
                reward = 10
            elif action == "AutoRespond":
                reward = -5
            else:
                reward = -15
        elif risk == "medium":
            if action == "AutoRespond":
                reward = 8
            elif action == "Escalate":
                reward = -2
            else:
                reward = -6
        else:  # low
            if action == "Ignore":
                reward = 5
            else:
                reward = -1

       
        self.state = random.randint(0, 29)
        done = False
        return self.state, reward, done, {}

def q_learning_train(episodes=2000, alpha=0.3, gamma=0.9, eps=0.2):
    env = ModerationEnv()
    Q = np.zeros((30, len(ACTIONS)))

    for _ in range(episodes):
        s = env.reset()
        done = False
        while not done:
            if random.random() < eps:
                a = random.randint(0, len(ACTIONS) - 1)
            else:
                a = int(np.argmax(Q[s]))

            s2, r, done, _ = env.step(a)
            Q[s, a] += alpha * (r + gamma * np.max(Q[s2]) - Q[s, a])
            s = s2

           
            if random.random() < 0.05:
                done = True

    return Q

def greedy_policy(Q):
    """Return mapping from risk level to best action."""
    mapping = {}
    for risk, rng in [("low", range(0,10)), ("medium", range(10,20)), ("high", range(20,30))]:
        avg_q = Q[list(rng)].mean(axis=0)
        best_action_idx = int(np.argmax(avg_q))
        mapping[risk] = ACTIONS[best_action_idx]
    return mapping
