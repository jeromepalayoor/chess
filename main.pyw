import pygame
import random

pygame.init()

width = 640
height = 640

small = pygame.font.SysFont("comicsans", 16)

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Chess")

pieces = []

speed = 10

lb = pygame.image.load('pieces/lb.png')
db = pygame.image.load('pieces/db.png')
lq = pygame.image.load('pieces/lq.png')
dq = pygame.image.load('pieces/dq.png')
lk = pygame.image.load('pieces/lk.png')
dk = pygame.image.load('pieces/dk.png')
lp = pygame.image.load('pieces/lp.png')
dp = pygame.image.load('pieces/dp.png')
lr = pygame.image.load('pieces/lr.png')
dr = pygame.image.load('pieces/dr.png')
ln = pygame.image.load('pieces/ln.png')
dn = pygame.image.load('pieces/dn.png')

class Pawn():
    def __init__(self,x,y,c):
        self.x = x-1
        self.xcoor = self.x*80+10
        self.y = y-1
        self.ycoor = self.y*80+10
        self.c = c
        self.type = "p"
        self.to = [0,0]
        self.toxcoor = 0
        self.toycoor = 0
        self.toxcoorval = 0
        self.toycoorval = 0
        self.count = 0
        self.selected = False
        self.moved = False
        self.moving = False
        self.movable = []
        self.blocked = False
        self.dblocked = False
        self.lcap = False
        self.rcap = False
        self.id = random.randint(100000,999999)

    def update(self,win,pieces):
        self.blocked = False
        self.dblocked = False
        self.lcap = False
        self.rcap = False
        self.movable = []
        if self.c == "l":
            for piece in pieces:
                if piece.y == self.y - 1 and piece.x == self.x:
                    self.blocked = True
                if piece.y == self.y - 2 and piece.x == self.x:
                    self.dblocked = True
                if piece.x == self.x-1 and piece.y == self.y-1 and piece.c != self.c:
                    self.lcap = True
                if piece.x == self.x+1 and piece.y == self.y-1 and piece.c != self.c:
                    self.rcap = True
        else:
            for piece in pieces:
                if piece.y == self.y + 1 and piece.x == self.x:
                    self.blocked = True
                if piece.y == self.y + 2 and piece.x == self.x:
                    self.dblocked = True
                if piece.x == self.x+1 and piece.y == self.y+1 and piece.c != self.c:
                    self.lcap = True
                if piece.x == self.x-1 and piece.y == self.y+1 and piece.c != self.c:
                    self.rcap = True
        if self.c == "l":
            if not self.moved and not self.blocked and not self.dblocked:
                self.movable.append((self.x,self.y-1))
                self.movable.append((self.x,self.y-2))
            elif not self.blocked:
                self.movable.append((self.x,self.y-1))
            if self.lcap:
                self.movable.append((self.x-1,self.y-1))
            if self.rcap:
                self.movable.append((self.x+1,self.y-1))
        else:
            if not self.moved and not self.blocked and not self.dblocked:
                self.movable.append((self.x,self.y+1))
                self.movable.append((self.x,self.y+2))
            elif not self.blocked:
                self.movable.append((self.x,self.y+1))
            if self.lcap:
                self.movable.append((self.x+1,self.y+1))
            if self.rcap:
                self.movable.append((self.x-1,self.y+1))
        if self.c == "l":
            win.blit(lp, (self.xcoor,self.ycoor))
        else:
            win.blit(dp, (self.xcoor,self.ycoor))
        if self.selected:
            pygame.draw.rect(win, (255,0,0),(self.x*80,self.y*80,80,80),3)
        if not self.moved and self.selected and not self.blocked:
            if self.c == "l":
                pygame.draw.circle(win, (200,200,0), (self.x*80+40, (self.y-1)*80+40), 10)
                if not self.dblocked:
                    pygame.draw.circle(win, (200,200,0), (self.x*80+40, (self.y-2)*80+40), 10)
            else:
                pygame.draw.circle(win, (200,200,0), (self.x*80+40, (self.y+1)*80+40), 10)
                if not self.dblocked:
                    pygame.draw.circle(win, (200,200,0), (self.x*80+40, (self.y+2)*80+40), 10)
        elif self.selected and not self.blocked:
            if self.c == "l":
                pygame.draw.circle(win, (200,200,0), (self.x*80+40, (self.y-1)*80+40), 10)
            else:
                pygame.draw.circle(win, (200,200,0), (self.x*80+40, (self.y+1)*80+40), 10)
        if self.selected and self.lcap:
            if self.c == "l":
                pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y-1)*80+40), 35, 3)
            else:
                pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y+1)*80+40), 35, 3)
        if self.selected and self.rcap:
            if self.c == "l":
                pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y-1)*80+40), 35, 3)
            else:
                pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y+1)*80+40), 35, 3)

        if self.moving and self.count != speed:
            self.xcoor += self.toxcoorval
            self.ycoor += self.toycoorval
            self.count += 1
        elif self.count == speed:
            self.moving = False
            self.count = 0
            self.to = [0,0]
            self.toxcoor = 0
            self.toycoor = 0
            self.toxcoorval = 0
            self.toycoorval = 0
        else:                
            self.xcoor = self.x*80+10
            self.ycoor = self.y*80+10
            
    def move(self,to,pieces):
        for piece in pieces:
            if piece.x == to[0] and piece.y == to[1] and piece.id != self.id:
                pieces.remove(piece)
        self.moving = True
        self.to = to
        self.x = self.to[0]
        self.y = self.to[1]
        self.toxcoor = self.to[0]*80+10 - self.xcoor
        self.toxcoorval = self.toxcoor // speed
        self.toycoor = self.to[1]*80+10 - self.ycoor
        self.toycoorval = self.toycoor // speed
        self.moved = True





