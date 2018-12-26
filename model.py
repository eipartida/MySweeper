#This file contains the code necessary to generate the game board, including bomb placement and board size

import random

diff = {'Easy':(9,9,10,'300x400'), 'Medium': (16,16,40,'750x700'), 'Hard': (16,30, 99,'1350x700')}

def make_board(mode):
    return [[0 for i in range(diff[mode][1])] for i in range(diff[mode][0])]

def bomb_place(board, mode):
    row = random.randint(0, diff[mode][0]-1)
    col = random.randint(0, diff[mode][1]-1)
    if board[row][col] == 0:
        board[row][col] = 'O'
    else:
        bomb_place(board, mode)

def inbounds(row, col,board):
    return row < len(board) and row >= 0 and col < len(board[0]) and col >= 0 and type(board[row][col]) == int

def number_place(board):
                 
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'O':
                if inbounds(row, col-1,board):
                    board[row] [col-1] += 1
                if inbounds(row-1, col,board):
                    board[row-1] [col] += 1
                if inbounds(row-1, col-1,board):
                    board[row-1] [col-1] += 1
                if inbounds(row-1, col+1,board):
                    board[row-1] [col+1] += 1
                if inbounds(row+1, col-1,board):
                    board[row+1] [col-1] += 1
                if inbounds(row+1, col,board):
                    board[row+1] [col] += 1
                if inbounds(row, col+1,board):
                    board[row] [col+1] += 1
                if inbounds(row+1, col+1,board):
                    board[row+1] [col+1] += 1

def new_game(difficulty):
    game = make_board(difficulty)
    for i in range(diff[difficulty][2]):
        bomb_place(game, difficulty)
    number_place(game)
    return game
