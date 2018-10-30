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
    except:return 3

def update(s):
    global LEARNING_COUNT, CURRENT_COUNT, STEP_COUNT,VALENCE
    if(CURRENT_COUNT < LEARNING_COUNT):
        beta = call_valence(s)
        towrite = str(CURRENT_COUNT) + ", " + str(STEP_COUNT) + ", " + str(beta) + "\n"
        log.write(towrite)
<<<<<<< HEAD
        #finish_flg = qlearning.onestep(call_valence(s))  # Learning 1 episode        
        finish_flg = qlearning.onestep(beta) # Learning 1 episode        
=======
        d = data
        #print(type(data))
        #finish_flg = qlearning.onestep(struct.unpack(">L", data)[0]))  # Taking one step (one action for the bot)
        finish_flg = qlearning.onestep(int(float(str(data)[2:8]))/10)  # Taking one step (one action for the bot)
	    #finish_flg = qlearning.onestep(data/50)
>>>>>>> 4e153b1fa74013b6da6fa15f871abf10fa3a6c15
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
    
    s.connect((HOST, PORT))
    env.redraw()
    update(s)
    root.mainloop()
 