class Rook():
    def __init__(self,x,y,c):
        self.x = x-1
        self.xcoor = self.x*80+10
        self.y = y-1
        self.ycoor = self.y*80+10
        self.c = c
        self.type = "r"
        self.movable = []
        self.captures = []
        self.selected = False
        self.moving = False
        self.to = [0,0]
        self.toxcoor = 0
        self.toycoor = 0
        self.toxcoorval = 0
        self.toycoorval = 0
        self.count = 0
        self.t = 0
        self.r = 0
        self.b = 0
        self.l = 0
        self.tcap = 0
        self.rcap = 0
        self.bcap = 0
        self.lcap = 0
        self.tf = False
        self.rf = False
        self.bf = False
        self.lf = False
        self.id = random.randint(100000,999999)

    def update(self,win,pieces):
        self.movable = []
        self.captures = []
        self.t = 0
        self.r = 0
        self.b = 0
        self.l = 0
        self.tcap = 0
        self.rcap = 0
        self.bcap = 0
        self.lcap = 0
        self.tf = False
        self.rf = False
        self.bf = False
        self.lf = False
        
        for i in range(1,9):
            if not self.tf:
                if self.y - i == -1:
                    self.t = i
                    self.tf = True
                    break
                for piece in pieces:
                    if piece.y == self.y - i and self.x == piece.x:
                        self.t = i
                        if piece.c != self.c:
                            self.tcap = i
                        self.tf = True
                        break

        for i in range(1,9):
            if not self.rf:
                if self.x + i == 8:
                    self.r = i
                    self.rf = True
                    break
                for piece in pieces:
                    if piece.x == self.x + i and piece.y == self.y:
                        self.r = i
                        if piece.c != self.c:
                            self.rcap = i
                        self.rf = True
                        break

        for i in range(1,9):
            if not self.bf:
                if self.y + i == 8:
                    self.b = i
                    self.bf = True
                    break
                for piece in pieces:
                    if piece.y == self.y + i and self.x == piece.x:
                        self.b = i
                        if piece.c != self.c:
                            self.bcap = i
                        self.bf = True
                        break

        for i in range(1,9):
            if not self.lf:
                if self.x - i == -1:
                    self.l = i
                    self.lf = True
                    break
                for piece in pieces:
                    if piece.x == self.x - i and piece.y == self.y:
                        self.l = i
                        if piece.c != self.c:
                            self.lcap = i
                        self.lf = True
                        break
                    
        for i in range(1,self.t):
            self.movable.append((self.x, self.y - i))

        for i in range(1,self.r):
            self.movable.append((self.x + i, self.y))

        for i in range(1,self.b):
            self.movable.append((self.x, self.y + i))

        for i in range(1,self.l):
            self.movable.append((self.x - i, self.y))

        if self.tcap > 0:
            self.captures.append((self.x, self.y - self.tcap))
        if self.rcap > 0:
            self.captures.append((self.x + self.rcap, self.y))
        if self.bcap > 0:
            self.captures.append((self.x, self.y + self.bcap))
        if self.lcap > 0:
            self.captures.append((self.x - self.lcap, self.y))     

        
        if self.c == "l":
            win.blit(lr, (self.xcoor,self.ycoor))
        else:
            win.blit(dr, (self.xcoor,self.ycoor))

        if self.selected:
            pygame.draw.rect(win,(255,0,0),(self.x*80,self.y*80,80,80),3)
            for move in self.movable:
                pygame.draw.circle(win, (200,200,0), ((move[0])*80+40, (move[1])*80+40), 10)
            for capture in self.captures:
                pygame.draw.circle(win, (200,200,0), ((capture[0])*80+40, (capture[1])*80+40), 35, 3)

        if self.tcap > 0:
            self.movable.append((self.x, self.y - self.tcap))
        if self.rcap > 0:
            self.movable.append((self.x + self.rcap, self.y))
        if self.bcap > 0:
            self.movable.append((self.x, self.y + self.bcap))
        if self.lcap > 0:
            self.movable.append((self.x - self.lcap, self.y))  

        if self.moving and self.count != speed:
            self.xcoor += self.toxcoorval
            self.ycoor += self.toycoorval
            self.count += 1
        elif self.count == speed:
            self.moving = False
            self.count = 0
            self.to = [0,0]
            self.toxcoor = 0
            self.toycoor = 0
            self.toxcoorval = 0
            self.toycoorval = 0
        else:                
            self.xcoor = self.x*80+10
            self.ycoor = self.y*80+10
            
    def move(self,to,pieces):
        for piece in pieces:
            if piece.x == to[0] and piece.y == to[1] and piece.id != self.id:
                pieces.remove(piece)
        self.moving = True
        self.to = to
        self.x = self.to[0]
        self.y = self.to[1]
        self.toxcoor = self.to[0]*80+10 - self.xcoor
        self.toxcoorval = self.toxcoor // speed
        self.toycoor = self.to[1]*80+10 - self.ycoor
        self.toycoorval = self.toycoor // speed
        self.moved = True




