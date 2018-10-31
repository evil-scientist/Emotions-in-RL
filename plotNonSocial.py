import matplotlib.pyplot as plt

file = "./logs/log_nonsocial3.txt"


file = open(file)
steps = []
rewards = []
for line in file.readlines():
    values = line.split(",")
    steps.append(int(values[0]))
    rewards.append(float(values[1]))

plt.plot(steps, rewards)
plt.ylabel("Avg reward")
plt.xlabel("Step")
plt.show()