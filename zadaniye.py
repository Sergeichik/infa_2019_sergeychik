from math import sin, cos


def primenum(a):
    l = []
    l.append(2)
    n = 0
    q = True
    for i in range(a):
        for k in range(n):
            if (i + 3) % l[k] == 0:
                q = False
       	if q =True:
            l.append(i + 3)
            n = n + 1     
        else:
            q = True         
    print(l)
    return(l)


def sort(m):
    q = 0
    for i in range (len(m)):
        for k in range(len(m) - i):
            if m[i + k] < m[q]:
                q = k + i
        m[i],m[q] = m[q],m[i]
        q = i + 1
    print(m)

    
def rotate(square, angle):
    sqnew = [[0, 0], [0, 0],  [0, 0],  [0, 0]]
    for i in range(4): 
        sqnew[i][0] = (square[i][0] - ((square[0][0] + square[2][0])/2))*cos(angle) - (square[i][1] - ((square[0][1] + square[2][1])/2))*sin(angle)
        sqnew[i][1] = (square[i][0] - ((square[0][0] + square[2][0])/2))*sin(angle) + (square[i][1] - ((square[0][1] + square[2][1])/2))*cos(angle)
        sqnew[i] = tuple(sqnew[i])
    print(sqnew)


def affordable_goods(good, prise):
    a = []
    for key in good:
        if good[key] < prise:
            a.append(key)
    print(a)


def unique(a):
    set1 = set(a)
    print(list(set1))


def difference(a1, a2):
    q = True
    a3 = []
    for i in a1:
        for j in a2:
            if i == j:
                q = False
        if q:
            a3.append(i)
        else:
            q = True
    print(list(set(a3)))

primenum(1000)
sort([2, 7, 16, 1, 21])
rotate(((1 , 1), (1, -1), (-1, -1), (-1, 1)), 0)
affordable_goods({'banana': 11, 'apple': 5, 'fish': 40}, 30)
unique([1, 1, 2, 6, 5, 11, 3, 3, 2, 2, 2])
difference([1, 2, 3, 4], [4, 5, 6])