class Bishop():
    def __init__(self,x,y,c):
        self.x = x-1
        self.xcoor = self.x*80+10
        self.y = y-1
        self.ycoor = self.y*80+10
        self.c = c
        self.type = "b"
        self.movable = []
        self.captures = []
        self.selected = False
        self.moving = False
        self.to = [0,0]
        self.toxcoor = 0
        self.toycoor = 0
        self.toxcoorval = 0
        self.toycoorval = 0
        self.count = 0
        self.tr = 0
        self.br = 0
        self.bl = 0
        self.tl = 0
        self.trcap = 0
        self.brcap = 0
        self.blcap = 0
        self.tlcap = 0
        self.trf = False
        self.brf = False
        self.blf = False
        self.tlf = False
        self.id = random.randint(100000,999999)

    def update(self,win,pieces):
        self.movable = []
        self.captures = []
        self.tr = 0
        self.br = 0
        self.bl = 0
        self.tl = 0
        self.trcap = 0
        self.brcap = 0
        self.blcap = 0
        self.tlcap = 0
        self.trf = False
        self.brf = False
        self.blf = False
        self.tlf = False
        
        for i in range(1,9):
            if not self.trf:
                if self.y - i == -1 or self.x + i == 8:
                    self.tr = i
                    self.trf = True
                    break
                for piece in pieces:
                    if piece.y == self.y - i and piece.x == self.x + i:
                        self.tr = i
                        if piece.c != self.c:
                            self.trcap = i
                        self.trf = True
                        break

        for i in range(1,9):
            if not self.brf:
                if self.x + i == 8 or self.y + i == 8:
                    self.br = i
                    self.brf = True
                    break
                for piece in pieces:
                    if piece.x == self.x + i and piece.y == self.y + i:
                        self.br = i
                        if piece.c != self.c:
                            self.brcap = i
                        self.brf = True
                        break

        for i in range(1,9):
            if not self.blf:
                if self.y + i == 8 or self.x - i == -1:
                    self.bl = i
                    self.blf = True
                    break
                for piece in pieces:
                    if piece.y == self.y + i and piece.x == self.x - i:
                        self.bl = i
                        if piece.c != self.c:
                            self.blcap = i
                        self.blf = True
                        break

        for i in range(1,9):
            if not self.tlf:
                if self.x - i == -1 or self.y - i == -1:
                    self.tl = i
                    self.tlf = True
                    break
                for piece in pieces:
                    if piece.x == self.x - i and piece.y == self.y - i:
                        self.tl = i
                        if piece.c != self.c:
                            self.tlcap = i
                        self.tlf = True
                        break
                    
        for i in range(1,self.tr):
            self.movable.append((self.x + i, self.y - i))

        for i in range(1,self.br):
            self.movable.append((self.x + i, self.y + i))

        for i in range(1,self.bl):
            self.movable.append((self.x - i, self.y + i))

        for i in range(1,self.tl):
            self.movable.append((self.x - i, self.y - i))

        if self.trcap > 0:
            self.captures.append((self.x + self.trcap, self.y - self.trcap))
        if self.brcap > 0:
            self.captures.append((self.x + self.brcap, self.y + self.brcap))
        if self.blcap > 0:
            self.captures.append((self.x - self.blcap, self.y + self.blcap))
        if self.tlcap > 0:
            self.captures.append((self.x - self.tlcap, self.y - self.tlcap))     

        
        if self.c == "l":
            win.blit(lb, (self.xcoor,self.ycoor))
        else:
            win.blit(db, (self.xcoor,self.ycoor))

        if self.selected:
            pygame.draw.rect(win,(255,0,0),(self.x*80,self.y*80,80,80),3)
            for move in self.movable:
                pygame.draw.circle(win, (200,200,0), ((move[0])*80+40, (move[1])*80+40), 10)
            for capture in self.captures:
                pygame.draw.circle(win, (200,200,0), ((capture[0])*80+40, (capture[1])*80+40), 35, 3)

        if self.trcap > 0:
            self.movable.append((self.x + self.trcap, self.y - self.trcap))
        if self.brcap > 0:
            self.movable.append((self.x + self.brcap, self.y + self.brcap))
        if self.blcap > 0:
            self.movable.append((self.x - self.blcap, self.y + self.blcap))
        if self.tlcap > 0:
            self.movable.append((self.x - self.tlcap, self.y - self.tlcap)) 

        if self.moving and self.count != speed:
            self.xcoor += self.toxcoorval
            self.ycoor += self.toycoorval
            self.count += 1
        elif self.count == speed:
            self.moving = False
            self.count = 0
            self.to = [0,0]
            self.toxcoor = 0
            self.toycoor = 0
            self.toxcoorval = 0
            self.toycoorval = 0
        else:                
            self.xcoor = self.x*80+10
            self.ycoor = self.y*80+10
            
    def move(self,to,pieces):
        for piece in pieces:
            if piece.x == to[0] and piece.y == to[1] and piece.id != self.id:
                pieces.remove(piece)
        self.moving = True
        self.to = to
        self.x = self.to[0]
        self.y = self.to[1]
        self.toxcoor = self.to[0]*80+10 - self.xcoor
        self.toxcoorval = self.toxcoor // speed
        self.toycoor = self.to[1]*80+10 - self.ycoor
        self.toycoorval = self.toycoor // speed
        self.moved = True



