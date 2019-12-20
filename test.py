
import math

import tkinter as tk
from Task_Processing import distance, task_processing, task_sort

from random import vonmisesvariate as rndangle

DT = 30
scale = 0.5
none = [None, 'a']
f = open('Entity_Dict.txt', 'r')
entity_list1 = f.read()
entity_list = eval(entity_list1)
X0 = 1920
Y0 = 1080
X = X0
Y = Y0
DX = 0
DY = 0
VX = 10 * scale
VY = 10 * scale
BX = 1500
BY = 900


class Entity():
    def __init__(self, canvas, param_dict, fraction, task, x, y):
        self.canvas = canvas
        self.max_hp = param_dict['hp'] * 100
        self.hp = self.max_hp
        self.dmg = param_dict['dmg']
        self.v = param_dict['velocity'] * 3 * canvas.scale
        self.select_r = param_dict['select_r'] * 50 * canvas.scale
        self.action_r = param_dict['action_r'] * 100 * canvas.scale
        self.type = param_dict['type']
        self.subtype = param_dict['subtype']
        self.wood_cost = param_dict['wood_cost']
        self.gold_cost = param_dict['gold_cost']
        self.fraction = fraction
        self.task = task
        self.unit_task = [none]
        self.r = self.select_r
        self.x = (x + DX) * canvas.scale
        self.y = (y + DY) * canvas.scale
        self.vx = 0
        self.vy = 0
        self.cool_down = 0
        self.image = self.choose_image()
        self.id = self.canvas.create_image(self.x, self.y, image=self.image)

    def choose_image(self):
        if self.subtype == 'Warrior':
            image = tk.PhotoImage(file="warrior.png")
        if self.subtype == 'Builder':
            image = tk.PhotoImage(file="builder.png")
        if self.subtype == 'Commander':
            image = tk.PhotoImage(file="commander.png")
        if self.subtype == 'Resource_gatherer':
            image = tk.PhotoImage(file="resource_gatherer.png")
        if self.subtype == 'Factory':
            image = tk.PhotoImage(file="factory.png")
        if self.subtype == 'Tower':
            image = tk.PhotoImage(file="tower.png")
        if self.subtype == 'Warrior' and self.fraction == 'Enemy':
            image = tk.PhotoImage(file="enemy.png")
        return image

    def take_damage(self, attacking_entity):
        self.hp -= attacking_entity.dmg

    def mine(self, mining_object):
        if mining_object.amount - self.dmg / 10 > 0:
            mining_object.amount -= self.dmg / 10
            if mining_object.type == 'Gold':
                self.canvas.gold_counter += self.dmg / 10
            elif mining_object.type == 'Wood':
                self.canvas.wood_counter += self.dmg / 10
        else:
            if mining_object.type == 'Gold':
                self.canvas.gold_counter += mining_object.amount
            elif mining_object.type == 'Wood':
                self.canvas.wood_counter += mining_object.amount
            mining_object.amount = 0


class Resource:
    def __init__(self, canvas, x, y, type, amount):
        self.canvas = canvas
        self.x = (x + DX) * canvas.scale
        self.y = (y + DY) * canvas.scale
        self.type = type
        self.amount = amount
        self.select_r = 30
        if self.type == 'Gold':
            self.id = self.canvas.create_oval(self.x - self.select_r + DX,
                                              self.y - self.select_r + DY,
                                              self.x + self.select_r + DX,
                                              self.y + self.select_r + DY,
                                              fill='yellow')
        elif self.type == 'Wood':
            self.id = self.canvas.create_oval(self.x - self.select_r + DX,
                                              self.y - self.select_r + DY,
                                              self.x + self.select_r + DX,
                                              self.y + self.select_r + DY,
                                              fill='green')
        self.canvas.tag_lower(self.id)


