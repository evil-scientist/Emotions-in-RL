from Map import Map
from Map import Bot
from UI import Canvas
import tkinter as tk
import q_learning_grid as qlearning
import os.path
import time
import struct
import socket
#from util import check_exit, encrypt, decrypt
import sys


HOST = '0.0.0.0'
PORT = 4000
updateperiod = 350


LEARNING_COUNT = 50
CURRENT_COUNT = 0
STEP_COUNT = 0
if(not os.path.isdir("./logs/")):
    os.mkdir("./logs/")
filename = "./logs/log1.txt"
i = 1
while(os.path.isfile(filename)):
    i = i + 1
    filename = "./logs/log" + str(i) + ".txt"
log = open(filename, "w+")

print("start")

def update():
    global LEARNING_COUNT, CURRENT_COUNT, STEP_COUNT
    if(CURRENT_COUNT < LEARNING_COUNT):
        beta = 3 + (CURRENT_COUNT / LEARNING_COUNT) * (6 - 3)
        towrite = str(CURRENT_COUNT) + ", " + str(STEP_COUNT) + ", " + str(beta) + "\n"
        log.write(towrite)
        finish_flg = qlearning.onestep(beta)  # Taking one step (one action for the bot)
        STEP_COUNT = STEP_COUNT + 1

    if finish_flg: #in this case we reached the goal in the last step, so go back to start
        print("Completed one run: " + str(CURRENT_COUNT))
        CURRENT_COUNT = CURRENT_COUNT + 1
        STEP_COUNT = 0
        qlearning.state = map.startTuple()

    bot.update(qlearning.state[0], qlearning.state[1]) #update the position of the bot on the UI
    env.redraw() #redraw the UI with the new state
    if(CURRENT_COUNT < LEARNING_COUNT):
        root.after(updateperiod, update) #after updateperiod take another step and update the uid again
    else:
        log.close()


root = tk.Tk()
map = Map.Map()
map.parse("testmap.txt")
qlearning = qlearning.QLearning(map)
bot = Bot.Bot(qlearning.state[0],qlearning.state[1])
env = Canvas.Canvas(root, map, bot)

env.redraw()

update()
root.mainloop()
print("after mainloop")