class Knight():
    def __init__(self,x,y,c):
        self.x = x-1
        self.xcoor = self.x*80+10
        self.y = y-1
        self.ycoor = self.y*80+10
        self.c = c
        self.type = "n"
        self.movable = []
        self.selected = False
        self.moving = False
        self.to = [0,0]
        self.toxcoor = 0
        self.toycoor = 0
        self.toxcoorval = 0
        self.toycoorval = 0
        self.count = 0
        self.tl = False
        self.tr = False
        self.rt = False
        self.rb = False
        self.bl = False
        self.br = False
        self.lb = False
        self.lt = False
        self.tlcap = False
        self.trcap = False
        self.rtcap = False
        self.rbcap = False
        self.blcap = False
        self.brcap = False
        self.lbcap = False
        self.ltcap = False
        self.id = random.randint(100000,999999)

    def update(self,win,pieces):
        self.movable = []
        self.tl = True
        self.tr = True
        self.rt = True
        self.rb = True
        self.bl = True
        self.br = True
        self.lb = True
        self.lt = True
        self.tlcap = False
        self.trcap = False
        self.rtcap = False
        self.rbcap = False
        self.blcap = False
        self.brcap = False
        self.lbcap = False
        self.ltcap = False
        for piece in pieces:
            if piece.x == self.x-1 and piece.y == self.y-2:
                self.tl = False
                if piece.c != self.c:
                     self.tlcap = True
            if piece.x == self.x+1 and piece.y == self.y-2:
                self.tr = False
                if piece.c != self.c:
                    self.trcap = True

                        
            if piece.x == self.x+2 and piece.y == self.y-1:
                self.rt = False
                if piece.c != self.c:
                    self.rtcap = True
            if piece.x == self.x+2 and piece.y == self.y+1:
                self.rb = False
                if piece.c != self.c:
                    self.rbcap = True

                        
            if piece.x == self.x+1 and piece.y == self.y+2:
                self.br = False
                if piece.c != self.c:
                    self.brcap = True
            if piece.x == self.x-1 and piece.y == self.y+2:
                self.bl = False
                if piece.c != self.c:
                    self.blcap = True

                        
            if piece.x == self.x-2 and piece.y == self.y+1:
                self.lb = False
                if piece.c != self.c:
                    self.lbcap = True
            if piece.x == self.x-2 and piece.y == self.y-1:
                self.lt = False
                if piece.c != self.c:
                    self.ltcap = True

        if self.tl:
            self.movable.append((self.x-1,self.y-2))
        if self.tr:
            self.movable.append((self.x+1,self.y-2))
        if self.rt:
            self.movable.append((self.x+2,self.y-1))
        if self.rb:
            self.movable.append((self.x+2,self.y+1))
        if self.br:
            self.movable.append((self.x+1,self.y+2))
        if self.bl:
            self.movable.append((self.x-1,self.y+2))
        if self.lb:
            self.movable.append((self.x-2,self.y+1))
        if self.lt:
            self.movable.append((self.x-2,self.y-1))

        if self.tlcap:
            self.movable.append((self.x-1,self.y-2))
        if self.trcap:
            self.movable.append((self.x+1,self.y-2))
        if self.rtcap:
            self.movable.append((self.x+2,self.y-1))
        if self.rbcap:
            self.movable.append((self.x+2,self.y+1))
        if self.brcap:
            self.movable.append((self.x+1,self.y+2))
        if self.blcap:
            self.movable.append((self.x-1,self.y+2))
        if self.lbcap:
            self.movable.append((self.x-2,self.y+1))
        if self.ltcap:
            self.movable.append((self.x-2,self.y-1))

                
        if self.c == "l":
            win.blit(ln, (self.xcoor,self.ycoor))
        else:
            win.blit(dn, (self.xcoor,self.ycoor))
        if self.selected:
            pygame.draw.rect(win,(255,0,0),(self.x*80,self.y*80,80,80),3)

        if self.tl and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y-2)*80+40), 10)
        if self.tr and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y-2)*80+40), 10)
        if self.rt and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+2)*80+40, (self.y-1)*80+40), 10)
        if self.rb and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+2)*80+40, (self.y+1)*80+40), 10)
        if self.br and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y+2)*80+40), 10)
        if self.bl and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y+2)*80+40), 10)
        if self.lb and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-2)*80+40, (self.y+1)*80+40), 10)
        if self.lt and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-2)*80+40, (self.y-1)*80+40), 10)


        if self.tlcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y-2)*80+40), 35, 3)
        if self.trcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y-2)*80+40), 35, 3)
        if self.rtcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+2)*80+40, (self.y-1)*80+40), 35, 3)
        if self.rbcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+2)*80+40, (self.y+1)*80+40), 35, 3)
        if self.brcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y+2)*80+40), 35, 3)
        if self.blcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y+2)*80+40), 35, 3)
        if self.lbcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-2)*80+40, (self.y+1)*80+40), 35, 3)
        if self.ltcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-2)*80+40, (self.y-1)*80+40), 35, 3)

        if self.moving and self.count != speed:
            self.xcoor += self.toxcoorval
            self.ycoor += self.toycoorval
            self.count += 1
        elif self.count == speed:
            self.moving = False
            self.count = 0
            self.to = [0,0]
            self.toxcoor = 0
            self.toycoor = 0
            self.toxcoorval = 0
            self.toycoorval = 0
        else:                
            self.xcoor = self.x*80+10
            self.ycoor = self.y*80+10
            
    def move(self,to,pieces):
        for piece in pieces:
            if piece.x == to[0] and piece.y == to[1] and piece.id != self.id:
                pieces.remove(piece)
        self.moving = True
        self.to = to
        self.x = self.to[0]
        self.y = self.to[1]
        self.toxcoor = self.to[0]*80+10 - self.xcoor
        self.toxcoorval = self.toxcoor // speed
        self.toycoor = self.to[1]*80+10 - self.ycoor
        self.toycoorval = self.toycoor // speed
        self.moved = True




