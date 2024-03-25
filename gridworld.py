import numpy as np

class Umwelt:
    def __init__(self, rows, cols, existence_cost, border_cost, food_reward, partner_reward):
        self.rows = rows + 2
        self.cols = cols + 2
        self.existence_cost = existence_cost
        self.grid = np.zeros((self.rows, self.cols))
        self.start = [1,1]
        self.loc = self.start
        self.rewards = np.full((self.rows,self.cols), existence_cost)
        self.foods = [(1,8),(3,5),(4,2),(4,7),(5,4)]
        self.partner = [(2,2), (3,8)]
        for row_index in range(0,self.rows):
            for col_index in range(0,self.cols):
                if row_index in [0,self.rows-1] or col_index in [0, self.cols-1]:
                    self.rewards[row_index, col_index] =  border_cost
                if (row_index, col_index) in self.foods:
                    self.rewards[row_index, col_index] = food_reward
                if (row_index, col_index) in self.partner:
                    self.rewards[row_index, col_index] =  partner_reward
    
    def get_loc(self):
        return self.loc
    
    def set_loc(self, row, col):
        self.loc[0] = self.loc[0] + row
        self.loc[1] = self.loc[1] + col
    
    def get_reward(self):
        return self.rewards[self.loc[0], self.loc[1]]
    
    def unset_reward(self):
        self.rewards[self.loc[0], self.loc[1]] = self.existence_cost

    def print_world(self):
        for row_index in range(0, self.rows):
            print(row_index)
            for col_index in range(0, self.cols):
                if self.loc[0] == row_index and self.loc[1] == col_index:
                    print('LOID')
                else:
                    print(self.rewards[row_index,col_index])
            print("\n")
                



        