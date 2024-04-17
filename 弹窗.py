import time

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.core.window import Window
from kivy.event import EventDispatcher
# from kivy.core.window import Animation
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget

import random
import time

# 棋盘左下角位置x0,y0,格子边长30
x0, y0, l = 20, 170, 30
# 方块初始下落位置
drop_i, drop_j = 6, 20

# 存放已经存在物块的坐标
board = [[i, -1] for i in range(14)]

shapes = [[(0, 0, 1, 1), (0, 1, 0, 1)],  # 正方形
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
colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]

pre_color = (0, 0, 0, 0)
pre_color = [(0, 0, 0, 0), (0, 0, 0, 0)]
# 控制下落速度
global speed
speed = 0.5


class Next_Tetris(Widget):
    def __init__(self, color_index, shape_index,**kwargs):
        super(Next_Tetris, self).__init__(**kwargs)
        # 初始下落位置
        self.x = x0 + 0 * l
        self.y = y0 + 0 * l

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

    def draw_next(self):
        # 绘制俄罗斯方块
        with self.canvas:
            Color(rgb=self.color)
            for i in range(4):
                x_ = self.shape[0][i] * l + x0
                y_ = self.shape[1][i] * l + y0
                Rectangle(pos=(x_, y_), size=(l, l))




class Scene(FloatLayout, EventDispatcher):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)

        # 禁用continue按钮
        # self.ids.continue_.disabled = True
        self.j = 0

        # 控制颜色形状
        self.next_color_index = random.randint(0, 3)
        self.next_shape_index = random.randint(0, 13)
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
            Line(points=[x0 - 5, y0 - 5, x0 + 14 * l + 5, y0 - 5], width=1)
            Line(points=[x0 - 5, y0 + 19 * l + 5, x0 + 14 * l + 5, y0 + 19 * l + 5], width=1)
            Line(points=[x0 - 5, y0 - 5, x0 - 5, y0 + 19 * l + 5], width=1)
            Line(points=[x0 + 14 * l + 5, y0 - 5, x0 + 14 * l + 5, y0 + 19 * l + 5], width=1)
            # 格子
            Color(0, 0, 0, 0.2)
            for i in range(20):  # 横线
                Line(points=[x0, i * l + y0, x0 + 14 * l, i * l + y0], width=1)
            for j in range(15):  # 竖线
                Line(points=[j * l + x0, y0, j * l + x0, y0 + 19 * l], width=1)

            for b in board:
                if len(b) == 3:
                    Color(rgb=b[2])
                    x_ = b[0] * l + x0
                    y_ = b[1] * l + y0
                    Rectangle(pos=(x_, y_), size=(l, l))

    def random_next(self):
        self.pre_shape_index = self.next_shape_index
        self.pre_color_index = self.next_color_index
        while True:
            color_index = random.randint(0, 3)
            shape_index = random.randint(0, 13)
            if color_index != self.pre_color_index and shape_index != self.pre_shape_index:
                break
        self.next_shape_index = shape_index
        self.next_color_index = color_index

    # 创建Tetris实例
    def create_new_tetris(self):
        self.j += 1
        print(f"创建了{self.j}个新的Tetris实例")

        def on_ground(full_rows):
            # 将满格的最下面一行从画布中删除,一直清除直到这一行已经空了
            while len(full_rows) > 0 and self.is_full_row(full_rows[0]):
                # 清除面板
                self.clear_board(full_rows[0])
                self.canvas.clear()
                self.draw_canvas()

            self.next_tetris.clear_next()
            self.random_next()
            self.next_tetris = None
            self.next_tetris = Next_Tetris(self.next_color_index, self.next_shape_index)
            # 当Tetris触底时，创建新的Tetris实例
            self.tetris = None  # 清除旧的Tetris实例（如果需要的话）
            self.create_new_tetris()  # 创建新的Tetris实例

        # 创建新的Tetris实例，并传递on_ground作为回调函数
        # 下一个
        self.next_tetris = Next_Tetris(self.next_color_index, self.next_shape_index)
        # 当前的
        self.tetris = Tetris(self.pre_color_index, self.pre_shape_index, on_ground_callback=on_ground)
        self.add_widget(self.tetris)  # 将Tetris添加到场景中

    def is_full_row(self, row):
        # 判断第row行是否已经满了
        pos_arr = [b[:2] for b in board]
        flag = True
        for i in range(14):
            if [i, row] not in pos_arr:
                flag = False
                break
        return flag

    def clear_board(self, full_row):
        # 把full_row这一行从board中删除,它上面的方格下移
        for b in board[::-1]:
            if b[1] == full_row:
                board.remove(b)
            elif len(b) == 3 and b[1] > full_row:
                b[1] -= 1
        print(board)

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
            # 禁用START GAME按钮
            # self.ids.start.disabled = True
        elif operate == "GAME OVER":  # 结束游戏
            print("GAME OVER")
        elif operate == "CONTINUE GAME":  # 继续游戏
            print("CONTINUE GAME")
            # 打开下落动画
            self.tetris.start_animation()
            # # 禁用continue按钮,开启interrupt按钮
            # self.ids.continue_.disabled = True
            # self.ids.interrupt.disabled = False
            #
            # # 开启↑↓←→按钮
            # self.ids.up_btn.disabled = False
            # self.ids.down_btn.disabled = False
            # self.ids.left_btn.disabled = False
            # self.ids.right_btn.disabled = False
        elif operate == "INTERUPT GAME":  # 暂停游戏
            print("INTERUPT GAME")
            # 关闭下落动画
            self.tetris.stop_animation()
            # # 禁用interrupt按钮,开启continue按钮
            # self.ids.interrupt.disabled = True
            # self.ids.continue_.disabled = False
            #
            # # 禁用↑↓←→按钮
            # self.ids.up_btn.disabled = True
            # self.ids.down_btn.disabled = True
            # self.ids.left_btn.disabled = True
            # self.ids.right_btn.disabled = True
        else:
            print("重启")


