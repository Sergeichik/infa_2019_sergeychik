from graph import windowSize, canvasSize, polygon, brushColor, rectangle, penColor, circle, line, run

windowSize(1000, 600)
canvasSize(1000, 600)



def ellipse(a, b, x0, y0):
    x = a
    y = 0
    s = [(x0 + a, y0)]
    for i in range(2 * a):
        x -= 1
        y = ((1 - x ** 2 / (a ** 2)) * b ** 2) ** 0.5
        s.append((x + x0, y + y0))
    for i in range(2 * a):
        x += 1
        y = -(((1 - x ** 2 / (a ** 2)) * b ** 2) ** 0.5)
        s.append((x + x0, y + y0))
    polygon(s)


def man(a, b):
    penColor(133, 133, 133)
    brushColor(133, 133, 133)
    ellipse(50, 95, a, b + 120)
    penColor(229, 194, 152)
    brushColor(229, 194, 152)
    circle(a, b, 45)
    penColor(0, 0, 0)
# отрисовывает руки : первая строка - правую, а вторая строка - левую;
    line(a + 40, b + 60, a + 80, b + 140)
    line(a - 40, b + 60, a - 90, b + 140)

# отрисовывает ноги : первые две строки - правую, а вторые две строки - левую;
    line(a + 25, b + 200, a + 45, b + 330)
    line(a + 45, b + 330, a + 65, b + 330)
    line(a - 25, b + 200, a - 65, b + 330)
    line(a - 65, b + 330, a - 100, b + 330)

def woman(a, b):
    penColor(233, 99, 233)
    brushColor(233, 99, 233)
    polygon([(a, b + 30), (a + 75, b + 220), (a - 75, b + 220), (a, b + 30)])
    penColor(229, 194, 152)
    brushColor(229, 194, 152)
    circle(a, b, 45)
    penColor(0, 0, 0)
# отрисовывает ноги : первые две строки - правую, а вторые две строки - левую;
    line(a + 20, b + 220, a + 20, b + 330)
    line(a + 20, b + 330, a + 40, b + 330)
    line(a - 20, b + 220, a - 20, b + 330)
    line(a - 20, b + 330, a - 40, b + 330)
# отрисовывает руки : первая строка - правую, а вторая строка - левую;
    line(a + 12, b + 60, a + 50, b + 100)
    line(a + 50, b + 100, a + 120, b + 65)
    line(a - 12, b + 60, a - 82, b + 140)
def mirror ()
man(200,100)
woman(360,100)



run()