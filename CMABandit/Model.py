import numpy as np
import pandas as pd
import random, statistics, math

class MACBanditModel:

    def __init__(self, patient_data_dim, clinic_data_dim, lr=0.0001, eps=0.5, decay=True):
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
        self.steps = 1

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
        ''' 
        compute the preference score dot product of features and learned preferences 
        @returns
          tuple (pref_score, new_features)
        '''
        new_features = self.get_features(patient, clinic)
        new_pref_score = self.preferences.dot(new_features)
        return new_pref_score, new_features
    
    def update_func(self, new_features, rating):
        ''' update function that returns weighted average of old and new preferences '''
        return ((self.steps-1) / self.steps) * self.preferences + (1/self.steps) * rating * self.lr * new_features 

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
        new_pref, new_features = self.get_preference(patient, clinic.to_numpy()[0])
        regret = rating - new_pref
        self.preferences = self.update_func(new_features, rating)
        return regret
    
    def greedy_best(self, patient, clinics):
        '''
        finds clinic with highest preference and returns feature
        row for said clinic
        '''
        prefs = np.zeros(clinics.shape[0])
        for i, clinic in enumerate(clinics.iterrows()):
            clinic = clinic[1]
            pref, _ = self.get_preference(patient, clinic.to_numpy())
            prefs[i] = pref
        best = prefs.argmax()
        return clinics[clinics.index == clinics.index[best]]

    def eps_decay(self):
        ''' returns decaying eps value that decreases over time '''
        return 1 / math.sqrt(self.steps)

    def eps_greedy(self, patient, clinics):
        ''' epsilon-greedy strategy '''
        eps = self.eps_decay() if self.decay else self.eps
        if random.random() > eps:
            return clinics.sample()
        else:
            return self.greedy_best(patient, clinics)

    def train_step(self, patients, clinics, ratingfunc):
        ''' one training step that recommends to every patient once '''
        step_regret = []
        for i, patient in enumerate(patients.iterrows()):
            patient = patient[1]
            chosen_clinic = self.eps_greedy(patient.to_numpy(), clinics)
            rating = self.get_rating(patient, chosen_clinic, ratingfunc)
            usr_regret = self.update(patient, chosen_clinic, rating)
            step_regret.append(usr_regret)
        self.update_regret(step_regret)
        self.steps += 1

    def get_rating(self, patient, clinic, ratingfunc):
        return ratingfunc(patient, clinic)

    def train(self, patients, clinics, ratingfunc, epochs=20, steps_per_epoch=5, verbose=True):
        epoch_ave_regret = []
        for i in range(epochs):
            # reset steps and regret
            self.steps = 1
            self.regret = []

            for step in range(steps_per_epoch):
                self.train_step(patients, clinics, ratingfunc)

            # store average epoch regret
            epoch_ave_regret.append(statistics.mean(self.regret))
            if verbose:
                print("(Epoch %d)  Regret: %f"%(i, epoch_ave_regret[-1]))
        return epoch_ave_regret
