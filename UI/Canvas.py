import tkinter as tk

class Canvas:
    def __init__(self, root, map, bot, squaresize=100, botsize=20):
        self.map = map
        self.bot = bot
        self.botsize = botsize
        self.squaresize = squaresize
        self.canvas = tk.Canvas(root, width=map.width()*squaresize, height=map.height()*squaresize)
        self.canvas.pack()
        for x in range(self.map.width()):
            for y in range(self.map.height()):
                xcanvas = x*squaresize
                ycanvas = y*squaresize
                color = map.tileAt(x,y).color()
                self.canvas.create_rectangle(xcanvas, ycanvas, xcanvas + squaresize, ycanvas + squaresize, fill = color, outline=color)

        xcanvasbot = bot.x*squaresize + (squaresize - botsize)/2
        ycanvasbot = bot.y*squaresize + (squaresize - botsize)/2
        self.botrectangle = self.canvas.create_rectangle(xcanvasbot, ycanvasbot, xcanvasbot + botsize, ycanvasbot + botsize, fill="white", outline="white")

    def redraw(self):
        xcanvasbot = self.bot.x*self.squaresize + (self.squaresize - self.botsize)/2
        ycanvasbot = self.bot.y*self.squaresize +  (self.squaresize - self.botsize)/2
        self.canvas.coords(self.botrectangle, xcanvasbot, ycanvasbot, xcanvasbot + self.botsize, ycanvasbot + self.botsize)
