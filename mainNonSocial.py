from Map import Map
from Map import Bot
from UI import Canvas
import tkinter as tk
import q_learning_grid as ql
import os.path
import time
import struct
import socket
#from util import check_exit, encrypt, decrypt
import sys

from statistics import mean

sys.setrecursionlimit(10000)
HOST = '0.0.0.0'
PORT = 4000
updateperiod = 350


STEP_COUNT = 0
TOTAL_STEPS = 400
EXP_LEARNING_COUNT = 10
TOTAL_RUNS = 1000
CURRENT_RUN = 0
CURRENT_COUNT = 0

results = {}
for i in range(TOTAL_STEPS):
    results[i] = []

if(not os.path.isdir("./logs/")):
    os.mkdir("./logs/")
filename = "./logs/log_nonsocial1.txt"
i = 1
while(os.path.isfile(filename)):
    i = i + 1
    filename = "./logs/log_nonsocial" + str(i) + ".txt"
log = open(filename, "w+")

map = Map.Map()
map.parse("testmap.txt")
qlearning = ql.QLearning(map)
finish_flg = False
totalreward = 0
sugar_count = 0
food_count = 0
while(CURRENT_RUN < TOTAL_RUNS):
    while(STEP_COUNT < TOTAL_STEPS):
        
        beta = 3 + min((CURRENT_COUNT / EXP_LEARNING_COUNT),1) * (12-3)
        
        #beta = 0.1
        finish_flg, reward = qlearning.onestep(
            beta)  # Taking one step (one action for the bot)
        results[STEP_COUNT].append(totalreward)
        totalreward = totalreward + reward
        STEP_COUNT = STEP_COUNT + 1
        if(finish_flg):
            CURRENT_COUNT = CURRENT_COUNT + 1
            qlearning.state = map.startTuple()
            finish_flg = False
        endgoal = ""
        if (reward == 10):
            endgoal = "food"
            food_count = food_count + 1 
        elif (reward == 1):
            endgoal = "sugar"
            sugar_count = sugar_count + 1
        if endgoal != "":
            print("Run: " + str(CURRENT_RUN) + " Total Reward: " + str(totalreward)+" endgoal:"+endgoal + " beta: "+str(beta) + " Number of sugar: "+str(sugar_count) + " Number of food: "+str(food_count) )
    CURRENT_RUN = CURRENT_RUN + 1
    CURRENT_COUNT = 0
    STEP_COUNT = 0
    totalreward = 0
    qlearning = ql.QLearning(map)

for step in results.keys():
    towrite = (str(step) + str(", {0}") +  str("\n")).format(mean(results[step]))
    log.write(towrite)

log.close()

