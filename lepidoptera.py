import random
import numpy as np

stage = ['larva', 'adult', 'dead']
desires = {'survive':1, 'reproduce':0}
isAlive = True

state = {'stage':stage, 'desires':desires, 'energy': 1, 'isAlive': isAlive}
# goal is no goal?

actions = ['move','eat','metamorphize','mate','die']

# rewards if repro then 10, if survive then 10, 


from gridworld import Umwelt


class Loid():
    def __init__(self, lambda_energy):
        self.lambda_energy = lambda_energy
        self.timestep = 0
        self.actions = None
        self.rewards = {'evolve':0, 'reproduce':0, 'eat':0}
        self.reward_dict = {'food':'eat', 'partner':'reproduce'}
        self.umwelt = Umwelt(6,8,'nothing', 'border', 'food', 'partner')
        self.state = state
        self.last_reward = 0
    
    def policy(self):
        #be MDP
        pass 

    def evolve(self):
        if self.state['stage'] == 'larva':
            self.state['stage'] == 'adult'
        self.timestep += 1

    def mate(self):
        self.timestep += 1

    def pick_move(self):
        dir_prob_numerators ={}
        for i in range(9):
            indicator = 0
            value = self.umwelt.check_loc(i)
            if value == 'partner' and self.state['stage'] == 'larva':
                value = 'nothing'
            if value == 'food' or value == 'partner':
                indicator = 1

            dir_prob_numerators[i] = (1 + indicator * self.reward[self.reward_dict[value]])
        dir_prob_denominator = np.sum(dir_prob_numerators.values)
        dir_prob = {k : v * (1.0/dir_prob_denominator) for k,v in dir_prob_numerators.iteritems()}

        if self.state['stage'] == 'larva':
            dir_prob['evolve'] = np.sigmoid(self.reward["evolve"])

        max_value = max(dir_prob.values())
        best_actions = [k for k,v in dir_prob.items() if v == max_value]

        if len(best_actions) > 1:
            return random.choice(best_actions)
        elif len(best_actions) == 1:
            return best_actions[0]
        else:
            return random.choice([x for x in dir_prob.keys if x != 'evolve'])
    
    def move(self, action):
        if self.isAlive == False:
            print("DEAD. RIP LOID")
            return        

        if action == 0:
           row = -1
           col = -1
        if action == 1:
           row = -1
           col = 0
        if action == 2:
           row = -1
           col =  1
        if action == 3:
           row =  0
           col = -1
        if action == 4:
           row = 0
           col = 0
        if action == 5:
           row = 0
           col = 1
        if action == 6:
           row =  1
           col = -1
        if action == 7:
           row = 1
           col = 0 
        if action == 8:
           row = 1
           col = 1
        if action == 'evolve':
            row = 0
            col = 0
            self.evolve()
        
        self.umwelt.set_loc(row,col)
        self.timestep += 1

    def reward(self):
        reward = self.umwelt.get_reward()
        if reward == 'nothing':
            self.state['energy'] -= 0.20
        if reward == 'border':
            self.state['energy'] = 0
        if reward == 'food':
            self.state['energy'] += np.random.normal() * np.exp(-self.lambda_energy*self.timestep)
            self.umwelt.unset_reward()
        if reward == 'partner':
            self.state['energy'] -= 2
            self.umwelt.unset_reward()
        self.update_rewards()

    def update_rewards(self):
        self.rewards["reproduce"] *= self.timestep * self.state["energy"]
        self.rewards["evolve"] = self.timestep * self.state["energy"]
        self.rewards["eat"] = np.exp(-self.lambda_energy*self.timestep)


    def isAlive(self):
        return self.state['isAlive']
    
    
    def seeWorld(self):
        self.umwelt.print_world()



