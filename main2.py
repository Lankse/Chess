from os import system as os

class Board :

    def __init__(self) :
        self.brd = []
        for i in range(0, 64) :
            self.brd.append("---")
        self.passant = "--"
        self.rmoved = [False, False, False, False]
        self.kmoved = [False, False]
        self.turn = "white"
        self.moves = 0
        self.m50 = 100

    def setBrd(self) :
        self.brd[0] = "r10"
        self.brd[1] = "n10"
        self.brd[2] = "b10"
        self.brd[3] = "q10"
        self.brd[4] = "k1"
        self.brd[5] = "b11"
        self.brd[6] = "n11"
        self.brd[7] = "r11"
        for i in range(0, 8) :
            self.brd[i+8] = "p1" + str(i)
        self.brd[56] = "r20"
        self.brd[57] = "n20"
        self.brd[58] = "b20"
        self.brd[59] = "q20"
        self.brd[60] = "k2"
        self.brd[61] = "b21"
        self.brd[62] = "n21"
        self.brd[63] = "r21"
        for i in range(0, 8) :
            self.brd[i+48] = "p2" + str(i)

    def dpBrd(self) :
        txt = ""
        for x in range(0, 8) :
            x = 7-x
            for y in range(0, 8) :
                pos = a.pos(x, y)
                txt += a.brd[pos]
                if a.brd[pos] == "k1" or a.brd[pos] == "k2" : txt += " "
                if not y == 7 : txt += "  "
            if not x == 0 : txt += "\n"
        return txt

    def save(self) :
        f = open("save.txt", "w")
        for c in self.brd :
            f.writelines(c)
        for i in self.rmoved :
            f.writelines(str(i))
        for i in self.kmoved :
            f.writelines(str(i))
        f.writeline(self.turn)
    def pos(self, x, y) :
        return x*8+y

    def pos2(self, nb) :
        return nb // 8, nb % 8

    def move(self, pos1, pos2, real=False) :
        pc = self.brd[pos1]
        self.brd[pos2] = self.brd[pos1]
        self.brd[pos1] = "---"
        if real == True :
            if pc[0] == "r" : self.rmoved[int(pc[1])-1 + int(pc[2])] = True
            if pc[0] == "k" : self.kmoved[int(pc[1])-1] = True
            if pc[0] == "k" and abs(pos2 - pos1) == 2 :
                if pos2 - pos1 == 2 :
                    self.move(pos1+3, pos1+1)  
                if pos2 - pos1 == -2 :
                    self.move(pos1-4, pos1-1)
            if pc[0] == "p" and pc[1] == "1" :
                if abs(pos2-pos1) == 16 : self.passant = self.passant[0] + str(self.pos2(pos1)[1])
                if self.pos2(pos2)[0] == 7 :
                    pces =  ["n", "b", "r", "q"]
                    chosen = False
                    while not chosen == True :
                        print("Promote your pawn : type n, b, r or q for knight, bishop, rook or queen.")
                        chosenPce = input()
                        if chosenPce in pces :
                            chosen = True
                        else :
                            print("Invalid input. Please try again")
                    a = 0
                    for c in self.brd :
                        if c[0] == chosenPce and c[1] == "1" : a += 1
                    self.brd[pos2] = chosenPce + "1" + str(a)
                if self.passant[0] == str(self.pos2(pos2)[1]) : self.brd[pos2-8] = "---"
            if pc[0] == "p" and pc[1] == "2" :
                if abs(pos2-pos1) == 16 : self.passant = str(self.pos2(pos1)[1]) + self.passant[1]
                if self.pos2(pos2)[0] == 0 :
                    pces =  ["n", "b", "r", "q"]
                    chosen = False
                    while not chosen == True :
                        print("Promote your pawn : type n, b, r or q for knight, bishop, rook or queen.")
                        chosenPce = input()
                        if chosenPce in pces :
                            chosen = True
                        else :
                            print("Invalid input. Please try again")
                    a = 0
                    for c in self.brd :
                        if c[0] == chosenPce and c[1] == "2" : a += 1
                    self.brd[pos2] = chosenPce + "2" + str(a)
                if self.passant[1] == str(self.pos2(pos2)[1]) : self.brd[pos2+8] = "---"

    def check(self, clr) :     
        k = False
        for c in self.brd :
            if c == "k" + str(clr) : k = True
        if k == False : return False
        for c in self.brd :
            if c[1] != str(clr) and c[1] != 0 and c[0] != "k" :
                for m in self.pmove(self.pos2(self.brd.index(c))[0], self.pos2(self.brd.index(c))[1]) :
                    if m == self.brd.index("k" + str(clr)) : return True
        return False
    
    def reachable(self, case, clr) :
        for c in self.brd :
            if c[1] != str(clr) and c[1] != 0 and c[0] != "k" :
                for m in self.pmove(self.pos2(self.brd.index(c))[0], self.pos2(self.brd.index(c))[1]) :
                    if m == case : return True
        return False

    def clear(self) :
        try :
            os("clear")
        except :
            try :
                os("cls")
            except :
                pass

    def mm50(self, pc, pos2) :
        end = False ; endCause = ""
        if pc[0] == "p" or not pos2 == "---" :
            self.m50 = 100
        else :
            self.m50 += -1
            if self.m50 == 0 : end = True ; endCause = "Draw by 50 moves rule"
        return end, endCause

    def pmove(self, x, y) :

        pos = self.pos(x, y)
        info = self.brd[self.pos(x, y)]
        pc = info[0]
        clr = info[1]
        mov = []

        if pc == "k" :
            if not x == 0 and not y == 0 : mov.append(pos-9)
            if not x == 0 and not y == 7 : mov.append(pos-7)
            if not x == 7 and not y == 0 : mov.append(pos+7)
            if not x == 7 and not y == 7 : mov.append(pos+9)
            if not x == 0 : mov.append(pos-8)
            if not x == 7 : mov.append(pos+8)
            if not y == 0 : mov.append(pos-1)
            if not y == 7 : mov.append(pos+1)
            if self.kmoved[int(clr)-1] == False and self.rmoved[int(clr)-1] == False and self.check(clr) == False :
                castle = True
                for i in range(self.brd.index("r"+clr+"0")+1, pos) :
                    if not self.brd[i] == "---" : castle = False
                    if self.reachable(i, clr) == True and not i == pos-3: castle = False
                if castle == True : mov.append(pos-2)
            if self.kmoved[int(clr)-1] == False and self.rmoved[int(clr)+1] == False and self.check(clr) == False :
                castle = True
                for i in range(pos+1, self.brd.index("r"+clr+"1")) :          
                    if not self.brd[i] == "---" or self.reachable(i, clr) == True : castle = False
                if castle == True : mov.append(pos+2)
            movtemp = mov.copy()
            for i in mov :
                if clr == self.brd[i][1] : movtemp.remove(i)
            mov = movtemp.copy()


        elif pc == "n":
            if not x < 2 and not y == 0 : mov.append(pos-17)
            if not x < 2 and not y == 7 : mov.append(pos-15)
            if not x == 0 and not y < 2 : mov.append(pos-10)
            if not x == 0 and not y > 5 : mov.append(pos-6)
            if not x == 7 and not y < 2 : mov.append(pos+6)
            if not x == 7 and not y > 5 : mov.append(pos+10)
            if not x > 5 and not y == 0 : mov.append(pos+15)
            if not x > 5 and not y == 7 : mov.append(pos+17)
            movtemp = mov.copy()
            for i in mov :
                if clr == self.brd[i][1] : movtemp.remove(i)
            mov = movtemp.copy()

        elif pc == "p" :
            if clr == "1" :
                if not x == 7 and not y == 7 and self.brd[pos+9][1] == "2" : mov.append(pos+9)
                if not x == 7 and not y == 0 and self.brd[pos+7][1] == "2" : mov.append(pos+7)
                if not x == 7 and self.brd[pos+8] == "---" : mov.append(pos+8)
                if x == 1 and self.brd[pos+16] == "---" and self.brd[pos+8] == "---" : mov.append(pos+16)
                if x == 4 and not y == 7 and self.passant[0] == str(y+1) : mov.append(pos+9)
                if x == 4 and not y == 0 and self.passant[0] == str(y-1) : mov.append(pos+7)
            elif clr == "2" :
                if not x == 0 and not y == 0 and self.brd[pos-9][1] == "1" : mov.append(pos-9)
                if not x == 0 and not y == 7 and self.brd[pos-7][1] == "1" : mov.append(pos-7)
                if not x == 0 and self.brd[pos-8] == "---" : mov.append(pos-8)
                if x == 6 and self.brd[pos-16] == "---" and self.brd[pos-8] == "---" : mov.append(pos-16)
                if x == 3 and not y == 7 and self.passant[1] == str(y+1) : mov.append(pos-7)
                if x == 3 and not y == 0 and self.passant[1] == str(y-1) : mov.append(pos-9)

        elif pc == "b" :
            i = 1
            stop = False
            while i <= min(x, y) and stop == False :
                if self.brd[pos-i*9] == "---" :
                    mov.append(pos-i*9)
                elif clr != self.brd[pos-i*9][1] :
                    mov.append(pos-i*9)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= min(x, 7-y) and stop == False :
                if self.brd[pos-i*7] == "---" :
                    mov.append(pos-i*7)
                elif clr != self.brd[pos-i*7][1] :
                    mov.append(pos-i*7)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= min(7-x, y) and stop == False :
                if self.brd[pos+i*7] == "---" :
                    mov.append(pos+i*7)
                elif clr != self.brd[pos+i*7][1] :
                    mov.append(pos+i*7)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= min(7-x, 7-y) and stop == False :
                if self.brd[pos+i*9] == "---" :
                    mov.append(pos+i*9)
                elif clr != self.brd[pos+i*9][1] :
                    mov.append(pos+i*9)
                    stop = True
                else :
                    stop = True
                i += 1

        elif pc == "r" :
            i = 1
            stop = False
            while i <= x and stop == False :
                if self.brd[pos-i*8] == "---" :
                    mov.append(pos-i*8)
                elif clr != self.brd[pos-i*8][1] :
                    mov.append(pos-i*8)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= y and stop == False :
                if self.brd[pos-i*1] == "---" :
                    mov.append(pos-i*1)
                elif clr != self.brd[pos-i*1][1] :
                    mov.append(pos-i*1)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= 7-y and stop == False :
                if self.brd[pos+i*1] == "---" :
                    mov.append(pos+i*1)
                elif clr != self.brd[pos+i*1][1] :
                    mov.append(pos+i*1)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= 7-x and stop == False :
                if self.brd[pos+i*8] == "---" :
                    mov.append(pos+i*8)
                elif clr != self.brd[pos+i*8][1] :
                    mov.append(pos+i*8)
                    stop = True
                else :
                    stop = True
                i += 1

        elif pc == "q" :
            i = 1
            stop = False
            while i <= min(x, y) and stop == False :
                if self.brd[pos-i*9] == "---" :
                    mov.append(pos-i*9)
                elif clr != self.brd[pos-i*9][1] :
                    mov.append(pos-i*9)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= min(x, 7-y) and stop == False :
                if self.brd[pos-i*7] == "---" :
                    mov.append(pos-i*7)
                elif clr != self.brd[pos-i*7][1] :
                    mov.append(pos-i*7)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= min(7-x, y) and stop == False :
                if self.brd[pos+i*7] == "---" :
                    mov.append(pos+i*7)
                elif clr != self.brd[pos+i*7][1] :
                    mov.append(pos+i*7)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= min(7-x, 7-y) and stop == False :
                if self.brd[pos+i*9] == "---" :
                    mov.append(pos+i*9)
                elif clr != self.brd[pos+i*9][1] :
                    mov.append(pos+i*9)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= x and stop == False :
                if self.brd[pos-i*8] == "---" :
                    mov.append(pos-i*8)
                elif clr != self.brd[pos-i*8][1] :
                    mov.append(pos-i*8)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= y and stop == False :
                if self.brd[pos-i*1] == "---" :
                    mov.append(pos-i*1)
                elif clr != self.brd[pos-i*1][1] :
                    mov.append(pos-i*1)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= 7-y and stop == False :
                if self.brd[pos+i*1] == "---" :
                    mov.append(pos+i*1)
                elif clr != self.brd[pos+i*1][1] :
                    mov.append(pos+i*1)
                    stop = True
                else :
                    stop = True
                i += 1
            i = 1
            stop = False
            while i <= 7-x and stop == False :
                if self.brd[pos+i*8] == "---" :
                    mov.append(pos+i*8)
                elif clr != self.brd[pos+i*8][1] :
                    mov.append(pos+i*8)
                    stop = True
                else :
                    stop = True
                i += 1
        mov.sort()
        return mov

    def pmove2(self, pos) :
        return self.pmove(self.pos2(pos)[0], self.pos2(pos)[1])
        
    def lmove(self, x, y) :
        pos = self.pos(x, y)
        a = self.brd[pos]
        clr = a[1]
        mov = self.pmove(x, y)
        save = self.brd.copy()
        movtemp = mov.copy()
        for m in mov :         
            self.move(pos, m)
            if self.check(clr) == True : movtemp.remove(m)
            self.brd = save.copy()
        return movtemp

    def lmove2(self, pos) :
        return self.lmove(self.pos2(pos)[0], self.pos2(pos)[1])

