'''
@ author                : Joey
@ tools                 : VSCode
@ core version          : python 3.5.3
@ content               : 接彈球遊戲
@ date                  : 2023/11/21

'''
from tkinter import *
import random
import winsound

# 製作視窗
win = Tk()
txt = Label(win, text="接彈球遊戲:左右移動滑鼠可以移動擋板。球落地一局結束，點擊滑鼠左鍵開新局")
txt.pack()
cv = Canvas(win, width = 640, height = 480)
cv.pack()

# 初始化遊戲
def init_game():
    global is_gameover, ball_weizhi_x, ball_weizhi_y
    global ball_yidong_x, ball_yidong_y, ball_size
    global racket_weizhi_x, racket_size, point, speed

    is_gameover = False
    ball_weizhi_x = 0
    ball_weizhi_y = 250
    ball_yidong_x = 15
    ball_yidong_y = 15
    ball_size = 10
    racket_weizhi_x = 0
    racket_size = 100
    point = 0
    speed = 50
    win.title("彈跳遊戲: 開始!")

# 控制畫面
def draw_screen():
    # 清空畫面
    cv.delete('all')
    # 製作畫布(畫面)
    cv.create_rectangle(0, 0, 640, 480, fill="white", width=0)

def draw_ball():
    # 控制小球
    cv.create_oval(ball_weizhi_x - ball_size, ball_weizhi_y - ball_size,
                   ball_weizhi_x + ball_size, ball_weizhi_y + ball_size, fill="red")

def draw_racket():
    # 繪製擋板
    cv.create_rectangle(racket_weizhi_x, 470, racket_weizhi_x + racket_size, 480, fill="yellow", )


# 移動小球
def move_ball():
    global is_gameover, point, ball_weizhi_x, ball_weizhi_y, ball_yidong_x, ball_yidong_y
    if is_gameover: return
    
    # 判斷是否撞到了左右的牆壁
    if ball_weizhi_x + ball_yidong_x < 0 or ball_weizhi_x + ball_yidong_x > 640:
        ball_yidong_x *= -1
        winsound.Beep(1320, 50)
    # 判斷是否撞到了頂部
    if ball_weizhi_y + ball_yidong_y < 0:
        ball_yidong_y *= -1
        winsound.Beep(1320, 50)
    
    # 判斷是否撞到了擋板
    if ball_weizhi_y + ball_yidong_y > 470 and (racket_weizhi_x <= (ball_weizhi_x + ball_yidong_x) <= 
                                                (racket_weizhi_x + racket_size)):
        ball_yidong_y *= -1
        if random.randint(0, 1) == 0:
            ball_yidong_x *= -1
        winsound.Beep(2000, 50)
        mes = random.randint(0, 4)
        if mes == 0:
            message = "不錯!"
        if mes == 1:
            message = "真棒!"
        if mes == 2:
            message = "幹得好!"
        if mes == 3:
            message = "真厲害!"
        if mes == 4:
            message = "完美!"
        point += 10
        win.title(message + "得分=" + str(point))
    
    # 失誤時的判斷
    if 0 <= ball_weizhi_x + ball_yidong_x <= 640:
        ball_weizhi_x = ball_weizhi_x + ball_yidong_x
    if 0 <= ball_weizhi_y + ball_yidong_y <= 480:
        ball_weizhi_y = ball_weizhi_y + ball_yidong_y
    if ball_weizhi_y + ball_yidong_y >= 480:
        mes = random.randint(0, 2)
        if mes == 0:
            message = "太弱了!"
        if mes == 1:
            message = "失誤了喔!"
        if mes == 2:
            message = "啊,慘不忍睹!"
        win.title(message + "得分=" + str(point))
        winsound.Beep(600, 50)
        is_gameover = True

# 處理滑鼠動作
def motion(event):  # 確認滑鼠指標位址
    global racket_weizhi_x
    racket_weizhi_x = event.x

def click(event): # 點擊，重新開始
    if event.num == 1 and is_gameover :
        init_game()

# 確認滑鼠的動作和點擊
win.bind("<Motion>", motion)
win.bind("<Button>", click)

def game_loop():
    draw_screen()
    draw_ball()
    draw_racket()
    move_ball()
    win.after(speed, game_loop)

# 遊戲的主處理
init_game()
game_loop()
win.mainloop()