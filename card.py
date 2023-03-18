import random

class Bingo:
    marked_ele=[]
    bingo_matrix=[]
    def __init__(self,size):
        self.row=size
        self.col=size
        bingo_matrix=[x+1 for x in range (size**2)]
        random.shuffle(bingo_matrix)



        for i in range(2*(size+1)):
            marked_ele.append(0)
    def marked_entry(val,r,c):
        if(bingo_matrix[r][c]==val):
            if (r==c and r ==row/2 ):
                marked_ele[-2]+=1
                marked_ele[-1]+=1    
            elif(r==c and r!=row/2):
                marked_ele[-2]+=1
            elif(r==row-c and r!=c):
                marked_ele[-1]+=1
            marked_ele[r-1]+=1
            marked_ele[c-1]+=1
            
            