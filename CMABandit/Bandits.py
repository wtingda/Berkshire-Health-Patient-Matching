'''
bandit setup of patient-clinic matching problem
used for testing various algorithsm
'''

import random

class Bandit:
    def __init__(self, payoff_probs):
        self.actions = range(len(payoff_probs))
        self.pay_offs = payoff_probs

    def sample(self, action):
        selector = random.random()
        return 1 if selector <= self.pay_offs[action] else 0



