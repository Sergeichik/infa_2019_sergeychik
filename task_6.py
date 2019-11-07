from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
root.geometry('1280x720')

c = tk.Canvas(root, bg='white')
c.pack(fill=tk.BOTH, expand=1)

colors = ['black', 'pink']


class Vector: 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, v):
        self.x += v.x
        self.y += v.y
        return self

    def __mul__(self, c):
        return Vector(self.x * c, self.y * c)

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def multiply(self, c):
        self.x = c * self.x
        self.y = c * self.y


class Ball:
    def __init__(self):
        self.pos = Vector(rnd(100, 1200), rnd(100, 600))
        self.vel = Vector(rnd(-10, 10), rnd(-10, 10))
        self.acc = Vector(0, 0)
        self.rf = Vector(0, 0)
        self.airres = Vector(0, 0)
        self.g = Vector(0, 0.5)
        self.r = 25
        self.t = 0
        self.obj = c.create_oval(self.pos.x - self.r, self.pos.y - self.r, self.pos.x + self.r,
                                 self.pos.y + self.r,
                                 fill=choice(colors), width=0)

    def move(self):
        self.vel += self.acc
        self.vel += self.rf
        self.vel += self.airres
        self.vel += self.g
        self.pos += self.vel
        c.move(self.obj, self.vel.x, self.vel.y)

    def reflection(self):
        if self.pos.x < self.r:
            self.acc.x = self.r - self.pos.x
        elif self.pos.x > 1280 - self.r:
            self.acc.x = 1280 - self.pos.x - self.r
        else:
            self.acc.x = 0
        if self.pos.y < self.r:
            self.acc.y = self.r - self.pos.y
        elif self.pos.y > 720 - self.r:
            self.acc.y = 720 - self.pos.y - self.r
        else:
            self.acc.y = 0

    def collision(self, ball): 
        if ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2) < (self.r + ball.r):
            r = self.r + ball.r - (((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2))
            sin = math.fabs((self.pos.x - ball.pos.x) / (
                    ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2)))
            cos = math.fabs((self.pos.y - ball.pos.y) / (
                    ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2)))
            if self.pos.x > ball.pos.x:
                self.rf.x = r * sin
                ball.rf.x = - r * sin
            else:
                self.rf.x = - r * sin
                ball.rf.x = r * sin
            if self.pos.y > ball.pos.y:
                self.rf.y = r * cos
                ball.rf.y = - r * cos
            else:
                self.rf.y = - r * cos
                ball.rf.y = r * cos

    def check(self, ball):
        if ((self.pos.x - ball.pos.x) ** 2 + (self.pos.y - ball.pos.y) ** 2) ** (1 / 2) < (self.r + ball.r):
            self.t += 1

    def zerorf(self):
        if self.t == 0:
            self.rf.x = 0
            self.rf.y = 0

    def airresistance(self, k): 
        if math.fabs(self.vel.x) > 5:
            self.airres.x = -1 * k * (self.vel.x) * math.fabs(self.vel.x)
        if math.fabs(self.vel.y) > 5:
            self.airres.y = -1 * k * (self.vel.y) * math.fabs(self.vel.y)



def rfdelete(list):
    for i in range(len(list)):
        for g in range(len(list)):
            if i != g:
                list[g].check(list[i])
    for k in range(len(list)):
        list[k].zerorf()


def cleart(list):
    for i in range(len(list)):
        list[i].t = 0


def mover(list):
    for i in range(len(list)):
        list[i].move()


def reflector(list):
    for i in range(len(list)):
        list[i].reflection()

def air(list, k):
    for i in range(len(list)):
        list[i].airresistance(k)


def collider(list):
    for i in range(len(list)):
        for g in range(len(list)):
            if i != g:
                list[g].collision(list[i])



ballpack = [Ball() for i in range(20)]


def update():  #Time function
    reflector(ballpack)
    air(ballpack, 0.0003)
    collider(ballpack)
    rfdelete(ballpack)
    mover(ballpack)
    cleart(ballpack)

    root.after(10, update)


update()
tk.mainloop()