class Queen():
    def __init__(self,x,y,c):
        self.x = x-1
        self.xcoor = self.x*80+10
        self.y = y-1
        self.ycoor = self.y*80+10
        self.c = c
        self.type = "q"
        self.movable = []
        self.captures = []
        self.selected = False
        self.moving = False
        self.to = [0,0]
        self.toxcoor = 0
        self.toycoor = 0
        self.toxcoorval = 0
        self.toycoorval = 0
        self.count = 0
        self.tr = 0
        self.br = 0
        self.bl = 0
        self.tl = 0
        self.trcap = 0
        self.brcap = 0
        self.blcap = 0
        self.tlcap = 0
        self.trf = False
        self.brf = False
        self.blf = False
        self.tlf = False
        self.t = 0
        self.r = 0
        self.b = 0
        self.l = 0
        self.tcap = 0
        self.rcap = 0
        self.bcap = 0
        self.lcap = 0
        self.tf = False
        self.rf = False
        self.bf = False
        self.lf = False
        self.id = random.randint(100000,999999)

    def update(self,win,pieces):
        self.movable = []
        self.captures = []
        self.tr = 0
        self.br = 0
        self.bl = 0
        self.tl = 0
        self.trcap = 0
        self.brcap = 0
        self.blcap = 0
        self.tlcap = 0
        self.trf = False
        self.brf = False
        self.blf = False
        self.tlf = False

        self.t = 0
        self.r = 0
        self.b = 0
        self.l = 0
        self.tcap = 0
        self.rcap = 0
        self.bcap = 0
        self.lcap = 0
        self.tf = False
        self.rf = False
        self.bf = False
        self.lf = False
        
        for i in range(1,9):
            if not self.tf:
                if self.y - i == -1:
                    self.t = i
                    self.tf = True
                    break
                for piece in pieces:
                    if piece.y == self.y - i and self.x == piece.x:
                        self.t = i
                        if piece.c != self.c:
                            self.tcap = i
                        self.tf = True
                        break

        for i in range(1,9):
            if not self.rf:
                if self.x + i == 8:
                    self.r = i
                    self.rf = True
                    break
                for piece in pieces:
                    if piece.x == self.x + i and piece.y == self.y:
                        self.r = i
                        if piece.c != self.c:
                            self.rcap = i
                        self.rf = True
                        break

        for i in range(1,9):
            if not self.bf:
                if self.y + i == 8:
                    self.b = i
                    self.bf = True
                    break
                for piece in pieces:
                    if piece.y == self.y + i and self.x == piece.x:
                        self.b = i
                        if piece.c != self.c:
                            self.bcap = i
                        self.bf = True
                        break

        for i in range(1,9):
            if not self.lf:
                if self.x - i == -1:
                    self.l = i
                    self.lf = True
                    break
                for piece in pieces:
                    if piece.x == self.x - i and piece.y == self.y:
                        self.l = i
                        if piece.c != self.c:
                            self.lcap = i
                        self.lf = True
                        break
                    
        for i in range(1,self.t):
            self.movable.append((self.x, self.y - i))

        for i in range(1,self.r):
            self.movable.append((self.x + i, self.y))

        for i in range(1,self.b):
            self.movable.append((self.x, self.y + i))

        for i in range(1,self.l):
            self.movable.append((self.x - i, self.y))

        if self.tcap > 0:
            self.captures.append((self.x, self.y - self.tcap))
        if self.rcap > 0:
            self.captures.append((self.x + self.rcap, self.y))
        if self.bcap > 0:
            self.captures.append((self.x, self.y + self.bcap))
        if self.lcap > 0:
            self.captures.append((self.x - self.lcap, self.y)) 
        
        for i in range(1,9):
            if not self.trf:
                if self.y - i == -1 or self.x + i == 8:
                    self.tr = i
                    self.trf = True
                    break
                for piece in pieces:
                    if piece.y == self.y - i and piece.x == self.x + i:
                        self.tr = i
                        if piece.c != self.c:
                            self.trcap = i
                        self.trf = True
                        break

        for i in range(1,9):
            if not self.brf:
                if self.x + i == 8 or self.y + i == 8:
                    self.br = i
                    self.brf = True
                    break
                for piece in pieces:
                    if piece.x == self.x + i and piece.y == self.y + i:
                        self.br = i
                        if piece.c != self.c:
                            self.brcap = i
                        self.brf = True
                        break

        for i in range(1,9):
            if not self.blf:
                if self.y + i == 8 or self.x - i == -1:
                    self.bl = i
                    self.blf = True
                    break
                for piece in pieces:
                    if piece.y == self.y + i and piece.x == self.x - i:
                        self.bl = i
                        if piece.c != self.c:
                            self.blcap = i
                        self.blf = True
                        break

        for i in range(1,9):
            if not self.tlf:
                if self.x - i == -1 or self.y - i == -1:
                    self.tl = i
                    self.tlf = True
                    break
                for piece in pieces:
                    if piece.x == self.x - i and piece.y == self.y - i:
                        self.tl = i
                        if piece.c != self.c:
                            self.tlcap = i
                        self.tlf = True
                        break
                    
        for i in range(1,self.tr):
            self.movable.append((self.x + i, self.y - i))

        for i in range(1,self.br):
            self.movable.append((self.x + i, self.y + i))

        for i in range(1,self.bl):
            self.movable.append((self.x - i, self.y + i))

        for i in range(1,self.tl):
            self.movable.append((self.x - i, self.y - i))

        if self.trcap > 0:
            self.captures.append((self.x + self.trcap, self.y - self.trcap))
        if self.brcap > 0:
            self.captures.append((self.x + self.brcap, self.y + self.brcap))
        if self.blcap > 0:
            self.captures.append((self.x - self.blcap, self.y + self.blcap))
        if self.tlcap > 0:
            self.captures.append((self.x - self.tlcap, self.y - self.tlcap))     

        
        if self.c == "l":
            win.blit(lq, (self.xcoor,self.ycoor))
        else:
            win.blit(dq, (self.xcoor,self.ycoor))

        if self.selected:
            pygame.draw.rect(win,(255,0,0),(self.x*80,self.y*80,80,80),3)
            for move in self.movable:
                pygame.draw.circle(win, (200,200,0), ((move[0])*80+40, (move[1])*80+40), 10)
            for capture in self.captures:
                pygame.draw.circle(win, (200,200,0), ((capture[0])*80+40, (capture[1])*80+40), 35, 3)

        if self.trcap > 0:
            self.movable.append((self.x + self.trcap, self.y - self.trcap))
        if self.brcap > 0:
            self.movable.append((self.x + self.brcap, self.y + self.brcap))
        if self.blcap > 0:
            self.movable.append((self.x - self.blcap, self.y + self.blcap))
        if self.tlcap > 0:
            self.movable.append((self.x - self.tlcap, self.y - self.tlcap))

        if self.tcap != 0:
            self.movable.append((self.x, self.y - self.tcap))
        if self.rcap != 0:
            self.movable.append((self.x + self.rcap, self.y))
        if self.bcap != 0:
            self.movable.append((self.x, self.y + self.bcap))
        if self.lcap != 0:
            self.movable.append((self.x - self.lcap, self.y))  

        if self.moving and self.count != speed:
            self.xcoor += self.toxcoorval
            self.ycoor += self.toycoorval
            self.count += 1
        elif self.count == speed:
            self.moving = False
            self.count = 0
            self.to = [0,0]
            self.toxcoor = 0
            self.toycoor = 0
            self.toxcoorval = 0
            self.toycoorval = 0
        else:                
            self.xcoor = self.x*80+10
            self.ycoor = self.y*80+10
            
    def move(self,to,pieces):
        for piece in pieces:
            if piece.x == to[0] and piece.y == to[1] and piece.id != self.id:
                pieces.remove(piece)
        self.moving = True
        self.to = to
        self.x = self.to[0]
        self.y = self.to[1]
        self.toxcoor = self.to[0]*80+10 - self.xcoor
        self.toxcoorval = self.toxcoor // speed
        self.toycoor = self.to[1]*80+10 - self.ycoor
        self.toycoorval = self.toycoor // speed
        self.moved = True

        




