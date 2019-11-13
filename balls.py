from tkinter import (Tk, Canvas, BOTH, NW, CENTER, mainloop)
from random import randrange as rnd, choice
root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

width = 800
height = 600
cont = True

colors = ['red', 'orange', 'black', 'green', 'blue']
score = 0


# Makes stationary balls, click makes them all disappear
# Click - +1 point
# No click - -1 point
# Missed click  - -2 points
# Additional feature - function create_ball makes the ball shrink a little bit with time
# Can be changed by changing the delta of r[j]
def new_ball():
    global x, y, r, cont, score, color_new, create_ball_cont, num
    if cont and overall_cont:
        for i in range(num):
            canv.delete('new_ball_' + str(i))

        def create_ball():
            global r, color_new, create_ball_cont
            if create_ball_cont is True:
                for j in range(num):
                    r[j] -= 0.1
                    canv.delete('new_ball_' + str(j))
                    canv.create_oval(x[j] - r[j], y[j] - r[j], x[j] + r[j], y[j] + r[j], fill=color_new[j], width=0,
                                     tag='new_ball_'+str(j))
                root.after(2, create_ball)
        score -= 1
        root.after(5, create_ball_cont_true)
        root.after(6, create_ball)
        root.after(500, new_ball)
        root.after(500, rnd_coord_new_ball)
        root.after(500, create_ball_cont_false)
    elif overall_cont:
        cont = True
    else:
        pass


def create_ball_cont_true():
    global create_ball_cont
    create_ball_cont = True


def create_ball_cont_false():
    global create_ball_cont
    create_ball_cont = False


# Randomizes coordinates for static balls
def rnd_coord_new_ball():
    global x, y, r, color_new, num
    x = []
    y = []
    r = []
    color_new = []
    for i in range(num):
        x.append(rnd(100, 700))
        y.append(rnd(100, 500))
        r.append(rnd(30, 50))
        color_new.append(choice(colors))


# Makes a score label, refreshing every 500 ms
def score_label():
    global score
    canv.delete('score')
    canv.create_text(100, 10, text=('SCORE:', score), anchor=NW, tag='score', justify=CENTER, font=('Arial 32', 20))
    canv.after(500, score_label)


# Randomizes coordinates for exotic balls
def exotic_ball_coord():
    global xe, ye, xr1, yr1, rie, roe, num_exotic
    xe = []
    ye = []
    xr1 = []
    yr1 = []
    rie = []
    roe = []
    for i in range(num_exotic):
        xe.append(rnd(200, 550))
        ye.append(rnd(250, 350))
        xr1.append(xe[i])
        yr1.append(ye[i])
        roe.append(rnd(50, 70))
        rie.append(rnd(5, 10))


# Randomizes directions of balls
def moving_ball_dir():
    global x_dir, y_dir, num_exotic
    x_dir = []
    y_dir = []
    for i in range(num_exotic):
        x_dir.append(rnd(19999)/10000)
        if x_dir[i] > 1:
            x_dir[i] = 1 - x_dir[i]
        y_dir.append(rnd(19999)/10000)
        if y_dir[i] > 1:
            y_dir[i] = 1 - y_dir[i]


# Randomizes individual directions of a ball
def moving_ball_dir_i(i):
    global x_dir, y_dir
    x_dir[i] = rnd(19999) / 10000
    if x_dir[i] > 1:
        x_dir[i] = 1 - x_dir[i]
    y_dir[i] = rnd(19999) / 10000
    if y_dir[i] > 1:
        y_dir[i] = 1 - y_dir[i]


# Randomizes directions of inside balls
def moving_ball_dir_1():
    global x_dir_1, y_dir_1, num_exotic
    x_dir_1 = []
    y_dir_1 = []
    for i in range(num_exotic):
        x_dir_1.append(rnd(19999)/10000)
        if x_dir_1[i] > 1:
            x_dir_1[i] = 1 - x_dir_1[i]
        y_dir_1.append(rnd(19999)/10000)
        if y_dir_1[i] > 1:
            y_dir_1[i] = 1 - y_dir_1[i]


# Randomizes directions of an individual inside ball
def moving_ball_dir_1_i(i):
    global x_dir_1, y_dir_1
    x_dir_1[i] = rnd(19999) / 10000
    if x_dir_1[i] > 1:
        x_dir_1[i] = 1 - x_dir_1[i]
    y_dir_1[i] = rnd(19999) / 10000
    if y_dir_1[i] > 1:
        y_dir_1[i] = 1 - y_dir_1[i]


