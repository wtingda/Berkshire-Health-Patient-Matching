import numpy as np
import pandas as pd
import random

def MACBanditModel:

    def __init__(self, patient_data, clinic_data_dim=5, lr=0.1, eps=0.5, decay=True):
        ''' 
        Multi-armed Contextual Bandit model for matching patients with clinics

        @Args:
          patient_data: np array of patient data
          clinic_data_dim: col count of clinic feature data
          lr: learning rate, higher implies greater magnitude of updates
          eps: epsilon exploration rate, between [0,1]. 1 implies explore only
               ignore if decay=True
          decay: whether epsilon decays over time
        '''
        
        self.patient_data = patient_data
        
        # preference weights take into account contextual info from patient and clinic
        self.preferences = np.zeros(self.patient_data.shape[1] + clinic_data_dim)

        # number of steps taken
        self.steps = 0

        # learning error/loss
        self.regret = []

        # exploration rate
        self.eps = eps

        # learning rate
        self.lr = lr

        # whether eps decreases over time
        self.decay = decay
        
    def get_features(self, clinic):
        ''' Returns concatenated feature vector containing patient and clinic data '''
        return np.concatenate((self.patient_data, clinic))
    
    def get_utility(self, clinic):
        ''' compute the preference dot product of features and learned preferences ''' 
        return self.preferences.dot(self.get_features(clinic))

    def update_func(new_pref, rating):
        ''' update function thatreturns weighted average of old and new preferences '''
        return ((self.steps-1) / self.steps) * self.preferences + (1/self.steps) * new_pref * rating * self.lr

    def update_regret(self, pref, rating):
        ''' 
        returns regret as difference in 
        predicted preference and true preference (rating) 
        '''
        self.regret.append(pref - rating)

    def update(self, clinic, rating):
        ''' updates preferences based on rating '''
        new_pref = self.get_utility(clinic)
        self.preferences = self.update_func(new_pref, rating)
        self.update_regret(new_pref, rating)
        self.steps += 1
        
    def eps_decay(self):
        ''' returns decaying eps value that decreases over time '''
        return 1 / math.sqrt(self.steps+1)
    
    def eps_greedy(self, clinics):
        ''' epsilon-greedy strategy '''

        eps = self.eps_decay if self.decay else self.eps
        if random.random() > eps:
            return clinics.sample()
        else:
            return self.greedy_best(clinics)