class Menu:
    def __init__(self, canvas):
        self.canvas = canvas
        self.background = canvas.create_rectangle(0, 0, X, Y, fill='green')
        self.canvas.tag_raise(self.background)
        self.play_button = tk.Button(text="Continue",
                                     command=self.play_button,
                                     width=12)
        self.play_button.place(x=0.5 * X, y=0.5 * Y)
        self.NewGame_button = tk.Button(text="New Game",
                                        command=self.new_game_button,
                                        width=12)
        self.NewGame_button.place(x=0.5 * X, y=0.5 * Y + 30)
        self.EndGame_button = tk.Button(text="End Game",
                                        command=self.end_game_button,
                                        width=12)
        self.EndGame_button.place(x=0.5 * X, y=0.5 * Y + 60)
        self.save_game_button = tk.Button(text="Save Game",
                                          command=self.save_game_button,
                                          width=12)
        self.save_game_button.place(x=0.5 * X, y=0.5 * Y + 90)
        self.label = tk.Label(text="Warcraft",
                              font="Helvetica 54",
                              fg='black', bg='green')
        self.label.place(x=0.5 * X - 110, y=0.5 * Y - 100)

    def new_game(self):
        self.canvas.new_game()

    def new_game_button(self):
        self.new_game()
        self.delete_menu()

    def play(self):
        self.canvas.play()

    def play_button(self):
        self.play()
        self.delete_menu()

    def end_game(self):
        self.canvas.end_game()

    def end_game_button(self):
        self.end_game()
        self.delete_menu()

    def save_game(self):
        self.canvas.save_game()

    def save_game_button(self):
        self.save_game()
        self.delete_menu()

    def delete_menu(self):
        self.play_button.destroy()
        self.NewGame_button.destroy()
        self.EndGame_button.destroy()
        self.save_game_button.destroy()
        self.canvas.delete(self.background)
        self.label.destroy()


class WarcraftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(X0) + 'x' + str(Y0))
        self.main_frame = MainFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.attributes("-fullscreen", True)
        self.menu = Menu(self.main_frame.battlefield)
        self.menu.canvas.tag_raise(self.menu.background)

    def new_game(self):
        self.main_frame.new_game()

    def end_game(self):
        self.main_frame.end_game()

    def pause(self):
        self.main_frame.pause()

    def play(self):
        self.main_frame.play()


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.battlefield = BattleField(self, self)
        self.battlefield.pack(fill=tk.BOTH, expand=1)
        self.lower_panel = self.battlefield.create_rectangle(0,
                                                             Y,
                                                             X,
                                                             Y * 0.8,
                                                             fill='blue',
                                                             tag='lower')
        self.upper_panel = self.battlefield.create_rectangle(0,
                                                             Y * 0.02,
                                                             X,
                                                             0,
                                                             fill='black',
                                                             tag='upper')
        self.lower_frame = tk.Frame(self, bg='brown', height=0.2 * Y, width=X)
        self.lower_frame.place(x=0, y=Y, anchor='sw')
        self.upper_frame = tk.Frame(self, bg='black', height=0.03 * Y, width=X)
        self.upper_frame.place(x=0, y=0, anchor='nw')
        self.gold_label = tk.Label(self.upper_frame, text='Gold: ' + str(self.battlefield.gold_counter),
                                   height=int(0.02*Y), width=int(0.2*X), font='Helvetica 20', anchor='center',
                                   bg='black', fg='white')
        self.gold_label.place(relx=0, rely=0, anchor='nw', relwidth=0.5, relheight=1)
        self.wood_label = tk.Label(self.upper_frame, text='Wood: ' + str(self.battlefield.wood_counter),
                                   height=int(0.02*Y), width=int(0.2*X), font='Helvetica 20', anchor='center',
                                   bg='black', fg='white')
        self.wood_label.place(relx=0.5, rely=0, anchor='nw', relwidth=0.5, relheight=1)
        self.factory_button = tk.Button(self.lower_frame,
                                        text='Factory',
                                        command=lambda: self.battlefield.building_place('Factory'),
                                        height=int(0.005 * Y),
                                        width=int(0.005 * X),
                                        bg='green')
        self.mineshaft_button = tk.Button(self.lower_frame,
                                          text='WIP',
                                          command=lambda: self.battlefield.building_place('MineShaft'),
                                          height=int(0.005 * Y),
                                          width=int(0.005 * X))
        self.tower_button = tk.Button(self.lower_frame,
                                      text='Tower',
                                      command=lambda: self.battlefield.building_place('Tower'),
                                      height=int(0.005 * Y),
                                      width=int(0.005 * X))
        self.builder_button = tk.Button(self.lower_frame, text='Builder',
                                        command=lambda: self.battlefield.assemble('Builder'),
                                        height=int(0.005 * Y),
                                        width=int(0.005 * X))
        self.warrior_button = tk.Button(self.lower_frame,
                                        text='Warrior',
                                        command=lambda: self.battlefield.assemble('Warrior'),
                                        height=int(0.005 * Y),
                                        width=int(0.005 * X))
        self.tower_button.place(x=X / 2 - 0.07 * X, y=0.01 * Y, anchor='n')
        self.builder_button.place(x=X / 2 + 0.07 * X, y=0.11 * Y, anchor='n')
        self.warrior_button.place(x=X / 2 - 0.07 * X, y=0.11 * Y, anchor='n')
        self.factory_button.place(x=X / 2, y=0.01 * Y, anchor='n')
        self.mineshaft_button.place(x=X / 2 + 0.07 * X, y=0.01 * Y, anchor='n')
        self.battlefield.focus_set()
        self.battlefield.tag_raise(self.lower_panel)
        self.battlefield.tag_raise(self.upper_panel)

    def new_game(self):
        self.battlefield.new_game()

    def end_game(self):
        self.battlefield.end_game()

    def pause(self):
        self.battlefield.pause()

    def play(self):
        self.battlefield.play()


