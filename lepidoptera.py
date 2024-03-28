import random
import numpy as np
import math



# stage = ['larva', 'adult', 'dead']
# desires = {'survive':1, 'reproduce':0}
isAlive = True

state = {'stage':'larva', 'energy': 1, 'isAlive': isAlive}
# goal is no goal?

actions = ['move','eat','metamorphize','mate','die']

# desires if repro then 10, if survive then 10, 


from gridworld import Umwelt


class Loid():
    def __init__(self, lambda_energy):
        self.lambda_energy = lambda_energy
        self.timestep = 0
        self.actions = None
        self.desires = {'metamorphose':0, 'reproduce':0, 'eat':0, 'nothing': 0, 'border':0}
        self.desire_dict = {'food':'eat', 'partner':'reproduce', 'nothing': 'nothing', 'border':'border'}
        self.interactions = {'food_as_larva':0, 'food_as_adult':0, 'partner':0}
        # self.rewards = {'metamorphose':0, 'reproduce':0, 'eat':0}
        # self.rewards_coeff = {'metamorphose':[1,1], 'reproduce':[1,1], 'eat':[1,1]}
        self.umwelt = Umwelt(6,8,'nothing', 'border', 'food', 'partner')
        self.state = {'stage':'larva', 'energy': 1, 'isAlive': isAlive}
        # self.last_desire = 0
    
    def metamorphose(self):
        if self.state['stage'] == 'larva' and self.state['energy'] >= 3 :
            self.state['stage'] = 'adult'        
            self.state['energy'] *= -0.8
            self.desires['metamorphose'] = 0

        self.timestep += 1

    def canEvo(self):
        if self.state['stage'] == 'larva' and self.state['energy'] >= 3:
            return True
        return False
    

    def mate(self):
        self.timestep += 1

    def pick_move(self):
        dir_prob_numerators ={}
        for i in range(9):
            indicator = 0
            row, col = self.map_action_to_rowcol(i)
            value = self.umwelt.check_loc(row, col)
            if value == 'partner' and self.state['stage'] == 'larva':
                value = 'nothing'
            if value == 'food' or value == 'partner':
                indicator = 1

            dir_prob_numerators[i] = (1 + indicator * self.desires[self.desire_dict[value]])
        dir_prob_denominator = sum(dir_prob_numerators.values())
        dir_prob = {k : v * (1.0/dir_prob_denominator) for k,v in dir_prob_numerators.items()}

        if self.canEvo():
            print("Evo desire: ",self.desires["metamorphose"])
            dir_prob[9] = self.sigmoid(-100 if self.desires["metamorphose"] < -100 else self.desires["metamorphose"])

        max_value = max(dir_prob.values())
        best_actions = [k for k,v in dir_prob.items() if v == max_value]

        if len(best_actions) > 1:
            return random.choice(best_actions)
        elif len(best_actions) == 1:
            return best_actions[0]
        else:
            return random.choice([x for x in dir_prob.keys if x != 9])
    
    def move(self, action):
        if self.state['isAlive'] == False:
            return self.loc()

        row , col = self.map_action_to_rowcol(action)   

        if action == 9:
            self.metamorphose()
        
        self.umwelt.set_loc(row,col)
        self.update_energy()
        self.update_desires()
        self.timestep += 1
        return row, col
    
    def map_action_to_rowcol(self, action):
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
        if action == 9:
            row = 0
            col = 0
        return row, col

    def update_energy(self):
        box_type = self.umwelt.get_box_type()
        if box_type == 'nothing':
            self.state['energy'] -= 0.02
        if box_type == 'border':
            self.state['energy'] = 0
        if box_type == 'food':
            self.state['energy'] += random.uniform(1,3) * np.exp(-self.lambda_energy*self.timestep)
            self.umwelt.unset_box_type()
            if self.state['stage'] == 'larva':
                self.interactions['food_as_larva'] += 1
            else:
                self.interactions['food_as_adult'] += 1
        if box_type == 'partner' and self.state['stage']=='adult':
            self.state['energy'] -= 2
            self.umwelt.unset_box_type()
            self.interactions['partner'] += 1
        else:
            self.state['energy'] -= 0.02 

        if self.state['energy'] <= 0:
            self.state['isAlive'] = False

        self.update_desires()

    def update_desires(self):
        if self.state['stage'] == 'larva':
            self.desires["metamorphose"] = self.timestep * self.state["energy"]
            self.desires["eat"] = np.exp(-self.lambda_energy*self.timestep/self.state["energy"])
        else:
            self.desires["reproduce"] = self.timestep * self.state["energy"]
            self.desires["eat"] = np.exp(-self.lambda_energy*self.timestep/self.state["energy"])
        
    
    def reward(self):
        if self.state['stage'] == 'larva':
            return self.desires['metamorphose'] + self.desires['eat']
        else:
            return self.desires['reproduce'] + self.desires['eat']

    def isAlive(self):
        return self.state['isAlive']
    
    
    def seeWorld(self):
        self.umwelt.print_world()


    def get_dims(self):
        return self.umwelt.get_dims()
    
    def loc(self):
        return self.umwelt.get_loc()
    
    def print_stats(self):
        print("States: ", self.state)
        print("Rewards: ", self.desires)
        print("Interactions: ",self.interactions)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))



