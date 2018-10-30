from Map import Tile

class Map:

    #Creates an empty 1x1 map
    def __init__(self):
        self.tiles = [[Tile.EmptyTile()]]

    def __str__(self):
        result = ""
        for row in self.tiles:
            result = result + "|"
            for tile in row:
                result = result + str(tile)
            result = result + "|\n"
        return result

    def parse(self, path):
        file = open(path, "r")
        lines = file.readlines()
        file.close()
        result = []
        lastlength = None
        for line in lines:
            currentrow = []
            for char in line:
                if char == "X":
                    currentrow.append(Tile.Wall())
                elif char == "O":
                    currentrow.append(Tile.EmptyTile())
                elif char == "R":
                    currentrow.append(Tile.EndTile())
                elif char == "S":
                    currentrow.append(Tile.StartTile())
                elif char == "\n":
                    pass
                else:
                    raise InvalidMapFileException("File: " + path + " contains an invalid character: " + char)
            if lastlength is not None:
                if lastlength != len(currentrow):
                    raise InvalidMapFileException("File: " + path + "has rows of unequal length")
            lastlength = len(currentrow)
            result.append(currentrow)
        self.tiles = result

    def width(self):
        return len(self.tiles[0])

    def height(self):
        return len(self.tiles)

    def tileAt(self, x, y):
        return self.tiles[y][x]

    def isTile(self, x, y):
        if y < len(self.tiles):
            if x < len(self.tiles[y]):
                return True

        return False

    def startTuple(self):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.isStartPoint():
                    return (x,y)
        raise InvalidMapFileException("Map does not have a starting point")

    def endTuple(self):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.isEndPoint():
                    return (x,y)
        raise InvalidMapFileException("Map does not have a starting point")

    def getPossibleActions(self, state):
        x, y = state
        if not self.tileAt(x,y).isAccessible():
            raise InvalidLocationException("Location: (" + x + "," + y + ") is not accessible")
        around_map = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        actions = []
        for point in around_map:
            if self.isTile(point[0], point[1]):
                if self.tileAt(point[0], point[1]).isAccessible():
                    actions.append(point)

        return actions


class InvalidMapFileException(Exception):
    pass

class InvalidLocationException(Exception):
    pass