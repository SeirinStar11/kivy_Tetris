import time
import sys
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.event import EventDispatcher
# from kivy.core.window import Animation
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget

import random
import time
is_over = False
# 棋盘左下角位置x0,y0,格子边长30
x0, y0, l = 20, 170, 30
# 横格,竖格
w,h = 11,16
# 方块初始下落位置
drop_i, drop_j = 4, h+1

# 存放已经存在物块的坐标
board = [[i, -1] for i in range(w)]
# 控制下落速度
global speed
speed = 0.5
# 得分
global score
score = 0

global history
history = 0

class Tetris(Widget):
    def __init__(self, color_index, shape_index, on_ground_callback=None, **kwargs):
        super(Tetris, self).__init__(**kwargs)
        # global pre_shape, pre_color
        global speed
        # 初始下落位置
        self.x = x0 + drop_i * l
        self.y = y0 + drop_j * l

        # 形状、颜色列表
        self.shapes = [[(0, 0, 1, 1), (0, 1, 0, 1)],  # 正方形
                       [(0, 0, 0, 0), (1, 0, -1, -2)],  # 长条
                       [(-1, 0, 1, 2), (0, 0, 0, 0)],
                       [(0, 1, 0, -1), (0, 1, 1, 0)],  # 右Z
                       [(0, -1, -1, 0), (0, 1, 0, -1)],
                       [(0, -1, 0, 1), (0, 1, 1, 0)],  # 左Z
                       [(0, 1, 1, 0), (0, 1, 0, -1)],
                       [(0, 0, -1, 1), (0, 1, 0, 0)],  # T型
                       [(0, 0, 0, 1), (0, 1, -1, 0)],
                       [(0, 1, 0, -1), (0, 0, -1, 0)],
                       [(0, 0, -1, 0), (0, 1, 0, -1)],
                       [(0, 1, 1, -1), (0, -1, 0, 0)],  # 左钩
                       [(0, 1, 0, 0), (0, 1, 1, -1)],
                       [(0, -1, -1, 1), (0, 1, 0, 0)],
                       [(0, 0, 0, -1), (0, 1, -1, -1)],
                       [(0, 1, 1, -1), (0, 1, 0, 0)],  # 右钩
                       [(0, -1, 0, 0), (0, 1, 1, -1)],
                       [(0, -1, -1, 1), (0, -1, 0, 0)],
                       [(0, 0, 0, 1), (0, 1, -1, -1)]]
        self.colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]
        # 生成随机的俄罗斯方块
        self.color = self.colors[color_index]  # 颜色
        self.shape = self.shapes[shape_index]  # 形状
        # self.shape = [(0, 0, 0, 0), (1, 0, -1, -2)]
        # Color(rgb=self.color)
        self.draw_shape()

        self.next_color = self.colors[random.randint(1,3)]  # 颜色
        self.next_shape = self.shapes[random.randint(1,13)]  # 形状
        

        # 触底检测函数
        self.on_ground_callback = on_ground_callback

        # 方块下落
        self.is_animating = False  # 添加这个变量来控制动画
        self.start_animation()  # 添加这个函数来启动动画
        self.i = 0

    # 开始动画
    def start_animation(self):
        if not self.is_animating:
            self.is_animating = True
            Clock.schedule_interval(self.animate, speed)  # 每隔speed秒调用一次animate函数

    # 停止动画
    def stop_animation(self):
        if self.is_animating:
            self.is_animating = False
            Clock.unschedule(self.animate)

    # 下落动画
    def animate(self, dt):
        self.i += 1
        if not self.is_animating:
            return  # 如果动画被停止，则直接返回
        # 调用下降函数
        self.move_down()
    
    # 绘制俄罗斯方块
    def draw_shape(self):
        shape = self.shape
        # 绘制俄罗斯方块
        with self.canvas:
            for i in range(4):
                Color(rgb=self.color)
                x_ = shape[0][i] * l + self.x
                y_ = shape[1][i] * l + self.y
                Rectangle(pos=(x_, y_), size=(l, l))
                Color(0,0,0,.5)
                Line(points=[x_,y_,x_+l,y_], width=1)
                Line(points=[x_, y_+l, x_ + l, y_+l], width=1)
                Line(points=[x_, y_, x_ , y_+l], width=1)
                Line(points=[x_+l, y_, x_ + l, y_+l], width=1)


    # 上下左右移动
    def move_left(self):
        # 已经触底则不可移动
        if y0 == self.y + min(self.shape[1]) * l:
            return
        # 最左边的方块已经抵住左边框则不再移动
        if self.x + min(self.shape[0]) * l == x0:
            return
        self.x = max(x0, self.x - l)
        self.canvas.clear()
        self.draw_shape()

    def move_right(self):
        if y0 == self.y + min(self.shape[1]) * l:
            return
        # 最右边的方块已经抵住右边框则不再移动
        if self.x + max(self.shape[0]) * l == x0 + (w-1) * l:
            return
        self.x = min(x0 + (w-1) * l, self.x + l)
        self.canvas.clear()
        self.draw_shape()

    def move_up(self):
        pass

    def move_down(self):
        # print((self.x-x0)//l,(self.y-y0)//l)
        # 判断是否已经触底
        if self.is_on_ground():
            self.stop_animation()  # 停止下落动画
            # 将触底的物块坐标添加到board中
            for i in range(4):
                x_i = self.shape[0][i] + (self.x-x0) // l
                y_i = self.shape[1][i] + (self.y-y0) // l
                if [x_i, y_i] not in board: board.append([x_i, y_i, self.color])

            # 搜索已经满格的行
            full_rows = self.is_full()

            self.on_ground_callback(full_rows)  # 调用触底回调函数
            return

        # 更新坐标重绘方块
        self.y = min(y0 + h * l, self.y - l)
        self.canvas.clear()
        self.draw_shape()

    # 判断是否有满格的行
    def is_full(self):
        full_rows = []  # 满格的行号列表
        # 判断是否满行
        rows = list(set([(self.y-y0) // l + self.shape[1][i] for i in range(4)]))  # 需要判断的行
        # 去掉元组的位置数组
        pos_arr = [b[:2] for b in board]
        for row in rows:
            flag = True
            for i in range(w):
                if [i, row] not in pos_arr:
                    flag = False
                    break
            if flag == True:
                full_rows.append(row)
        return full_rows

    # 判断是否触底
    def is_on_ground(self):
        global score
        # ... 检查是否触底的逻辑 ...
        # 俄罗斯方块的四个格子有一个下方已经存在格子就算触底
        for i in range(4):
            pos_arr = [b[:2] for b in board]
            if [self.shape[0][i] + (self.x - x0) // l, self.shape[1][i] + (self.y-y0) // l - 1] in pos_arr:
                score += 4
                # print(self.shape[1][i] + (self.y-y0) // l)
                if self.shape[1][i] + (self.y-y0) // l > h-1:
                    global is_over
                    is_over = True
                return True
        # return True  # 或者False，取决于实际情况

    # 旋转函数
    def rotate(self):
        # print("前",self.shape[1])
        xs = tuple([i for i in self.shape[1]])  # 新的x变成原来的y
        ys = tuple([-i for i in self.shape[0]])  # 新的y变成原来的-x
        for x in xs:
            if (self.x - x0)//l-x < 0 or (self.x - x0)//l + x > w-1:
                return
        self.shape = [xs, ys]
        self.canvas.clear()
        self.draw_shape()

    # 控制物块下落速度
    def control_speed(self, s):
        global speed
        speed = s
        self.stop_animation()
        self.start_animation()

class Next_Tetris(Widget):
    # print("创建next")
    def __init__(self, color_index, shape_index, **kwargs):
        super(Next_Tetris, self).__init__(**kwargs)

        # 形状、颜色列表
        self.shapes = [[(0, 0, 1, 1), (0, 1, 0, 1)],  # 正方形
                       [(0, 0, 0, 0), (1, 0, -1, -2)],  # 长条
                       [(-1, 0, 1, 2), (0, 0, 0, 0)],
                       [(0, 1, 0, -1), (0, 1, 1, 0)],  # 右Z
                       [(0, -1, -1, 0), (0, 1, 0, -1)],
                       [(0, -1, 0, 1), (0, 1, 1, 0)],  # 左Z
                       [(0, 1, 1, 0), (0, 1, 0, -1)],
                       [(0, 0, -1, 1), (0, 1, 0, 0)],  # T型
                       [(0, 0, 0, 1), (0, 1, -1, 0)],
                       [(0, 1, 0, -1), (0, 0, -1, 0)],
                       [(0, 0, -1, 0), (0, 1, 0, -1)],
                       [(0, 1, 1, -1), (0, -1, 0, 0)],  # 左钩
                       [(0, 1, 0, 0), (0, 1, 1, -1)],
                       [(0, -1, -1, 1), (0, 1, 0, 0)],
                       [(0, 0, 0, -1), (0, 1, -1, -1)],
                       [(0, 1, 1, -1), (0, 1, 0, 0)],  # 右钩
                       [(0, -1, 0, 0), (0, 1, 1, -1)],
                       [(0, -1, -1, 1), (0, -1, 0, 0)],
                       [(0, 0, 0, 1), (0, 1, -1, -1)]]
        self.colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]

        # 生成随机的俄罗斯方块
        self.color = self.colors[color_index]  # 颜色
        self.shape = self.shapes[shape_index]  # 形状

        self.draw_next()

    # 绘制下一个方块
    def draw_next(self):
        # 绘制俄罗斯方块
        with self.canvas:
            for i in range(4):
                Color(rgb=self.color)
                x_ = self.shape[0][i] * l + x0 + 1.5*l
                y_ = self.shape[1][i] * l + y0 - 3.5*l
                Rectangle(pos=(x_, y_), size=(l, l))
                Color(0, 0, 0, .5)
                Line(points=[x_, y_, x_ + l, y_], width=1)
                Line(points=[x_, y_ + l, x_ + l, y_ + l], width=1)
                Line(points=[x_, y_, x_, y_ + l], width=1)
                Line(points=[x_ + l, y_, x_ + l, y_ + l], width=1)

class Scene(FloatLayout, EventDispatcher):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)

        self.j = 0

        # 控制颜色形状
        self.next_color_index = random.randint(0,3)
        self.next_shape_index = random.randint(0,13)
        self.random_next()

        # 绘制背景
        self.draw_canvas()
        self.register_event_type('on_button_press')

        # 控制游戏暂停继续
        self.status = 1

    def on_button_press(self, method):
        # print("Button in A was pressed!")
        # 这里可以触发B类中按钮的某些行为
        if isinstance(method, float):  # method是一个数值(触发了控制速度)
            self.call_back(method)
        elif method in ["up", "down", "left", "right", "Rotate"]:  # 上下左右事件
            self.call_back(method)  # 游戏进度事件
        else:
            self.Button_event(method)

    def draw_canvas(self):
        with self.canvas:
            # 1.画网格背景20x10
            # 边框
            Color(0, 0, 0, 0.5)
            Line(points=[x0 - 5, y0-5, x0+w*l+5, y0-5], width=1)
            Line(points=[x0 - 5, y0+h*l+5, x0+w*l+5, y0+h*l+5], width=1)
            Line(points=[x0 - 5, y0-5, x0 - 5, y0+h*l+5], width=1)
            Line(points=[x0+w*l+5, y0-5, x0+w*l+5, y0+h*l+5], width=1)
            # 格子
            Color(0, 0, 0, 0.2)
            for i in range(h+1):  # 横线
                Line(points=[x0, i * l + y0, x0 + w * l, i * l + y0], width=1)
            for j in range(w+1):  # 竖线
                Line(points=[j * l + x0, y0, j * l + x0, y0 + h * l], width=1)

            # 2.画已经有的方块
            for b in board:
                if len(b) == 3:
                    Color(rgb=b[2])
                    x_ = b[0] * l + x0
                    y_ = b[1] * l + y0
                    Rectangle(pos=(x_, y_), size=(l, l))
                    Color(0, 0, 0, .5)
                    Line(points=[x_, y_, x_ + l, y_], width=1)
                    Line(points=[x_, y_ + l, x_ + l, y_ + l], width=1)
                    Line(points=[x_, y_, x_, y_ + l], width=1)
                    Line(points=[x_ + l, y_, x_ + l, y_ + l], width=1)

            # 3.得分
            # 创建Label实例

            self.history_label = Label(
                text=f'历史最高:{history}',  # 设置text属性
                color=(0, 0, 0, .5),  # 设置颜色为红色，格式为(r, g, b, a)
                pos=(310,690),
                font_size=26,
                font_name = './pic/msyh.ttf',
                halign='left',
                text_size=(200,None)
            )

            self.score_label = Label(
                text=f'当前得分:{score}',  # 设置text属性
                color=(0, 0, 0, .5),  # 设置颜色为红色，格式为(r, g, b, a)
                pos=(310,645),
                font_size=26,
                font_name='./pic/msyh.ttf',
                halign='left',
                text_size=(200,None)
            )


    def random_next(self):
        self.pre_shape_index = self.next_shape_index
        self.pre_color_index = self.next_color_index
        while True:
            color_index = random.randint(0, 3)
            shape_index = random.randint(0, 13)
            if color_index!=self.pre_color_index and shape_index!=self.pre_shape_index:
                break
        self.next_shape_index = shape_index
        self.next_color_index = color_index

    # 创建Tetris实例
    def create_new_tetris(self):
        self.j += 1
        # print(f"创建了{self.j}个新的Tetris实例")

        def on_ground(full_rows):
            global score,is_over

            # 游戏结束弹窗
            if is_over == True:
                self.Button_event("INTERUPT GAME")
                # # 创建弹窗内容布局
                content = BoxLayout(orientation='vertical', padding=10, spacing=10)
                content.add_widget(Button(text=f'QUIT', size_hint_y=None, height=40,on_press=self.Button_event))
                content.add_widget(Button(text=f'RESTART', size_hint_y=None, height=40,on_press=self.Button_event))
                # 创建弹窗并设置其尺寸和内容
                self.gameover_popup = Popup(title='GAME OVER',size_hint=(None, None),
                      content=content,
                      size=(300, 200),auto_dismiss=False)
                self.gameover_popup.open()
                is_over = False
                return

            # 将满格的最下面一行从画布中删除,一直清除直到这一行已经空了
            while len(full_rows) > 0 and self.is_full_row(full_rows[0]):
                # 清除面板
                self.clear_board(full_rows[0])
                self.canvas.clear()
                self.draw_canvas()

            self.score = score
            self.score_label.text = f"当前得分:{score}"

            self.next_tetris.canvas.clear()
            self.random_next()
            self.next_tetris = None
            self.next_tetris = Next_Tetris(self.next_color_index,self.next_shape_index)
            # 当Tetris触底时，创建新的Tetris实例
            self.tetris = None  # 清除旧的Tetris实例（如果需要的话）
            self.create_new_tetris()  # 创建新的Tetris实例


        # 创建新的Tetris实例，并传递on_ground作为回调函数
        # 下一个
        self.next_tetris = Next_Tetris(self.next_color_index,self.next_shape_index)
        self.add_widget(self.next_tetris)
        # 当前的
        self.tetris = Tetris(self.pre_color_index, self.pre_shape_index, on_ground_callback=on_ground)
        self.add_widget(self.tetris)  # 将Tetris添加到场景中

    # 判断是否满格
    def is_full_row(self, row):
        # 判断第row行是否已经满了
        pos_arr = [b[:2] for b in board]
        flag = True
        for i in range(w):
            if [i, row] not in pos_arr:
                flag = False
                break
        return flag

    # 清除满格的行
    def clear_board(self, full_row):
        global score
        score += 10  # 清除一排+10分
        # 把full_row这一行从board中删除,它上面的方格下移
        for b in board[::-1]:
            if b[1] == full_row:
                board.remove(b)
            elif len(b) == 3 and b[1] > full_row:
                b[1] -= 1
        # print(board)

    # 点击上下左右按钮触发移动
    def call_back(self, direction):
        if direction == "up":
            self.tetris.move_up()
        elif direction == "down":
            is_down = self.tetris.move_down()
        elif direction == "left":
            self.tetris.move_left()
        elif direction == "right":
            self.tetris.move_right()
        elif direction == "Rotate":
            self.tetris.rotate()
        else:
            self.tetris.control_speed(direction)  # 触发控制速度

    # 游戏操作事件restart、start、game_over...
    def Button_event(self, operate):
        if operate == "START GAME":  # 开始游戏
            # 创建俄罗斯方块
            self.create_new_tetris()
        elif operate == "GAME OVER" or (type(operate)!=str and operate.text=="QUIT"):  # 结束游戏
            print("GAME OVER")
            sys.exit()
        elif operate == "CONTINUE GAME":  # 继续游戏
            print("CONTINUE GAME")
            # 打开下落动画
            self.tetris.start_animation()
        elif operate == "INTERUPT GAME":  # 暂停游戏
            print("INTERUPT GAME")
            # 关闭下落动画
            self.tetris.stop_animation()
        else:
            print("重启")
            if hasattr(self,'gameover_popup'):
                self.gameover_popup.dismiss()
            global score,history
            if score>history:
                history = score
            self.restart()

    #  重启
    def restart(self):
        global board,history,score
        # 清空画布
        self.canvas.clear()
        board = [[i, -1] for i in range(w)]
        self.draw_canvas()
        score = 0
        self.score_label.text = f"当前得分:{score}"
        self.history_label.text = f"历史最高:{history}"
        # 重新创建方块
        self.create_new_tetris()

class B(BoxLayout):
    a_instance = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)
        self.status = 0
        self.start = 0
        with self.canvas:
            Color(0, 0, 0, 0.5)
            Line(points=[x0 - 5, y0 - 150, x0 - 5, y0 - 20], width=1) # 左
            Line(points=[x0 - 5 + l*5, y0 - 150, x0 - 5 + l*5, y0 - 20], width=1) # 右
            Line(points=[x0 - 5, y0 - 150, x0 - 5 + 5 * l, y0 - 150], width=1)  # 下
            Line(points=[x0 - 5, y0 - 20, x0 - 5 + 5 * l, y0 - 20], width=1)  #上
            Color(0, 0, 0, 0.2)
            Line(points=[x0, y0 - 145, x0, y0 - 25], width=1)
            Line(points=[x0 - 10 + l * 5, y0 - 145, x0 - 10 + l * 5, y0 - 25], width=1)
            Line(points=[x0, y0 - 145, x0 - 10 + 5 * l, y0 - 145], width=1)
            Line(points=[x0, y0 - 25, x0 - 10 + 5 * l, y0 - 25], width=1)
            # print(self.ids.HISTORY.text)

    # 点击按钮调用事件
    def on_b_button_press(self, *args):
        # 关闭弹窗
        self.popup.dismiss()

        if type(args[0])!= str and type(args[0]) not in [float,int]:  # 弹窗传过来的事件
            global speed
            if self.spinner.text == "EASY":
                speed = 1.0
                self.ids.slider.max = 1.0
                self.ids.slider.min = 0.3
                self.ids.slider.value = 1.0
            elif self.spinner.text == "NORMAL":
                speed = 0.6
                self.ids.slider.max = 0.6
                self.ids.slider.min = 0.2
                self.ids.slider.value = 0.6
            else:
                speed = 0.4
                self.ids.slider.max = 0.4
                self.ids.slider.min = 0.1
                self.ids.slider.value = 0.4
            self.ids.ing_btn.background_normal = './pic/进行中.png'
            self.a_instance.dispatch('on_button_press', args[0].text)

        elif args[0] == "ing":  # 继续和暂停按钮传过来的事件
            # 暂停游戏
            self.ids.ing_btn.background_normal = './pic/暂停.png'
            self.a_instance.dispatch('on_button_press', "INTERUPT GAME")
            # 调用弹窗
            self.show_popup("ing")
        else:
            # 这里可以调用Scene类的方法或修改A类的属性
            self.a_instance.dispatch('on_button_press', *args)

    # 展示弹窗(开始游戏之前/暂停游戏)
    def show_popup(self, *args):
        # 在这里创建并显示弹窗
        # 获取窗口的尺寸
        window_width = Window.width
        window_height = Window.height
        # 计算弹窗的尺寸（宽度为窗口的一半，高度根据内容自适应）
        popup_width = window_width / 3

        # 创建弹窗内容布局
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        QUIT = Button(text=f'QUIT', size_hint_y=None, height=40,on_press=self.quit)
        content.add_widget(QUIT)

        # 游戏开始的时候调用的弹窗
        if args[0] == "START GAME":
            # content.add_widget(Image(source="./pic/大圣.jpg"),)
            self.spinner = Spinner(
                text='EASY',
                values=('EASY', 'NORMAL', 'HARD'),
                size_hint_y=None, height=40,
            )
            content.add_widget(self.spinner)
            START = Button(text=f'START GAME', size_hint_y=None, height=40,on_press=self.on_b_button_press)
            content.add_widget(START)
        # 游戏暂停的时候调用的弹窗
        else:
            RESTART = Button(text=f'RESTART', size_hint_y=None, height=40,on_press=self.on_b_button_press)
            content.add_widget(RESTART)
            CONTINUE = Button(text=f'CONTINUE GAME', size_hint_y=None, height=40,on_press=self.on_b_button_press)
            content.add_widget(CONTINUE)

        # 创建弹窗并设置其尺寸和内容
        self.popup = Popup(title='GAME ING',
                      content=content,
                      size_hint=(None, None),
                      size=(300,300),
                      auto_dismiss = False)
        self.popup.open()

    # 退出
    def quit(self,*args):
        sys.exit()
        # 结束游戏
        pass


class TestApp(App):
    def build(self):
        Window.size = (300,530)
        root = BoxLayout(orientation='vertical')

        a = Scene()
        self.b = B(a_instance=a)

        root.add_widget(a)
        a.size_hint_y = 0.95
        root.add_widget(self.b)
        self.b.size_hint_y = 0.05

        return root

    def on_start(self):
        # 覆盖App类的on_start方法
        # 当应用启动时，这个方法会自动被调用
        # 调出弹窗
        self.b.show_popup("START GAME")




if __name__ == '__main__':
    TestApp().run()