class King():
    def __init__(self,x,y,c):
        self.x = x-1
        self.xcoor = self.x*80+10
        self.y = y-1
        self.ycoor = self.y*80+10
        self.c = c
        self.type = "k"
        self.movable = []
        self.selected = False
        self.moving = False
        self.to = [0,0]
        self.toxcoor = 0
        self.toycoor = 0
        self.toxcoorval = 0
        self.toycoorval = 0
        self.count = 0
        self.t = False
        self.tr = False
        self.r = False
        self.rb = False
        self.b = False
        self.bl = False
        self.l = False
        self.lt = False
        self.tcap = False
        self.trcap = False
        self.rcap = False
        self.rbcap = False
        self.bcap = False
        self.blcap = False
        self.lcap = False
        self.ltcap = False
        self.id = random.randint(100000,999999)

    def update(self,win,pieces):
        self.movable = []
        self.t = True
        self.tr = True
        self.r = True
        self.rb = True
        self.b = True
        self.bl = True
        self.l = True
        self.lt = True
        self.tcap = False
        self.trcap = False
        self.rcap = False
        self.rbcap = False
        self.bcap = False
        self.blcap = False
        self.lcap = False
        self.ltcap = False
        for piece in pieces:
            if piece.x == self.x and piece.y == self.y-1:
                self.t = False
                if piece.c != self.c:
                     self.tcap = True
            if piece.x == self.x+1 and piece.y == self.y-1:
                self.tr = False
                if piece.c != self.c:
                    self.trcap = True
            if piece.x == self.x+1 and piece.y == self.y:
                self.r = False
                if piece.c != self.c:
                    self.rcap = True
            if piece.x == self.x+1 and piece.y == self.y+1:
                self.rb = False
                if piece.c != self.c:
                    self.rbcap = True
            if piece.x == self.x and piece.y == self.y+1:
                self.b = False
                if piece.c != self.c:
                    self.bcap = True
            if piece.x == self.x-1 and piece.y == self.y+1:
                self.bl = False
                if piece.c != self.c:
                    self.blcap = True
            if piece.x == self.x-1 and piece.y == self.y:
                self.l = False
                if piece.c != self.c:
                    self.lcap = True
            if piece.x == self.x-1 and piece.y == self.y-1:
                self.lt = False
                if piece.c != self.c:
                    self.ltcap = True

        if self.t or self.tcap:
            self.movable.append((self.x,self.y-1))
        if self.tr or self.trcap:
            self.movable.append((self.x+1,self.y-1))
        if self.r or self.rcap:
            self.movable.append((self.x+1,self.y))
        if self.rb or self.rbcap:
            self.movable.append((self.x+1,self.y+1))
        if self.b or self.bcap:
            self.movable.append((self.x,self.y+1))
        if self.bl or self.blcap:
            self.movable.append((self.x-1,self.y+1))
        if self.l or self.lcap:
            self.movable.append((self.x-1,self.y))
        if self.lt or self.ltcap:
            self.movable.append((self.x-1,self.y-1))
                
        if self.c == "l":
            win.blit(lk, (self.xcoor,self.ycoor))
        else:
            win.blit(dk, (self.xcoor,self.ycoor))
        if self.selected:
            pygame.draw.rect(win,(255,0,0),(self.x*80,self.y*80,80,80),3)

        if self.t and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x)*80+40, (self.y-1)*80+40), 10)
        if self.tr and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y-1)*80+40), 10)
        if self.r and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y)*80+40), 10)
        if self.rb and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y+1)*80+40), 10)
        if self.b and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x)*80+40, (self.y+1)*80+40), 10)
        if self.bl and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y+1)*80+40), 10)
        if self.l and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y)*80+40), 10)
        if self.lt and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y-1)*80+40), 10)



        if self.tcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x)*80+40, (self.y-1)*80+40), 35, 3)
        if self.trcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y-1)*80+40), 35, 3)
        if self.rcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y)*80+40), 35, 3)
        if self.rbcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x+1)*80+40, (self.y+1)*80+40), 35, 3)
        if self.bcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x)*80+40, (self.y+1)*80+40), 35, 3)
        if self.blcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y+1)*80+40), 35, 3)
        if self.lcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y)*80+40), 35, 3)
        if self.ltcap and self.selected:
            pygame.draw.circle(win, (200,200,0), ((self.x-1)*80+40, (self.y-1)*80+40), 35, 3)

        if self.moving and self.count != speed:
            self.xcoor += self.toxcoorval
            self.ycoor += self.toycoorval
            self.count += 1
        elif self.count == speed:
            self.moving = False
            self.count = 0
            self.to = [0,0]
            self.toxcoor = 0
            self.toycoor = 0
            self.toxcoorval = 0
            self.toycoorval = 0
        else:                
            self.xcoor = self.x*80+10
            self.ycoor = self.y*80+10
            
    def move(self,to,pieces):
        for piece in pieces:
            if piece.x == to[0] and piece.y == to[1] and piece.id != self.id:
                pieces.remove(piece)
        self.moving = True
        self.to = to
        self.x = self.to[0]
        self.y = self.to[1]
        self.toxcoor = self.to[0]*80+10 - self.xcoor
        self.toxcoorval = self.toxcoor // speed
        self.toycoor = self.to[1]*80+10 - self.ycoor
        self.toycoorval = self.toycoor // speed
        self.moved = True