a = Board()

a.setBrd()

end = False
endCause = "Empty"
clear = True

while not end == True :

    a.turn = "white"
    if not end == True and a.turn == "white" :
        a.passant = a.passant[0] + "-"
        noMove = True
        for c in a.brd :
            if c[1] == "1" :
                if a.lmove2(a.brd.index(c)) != [] : noMove = False
        if noMove == True and a.check(1) == False : end = True ; endCause = "Stalemate"
        if a.lmove2(a.brd.index("k1")) == [] and a.check(1) == True : end = True ; endCause = "Black won by checkmate"
        if end == False :
            if clear == True : a.clear()
            print("----- WHITE'S TURN -----")
            a.turn = "white"
            pcs = []
            pcsTxt = []
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
            for c in a.brd :
                if c[1] == "1" :
                    pcs.append(c)
                    pcsTxt.append(letters[a.pos2(a.brd.index(c))[1]] + str(a.pos2(a.brd.index(c))[0]+1))
            chosenMain = False
            while not chosenMain == True :
                print(a.dpBrd())
                print("Here are the pieces you have ; choose the one you want to move by typing its coordonates.")
                print(pcsTxt)
                chosen = False
                while not chosen == True :
                    cPc = input()
                    if cPc in pcsTxt :
                        chosen = True
                        chosenPc = pcs[pcsTxt.index(cPc)]
                    elif cPc == "save" :
                        a.save()
                    elif cPc == "load" :
                        a.load()
                        chosen = True
                        chosenMain = True
                    else :
                        print("Invalid input. Please try again")
                    if list(a.lmove2(a.brd.index(chosenPc))) == [] :
                        print("This piece has no legal moves. Please choose another one.")
                        chosen = False
                legalMoves = list(a.lmove2(a.brd.index(chosenPc)))
                legalMovesTxt = []
                for m in legalMoves :
                    legalMovesTxt.append(letters[a.pos2(m)[1]] + str(a.pos2(m)[0] + 1))
                print("Here are the legals moves of this piece ; choose the one you want by typing its coordonates. Type \"back\" to go back to the choice of the piece.")
                printing = legalMovesTxt.copy()
                printing.sort()
                print(printing)
                chosen = False
                while not chosen == True :
                    cM = input()
                    if cM in legalMovesTxt :
                        chosen = True
                        chosenMain = True
                        chosenMove = legalMoves[legalMovesTxt.index(cM)]
                    elif cM == "back" :
                        chosen = True
                    else :
                        print("Invalid input. Please try again")
        #end, endCause = a.mm50(chosenPc, chosenMove)
        a.move(a.brd.index(chosenPc), chosenMove, True)
        a.moves += 1

    a.turn = "black"
    if end == False and a.turn == "black" :
        a.passant = "-" + a.passant[1]
        noMove = True
        for c in a.brd :
            if c[1] == "2" :
                if a.lmove2(a.brd.index(c)) != [] : noMove = False
        if noMove == True and a.check(2) == False : end = True ; endCause = "Stalemate"
        if a.lmove2(a.brd.index("k2")) == [] and a.check(2) == True : end = True ; endCause = "White won by checkmate"
        if end == False :
            if clear == True : a.clear()
            print("----- BLACK'S TURN -----")
            a.turn = "black"
            pcs = []
            pcsTxt = []
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
            for c in a.brd :
                if c[1] == "2" :
                    pcs.append(c)
                    pcsTxt.append(letters[a.pos2(a.brd.index(c))[1]] + str(a.pos2(a.brd.index(c))[0]+1))
            chosenMain = False
            while not chosenMain == True :
                print(a.dpBrd())
                print("Here are the pieces you have ; choose the one you want to move by typing its coordonates.")
                print(pcsTxt)
                chosen = False
                while not chosen == True :
                    cPc = input()
                    if cPc in pcsTxt :
                        chosen = True
                        chosenPc = pcs[pcsTxt.index(cPc)]
                    elif cPc == "save" :
                        a.save()
                    elif cPc == "load" :
                        a.load()
                    else :
                        print("Invalid input. Please try again")
                    if list(a.lmove2(a.brd.index(chosenPc))) == [] :
                        print("This piece has no legal moves. Please choose another one.")
                        chosen = False
                legalMoves = list(a.lmove2(a.brd.index(chosenPc)))
                legalMovesTxt = []
                for m in legalMoves :
                    legalMovesTxt.append(letters[a.pos2(m)[1]] + str(a.pos2(m)[0] + 1))
                print("Here are the legals moves of this piece ; choose the one you want by typing its coordonates. Type \"back\" to go back to the choice of the piece.")
                printing = legalMovesTxt.copy()
                printing.sort()
                print(printing)
                chosen = False
                while not chosen == True :
                    cM = input()
                    if cM in legalMovesTxt :
                        chosen = True
                        chosenMain = True
                        chosenMove = legalMoves[legalMovesTxt.index(cM)]
                    elif cM == "back" :
                        chosen = True
                    else :
                        print("Invalid input. Please try again")
        #end, endCause = a.mm50(chosenPc, chosenMove)
        a.move(a.brd.index(chosenPc), chosenMove, True)
        a.moves += 1

print(endCause)