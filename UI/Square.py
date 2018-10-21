import tkinter as tk

class Square:
    #Map is map object from Map package
    def __init__(self, root, associatedtile, size=10):
        self.root = root
        self.layout = [[0]*10]*10
        self.tile = associatedtile
        for x in range(10):
            for y in range(10):
                self.layout[y][x] = tk.Label(root, text='  ', bg=self.tile.color())


