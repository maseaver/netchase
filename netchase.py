import random

class State(object):
    def __init__(self, strategy, opponent):
        self.opponent = opponent
        self.strategy = strategy
        self.score = 0
        self.pX = 7
        self.pY = 7
        self.eX = 0
        self.eY = 0

    def run(self):
        while self.pX != self.eX or self.pY != self.eY:
            self.drawBoard()
            self.eX, self.eY = bound(self.strategy(self.pX, self.pY,
                                                   self.eX, self.eY))
            self.drawOptions()
            self.pX, self.pY = bound(player(self.pX, self.pY,
                                            raw_input(">")))
            self.score = self.score + 1
        self.drawBoard()
        print "You lost. Final score: {}\n".format(self.score)

    def board(self):
        rows = []
        for row in range(8):
            cells = []
            for col in range(8):
                if row == self.pY and col == self.pX:
                    if row == self.eY and col == self.eX:
                        cells.append("O")
                    else:
                        cells.append("@")
                elif row == self.eY and col == self.eX:
                    cells.append(self.opponent)
                else:
                    cells.append("X")
            rows.append(cells)

        return rows
                  
    def drawBoard(self):
        print "OV V V V V V V VO"

        for line in self.board():
            print ">" + " ".join(line) + "<"

        print "OA A A A A A A AO\nScore: {}\n".format(self.score)

    def drawOptions(self):
        if self.pX == self.eX and self.pY == self.eY:
            print ">You lose."
        else:
            if self.pY != 0:
                print ">W for Up"
            if self.pX != 0:
                print ">A for Left"
            if self.pY != 7:
                print ">S for Down"
            if self.pX != 7:
                print ">D for Right"

def nearer_horizontal(pX, pY, eX, eY):
    if pX == eX:
        if pY > eY:
            return (eX, eY + 1)
        else:
            return (eX, eY - 1)
    elif pX > eX:
        return (eX + 1, eY)
    else:
        return (eX - 1, eY)

def nearer_vertical(pX, pY, eX, eY):
    if pY == eY:
        if pX > eX:
            return (eX + 1, eY)
        else:
            return (eX - 1, eY)
    elif pY > eY:
        return (eX, eY + 1)
    else:
        return (eX, eY - 1)

def nearer_random(pX, pY, eX, eY):
    choice = random.choice([nearer_horizontal, nearer_vertical])
    return choice(pX, pY, eX, eY)

def erratic(pX, pY, eX, eY):
    return random.choice([(eX + 1, eY),
                         (eX - 1, eY),
                         (eX, eY + 1),
                         (eX, eY - 1),
                         (eX, eY),
                          ])

def player(pX, pY, move):
    if move == "w" or move == "W":
        return (pX, pY - 1)
    if move == "a" or move == "A":
        return (pX - 1, pY)
    if move == "s" or move == "S":
        return (pX, pY + 1)
    if move == "d" or move == "D":
        return (pX + 1, pY)
    else:
        return (pX, pY)

def bound(xy):
    x, y = xy
    if x > 7:
        x = 7
    if x < 0:
        x = 0
    if y > 7:
        y = 7
    if y < 0:
        y = 0
    return (x, y)

def start():
    rogues = {"!" : (nearer_horizontal, "Chases you sideways"),
              "~" : (nearer_vertical, "Chases you up and down"),
              "^" : (nearer_random, "A cleverer opponent"),
              "?" : (erratic, "Totally unpredictable"), }
    print "Welcome to N E T C H A S E . \n Select an opponent."
    for (key, rogue) in rogues.items():
        print key + ": " + rogue[1]

    selection = raw_input(">Type the character: ")
    while selection not in rogues:
        selection = raw_input(""">Type one of the ASCII characters to the left
of the colon: """)
    return rogues[selection][0], selection

if __name__ == "__main__":
    play = True
    
    while play:
        strategy, opponent = start()
        state = State(strategy, opponent)
        state.run()
        restart = raw_input(">Restart? Y/N: ")
        if restart != "y" and restart != "Y":
            play = False
            
