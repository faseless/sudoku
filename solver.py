"""
File: solver.py
Author: Ethan Lan
Description: Solves a sudoku puzzle scraped from puzzleScraper.py.
    Average time: ~130 seconds.
    Time taken to write: 3 days.
    Built without looking at any online resources involving solving Sudoku
    Last edit: 7/30/2019
    Things to do: Improve style/readability, thinking of ways to improve time efficiency,
        would like to design a decent front end for the script
"""
import numpy as np
import math
import time
from puzzleScraper import grid, idVal

table = np.array(grid)


#table = np.array([[1,0,0,0],[3,0,1,0],[0,1,2,0],[2,0,0,1]])
#used to test on smaller scale


#table = np.array([[9, 0, 0, 0, 0, 0, 0, 0, 1],
#        [0, 0, 4, 9, 0, 0, 0, 0, 0],
#        [0, 3, 0, 0, 0, 1, 0, 7, 4],
#        [0, 2, 0, 0, 8, 0, 0, 0, 0],
#        [0, 0, 9, 2, 7, 5, 3, 0, 0],
#        [0, 0, 0, 0, 3, 0, 0, 9, 0],
#        [2, 8, 0, 5, 0, 0, 0, 1, 0],
#        [0, 0, 0, 0, 0, 7, 5, 0, 0],
#        [4, 0, 0, 0, 0, 0, 0, 0, 6]])
#used to test when offline


#use slices to check rows, that way each row is automatically updated
#when the table changes


print(table)


#declare dimensions
rows = table.shape[0]
cols = table.shape[1]


#define rows
rowDict = {}
"""
previously manually defined rows, now entirely defined
in method based on table dimensions for scalability
rowDict[0] = table[0, :]
rowDict[1] = table[1, :]
rowDict[2] = table[2, :]
rowDict[3] = table[3, :]
rowDict[4] = table[4, :]
rowDict[5] = table[5, :]
rowDict[6] = table[6, :]
rowDict[7] = table[7, :]
rowDict[8] = table[8, :]
"""


#define columns
colDict = {}
"""
previously manually defined columns, now entirely defined
in method based on table dimensions for scalability
colDict[0] = table[:, 0]
colDict[1] = table[:, 1]
colDict[2] = table[:, 2]
colDict[3] = table[:, 3]
colDict[4] = table[:, 4]
colDict[5] = table[:, 5]
colDict[6] = table[:, 6]
colDict[7] = table[:, 7]
colDict[8] = table[:, 8]
"""


#create a dictionary of rows
for i in range(0, rows):
    rowDict[i] = table[i, :]


#create a dictionary of columns
for i in range(0, cols):
    colDict[i] = table[:, i]

print(rowDict)
print(colDict)


#used to determine the boxes of sudoku
root = (int)(math.sqrt(rows))


#get the respective box any coordinate position
#possibly replace with dictionary method for readability/ease-of-use
def getBox(row, col):
    rMin = rMax = cMin = cMax = -1
    for i in range(0, root):
        if row >= i * root:
            rMin = i * root
            rMax = (i + 1) * root
        if col >= i * root:
            cMin = i * root
            cMax = (i + 1) * root
    return table[rMin:rMax, cMin:cMax]


#try to make method to define boxes in a dictionary?
boxDict = {}
for i in range(0, root):
    for j in range(0, root):
        boxDict[(i, j)] = table[i * root : (i + 1) * root, j * root : (j + 1) * root]
#print(boxDict)


#make a set of the coordinate positions of read-only values
readOnly = set()
for d in range(0, rows):
    for e in range(0, cols):
        if table[d,e] != 0:
            readOnly.add((d,e))
#print(readOnly)

#def getBox(row, col):
#    rMin = rMax = cMin = cMax = -1
#    for i in range(0, root):
#        if row >= i * root:
#            rMin = i * root
#            rMax = (i + 1) * root
#        if col >= i * root:
#            cMin = i * root
#            cMax = (i + 1) * root
#    return table[rMin:rMax, cMin:cMax]
#IMPORTANT: find out which one is faster later
#for x in range(0, rows):
#    for y in range(0, cols):
#        print(f'{x/root}, {y/root}')


