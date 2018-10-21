from Map import Map
from Map import Bot
from UI import Canvas
import tkinter as tk
import q_learning_grid as qlearning
import time

print("start")

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



def update():
    global LEARNING_COUNT, CURRENT_COUNT
    if(CURRENT_COUNT < LEARNING_COUNT):
        beta = 3 + (CURRENT_COUNT / 200) * (6 - 3)
        finish_flg = qlearning.onestep(beta)  # Learning 1 episode

    if finish_flg:
        print("Completed one run: " + str(CURRENT_COUNT))
        CURRENT_COUNT = CURRENT_COUNT + 1
        qlearning.state = map.startTuple()

    bot.update(qlearning.state[0], qlearning.state[1])
    env.redraw()
    root.after(updateperiod, update)

update()
root.mainloop()
print("after mainloop")