from Map import Map
from Map import Bot
from UI import Canvas
from ReinforcementLearning.devsample import map_boltzmann_q_learning as qlearning
import tkinter as tk
import time

print("start")

updateperiod = 50

root = tk.Tk()
map = Map.Map()
map.parse("testmap.txt")
state_key = map.startTuple()
bot = Bot.Bot(state_key[0],state_key[1])
env = Canvas.Canvas(root, map, bot)
print("after init of own")
qlearning = qlearning.MapBoltzmannQLearning()
qlearning.initialize(map)
print("after init of qlearning")

env.redraw()
print("before sleep")
#time.sleep(updateperiod/1000)
print("after sleep")


alpha_value = 0.1

gamma_value = 0.1

greedy_rate = 0.1

qlearning.epsilon_greedy_rate = greedy_rate
qlearning.alpha_value = alpha_value
qlearning.gamma_value = gamma_value


def update():
    global state_key, waitperiod
    print("----update----")
    print("state_key: " + str(state_key))
    state_key = qlearning.onestep(state_key)
    bot.update(state_key[0], state_key[1])
    env.redraw()
    root.after(updateperiod, update)

update()
root.mainloop()
print("after mainloop")