#determine which box a given row/column position is in
def getBox(row, col):
    boxRow = boxCol = -1
    for i in range(0, root):
        if row >= i * root:
            boxRow = i
        if col >= i * root:
            boxCol = i
    return boxDict[(boxRow, boxCol)]


#gets all valid numbers for a position based on 
#respective row, column, and box
def getValidNums(row, col): #seems to be working
    nums = np.arange(1, rows + 1)
    for num in nums:
        if num in rowDict[row] or num in colDict[col] or num in getBox(row, col):
            nums = nums[nums != num]
    return nums


"""
    base case:
        puzzle is filled with valid solution

    else:
        pick x from 1-9
            remove x from pool for that position
        if no valid number from 1-9
            retreat to the last number with more spots

    should this be recursive?
        recurse on remaining squares
        how to do iterative then?

    somewhat-pseudocode


#previously manually defined boxes, now defined with variables
#for scalability
#def getBox(row, col): #seems to be working
#    #rows 0,1,2 = [0,]
#    #rows 3,4,5 = [1,]
#    #rows 6,7,8 = [2,]
#
#    #cols 0,1,2 = [,0]
#    #cols 3,4,5 = [,1]
#    #cols 6,7,8 = [,2]
#
#    rmin = rmax = cmin = cmax = -1
#
#    if row < 3:     #top layer box
#        rmin = 0
#        rmax = 3
#    elif row < 6:   #middle layer box
#        rmin = 3
#        rmax = 6
#    else:           #bottom layer box
#        rmin = 6
#        rmax = 9
#
#    if col < 3:     #left layer box
#        cmin = 0
#        cmax = 3
#    elif col < 6:   #middle layer box
#        cmin = 3
#        cmax = 6
#    else:           #right layer box
#        cmin = 6
#        cmax = 9
#
#    return np.array(table[rmin:rmax, cmin:cmax])
"""


#recursive algorithm used to solve sudoku
#loop through each position in the table, pick
#a random valid number and recurse through the rest
#of the table given the selected number
def subSolve(curX, curY):

    #if curX == rows, then a valid number was found at at table[8,8]
    #and subSolve(9,0) was called
    if curX == rows:
        print('arrived')
        return True

    while curX < rows:
        while curY < cols:
            #check if current position is a read-only number
            if (curX, curY) not in readOnly:
                #get next coordinates
                nextX = curX if curY + 1 < cols else curX + 1
                nextY = curY + 1 if curY + 1 < cols else 0

                #grab all valid numbers and shuffle so numbers are picked pseudo-randomly
                nums = getValidNums(curX, curY)
                np.random.shuffle(nums)

                #loop through all valid numbers at this position
                for num in nums:
                    table[curX, curY] = num
                    print(table)
                    #time.sleep(0.150)  #used to help visualize progress of algorithm
                    if subSolve(nextX, nextY):  #recursive call
                        return True             #returns True if the selected number gave a solution
                    else:
                        table[curX, curY] = 0   #reset to 0 if selected number didn't give a valid solution

                #invalid position, aka no numbers are valid in this position
                if table[curX, curY] == 0:
                    return False

            #continue looping through positions
            curY = curY + 1
        #continue looping through positions
        curY = 0
        curX = curX + 1

    #the only way here is reached is if the last numbers are read-only numbers
    #in which case the loop will finish, and the only way that the last loop
    #finishes if the last numbers are read-only is that all the numbers used
    #to reach the last position are valid, otherwise the loop will return false
    #after discovering an invalid number/position
    return True


def solvePuzzle():
    #table in global scope lul
    if np.sum(table) == 0:
        print('Empty table given')
    else:
        t1 = time.time()
        result = subSolve(0,0)
        t2 = time.time()
        if result:
            print('success yeet')
            print(idVal)
        else:
            print('failure not yeet')
        print(t2 - t1)


if __name__ == '__main__':
    print('begin solving puzzle')
    solvePuzzle()