class B(BoxLayout):
    a_instance = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)
        self.status = 0
        self.start = 0

    def on_b_button_press(self, *args):
        # 关闭弹窗
        self.popup.dismiss()

        if type(args[0]) != str and type(args[0]) not in [float, int]:  # 弹窗传过来的事件
            global speed
            if self.spinner.text == "EASY":
                speed = 1
            elif self.spinner.text == "NORMAL":
                speed = 0.6
            else:
                speed = 0.4
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

    def show_popup(self, *args):
        # 在这里创建并显示弹窗
        # 获取窗口的尺寸
        window_width = Window.width
        window_height = Window.height
        # 计算弹窗的尺寸（宽度为窗口的一半，高度根据内容自适应）
        popup_width = window_width / 2

        # 创建弹窗内容布局
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 游戏开始的时候调用的弹窗
        if args[0] == "START GAME":
            self.spinner = Spinner(
                text='EASY',
                values=('EASY', 'NORMAL', 'HARD'),
                size_hint_y=None, height=40,
            )
            content.add_widget(self.spinner)
            START = Button(text=f'START GAME', size_hint_y=None, height=40, on_press=self.on_b_button_press)
            content.add_widget(START)
        # 游戏暂停的时候调用的弹窗
        else:
            CONTINUE = Button(text=f'CONTINUE GAME', size_hint_y=None, height=40, on_press=self.on_b_button_press)
            content.add_widget(CONTINUE)
            RESTART = Button(text=f'RESTART', size_hint_y=None, height=40, on_press=self.on_b_button_press)
            content.add_widget(RESTART)

        QUIT = Button(text=f'QUIT', size_hint_y=None, height=40, on_press=self.quit)
        content.add_widget(QUIT)

        # 创建弹窗并设置其尺寸和内容
        self.popup = Popup(title='GAME ING',
                           content=content,
                           size_hint=(None, None),
                           size=(popup_width, popup_width),
                           auto_dismiss=False)
        self.popup.open()

    def quit(self, *args):
        # 结束游戏
        pass


class TestApp(App):
    def build(self):
        Window.size = (400, 600)
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
