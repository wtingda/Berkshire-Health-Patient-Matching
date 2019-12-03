import numpy as np
import pandas as pd
import random, statistics

def MACBanditModel:

    def __init__(self, patient_data_dim, clinic_data_dim=5, lr=0.1, eps=0.5, decay=True):
        '''
        Multi-armed Contextual Bandit model for matching patients with clinics

        @Args:
          patient_data_dim: col count of patient feature data
          clinic_data_dim: col count of clinic feature data
          lr: learning rate, higher implies greater magnitude of updates
          eps: epsilon exploration rate, between [0,1]. 1 implies explore only
               ignore if decay=True
          decay: whether epsilon decays over time
        '''

        # preference weights take into account contextual info from patient and clinic
        self.preferences = np.zeros(patient_data_dim + clinic_data_dim)

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

    def get_features(self, patient, clinic):
        ''' Returns concatenated feature vector containing patient and clinic data '''
        return np.concatenate((patient, clinic))

    def get_preference(self, patient, clinic):
        ''' compute the preference dot product of features and learned preferences '''
        return self.preferences.dot(self.get_features(patient, clinic))

    def update_func(new_pref, rating):
        ''' update function thatreturns weighted average of old and new preferences '''
        return ((self.steps-1) / self.steps) * self.preferences + (1/self.steps) * new_pref * rating * self.lr

    def update_regret(self, step_regret):
        '''
        stores average regret for training step
        '''
        self.regret.append(statistics.mean(step_regret))

    def update(self, patient, clinic, rating):
        '''
        updates preferences based on rating
        @returns: regret as difference in
            predicted preference and true preference (rating)
        '''
        new_pref = self.get_preference(patient, clinic)
        self.preferences = self.update_func(new_pref, rating)
        return rating - regret

    def greedy_best(self, patient, clinics):
        '''
        finds clinic with highest preference and returns feature
        row for said clinic
        '''
        prefs = np.zeros(clinics.shape[0])
        for i, clinic in enumerate(clinics.iterrows()):
            pref = self.get_preference(patient, clinic)
            prefs[i] = pref
        best = prefs.argmax()
        return clinics[clinics.index == clinics.index[best]]

    def eps_decay(self):
        ''' returns decaying eps value that decreases over time '''
        return 1 / math.sqrt(self.steps + 1)

    def eps_greedy(self, patient, clinics):
        ''' epsilon-greedy strategy '''
        eps = self.eps_decay() if self.decay else self.eps
        if random.random() > eps:
            return clinics.sample()
        else:
            return self.greedy_best(patient, clinics)

    def train_step(self, patients, clinics):
        ''' one training step that recommends to every patient once '''
        step_regret = []
        for _, patient in enumerate(patients.iterrows()):
            chosen_clinic = self.eps_greedy(patient, clinics)
            rating = self.get_rating(patient, chosen_clinic)
            usr_regret = self.update(clinic, rating)
            step_regret.append(usr_regret)
        self.update_regret(step_regret)
        self.steps += 1

    def get_rating(self, patient, clinic, ratingfunc):
        return ratingfunc(patient, clinic)

    def train(self, patients, clinics, epochs=20, steps_per_epoch=5):
        epoch_ave_regret = []
        for _ in range(epochs):
            # reset steps and regret
            self.steps = 0
            self.regret = []

            for step in range(steps_per_epoch):
                self.train_step(patients, clinics)

            # store average epoch regret
            epoch_ave_regret.append(statistics.mean(self.regret))
        return epoch_ave_regret
