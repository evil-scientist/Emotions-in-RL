from Map import Map
from Map import Bot
from UI import Canvas
import tkinter as tk
import q_learning_grid as qlearning
import time
import socket
#from util import check_exit, encrypt, decrypt
import sys


HOST = '0.0.0.0'
PORT = 4000

print("start")

def update(data):
    global LEARNING_COUNT, CURRENT_COUNT
    if(CURRENT_COUNT < LEARNING_COUNT):
        #beta = 3 + (CURRENT_COUNT / 200) * (6 - 3)
        finish_flg = qlearning.onestep(data/50)  # Learning 1 episode

    if finish_flg:
        print("Completed one run: " + str(CURRENT_COUNT))
        CURRENT_COUNT = CURRENT_COUNT + 1
        qlearning.state = map.startTuple()

    bot.update(qlearning.state[0], qlearning.state[1])
    env.redraw()
    root.after(updateperiod, update)

updateperiod = 1000

root = tk.Tk()
map = Map.Map()
map.parse("testmap.txt")
qlearning = qlearning.QLearning(map)
bot = Bot.Bot(qlearning.state[0],qlearning.state[1])
env = Canvas.Canvas(root, map, bot)
print("after init of own")

print("after init of qlearning")

LEARNING_COUNT = 200
CURRENT_COUNT = 0

env.redraw()
print("before sleep")
#time.sleep(updateperiod/1000)
print("after sleep")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Socket Connected.")
    print("Enter # to disconnect....")
    while (1):
        print("Client:")
        #d = str.encode(input())
        # #s.sendall(d)#s.sendall(encrypt(d))
        #  check_exit(d)
        data = s.recv(1024)#data = decrypt(s.recv(1024))
        update(data)
        print("Server:", data)

		#check_exit(data)

#update()
root.mainloop()
print("after mainloop")
