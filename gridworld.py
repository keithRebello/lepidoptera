import numpy as np

class Umwelt:
    def __init__(self, rows, cols, existence_cost, border_cost, food_energy, partner_energy):
        self.rows = rows + 2
        self.cols = cols + 2
        self.existence_cost = existence_cost
        self.grid = np.zeros((self.rows, self.cols))
        self.start = [1,1]
        self.loc = self.start
        self.energy = np.full((self.rows,self.cols), existence_cost)
        self.foods = [(1,8),(3,5),(4,2),(4,7),(5,4)]
        self.partner = [(2,2), (3,8)]
        for row_index in range(0,self.rows):
            for col_index in range(0,self.cols):
                if row_index in [0,self.rows-1] or col_index in [0, self.cols-1]:
                    self.energy[row_index, col_index] =  border_cost
                if (row_index, col_index) in self.foods:
                    self.energy[row_index, col_index] = food_energy
                if (row_index, col_index) in self.partner:
                    self.energy[row_index, col_index] =  partner_energy
    
    def get_loc(self):
        return self.loc
    
    def get_dims(self):
        return self.rows, self.cols
    
    def set_loc(self, row, col):
        if self.check_loc(row, col) == 'border':
            row = 0
            col = 0
            
        self.loc[0] = self.loc[0] + row
        self.loc[1] = self.loc[1] + col
    
    def get_energy(self):
        return self.energy[self.loc[0], self.loc[1]]
    
    def unset_energy(self):
        self.energy[self.loc[0], self.loc[1]] = self.existence_cost

    def check_loc(self, row, col):
        return self.energy[self.loc[0]+row, self.loc[1]+col] 

    def print_world(self):

        for row_index in range(0, self.rows):
            row  = str(row_index) + ':'
            for col_index in range(0, self.cols):
                if self.loc[0] == row_index and self.loc[1] == col_index:
                    row += " " + "L"
                elif self.energy[row_index,col_index] == 'nothing':
                    row += " " + "*"
                elif self.energy[row_index,col_index] == 'food':
                    row += " " + "F"
                elif self.energy[row_index,col_index] == 'partner':
                    row += " " + "P"
                elif self.energy[row_index,col_index] == 'border':
                    row += " " + "x"
            print(row)

                



        