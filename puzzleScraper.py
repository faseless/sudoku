"""
File: puzzleScraper.py
Author: Ethan Lan
Description: Scrapes a sudoku puzzle from a website.
Last Edit: 7/30/2019
Things to do: Improve style/readability, maybe find ways to improve time - but not necessary
"""
import bs4
import requests
import urllib.request
import time
from bs4 import BeautifulSoup as bs

#url = 'https://www.websudoku.com/?level=4'
url = 'https://nine.websudoku.com/?level=4'
#url = 'https://sudoku.com/expert/'

print(f'URL: {url}')


#use HTTP GET request to get HTML of url
print('Getting HTML of online puzzle')
htmlPreParse = requests.get(url)
print('Success')

time.sleep(1)


#parse HTML
print('Parsing HTML')
htmlParsed = bs(htmlPreParse.text, 'html.parser')
print('Success')

time.sleep(1)


#grab the overall table
print('Grabbing puzzle')
table = htmlParsed.findAll('table', {'id':'puzzle_grid'})
print('Success')

time.sleep(0.5)


#grab ID
pid = htmlParsed.find('input', {'id':'pid'})
idVal = pid['value']
print(f"ID: {idVal}")



#grab all the rows
rows = table[0].findAll('tr')

x = 9
y = 9
grid = [[0] * x for i in range(y)]
#create a 9x9 -1 filled array
gridLength = len(grid)

#orig = rows[0].findAll('td')[0]

#dic = rows[0].findAll('td')[0].input

#print(orig)    #looking at a box within a row

#print(dic)     #looking at the input section within a box

for i in range(0,gridLength):    #
    curRow = rows[i].findAll('td')
    for j in range(0,gridLength):
        curBox = curRow[j]
        if 'readonly' in curBox.input.attrs:
            grid[i][j] = ord(curBox.input['value'][0]) - ord('0')
            #assign grid position given value



print('Puzzle successfully retrieved')
print("Empty boxes are replaced with 0's")
for arr in grid:
    print(arr)
