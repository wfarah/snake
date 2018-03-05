#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 13:16:46 2018

@author: wfarah
"""

import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from snake.game import Snake,GameLostException,GameWonException
from snake.gui import gameGUI
from snake.game.utils import numToLetter,oneHotVector


GUI_SLEEP_TIME = 0.1


board_dim = 50

input_num_units = board_dim * board_dim
hidden_num_units = 100
num_actions = 4

actions = tf.placeholder(tf.int32, [None])
rewards = tf.placeholder(tf.float32, [None])
obs = tf.placeholder(tf.float32, [None, input_num_units])


epochs = 5
batch_size = 128
learning_rate = 0.01
decay = 0.99

seed = 128

Y = tf.layers.dense(obs,hidden_num_units, activation=tf.nn.relu)
Ylogits = tf.layers.dense(Y, num_actions)

sample_op = tf.multinomial(logits=tf.reshape(Ylogits, shape=(1, num_actions)), 
                           num_samples=1)



cross_entropies = tf.losses.softmax_cross_entropy(
        onehot_labels=tf.one_hot(actions,num_actions),
        logits=Ylogits)

optimiser = tf.train.RMSPropOptimizer(learning_rate, decay)

loss = tf.reduce_sum(rewards * cross_entropies)

snake = Snake(dimension=board_dim,start_size=10,survivalmode=True)
board = snake.returnBoard(trimmed=True).astype("float32")

gui = gameGUI()
gui.updateFrame(board)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(100):
        _obs = []
        _rewards = []
        _actions = []
        gameover = 0
        niter = 0
        snake.resetSnake()
        while not gameover or niter > 600:
            out = sess.run(sample_op, feed_dict = {obs: [board.flatten()]})[0][0]
            letter = numToLetter(out)
            vector = oneHotVector(letter)
            _actions.append(vector)
            try:
                snake.move(letter)
            except GameLostException:
                gameover = 1
                continue
            board = snake.returnBoard(trimmed = True).astype("float32")
            gui.updateFrame(board,GUI_SLEEP_TIME)
            niter += 1
            
        