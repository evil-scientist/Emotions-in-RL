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

    def reward(self):
        return 0.0

    def __str__(self):
        return "E"

class EmptyTile(Tile):
    def isAccessible(self):
        return True

    def color(self):
        return "green"

    def __str__(self):
        return " "


class Wall(Tile):

    def color(self):
        return "black"

    def __str__(self):
        return "X"

class StartTile(EmptyTile):
    def isStartPoint(self):
        return True

    def __str__(self):
        return "S"

    def color(self):
        return "purple"


class EndTile(EmptyTile):
    def isEndPoint(self):
        return True

    def color(self):
        return "yellow"

    def reward(self):
        return 100.0

    def __str__(self):
        return "R"