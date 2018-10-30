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

def call_valence(s):
    data = s.recv(1024)#data = decrypt(s.recv(1024))
    try:
        print("Server:", int(float(str(data)[2:8])))
#./opencv-webcam-demo/opencv-webcam-demo -d /opt/affdex-sdk/data
        VALENCE = int(float(str(data)[2:8]))
        return VALENCE
    except:return 0

def update():
    global LEARNING_COUNT, CURRENT_COUNT, STEP_COUNT,VALENCE
    if(CURRENT_COUNT < LEARNING_COUNT):
        beta = 3 + (CURRENT_COUNT / LEARNING_COUNT) * (6 - 3)
        towrite = str(CURRENT_COUNT) + ", " + str(STEP_COUNT) + ", " + str(beta) + "\n"
        log.write(towrite)
        # Learning 1 episode
        #finish_flg = qlearning.onestep(call_valence(s))  # Learning 1 episode        
	#finish_flg = qlearning.onestep(data/50)  # Learning 1 episode
        STEP_COUNT = STEP_COUNT + 1

    if finish_flg:
        print("Completed one run: " + str(CURRENT_COUNT))
        CURRENT_COUNT = CURRENT_COUNT + 1
        STEP_COUNT = 0
        qlearning.state = map.startTuple()

    bot.update(qlearning.state[0], qlearning.state[1])
    env.redraw()
    if(CURRENT_COUNT < LEARNING_COUNT):
        root.after(updateperiod, update)
    else:
        log.close()

if(not os.path.isdir("./logs/")):
    os.mkdir("./logs/")
filename = "./logs/log1.txt"
i = 1
while(os.path.isfile(filename)):
    i = i + 1
    filename = "./logs/log" + str(i) + ".txt"
log = open(filename, "w+")


root = tk.Tk()
map = Map.Map()
map.parse("testmap.txt")
qlearning = qlearning.QLearning(map)
bot = Bot.Bot(qlearning.state[0],qlearning.state[1])
env = Canvas.Canvas(root, map, bot)
print("after init of own")
print("after init of qlearning")

#./opencv-webcam-demo/opencv-webcam-demo -d /opt/affdex-sdk/data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    
    s.connect((HOST, PORT))
    print("Socket Connected.")
    print("Enter # to disconnect....")

    print("start")

    



env.redraw()

update()


print("after mainloop")
