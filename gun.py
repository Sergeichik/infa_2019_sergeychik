from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):

        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Перемещение мяча"""
        self.xbound = 700
        self.ybound = 510
        if self. live <= 0:
            canv.delete(self.id)
        else:
            self.vy += 9.81/10
            self.x += self.vx
            self.y += self.vy
            self.set_coords()
        if self.x > self.xbound:
            self.x -= self.vx
            self.vx = -self.vx/2.5
        if self.y > self.ybound:
            self.y -= self.vy
            self.vy = -self.vy/2.5
            self.vx -= self.vx*0.15

    def hittest(self, obj):
        """Проверка столкновения. Возвращает True, если столкновение произошло"""
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) < (self.r + obj.r):
            canv.delete(obj.id)
            obj.live = 0
            return True
        else:
            return False


class gun():
    def idle(self, event):
        pass

    def fire2_set(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7, fill='black')

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet, launched
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10
        launched = True

    def targetting(self, event=0):
        """прицеливание"""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )
        canv.coords(self.id)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def error(self):
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()
        self.vx = 10 * self.points
        self.vy = 10 * self.points

    def set_points(self):
        self.points = 0

    def score_table(self):
        self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        canv.itemconfig(self.id_points, text=self.points)
        canv.coords(self.id_points)

    def new_target(self):
        x = self.x = rnd(400, 700)
        y = self.y = rnd(200, 500)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """поражение цели шариком"""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)

    def sub_hit(self, points=1):
        self.points += points

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        self.x1bound = 400
        self.x2bound = 700
        self.y1bound = 100
        self.y2bound = 400
        if self.live <= 0:
            canv.delete(self.id)
        else:
            self.x += self.vx
            self.y += self.vy
            self.set_coords()
        if self.x < self.x1bound or self.x > self.x2bound:
            self.x -= self.vx
            self.vx = -self.vx
            self.set_coords()
        if self.y < self.y1bound or self.y > self.y2bound:
            self.y -= self.vy
            self.vy = -self.vy
            self.set_coords()


t1 = target()
t2 = target()
t1.set_points()
t2.set_points()
t1.score_table()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, t1, screen1, balls, bullet, g1, b, t2
    canv.itemconfig(screen1, text='')
    t1.error()
    t2.error()
    t2.points = 0
    bullet = 0
    balls = []
    g1.fire2_set()
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    t1.live = 1
    t2.live = 1
    while t1.live or t2.live:
        for b in balls:
            b.move()
            t1.move()
            t2.move()
            b.hittest(t1)
            b.hittest(t2)
            if not t1.live and not t2.live:
                t1.live = 0
                t1.hit()
                t2.live = 0
                t2.sub_hit()
                canv.bind('<Button-1>', g1.idle)
                canv.bind('<ButtonRelease-1>', g1.idle)
                canv.bind('<Motion>', g1.targetting)
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.delete(g1.id)
    for i in balls:
        canv.delete(i.id)
    root.after(3000, new_game)


new_game()

canv.mainloop()
