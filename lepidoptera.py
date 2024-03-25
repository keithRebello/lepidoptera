stage = ['larvae', 'adult', 'dead']
desires = {'survive':1, 'reproduce':0}
isAlive = True

state = {'stage':stage, 'desires':desires, 'energy': 1, 'isAlive': isAlive}
# goal is no goal?

actions = ['move','eat','metamorphize','mate','die']

# rewards if repro then 10, if survive then 10, 


from gridworld import Umwelt


class Loid():
    def __init__(self):
        self.actions = None
        self.rewards = None
        self.umwelt = Umwelt(6,8,'nothing', 'border', 'food', 'partner')
        self.state = state
    
    def policy(self):
        #be MDP
        pass 

    def evolve(self):
        if self.state['stage'] == 'larvae' and self.state['energy'] == self.goal['evolution_trigger']:
            self.evolve() 

    def eat(self):
        if self.state["energy_storage"] <= self.goal["energy_storage_capacity"]:
            self.eat()

    def mate(self):
        if self.state['stage'] == 'adult' and self.goal['mate'] == 'found':
            self.mate()

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
        
        self.umwelt.set_loc(row,col)

    def reward(self):
        reward = self.umwelt.get_reward()
        if reward == 'nothing':
            energy -= 0.20
        if reward == 'border':
            energy = 0
        if reward == 'food':
            energy += 1
            self.umwelt.unset_reward()
        if reward == 'partner':
            energy -= 2
            self.umwelt.unset_reward()

    def isAlive(self):
        return self.state['isAlive']
    
    def seeWorld(self):
        self.umwelt.print_world()



