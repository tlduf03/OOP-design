import enum

class GridPosition(enum.Enum):
    EMPTY = 0
    YELLOW = 1
    RED = 2
    
class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color

    def getName(self):
        return self._name
    
    def getColor(self):
        return self._color
    
class Grid:
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._grid = None
        self.initGrid()

    def initGrid(self):
        #create an empty grid
        self._grid = [[GridPosition.EMPTY for _ in range(self._columns)] for _ in range(self._rows)]
    
    def getGrid(self):
        return self._grid
    
    def getColumnCount(self):
        return self._columns
    
    def placePiece(self, column, color):
        #validation check
        if column < 0 or column > self._columns:
            raise ValueError("Invalid Column!")
        if color == GridPosition.EMPTY:
            raise ValueError("Invalid Piece!")

        #placing the piece
        for row in range(self._rows-1, -1, -1):
            if self._grid[row][column] == GridPosition.EMPTY:
                self._grid[row][column] = color
                return row

    def checkNconnected(self, connectedN, row, col, color):
        #check horizontal at the location
        count = 0
        for c in range(self._columns):
            if self._grid[row][c] == color:
                count+=1
            else:
                count = 0
            if count == connectedN:
                return True
        
        # check vertical
        count = 0
        for r in range(self._rows):
            if self._grid[r][col] == color:
                count += 1
            else:
                count = 0
            if count == connectedN:
                return True
        
        #check diagonal
        count = 0
        for r in range(self._rows):
            c = row + col - r
            if c >= 0 and c < self._columns and self._grid[r][c] == color:
                count += 1
            else:
                count = 0
            if count == connectedN:
                return True
             
        #check anti-diagonal
        count = 0
        for r in range(self._rows):
            c = col - row + r
            if c >= 0 and c < self._columns and self._grid[r][c] == color:
                count += 1
            else:
                count = 0
            if count == connectedN:
                return True

        return False