def draw_text(win, text, x, y, color, size="s"):
    if size == "s":
        text = small.render(str(text), True, color)
        win.blit(text, (x,y))

def draw_board(win,color):
    if color == "l":
        for j in range(4):
            for i in range(4):
                pygame.draw.rect(win,(100,100,255),(i*160+80,j*160,80,80))
        for j in range(4):
            for i in range(4):
                pygame.draw.rect(win,(100,100,255),(i*160,j*160+80,80,80))
        for j in range(8):
            if j % 2 == 0:
                draw_text(win,8-j,3,j*80,(0,0,0))
            else:
                draw_text(win,8-j,3,j*80,(255,255,255))
        draw_text(win,"a",80-15,height-25,(255,255,255))
        draw_text(win,"b",80*2-15,height-25,(0,0,0))
        draw_text(win,"c",80*3-15,height-25,(255,255,255))
        draw_text(win,"d",80*4-15,height-25,(0,0,0))
        draw_text(win,"e",80*5-15,height-25,(255,255,255))
        draw_text(win,"f",80*6-15,height-25,(0,0,0))
        draw_text(win,"g",80*7-15,height-25,(255,255,255))
        draw_text(win,"h",80*8-15,height-25,(0,0,0))

def draw_win(win,pieces):
    win.fill((255,255,255))
    draw_board(win, "l")
    for piece in pieces:
        piece.update(win,pieces)

