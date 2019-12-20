import math

none = [None, 'a']

f = open('Entity_Dict.txt', 'r')
entity_list1 = f.read()
entity_list = eval(entity_list1)


def distance(x1, y1, x2, y2):
    a = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return a


def sign(x):
    if x >= 0:
        a = 1
    else:
        a = -1
    return a


def task_processing(canvas, entity, task_name, *args):
    if task_name is None:
        all_none = True
        try:
            for i in range(len(entity.task)):
                if not entity.task[i] is none:
                    shit = entity.task[i]
                    shiti = i
                    all_none = False
                    break
            if all_none is False:
                entity.task[0] = shit
                entity.task[shiti] = none
            else:
                q = len(entity.task)
                for i in range(q - 1):
                    entity.task.remove(entity.task[i + 1])

        except IndexError:
            pass

    elif task_name == 'move_by_DT':
        t = math.atan2(args[1] - entity.y, args[0] - entity.x)
        entity.task[0] = ['move_by', entity.v * math.cos(t), entity.v * math.sin(t)]

    elif task_name == 'move_by':  # args = x, y
        if args[0] == 0:
            t = 0
        else:
            t = args[1] / args[0]
        if args[1] ** 2 + args[0] ** 2 < (entity.v ** 2 * canvas.DT ** 2) / 1024:
            entity.x += args[0]
            entity.y += args[1]
            entity.vx = 0
            entity.vy = 0
            if len(entity.task) > 1:
                entity.task.remove(entity.task[0])
            else:
                entity.task[0] = none
        else:
            entity.vx = entity.v / math.sqrt(1 + t * t) * sign(args[0])
            entity.vy = entity.v / math.sqrt(1 + t * t) * abs(t) * sign(args[1])
            entity.task[0] = ['move_by', args[0] - entity.vx, args[1] - entity.vy]

    elif task_name == 'move_to':  # args = x, y
        entity.task[0] = ['move_by', args[0] - entity.x, args[1] - entity.y]

    elif task_name == 'attack':
        if distance(entity.x, entity.y, args[0].x, args[0].y) > entity.action_r:
            t = math.atan2(args[0].y - entity.y, args[0].x - entity.x)
            entity.task.insert(0, ['move_by', entity.v * math.cos(t), entity.v * math.sin(t)])
        else:
            if args[0].hp > 0:
                args[0].take_damage(entity)
                entity.vx = entity.vy = 0
            else:
                entity.task[0] = none
                entity.vx = entity.vy = 0

    elif task_name == 'follow':
        if distance(entity.x, entity.y, args[0].x, args[0].y) > entity.select_r + args[0].r + 1:
            entity.task.insert(0, ['move_to', args[0].x, args[0].y])
        else:
            entity.task.insert(0, args[0].tasks[0])

    elif task_name == 'build':  # args = type, x, y
        if distance(entity.x, entity.y, args[1], args[2]) > entity.action_r + entity_list[args[0]]['select_r']:
            t = math.atan2(args[2] - entity.y, args[1] - entity.x)
            entity.task.insert(0, ['move_by', entity.v * math.cos(t), entity.v * math.sin(t)])
        else:
            entity.canvas.building_place_3(args[0], args[1], args[2])
            entity.vx = 0
            entity.vy = 0
            entity.task[0] = none

    elif task_name == 'assemble':  # entity_to_create, task
        entity.canvas.assemble_2(args[0], entity)
        entity.task[0] = none

    elif task_name == 'mine':
        if distance(entity.x, entity.y, args[0].x, args[0].y) > entity.action_r:
            t = math.atan2(args[0].y - entity.y, args[0].x - entity.x)
            entity.task.insert(0, ['move_by', entity.v * math.cos(t), entity.v * math.sin(t)])
        else:
            if args[0].amount > 0:
                entity.mine(args[0])
                entity.vx = entity.vy = 0
            else:
                entity.task[0] = none
                entity.vx = entity.vy = 0


def task_sort(self, entity):
    if len(entity.task) > 1:
        while True:
            try:
                entity.task.remove(none)
            except ValueError:
                break
        while True:
            try:
                entity.task.remove(['move_by', 0.0, 0.0])
            except ValueError:
                break
    if len(entity.task) < 1:
        try:
            entity.task[0] = none
        except ValueError:
            pass
