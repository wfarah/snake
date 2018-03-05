#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 21:13:03 2018

@author: wfarah
"""

import numpy as np
from utils import mapLetterToPosition, getOppositeDir,numToLetter

EMPTY = 0
EDGES = -1
SNAKE_HEAD = 1
SNAKE_BODY = -1
APPLE = 2


class GameLostException(Exception):
    pass


class GameWonException(Exception):
    pass


class Snake(object):
    def __init__(self,dimension=50, start_size=5, start_position=None,
                 start_direction=None, godmode=False, survivalmode=False):
        # if start_direction not in ["u","d","l","r"]:
        #    raise ValueError("Start dir can only be 'u', 'd', 'l' or 'r'")
        self.dim = dimension
        self.start_size = start_size - 1  # without head
        if not start_position:
            start_position = int(self.dim/2.),int(self.dim/2.)
        self.position = tuple(start_position)
        # self.direction = start_direction
        
        self.godmode = godmode
        self.survivalmode = survivalmode
        
        self.resetSnake(start_direction)
    
    def resetSnake(self, start_direction=None):
        if not start_direction:
            self.direction = numToLetter(np.random.randint(4))
        else:
            self.direction = start_direction
                
        self._initialiseBoard()
        self._initialiseSnake()
        if not self.survivalmode:
            self._spawnApple()
        else:
            self.applePosition = None
        self._eatenCoords = []
        self.napples = 0
        self.iteration = 0
        
        
    def _initialiseBoard(self):
        self._emptyBoard = np.zeros((self.dim+2,self.dim+2)) + EMPTY
        self._emptyBoard[:,0] = EDGES
        self._emptyBoard[0] = EDGES
        self._emptyBoard[:,-1] = EDGES
        self._emptyBoard[-1] = EDGES
    
    def _initialiseSnake(self):
        self._snakeCoords = {}
        for i in range(self.start_size):
            self._snakeCoords[str(i)] = \
                mapLetterToPosition(self.position,
                                    getOppositeDir(self.direction),
                                    i+1)
    
            
    def returnBoard(self, trimmed=False):
        #Return a representation of the current board
        board = self._emptyBoard.copy()
        board[self.position] = SNAKE_HEAD
        for coord in self._snakeCoords.itervalues():
            board[coord] = SNAKE_BODY
        if not self.survivalmode:
            board[self.applePosition] = APPLE
        if trimmed:
            board = np.delete(board,[0,self.dim+1],0)
            board = np.delete(board,[0,self.dim+1],1)
        return board

    def move(self, move=None):
        if not move:
            pass
        elif move.lower() not in ["u","d","l","r"]:
            raise ValueError("Move can only be 'u', 'd', 'l' or 'r'")
        else:
            if move == getOppositeDir(self.direction):
                pass
            else:
                self.direction = move
        
        old_position = self.position  # For godmode
        old_snakeCoords = self._snakeCoords  # For godmode
        
        self._updatePosition()
        
        try:
            if self._hitEdge():
                raise GameLostException("Hit Edge. Gameover")
            elif self._hitBody():
                raise GameLostException("Hit Body. Gameover")
        except GameLostException as e:
            if self.godmode:
                self.position = old_position
                self._snakeCoords = old_snakeCoords
            else:
                raise e
             
        self.iteration += 1
        
        if not self.survivalmode:
            self._increaseSize()
            if self._hitApple():
                self.napples += 1
                if len(self._snakeCoords) == self.dim*self.dim - 1:
                    raise GameWonException("Game Won!")
                self._eatenCoords.append(self.position)
                self._spawnApple()
        
        
    def _updatePosition(self):
        # Update snake head/body on board after a move
        old_position = self.position
        self.position = mapLetterToPosition(self.position,
                                            self.direction)
        for i in range(len(self._snakeCoords))[::-1]:
            if i == 0:
                continue
            else:
                self._snakeCoords[str(i)] = self._snakeCoords[str(i-1)]
        self._snakeCoords[str(0)] = old_position
    
    def _increaseSize(self):
        # Check for previous eaten apple positions, and
        # increase size of snake
        last_chunk = len(self._snakeCoords) - 1
        for eatenCoord in self._eatenCoords:
            if self._snakeCoords[str(last_chunk)] == eatenCoord:
                self._snakeCoords[str(last_chunk+1)] = eatenCoord
                self._eatenCoords.remove(eatenCoord)

    
    def _hitEdge(self):
        # Return True if snake head hit edge
        if self.position[0] in [0,self.dim+1] or\
                self.position[1] in [0,self.dim+1]:
            return True
        return False
    
    def _hitBody(self):
        # Return True if snake head hit body
        for coord in self._snakeCoords.itervalues():
            if coord == self.position:
                return True
        return False
    
    
    def _hitApple(self):
        # Return True if snake ate apple
        if self.position == self.applePosition:
            return True
        return False
    
    def _spawnApple(self):
        # Spawn apple somewhere on board, except on snake's head/body
        flag = 0
        while not flag:
            tmp = np.random.randint(self.dim) + 1,\
            np.random.randint(self.dim) + 1
            if tmp in self._snakeCoords.values() or tmp == self.position:
                pass
            else:
                flag = 1
        
        self.applePosition = tmp

