'''
@ author : Joey
@ tools : VScode
@ content : 貪吃蛇
@ date:2023/11/29
'''

import tkinter as tk
from tkinter.messagebox import showinfo
import random

class Snake():
    # 貪吃蛇遊戲
    def __init__(self):
        # 遊戲參數設置

        self.window     = None      # 實體化的視窗
        self.canvas     = None      # 實體化的圖布
        self.loop       = 0         # 暫停旗標，1為開啟，0為暫停
        self.loop_id    = None      # 實例化Loop，用來取消循環

        self.game_map   = []        # 整個遊戲地圖
        self.snake_body = []        # 蛇身的座標集
        self.food_xy    = []        # 食物座標
        self.head_x     = 0         # 蛇頭的x座標
        self.head_y     = 0         # 蛇頭的y座標
        self.dd         = [0]       # 紀錄按鍵方向

        self.len        = 3         # 蛇身初始化長度(最小設定值為1，不包括蛇頭)
        self.body_len   = self.len  # 蛇身當前長度
        self.FPS        = 120       # 蛇的移動速度(單位毫秒)
        self.row_cells  = 22        # 一行多少個單元格(含邊框)
        self.col_cells  = 22        # 一共多少行單元格(含邊框)
        self.canvas_bg  = 'white'   # 遊戲背景色
        self.cell_size  = 25        # 方格單元格大小
        self.cell_gap   = 1         # 方格間距
        self.frame_x    = 15        # 左右邊距
        self.frame_y    = 15        # 上下邊距
        self.win_w_plus = 220       # 窗口右邊額外多出的寬度

        self.color_dict = {0:   '#d7d7d7',  # 0表示空白
                           1:    'yellow',  # 1代表蛇頭
                           2:   '#009700',  # 2代表蛇身
                           3:       'red',  # 3代表食物
                           4:   '#808080',} # 4代表牆

        self.run_game()

    def window_center(self, window, w_size, h_size):
        """"視窗居中"""
        screenWidth = window.winfo_screenwidth()    # 獲取顯示區域的寬度
        screenHeight = window.winfo_screenheight()  # 獲取顯示區域的高度
        left = (screenWidth - w_size) // 2
        top = (screenHeight - h_size) // 2
        window.geometry("%dx%d+%d+%d" % (w_size, h_size, left, top))

    def creat_map(self):
        """ 創建地圖列表 """
        self.game_map = []
        for i in range(0, self.col_cells):
            self.game_map.append([])
        for i in range(0, self.col_cells):
            for j in range(0, self.row_cells):
                self.game_map[i].append(j)
                self.game_map[i][j] = 0     # 生成一個全部為0的空數列
    
    def creat_wall(self):
        """ 繪製邊框 """
        for i in range(0, self.row_cells - 1):
            self.game_map[0][i] = 4
            self.game_map[self.col_cells - 1][i] = 4

        for i in range(0, self.col_cells - 1):
            self.game_map[i][0] = 4
            self.game_map[i][self.row_cells - 1] = 4
        self.game_map[-1][-1] = 4
    
    def creat_canvas(self):
        """ 創建畫布 """
        canvas_h = self.cell_size * self.col_cells + self.frame_y * 2
        canvas_w = self.cell_size * self.row_cells + self.frame_x * 2

        self.canvas = tk.Canvas(self.window, bg = self.canvas_bg,
                                height = canvas_h,
                                width = canvas_w,
                                highlightthickness = 0)
        self.canvas.place(x = 0, y = 0)

    def creat_cells(self):
        """ 創建單元格 """
        for y in range(0, self.col_cells):
            for x in range(0, self.row_cells):
                a = self.frame_x + self.cell_size * x
                b = self.frame_y + self.row_cells * y
                c = self.frame_x + self.cell_size * (x + 1)
                d = self.frame_y + self.cell_size * (y + 1)
                e = self.canvas_bg
                f = self.cell_gap
                g = self.color_dict[self.game_map[y][x]]
                self.canvas.itemconfig(self.canvas.create_rectangle(a, b, c, d, outline = e, width = f, fill = g), fill = g)
    
    def creat_snake(self):
        """ 創建蛇頭和蛇身 """
        self.snake_body = [[self.col_cells // 2, self.row_cells // 2]]      # 蛇頭出身地在地圖的中央
        self.game_map[self.snake_body[0][0]][self.snake_body[0][1]] = 1     # 蛇頭上色，顏色為定義的1

    def creat_food(self):
        """ 創造食物 """
        self.food_xy = [0,0]
        self.food_xy[1] = random.randint(1, self.row_cells - 2)
        self.food_xy[0] = random.randint(1, self.col_cells - 2)

        while self.game_map[self.food_xy[0]][self.food_xy[1]] != 0:
            self.food_xy[1] = random.randint(1, self.row_cells - 2)
            self.food_xy[0] = random.randint(1, self.col_cells - 2)
        
        self.game_map[self.food_xy[0]][self.food_xy[1]] = 3

    def snake_xy(self):
        """ 獲得蛇頭座標 """
        xy = []
        for i in range(0, self.col_cells):
            try:    # 查找數值為1的座標，沒有就返回0。為防止在0列，先加上1，最後再減去。
                x = self.game_map[i].index(1) + 1
            except:
                x = 0
            xy.append(x)
        self.head_x = max(xy)
        self.head_y = xy.index(self.head_x)
        self.head_x = self.head_x - 1 # 之前加1，現在減回去
    
    def move_snake(self, event):
        """ 蛇體移動 """
        def move_key(a, b, c, d):   # 紀錄按鍵方向，1上2下3左4右
            direction = event.keysym

            if self.head_x != self.snake_body[-1][1]:
                if(direction == a):
                    self.dd[0] = 1
                if(direction == b):
                    self.dd[0] = 2
            else:
                if(direction == c):
                    self.dd[0] = 3
                if(direction == d):
                    self.dd[0] = 4

            if self.head_y != self.snake_body[-1][0]:
                if(direction == c):
                    self.dd[0] = 3
                if(direction == d):
                    self.dd[0] = 4
            else:
                if(direction == a):
                    self.dd[0] = 1
                if(direction == b):
                    self.dd[0] = 2
                
        def pause_key(key):
            """ 暫停鍵 """
            direction = event.keysym
            if(direction == key):
                self.loop = 0
                showinfo('暫停','按確定鍵繼續')
                self.loop = 1
                self.window.after(self.FPS, self.game_loop)
        
        move_key('w','s','a','d')
        move_key('W','S','A','D')
        move_key('Up', 'Down', 'Left', 'Right')
        pause_key('space')

    def game_over(self):
        def over():
            showinfo('Game Over','再來一局')
            self.body_len = self.len
            self.game_start()

        if [self.head_y,self.head_x] in self.snake_body[0:-2]:
            over()
        if self.head_x == self.row_cells - 1 or self.head_x == 0:
            over()
        if self.head_y == self.col_cells - 1 or self.head_y == 0:
            over()

    def snake_record(self):
        """ 蛇身 """    # 紀錄蛇頭運行軌跡，生成蛇身

        temp = []
        temp.append(self.head_y)
        temp.append(self.head_x)
        self.snake_body.append(temp)

        if self.snake_body[-1] == self.snake_body[-2]:
            del self.snake_body[-1]
        
        if [self.head_y, self.head_x] == self.food_xy:  # 碰到食物身體加長，並在隨機生成一個食物
            self.body_len += 1
            self.creat_food()
        elif len(self.snake_body) > self.body_len:      # 設定蛇身長度，不超過設定值
            self.game_map[self.snake_body[0][0]][self.snake_body[0][1]] = 0
            del self.snake_body[0]
        
    def auto_move(self):
        """ 自動前進 """
        def move(d, x, y):
            if self.dd[0] == d:     # 根據方向值來決定走向
                self.game_map[self.head_y + x][self.head_x + y] = 1
                self.game_map[self.head_y + 0][self.head_x + 0] = 2

        move( 1, -1, 0)
        move( 2, 1,  0)
        move( 3, 0, -1)
        move( 4, 0,  1)

    def game_loop(self):
        """ 遊戲循環刷新 """
        self.snake_record()
        self.auto_move()
        self.snake_xy()
        self.canvas.delete('all')   # 清除canvas
        self.creat_cells()
        self.game_over()
        
        if self.loop == 1:
            self.loop_id = self.window.after(self.FPS, self.game_loop)

    def  game_start(self):
        self.loop = 1    # 暫停標記， 1為開啟， 0為暫停
        self.dd = [0]    # 紀錄按鈕方向
        self.creat_map()
        self.creat_wall()
        self.creat_snake()
        self.creat_food()
        self.window.bind('<Key>', self.move_snake)
        self.snake_xy()  
        self.game_loop()

        def close_w():
            self.loop = 0
            self.window.after_cancel(self.loop_id)
            self.window.destroy()
        
        self.window.protocol('WM_DELETE_WINDOW', close_w)
        self.window.mainloop()

    def run_game(self):
        """ 開始遊戲 """
        

        self.window = tk.Tk()
        self.window.focus_force()   # 主視窗焦點
        self.window.title('Snake')

        win_w_size = self.row_cells * self.cell_size + self.frame_x * 2 + self.win_w_plus
        win_h_size = self.col_cells * self.cell_size + self.frame_y * 2
        self.window_center(self.window, win_w_size, win_h_size)

        txt_lable = tk.Label(self.window, text=
                             "方向鍵移動方向，或者"
                             +"\n字母鍵WSAD移動"
                             +"\n(大小寫均可)"
                             +"\n"
                             +"\n空格鍵暫停"
                             +"\n作者:Joey",
                             font = ('Yahei',15), anchor = "ne", justify = "left")

        txt_lable.place(x = self.cell_size * self.col_cells + self.cell_size*2,
                        y = self.cell_size * 6)


        self.creat_canvas()
        self.game_start()

if __name__ == '__main__':
    Snake()