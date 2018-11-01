class Tile:
    #whether a bot can walk on this tile
    def isAccessible(self):
        return False

    def isStartPoint(self):
        return False

    def isEndPoint(self):
        return False

    def color(self):
        return "red"

    def getReward(self):
        return 0.0

    def __str__(self):
        return "E"

class EmptyTile(Tile):
    def isAccessible(self):
        return True

    def getColor(self):
        return "green"

    def __str__(self):
        return " "


class Wall(Tile):

    def getColor(self):
        return "black"

    def __str__(self):
        return "X"

class StartTile(EmptyTile):
    def isStartPoint(self):
        return True

    def __str__(self):
        return "S"

    def getColor(self):
        return "purple"


class EndTile(EmptyTile):
    def __init__(self, reward=10, color="yellow"):
        self.reward = reward
        self.color = color
        self.flag = True

    def isEndPoint(self):
        return True

    def getColor(self):
        return self.color

    def getReward(self):
        return self.reward

    def __str__(self):
        return "R"