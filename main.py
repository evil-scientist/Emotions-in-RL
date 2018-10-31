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
updateperiod = 750

STEP_COUNT = 0
CURRENT_COUNT = 0
EXP_LEARNING_COUNT = 10
TOTAL_STEPS = 400
TOTAL_REWARD = 0
FLAG_social = False
KEY_PRESSED = False

FIRST_UPDATE = True

def update():
    global TOTAL_STEPS, STEP_COUNT, CURRENT_COUNT, EXP_LEARNING_COUNT, TOTAL_REWARD, FIRST_UPDATE, root, KEY_PRESSED
    if(KEY_PRESSED):
        if(STEP_COUNT < TOTAL_STEPS):
            beta = 3 + min((CURRENT_COUNT/EXP_LEARNING_COUNT),1)*(6-3)
            finish_flg, reward = qlearning.onestep(beta) # Learning 1 episode
            TOTAL_REWARD = TOTAL_REWARD + reward
            towrite = str(STEP_COUNT) + ", " + str(CURRENT_COUNT) + ", " + str(beta) + ", " + str(TOTAL_REWARD) + "\n"
            log.write(towrite)
            STEP_COUNT = STEP_COUNT + 1

        if finish_flg:
            print("Completed one run: " + str(CURRENT_COUNT))
            CURRENT_COUNT = CURRENT_COUNT + 1
            qlearning.state = map.startTuple()

        bot.update(qlearning.state[0], qlearning.state[1])
        env.redraw()
        if(STEP_COUNT < TOTAL_STEPS):
            root.after(updateperiod, update)
        else:
            log.close()
    else:
        root.after(updateperiod, update)

if FLAG_social:
    flag = 'social'
else:
    flag = 'normal'

if(not os.path.isdir("./logs/"+flag)):
    os.mkdir("./logs/"+flag)
filename = "./logs/"+flag+"/log1.txt"
i = 1
while(os.path.isfile(filename)):
    i = i + 1
    filename =  "./logs/"+flag+"/log" + str(i) + ".txt"
log = open(filename, "w+")

def key(event):
    global KEY_PRESSED
    KEY_PRESSED = True

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Key>", key)
map = Map.Map()
map.parse("testmap.txt")
qlearning = qlearning.QLearning(map)
bot = Bot.Bot(qlearning.state[0],qlearning.state[1])
env = Canvas.Canvas(root, map, bot)
print("after init of own")
print("after init of qlearning")


#./opencv-webcam-demo/opencv-webcam-demo -d /opt/affdex-sdk/data
if FLAG_social:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        env.redraw()
        update(s)
else:
    env.redraw()
    update()
    root.mainloop()
