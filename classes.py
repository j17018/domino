class Piece():
    def __init__(self,val1,val2):
        self.val = [val1,val2]

class GraphGameState:
    def __init__(self):
        self.levels = 0
    def addNode(self,Node):
        pass

class Node():
    def __init__(self,p1Pieces,p2Pieces,board,player,level,parent):
        self.p1Pieces = p1Pieces 
        self.p2Pieces = p2Pieces 
        self.board = board
        #the level is for printing
        self.level = level
        self.parent = None
        self.playerWhoDidTurn = player
