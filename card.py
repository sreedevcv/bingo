import random


class Bingo:
    
    def __init__(self, size):
        self.row = size
        self.col = size
        self.bingo_matrix = []
        self.marked_ele = []
        numbers = [x + 1 for x in range(size**2)]
        l = len(numbers)
    
        for i in range(0, size):
            temp = []
            for j in range(0, size):
                x = random.randint(0, l - 1)
                # print(x, l)
                temp.append([numbers[x], False])
                numbers.remove(numbers[x])
                l -= 1
            self.bingo_matrix.append(temp)

        for i in range(2 * (size + 1)):
            self.marked_ele.append(0)

    def marked_entry(self, r, c):
        # if(self.bingo_matrix[r][c][0]==val):
        if r == c and r == (self.row) // 2 and self.row%2!=0:
            self.marked_ele[-2] += 1
            self.marked_ele[-1] += 1
        elif r == c and r == (self.row) // 2 and self.row%2==0:
            self.marked_ele[-2] += 1
            # self.marked_ele[-1] += 1
        elif r == c and r != (self.row) // 2:
            self.marked_ele[-2] += 1
        elif r == self.row - c - 1 and r != c:
            self.marked_ele[-1] += 1
        self.marked_ele[r] += 1
        self.marked_ele[c + self.row] += 1
        # self.bingo_matrix[r][c][1]=True

    def analyse(self):
        count = 0
        for x in self.marked_ele:
            if x == self.row:
                count += 1
        if count == self.row:
            print("BINGO game over")

    def getPointIndices(self, val):
        for i in range(self.row):
            for j in range(self.row):
                if self.bingo_matrix[i][j][0] == val:
                    return i, j

    # def find_ele(val):
    #     for i in range(row):
    #         for j in range(col):
    #             if(self.bingo_matrix[i][j][0]==val and self.bingo_matrix[r][c][1]!=True):
    #                 marked_entry(val,i,j)
    #             elif(self.bingo_matrix[r][c][1]==True):
    #                 print("Say another number")

    def count_unmarked_cells(self, pos:int) -> int:
        count = 0
        if pos < self.row:
            for i in range(self.row):
                if self.bingo_matrix[pos][i][1] == False:
                    count += 1
            return count
        if pos < 2 * self.row:
            for j in range(self.row):
                if self.bingo_matrix[j][pos - self.row][1] == False:
                    count += 1
            return count
        if pos == 2 * self.row:
            for i in range(self.row):
                if self.bingo_matrix[i][i][1] == False:
                    count += 1
            return count
        if pos == 2 * self.row + 1:
            for i in range(self.row):
                if self.bingo_matrix[i][self.row - 1 - i][1] == False:
                    count += 1
            return count
        
        return  0