# Inside part of exotic balls, move strangely and fast
def moving_ball_1():
    global xr1, yr1, x_dir_1, y_dir_1, xe, ye, roe, rie, exotic_ball_clickable, num_exotic
    if overall_cont:
        for i in range(num_exotic):
            if exotic_ball_cont[i]:
                xr1[i] += x_dir_1[i] * 4
                yr1[i] += y_dir_1[i] * 4
                if (xr1[i] - rie[i] < xe[i] - roe[i]) or (xr1[i] + rie[i] > xe[i] + roe[i]) or\
                        (yr1[i] - rie[i] < ye[i] - roe[i]) or (yr1[i] + rie[i] > ye[i] + roe[i]):
                    xr1[i] -= x_dir_1[i] * 4
                    yr1[i] -= y_dir_1[i] * 4
                    moving_ball_dir_1_i(i)
                if (xr1[i] - rie[i] < xe[i] - roe[i]) or (xr1[i] + rie[i] > xe[i] + roe[i]) or\
                        (yr1[i] - rie[i] < ye[i] - roe[i]) or (yr1[i] + rie[i] > ye[i] + roe[i]):
                    exotic_ball_clickable[i] = False
                else:
                    exotic_ball_clickable[i] = True
                canv.delete('m_ball1' + str(i))
                canv.create_rectangle(xr1[i] - rie[i], yr1[i] - rie[i], xr1[i] + rie[i], yr1[i] + rie[i], fill='white',
                                      width=0, tag='m_ball1' + str(i))
        canv.after(1, moving_ball_1)
    else:
        pass


# Exotic ball is a ball that spawns only once and consists of two parts
# Outside part is a ball that just moves (coords xe, ye, roe(as radius))
# Inside part is a square, moving fast inside the outside ball(coords xr1, xr2, rie(as radius))
# Click on all inside balls - +50 points
# After click it disappears forever
def exotic_ball():
    global xe, ye, roe, rie, num_exotic
    if overall_cont:
        for i in range(num_exotic):
            if exotic_ball_cont[i]:
                xe[i] += x_dir[i] * 4
                ye[i] += y_dir[i] * 4
                if (xe[i] - roe[i] < 0) or (xe[i] + roe[i] > width)or (ye[i] - roe[i] < 0) or (ye[i] + roe[i] > height):
                    xe[i] -= x_dir[i] * 8
                    ye[i] -= y_dir[i] * 8
                    moving_ball_dir_i(i)
                canv.delete('e_b_o' + str(i))
                canv.create_oval(xe[i] - roe[i], ye[i] - roe[i], xe[i] + roe[i], ye[i] + roe[i], fill='blue', width=0,
                                 tag='e_b_o' + str(i))
        root.after(10, exotic_ball)
    else:
        pass


def click(event):
    global score, cont, exotic_ball_cont, num
    if overall_cont:
        miss = False
        for i in range(num):
            if (abs(event.x - x[i]) < r[i]) and (abs(event.y - y[i]) < r[i]):
                score += 2
                canv.delete('new_ball_' + str(i))
                cont = False
                new_ball()
            else:
                miss = True
        if miss is True:
            score -= 2
        for i in range(num_exotic):
            if (abs(event.x - xr1[i]) < rie[i]) and (abs(event.y < yr1[i]) < rie[i]) and (exotic_ball_cont[i] is True) \
                    and (exotic_ball_clickable[i] is True):
                score += 52/num_exotic
                exotic_ball_cont[i] = False
                root.after(10, canv.delete('e_b_o' + str(i), 'm_ball1' + str(i)))
    else:
        pass


# imports a leaderboard from local file, adds current player with score after 60 seconds, sorts it
# only works if the game is finished, otherwise the score won`t be added
def leaderboard():
    global score, name
    d = {}
    file1 = 'text.txt'
    with open(file1) as file:
        for line in file:
            key, *value = line.split()
            d[key] = int(value[0])
    if not isinstance(d.get(name), int):
        d.update({name: score})
    elif score > d.get(name):
        d.update({name: score})
    my_file = open(file1, "w")
    d1 = sorted(d.items(), key=lambda item: (-item[1], item[0]))
    for i in range(len(d)):
        my_file.write(f"{d1[i][0]} {d1[i][1]}\n")
    my_file.close()


def deny():
    global overall_cont
    overall_cont = False


num = 10         # Number of ordinary balls
num_exotic = 10  # Number of exotic balls

overall_cont = True
exotic_ball_cont = []
for l in range(num_exotic):
    exotic_ball_cont.append(True)
exotic_ball_clickable = []
for k in range(num_exotic):
    exotic_ball_clickable.append(True)
create_ball_cont = True

print("Type your name:")
name = input()

score_label()
exotic_ball_coord()
moving_ball_dir()
moving_ball_dir_1()
rnd_coord_new_ball()
new_ball()
exotic_ball()
moving_ball_1()

root.after(60000, deny)

root.after(60500, leaderboard)


canv.bind('<Button-1>', click)
mainloop()
