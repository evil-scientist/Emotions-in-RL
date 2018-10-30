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


LEARNING_COUNT = 15
CURRENT_COUNT = 0
STEP_COUNT = 0
CURRENT_RUN = 0 #current run for the averages
TOTAL_RUNS = 1000 #total number of runs to take the average over

results = {}
for i in range(LEARNING_COUNT):
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

while(CURRENT_RUN < TOTAL_RUNS):
    while(CURRENT_COUNT < LEARNING_COUNT):
        while(not finish_flg):

            beta = 3 + (CURRENT_COUNT / LEARNING_COUNT) * (6 - 3)
            finish_flg = qlearning.onestep(
                beta)  # Taking one step (one action for the bot)
            STEP_COUNT = STEP_COUNT + 1

        results[CURRENT_COUNT].append(STEP_COUNT)
        CURRENT_COUNT = CURRENT_COUNT + 1
        temp_count = STEP_COUNT
        STEP_COUNT = 0
        qlearning.state = map.startTuple()
        finish_flg = False

    print("Run: " + str(CURRENT_RUN) + "Iterartion: " + str(
        CURRENT_COUNT) + " STEP: " + str(temp_count))
    CURRENT_COUNT = 0
    CURRENT_RUN = CURRENT_RUN + 1
    qlearning = ql.QLearning(map)

for count in results.keys():
    towrite = (str(count) + str(", {0}") +  str("\n")).format(mean(results[count]))
    log.write(towrite)

log.close()

