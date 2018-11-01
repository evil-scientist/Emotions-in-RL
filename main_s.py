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
from scipy.interpolate import interp1d


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

global FLAG_12_3 

def call_valence(s):

    data = s.recv(1024)#data = decrypt(s.recv(1024))
    try:
        data = float(str(data)[2:8])
        print(data)
        if abs(data) >50:
            if data>0:
                data = 50
            else:
                data = -50
#+ valence --> higher beta -- > exploitation 
        a = interp1d([-50,50],[12,3])
#       FLAG_12_3 = True
#+ valence --> lower beta -- > exploration 
        #a = interp1d([-50,50],[3,12])
#       FLAG_12_3 = False

        value = float(a(data))
        print("beta:", value)
#./opencv-webcam-demo/opencv-webcam-demo -d /opt/affdex-sdk/data
        VALENCE = value
        return VALENCE
    except:
        print('Couldnt convert')
        return 4.5
'''
    a = interp1d([-100,100],[3,6])
    try:
        value = float(a(float(str(data)[2:8])))
        print("beta:", value)
#./opencv-webcam-demo/opencv-webcam-demo -d /opt/affdex-sdk/data
        VALENCE = value
        return VALENCE
    except:
        return 3
'''


def update():
    global TOTAL_STEPS, STEP_COUNT, CURRENT_COUNT, EXP_LEARNING_COUNT, TOTAL_REWARD, KEY_PRESSED
    if KEY_PRESSED:
        if(STEP_COUNT < TOTAL_STEPS):
            VALENCE = call_valence(s)
            beta = VALENCE
            finish_flg, reward = qlearning.onestep(beta) # Learning 1 episode
            endgoal = ""
            if (reward == 10):
                endgoal = "food"
            elif (reward == 1):
                endgoal = "sugar"
            TOTAL_REWARD = TOTAL_REWARD + reward
            towrite = str(STEP_COUNT) + ", " + str(CURRENT_COUNT) + ", " + str(beta) + ", " + str(TOTAL_REWARD) + endgoal+"\n"
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

FLAG_12_3 = True

if(not os.path.isdir("./logs/social/")):
    os.mkdir("./logs/social/")
# CASE 1
#+ valence --> higher beta -- > exploitation 
#       a = interp1d([-50,50],[12,3])
if FLAG_12_3:
    filename = "./logs/social/"+"/social_12-3_log1.txt"
    i = 1
    while(os.path.isfile(filename)):
        i = i + 1
        filename =  "./logs/social"+"/social_12-3_log" + str(i) + ".txt"
    log = open(filename, "w+")
# CASE 2
#+ valence --> lower beta -- > exploration 
#       a = interp1d([-50,50],[3,12])
else:
    filename = "./logs/social/"+"/social_3-12_log1.txt"
    i = 1
    while(os.path.isfile(filename)):
        i = i + 1
        filename =  "./logs/social"+"/social_3-12_log" + str(i) + ".txt"
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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
env.redraw()
update()
root.mainloop()