class BattleField(tk.Canvas):
    def __init__(self, master, main_frame):
        super().__init__(master, background='white')
        self.main_frame = main_frame
        self.bind_all()
        self.select_cont = False
        self.DT = DT
        self.DT0 = self.DT
        self.WL = 30000
        self.selecting_circles = {}
        self.hp_bars = {}
        self.all_entities = set()
        self.player_entities = []
        self.enemy_entities = []
        self.X0 = X0
        self.Y0 = Y0
        self.X = X
        self.Y = Y
        self.scale = scale
        self.old_scale = self.scale
        self.wood_counter = 100
        self.gold_counter = 100
        self.gold_counter = 100
        self.all_resources = set()
        self.commander_x = 100
        self.commander_y = 100
        self.wave_counter = 1
        self.stop = False
        self.shift_held = False
        self.is_paused = True

    def get_mouse_coords(self):
        abs_x = self.winfo_pointerx()
        abs_y = self.winfo_pointery()
        canvas_x = self.winfo_rootx()
        canvas_y = self.winfo_rooty()
        return [abs_x - canvas_x, abs_y - canvas_y]

    def new_game(self):
        self.is_paused = False
        self.delete('all')
        self.draw_background()
        self.create_resource_pack(150, 450)
        self.create_entity(entity_list['Commander'], 'Player', [none], 600, 450)
        self.enemy_spawner()
        self.refresh()

    def create_menu(self):
        self.pause()
        self.menu = Menu(self)
        self.tag_raise(self.menu.background)

    def draw_background(self):
        self.grass = tk.PhotoImage(file='grass.png')
        for n in range(5):
            self.background_grass = self.create_image((512 * n, 0), image=self.grass)
            self.background_grass = self.create_image((512 * n, 512), image=self.grass)
            self.background_grass = self.create_image((512 * n, 512 * 2), image=self.grass)
            self.tag_lower(self.background_grass)

    def end_game(self):
        self.label = tk.Label(text='You survived approximately ' + str(self.wave_counter - 1) + ' waves', width=1000, height=500,
                              font='Helvetica 54', fg='white', bg='green')
        self.label.pack()

    def pause(self):
        self.is_paused = True
        self.bind('<Escape>', lambda event: self.play())

    def play(self):
        self.bind('<Escape>', lambda event: self.create_menu())
        self.is_paused = False
        self.menu.delete_menu()
        self.refresh()

    def bind_all(self):
        self.bind('<Button-1>', self.select_start, add='')
        self.bind('<ButtonRelease-1>', self.select_end, add='')
        self.bind('<Double-1>', lambda event: self.select_all_subtype())
        self.bind('<Button-3>', self.right_click, add='')
        self.bind('a', lambda event: self.scroll_left())
        self.bind('d', lambda event: self.scroll_right())
        self.bind('w', lambda event: self.scroll_up())
        self.bind('s', lambda event: self.scroll_down())
        self.bind('<Prior>', lambda event: self.size_up())
        self.bind('<Next>', lambda event: self.size_down())
        self.bind('<Home>', lambda event: self.return_1())
        self.bind('<Escape>', lambda event: self.create_menu())

    def create_hp_bar(self, entity):
        if entity.fraction == 'Player':
            hp_bar_back = self.create_rectangle(entity.x - entity.r - 10, entity.y - entity.r - 10,
                                                entity.x + entity.r + 10, entity.y - entity.r - 20, fill='blue')
            self.tag_raise(hp_bar_back)
            hp_bar_front = self.create_rectangle(entity.x - entity.r - 10, entity.y - entity.r - 10,
                                                 entity.x + entity.r + 10, entity.y - entity.r - 20, fill='cyan')
            self.tag_raise(hp_bar_front)
        elif entity.fraction == 'Enemy':
            hp_bar_back = self.create_rectangle(entity.x - entity.r - 10, entity.y - entity.r - 10,
                                                entity.x + entity.r + 10, entity.y - entity.r - 20, fill='magenta')
            self.tag_raise(hp_bar_back)
            hp_bar_front = self.create_rectangle(entity.x - entity.r - 10, entity.y - entity.r - 10,
                                                 entity.x + entity.r + 10, entity.y - entity.r - 20, fill='red')
            self.tag_raise(hp_bar_front)
        hp_bar = [hp_bar_back, hp_bar_front]
        self.hp_bars.update({entity: hp_bar})

    def create_entity(self, param_dict, fraction, task, x, y):
        entity = Entity(self, param_dict, fraction, task, x, y)
        self.all_entities.add(entity)
        if entity.fraction == 'Player':
            self.player_entities.append(entity)
        elif entity.fraction == 'Enemy':
            self.enemy_entities.append(entity)
        self.create_hp_bar(entity)

    def create_resource(self, x, y, type, amount):
        resource = Resource(self, x, y, type, amount)
        self.all_resources.add(resource)
        self.tag_raise(resource.id)

    def create_resource_pack(self, x, y):
        self.create_resource(x + 100, y - 350, 'Gold', 100)
        self.create_resource(x + 50, y - 250, 'Wood', 100)
        self.create_resource(x, y - 150, 'Wood', 100)
        self.create_resource(x, y - 50, 'Wood', 100)
        self.create_resource(x, y + 50, 'Wood', 100)
        self.create_resource(x, y + 150, 'Wood', 100)
        self.create_resource(x + 50, y + 250, 'Wood', 100)
        self.create_resource(x + 100, y + 350, 'Gold', 100)

    def building_place(self, building):
        if not len(self.selecting_circles) == 0:
            self.bind('<Button-3>', lambda a: self.building_place_2(building), add='')

    def building_place_2(self, building):
        self.mc = [self.mouse_coords[0], self.mouse_coords[1]]
        self.bind('<Button-3>', self.right_click, add='')
        for key in self.selecting_circles:
            if key.subtype == 'Builder' or key.subtype == 'Commander':
                key.task = [['build', building, self.mc[0], self.mc[1]]]

    def building_place_3(self, building, x, y):
        self.create_entity(entity_list[building], 'Player', [none], x / self.scale - DX, y / self.scale - DY)
        self.wood_counter -= entity_list[building]['wood_cost']
        self.gold_counter -= entity_list[building]['gold_cost']

    def assemble(self, unit):
        if not len(self.selecting_circles) == 0:
            for key in self.selecting_circles:
                if key.subtype == 'Factory':
                    if key.cool_down <= 0:
                        key.task = [['assemble', unit, key.unit_task]]
                        key.cool_down = 5000

    def assemble_2(self, unit, building):
        self.create_entity(entity_list[unit],
                           'Player',
                           building.unit_task,
                           building.x / self.scale - DX,
                           building.y / self.scale - DY)
        self.wood_counter -= entity_list[unit]['wood_cost']
        self.gold_counter -= entity_list[unit]['gold_cost']

    def idle(self):
        pass

    def size_up(self):
        self.scale += 0.1

    def size_down(self):
        self.scale = max(0.2, self.scale - 0.1)

    def scroll_up(self):
        for key in self.all_entities:
            key.y += VY
        self.Y += VY
        for key in self.all_resources:
            key.y += VY

    def scroll_down(self):
        for key in self.all_entities:
            key.y -= VY
        self.Y -= VY
        for key in self.all_resources:
            key.y -= VY

    def scroll_right(self):
        for key in self.all_entities:
            key.x -= VX
        self.X -= VX
        for key in self.all_resources:
            key.x -= VX

    def scroll_left(self):
        for key in self.all_entities:
            key.x += VX
        self.X += VX
        for key in self.all_resources:
            key.x += VX

    def return_1(self):
        for key in self.all_entities:
            key.x -= self.X - self.X0
            key.y -= self.Y - self.Y0
        for key in self.all_resources:
            key.x -= self.X - self.X0
            key.y -= self.Y - self.Y0
        self.X = self.X0
        self.Y = self.Y0
        self.scale = 0.5

    def refresh(self):
        self.main_frame.gold_label.config(text='Gold: ' + str(int(self.gold_counter)))
        self.main_frame.wood_label.config(text='Wood: ' + str(int(self.wood_counter)))
        all_entities_copy = self.all_entities.copy()
        all_resources_copy = self.all_resources.copy()
        self.mouse_coords = self.get_mouse_coords()
        if self.mouse_coords[0] > X * 0.9:
            self.scroll_right()
            # scroll_right
        elif self.mouse_coords[0] < X * 0.04:
            self.scroll_left()
            # scroll_left
        if self.mouse_coords[1] > 0.96 * Y:
            self.scroll_down()
            # scroll_down
        elif self.mouse_coords[1] < 0.04 * Y:
            self.scroll_up()
        for key in all_resources_copy:
            if not self.scale == self.old_scale:
                key.x = key.x / self.old_scale * self.scale
                key.y = key.y / self.old_scale * self.scale
                key.select_r = key.select_r / self.old_scale * self.scale
            self.coords(key.id,
                        key.x - key.select_r,
                        key.y - key.select_r,
                        key.x + key.select_r,
                        key.y + key.select_r)
            if key.amount > 0:
                pass
            else:
                self.delete(key.id)
                self.all_resources.remove(key)
        if len(self.all_resources) == 0:
            angle = rndangle(1, 0)
            self.create_resource_pack((self.commander_x + 3000 * self.scale * math.cos(angle)) / self.scale - DX,
                                      (self.commander_y + 3000 * self.scale * math.sin(angle)) / self.scale - DY)

        for key in all_entities_copy:
            if not self.scale == self.old_scale:
                key.x = key.x / self.old_scale * self.scale
                key.y = key.y / self.old_scale * self.scale
                key.v = key.v / self.old_scale * self.scale
                key.r = key.r / self.old_scale * self.scale
                key.action_r = key.action_r / self.old_scale * self.scale
                key.select_r = key.select_r / self.old_scale * self.scale
            self.coords(self.hp_bars[key][0], key.x - key.r - 10, key.y - key.r - 10,
                        key.x + + key.r + 10, key.y - key.r - 20)
            self.coords(self.hp_bars[key][1], key.x - key.r - 10, key.y - key.r - 10,
                        key.x + - key.r - 10 + (2 * key.r + 20) * key.hp / key.max_hp, key.y - key.r - 20)
            if key.subtype == 'Factory':
                if key.cool_down > 0:
                    key.cool_down -= self.DT
            if key.fraction == 'Enemy':
                for key1 in all_entities_copy:
                    if key1.fraction == 'Player':
                        if distance(key.x, key.y, key1.x, key1.y) < key.action_r:
                            key.task.insert(0, ['attack', key1])
                if key.task == [none]:
                    key.task[0] = ['move_to', self.commander_x, self.commander_y]
            elif key.fraction == 'Player' and key.task == [none]:
                for key1 in all_entities_copy:
                    if key1.fraction == 'Enemy':
                        if distance(key.x, key.y, key1.x, key1.y) < key.action_r:
                            key.task.insert(0, ['attack', key1])
            try:
                task_processing(self, key, *key.task[0])
            except KeyError:
                pass
            task_sort(self, key)

            if key.hp <= 0 and key.subtype == 'Commander':
                self.end_game()
            if key.hp == 0:
                self.all_entities.remove(key)
                self.delete(key.id)
                if key.fraction == 'Player':
                    self.player_entities.remove(key)
                    try:
                        self.delete(self.selecting_circles[key])
                    except KeyError:
                        pass
                elif key.fraction == 'Enemy':
                    self.enemy_entities.remove(key)
                try:
                    self.delete(self.hp_bars[key][0])
                    self.delete(self.hp_bars[key][1])
                except KeyError:
                    pass
            else:
                key.x += key.vx
                key.y += key.vy
                self.coords(key.id, key.x, key.y)

                try:
                    self.coords('cir' + str(key).replace(' ', ''),
                                key.x - key.select_r - 10,
                                key.y - key.select_r - 10,
                                key.x + key.select_r + 10,
                                key.y + key.select_r + 10)
                except KeyError:
                    pass
            if key.subtype == 'Commander':
                self.commander_x = key.x
                self.commander_y = key.y
        self.old_scale = self.scale
        if not self.stop and not self.is_paused:
            self.after(self.DT, self.refresh)

    def enemy_spawner(self):
        for i in range(self.wave_counter):
            angle = rndangle(1, 0)
            self.create_entity(entity_list['Warrior'],
                               'Enemy',
                               [['move_to', self.commander_x, self.commander_y]],
                               (self.commander_x + 3000 * math.cos(angle) * self.scale) / self.scale - DX,
                               (self.commander_y + 3000 * math.sin(angle) * self.scale) / self.scale - DY)
        self.wave_counter += 1
        if not self.stop:
            self.after(self.WL, self.enemy_spawner)

    def right_click(self, event):
        self.select_end_1()
        attack = False
        mine = False
        if not len(self.selecting_circles) == 0:
            for key in self.all_entities:
                if distance(self.mouse_coords[0], self.mouse_coords[1], key.x, key.y) <= key.select_r and \
                        key.fraction == 'Enemy':
                    for key1 in self.selecting_circles:
                        if key1.subtype == 'Factory':
                            key1.unit_task = [['attack', key]]
                        else:
                            key1.task = [['attack', key]]
                        attack = True
        for key in self.all_resources:
            if distance(self.mouse_coords[0], self.mouse_coords[1], key.x, key.y) <= key.select_r:
                for key1 in self.selecting_circles:
                    if key1.subtype == 'Builder':
                        key1.task = [['mine', key]]
                        mine = True
        if attack is False and mine is False:
            for key, item in self.selecting_circles.items():
                if key.subtype == 'Factory':
                    key.unit_task = [['move_to', self.mouse_coords[0], self.mouse_coords[1]]]
                else:
                    key.task = [['move_to', self.mouse_coords[0], self.mouse_coords[1]]]

    def selecting_clear(self):
        for key, item in self.selecting_circles.items():
            self.b3 = str(key)
            self.b3 = self.b3.replace(' ', '')
            self.a3 = 'cir' + self.b3
            self.delete(self.a3)
        self.selecting_circles = {}

    def select_start(self, event):
        self.selecting_clear()
        self.sel_rect_id = [self.create_rectangle(-1, -1, -1, -1)]
        self.mouse_coords = self.get_mouse_coords()
        self.sel_rect = [self.mouse_coords[0], self.mouse_coords[1]]
        self.select_cont = True
        self.select_area()

    def select_end(self, event):
        self.select_cont = False

    def select_end_1(self):
        self.select_cont = False

    def select_all_subtype(self):
        self.selecting_clear()
        for key in self.player_entities:
            if distance(self.mouse_coords[0], self.mouse_coords[1], key.x, key.y) < key.select_r:
                for key1 in self.player_entities:
                    if key1.subtype == key.subtype:
                        self.b1 = str(key1)
                        self.b1 = self.b1.replace(' ', '')
                        self.a1 = 'cir' + self.b1
                        cir = self.create_oval(key1.x - key1.select_r - 10,
                                               key1.y - key1.select_r - 10,
                                               key1.x + key1.select_r + 10,
                                               key1.y + key1.select_r + 10,
                                               outline='brown',
                                               tag=self.a1)
                        self.selecting_circles.update({key1: cir})
                break

    def select_area(self):
        self.mouse_coords = self.get_mouse_coords()
        self.delete(self.sel_rect_id)
        self.sel_rect_id = self.create_rectangle(self.sel_rect[0],
                                                 self.sel_rect[1],
                                                 self.mouse_coords[0],
                                                 self.mouse_coords[1],
                                                 outline='green',
                                                 width=2)

        for i in self.player_entities:
            if (i. x - self.sel_rect[0]) * (i. x - self.mouse_coords[0]) <= 0 and i.fraction == 'Player' and \
                    (i. y - self.sel_rect[1]) * (i. y - self.mouse_coords[1]) <= 0:
                if self.selecting_circles.get(i) is None:
                    self.b1 = str(i)
                    self.b1 = self.b1.replace(' ', '')
                    self.a1 = 'cir' + self.b1
                    cir = self.create_oval(i.x - i.select_r - 10,
                                           i.y - i.select_r - 10,
                                           i.x + i.select_r + 10,
                                           i.y + i.select_r + 10,
                                           outline='brown',
                                           tag=self.a1)
                    self.selecting_circles.update({i: cir})

        for key, item in self.selecting_circles.items():
            if (key. x - self.sel_rect[0]) * (key. x - self.mouse_coords[0]) > 0 or (key. y - self.sel_rect[1]) * \
                    (key. y - self.mouse_coords[1]) > 0:
                self.b2 = str(key)
                self.b2 = self.b2.replace(' ', '')
                self.a2 = 'cir' + self.b2
                self.delete(self.a2)
                del self.selecting_circles[key]
                break

        if self.select_cont is True:
            self.after(DT, self.select_area)
        else:
            self.delete(self.sel_rect_id)


app = WarcraftApp()
app.mainloop()
