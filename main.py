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

def update(data):
    global LEARNING_COUNT, CURRENT_COUNT, STEP_COUNT
    if(CURRENT_COUNT < LEARNING_COUNT):
        beta = 3 + (CURRENT_COUNT / LEARNING_COUNT) * (6 - 3)
        towrite = str(CURRENT_COUNT) + ", " + str(STEP_COUNT) + ", " + str(beta) + "\n"
        log.write(towrite)
        d = data
        print(type(data))
        #finish_flg = qlearning.onestep(struct.unpack(">L", data)[0]))  # Learning 1 episode
        finish_flg = qlearning.onestep(int(float(str(data)[2:8]))/10)  # Learning 1 episode        
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



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    root = tk.Tk()
    map = Map.Map()
    map.parse("testmap.txt")
    qlearning = qlearning.QLearning(map)
    bot = Bot.Bot(qlearning.state[0],qlearning.state[1])
    env = Canvas.Canvas(root, map, bot)
    print("after init of own")

    print("after init of qlearning")

    env.redraw()
    print("before sleep")
        #time.sleep(updateperiod/1000)
    print("after sleep")
    s.connect((HOST, PORT))
    print("Socket Connected.")
    print("Enter # to disconnect....")
    while (1):
#        print("Client:")
        #d = str.encode(input())
        # #s.sendall(d)#s.sendall(encrypt(d))
#        #  check_exit(d)
        data = s.recv(1024)#data = decrypt(s.recv(1024))
        try:
            print("Server:", int(float(str(data)[2:8])))
#./opencv-webcam-demo/opencv-webcam-demo -d /opt/affdex-sdk/data
            update(data)
        except:continue
        


		#check_exit(data)

update()
root.mainloop()
print("after mainloop")