for i in range(8):
    pieces.append(Pawn(i+1,7,"l"))
    pieces.append(Pawn(i+1,2,"d"))
pieces.append(Queen(4,1,"d"))
pieces.append(Queen(4,8,"l"))
pieces.append(King(5,1,"d"))
pieces.append(King(5,8,"l"))
pieces.append(Rook(1,1,"d"))
pieces.append(Rook(1,8,"l"))
pieces.append(Rook(8,1,"d"))
pieces.append(Rook(8,8,"l"))
pieces.append(Knight(2,1,"d"))
pieces.append(Knight(2,8,"l"))
pieces.append(Knight(7,1,"d"))
pieces.append(Knight(7,8,"l"))
pieces.append(Bishop(3,1,"d"))
pieces.append(Bishop(3,8,"l"))
pieces.append(Bishop(6,1,"d"))
pieces.append(Bishop(6,8,"l"))

run = True
clock = pygame.time.Clock()
while run:
    clock.tick(40)
    draw_win(win,pieces)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            gridx = pos[0] // 80 
            gridy = pos[1] // 80 
            for piece in pieces:
                if piece.selected:
                    for move in piece.movable:
                        if gridx == move[0] and gridy == move[1]:
                            piece.move(move,pieces)
                    piece.selected = False
                elif pos[0] > piece.x*80-10 and pos[0] < piece.x*80+70 and pos[1] > piece.y*80-10 and pos[1] < piece.y*80+70:
                    piece.selected = True
    pygame.display.update()

pygame.quit()
quit()
