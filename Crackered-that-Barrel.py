class XY:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Board:
    def __init__(self,zeroPosition):
        self.jumpHistory = []

        #Mapping of Peg Number X,Y Coordinate (for simplicity)
        self.mapping = []
        self.mapping.append(XY(2,2))
        self.mapping.append(XY(2,3))
        self.mapping.append(XY(3,3))
        self.mapping.append(XY(2,4))
        self.mapping.append(XY(3,4))
        self.mapping.append(XY(4,4))
        self.mapping.append(XY(2,5))
        self.mapping.append(XY(3,5))
        self.mapping.append(XY(4,5))
        self.mapping.append(XY(5,5))
        self.mapping.append(XY(2,6))
        self.mapping.append(XY(3,6))
        self.mapping.append(XY(4,6))
        self.mapping.append(XY(5,6))
        self.mapping.append(XY(6,6))
        self.counter = 0

        #Intiailizes Board with One Empty Peg
        self.setup()
        self.setPegToZero(zeroPosition)
    
    def setup(self):
        #Board Position Numbers (arbitrary)
        self.boardnumbers =[[-1,-1,-1,-1,-1,-1,-1,-1,-1],
                            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
                            [-1,-1, 0,-1,-1,-1,-1,-1,-1],
                            [-1,-1, 1, 2,-1,-1,-1,-1,-1],
                            [-1,-1, 3, 4, 5,-1,-1,-1,-1],
                            [-1,-1, 6, 7, 8, 9,-1,-1,-1],
                            [-1,-1,10,11,12,13,14,-1,-1],
                            [-1,-1,-1,-1,-1,-1,-1,-1,-1],
                            [-1,-1,-1,-1,-1,-1,-1,-1,-1]]

        #x for peg, 0 for empty
        self.boardpegs =[   [-1,-1, -1, -1, -1, -1, -1,-1,-1],
                            [-1,-1, -1, -1, -1, -1, -1,-1,-1],
                            [-1,-1,'x', -1, -1, -1, -1,-1,-1],
                            [-1,-1,'x','x', -1, -1, -1,-1,-1],
                            [-1,-1,'x','x','x', -1, -1,-1,-1],
                            [-1,-1,'x','x','x','x', -1,-1,-1],
                            [-1,-1,'x','x','x','x','x',-1,-1],
                            [-1,-1, -1, -1, -1, -1, -1,-1,-1],
                            [-1,-1, -1, -1, -1, -1, -1,-1,-1]]
        

    def setPegToZero(self,position):
        temp = self.mapping[position]
        self.boardpegs[temp.y][temp.x] = 0

    def getPegValue(self,x,y):
        return self.boardpegs[y][x]

    def getPegNumber(self,x,y):
        return self.boardnumbers[y][x]

    def setPegValue(self,x,y,val):
        self.boardpegs[y][x] = val

    def printBoard(self):
        b =  ["      ","     ","    ","  ","","",""]
        a = ["","","    ","   ","  "," ","","",""]
        i = 0
        for row in self.boardpegs:
            print a[i],
            for item in row:
                if item != -1:
                    print item,
            print
            i = i + 1

    def score(self):
        count = 0
        for row in self.boardpegs:
            for item in row:
                if (item == 'x'):
                    count = count +1
        return count

    def printHistory(self):
        i = 1
        for x in self.jumpHistory:
            print "Jump",
            print i,
            print "-",
            print "Move peg at position",
            print x[0],
            print "to position",
            print x[1]
            i = i + 1

        
    def jumpDirection(self,position,jumpDirection):
        ###Conventions
        ##1 = left
        ##2 = upleft
        ##3 = upright
        ##4 = right
        ##5 = downright
        ##6 = downleft
        temp = self.mapping[position]
        if (jumpDirection ==1):
            return self.jump(position, self.getPegNumber(temp.x-2,temp.y),1)
        if (jumpDirection ==2):
            return self.jump(position, self.getPegNumber(temp.x-2,temp.y-2),2)
        if (jumpDirection ==3):
            return self.jump(position, self.getPegNumber(temp.x,temp.y-2),3)
        if (jumpDirection ==4):
            return self.jump(position, self.getPegNumber(temp.x+2,temp.y),4)
        if (jumpDirection ==5):
            return self.jump(position, self.getPegNumber(temp.x+2,temp.y+2),5)
        if (jumpDirection ==6):
            return self.jump(position, self.getPegNumber(temp.x,temp.y+2),6)
        
        
        
    def jump(self,fromNumber,toNumber, direction):
        
        frompos = self.mapping[fromNumber]
        topos = self.mapping[toNumber]
        removed = self.getPegNumber((frompos.x + topos.x)/2,(frompos.y + topos.y)/2)
        removedValue = self.getPegValue((frompos.x + topos.x)/2,(frompos.y + topos.y)/2)
        if ((toNumber >= 0) and (self.getPegValue(frompos.x,frompos.y) == 'x') and (self.getPegValue(topos.x,topos.y) == 0) and removedValue == 'x'):
            self.counter = self.counter + 1
            #print "Jump Okay ",            
            self.setPegValue((frompos.x + topos.x)/2,(frompos.y + topos.y)/2,0)
            self.setPegValue(frompos.x,frompos.y,0)
            self.setPegValue(topos.x,topos.y,'x')
            a = (fromNumber,toNumber,removed,direction)
            self.jumpHistory.append(a)
            #print a
            return 1
        else:
            return 0
        
    def backtrack(self):
        lastJump = self.jumpHistory.pop()
        frompos = self.mapping[lastJump[0]]
        topos = self.mapping[lastJump[1]]
        removedpos = self.mapping[lastJump[2]]
        direction = lastJump[3]
        self.setPegValue(frompos.x,frompos.y, 'x')
        self.setPegValue(topos.x,topos.y, 0)
        self.setPegValue(removedpos.x, removedpos.y, 'x')
        #i,j
        return (lastJump[0],direction + 1)
        
class Game:
    #Start a game by removing the zeroPosition peg (starting with position 0)
    def __init__(self,zeroPosition):
        self.board = Board(zeroPosition)
        self.board.printBoard()

    def play(self):
        endofiteration = 0
        gameover = 0
        backtrackmode = 0
        
        while gameover == 0:
            jumped = 0
            if (backtrackmode == 0):
                i = 0  #if not backtrack mode
            while i <= 14:
                endofiteration = 0
                if (backtrackmode == 0):
                    j = 1 #if not backtrack mode
                backtrackmode = 0
                while j <= 6:
                    if self.board.jumpDirection(i,j) == 1:
                        jumped = 1
                        break
                    j = j + 1
                if jumped == 1:
                    break
                i = i + 1
                
            #Exhausted all jump combinations (either win or backtrack) 
            if (j == 7 and i == 15):
                if (self.board.score() > 1):
                    backtracktemp = self.board.backtrack()
                    i = backtracktemp[0]
                    j = backtracktemp[1]
                    backtrackmode = 1
                else:
                    gameover = 1
                    self.board.printHistory()
            else:
                pass
                
        
x = Game(7)
x.play()
x.board.printBoard()

