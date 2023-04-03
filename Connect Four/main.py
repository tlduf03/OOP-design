from setup import *

class Game():
    def __init__(self, grid, connectN, targetScore):
        self._grid = grid
        self._connectN = connectN
        self._targetScore = targetScore

        self._players = [
            Player('Player 1', GridPosition.YELLOW),
            Player('Player 2', GridPosition.RED)
        ]
        
        self._score = {}
        for player in self._players:
            self._score[player.getName()] = 0

    def printBoard(self):
        print('Board:\n')
        grid = self._grid.getGrid()
        for i in range(len(grid)):
            row = ''
            for piece in grid[i]:
                if piece == GridPosition.EMPTY:
                    row += '0 '
                elif piece == GridPosition.YELLOW:
                    row += 'Y '
                elif piece == GridPosition.RED:
                    row += 'R '
            print(row)
        print('')

    def playMove(self,player):
        self.printBoard()
        print(f"{player.getName()}'s turn")
        colCnt = self._grid.getColumnCount()
        moveColumn = int(input(f"Enter column between {0} and {colCnt - 1} to add piece : "))
        moveRow = self._grid.placePiece(moveColumn, player.getColor())
        return (moveRow, moveColumn)

    def playRound(self):
        while True:
            for player in self._players:
                row, col = self.playMove(player)
                color = player.getColor()
                if self._grid.checkNconnected(self._connectN, row, col, color):
                    self._score[player.getName()] += 1
                    return player


    def play(self):
        maxScore = 0
        winner = None
        while maxScore < self._targetScore:
            winner = self.playRound()
            print(f"{winner.getName()} won the Round!")
            maxScore = max(self._score[winner.getName()], maxScore)
            
            #Display current score
            print(f"< Max Score : {maxScore} >")
            print("< Current Score >")
            for player in self._players:
                print(f"{player.getName()} : {self._score[player.getName()]}")
            print("")
            self._grid.initGrid() #reset the grid
        print(f"{winner.getName()} won the Game!")


grid = Grid(6,7) #6rows, 7cols
game = Game(grid,4,2) #4 connected, 2 target score
game.play()

