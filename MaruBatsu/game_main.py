#! Python3
# game_main.py
import tkinter
from PIL import ImageTk
import tkinter.font as tkFont
import copy
import random

root = tkinter.Tk()

turnFlg = True
user_point = "○"
cpu_point = "×"
empty_point = " "
view_list = [[empty_point, empty_point, empty_point], [empty_point, empty_point, empty_point], [empty_point, empty_point, empty_point]]

user_click_img = ImageTk.PhotoImage(file = "images/maru.jpg")
cpu_click_img = ImageTk.PhotoImage(file = "images/batsu.jpg")


# 行列のチェック数取得（詳細）
def count_point_detail(check, index1, check_point):
    count = 0
    for index2 in range(3):
        if check == "row":
            if view_list[index1][index2] == check_point:
                count += 1
            elif view_list[index1][index2] != empty_point:
                count -= 1
        else:
            if view_list[index2][index1] == check_point:
                count += 1
            elif view_list[index2][index1] != empty_point:
                count -= 1

    return count

# 行列のチェック数取得
def count_point(check, check_point):
    count_map = {}
    for index in range(3):
        count_map[index] = count_point_detail(check, index, check_point)

    return count_map

# 画面へ「×」印を表示させる
def cpu_click(row_index, cel_index):
    point_x = 0
    point_y = 0
    if row_index == 0:
        point_y = 205
    elif row_index == 1:
        point_y = 405
    elif row_index == 2:
        point_y = 605

    if cel_index == 0:
        point_x = 122
    elif cel_index == 1:
        point_x = 322
    elif cel_index == 2:
        point_x = 522

    canvas.create_image(point_x, point_y, image=cpu_click_img)

def check_empty_space(player, count_map):
    for key, value in count_map.items():
        if value == 3:
            return value
        elif value == 2:
            return key
    
    return -1

def check_diagonal(player, base_point, check_point):
    count = 0
    for index in range(3):
        if base_point == "left":
            if view_list[index][index] == check_point:
                count += 1
            elif view_list[index][index] != empty_point:
                count -= 1
        else:
            if view_list[index][2 - index] == check_point:
                count += 1
            elif view_list[index][2 - index] != empty_point:
                count -= 1

    return count

def cpu_turn(check, index1):
    for index2 in range(3):
        if check == "row":
            if view_list[index1][index2] == empty_point:
                view_list[index1][index2] = cpu_point
                cpu_click(index1, index2)
        else:
            if view_list[index2][index1] == empty_point:
                view_list[index2][index1] = cpu_point
                cpu_click(index2, index1)

def cpu_diagonal_turn(base_point):
    for index in range(3):
        if base_point == "left":
            if view_list[index][index] == empty_point:
                view_list[index][index] = cpu_point
                cpu_click(index, index)
        else:
            if view_list[index][2 - index] == empty_point:
                view_list[index][2 - index] = cpu_point
                cpu_click(index, 2 - index)

def defense_and_offence(check_point):
    ## ユーザーの勝利回避のためのチェック
    row_count_map = count_point("row", check_point)
    cel_count_map = count_point("cel", check_point)

    row_index = check_empty_space("cpu", row_count_map)
    cel_index = check_empty_space("cpu", cel_count_map)

    if row_index == 3 or cel_index == 3:
        titleFontStyle = tkFont.Font(family="System", size=40)
        game_end_msg = tkinter.Label(text="cpu win", font=titleFontStyle)
        game_end_msg.place(x=250, y=350)
        return

    left_to_right_count = check_diagonal("cpu", "left", check_point)
    right_to_left_count = check_diagonal("cpu", "right", check_point)

    if left_to_right_count == 3 or right_to_left_count == 3:
        titleFontStyle = tkFont.Font(family="System", size=40)
        game_end_msg = tkinter.Label(text="cpu win", font=titleFontStyle)
        game_end_msg.place(x=250, y=350)
        return

    return_flg = False
    if row_index != -1:
        cpu_turn("row", row_index)
        return_flg = True

    elif cel_index != -1:
        cpu_turn("cel", cel_index)
        return_flg = True

    elif left_to_right_count == 2:
        cpu_diagonal_turn("left")
        return_flg = True

    elif right_to_left_count == 2:
        cpu_diagonal_turn("right")
        return_flg = True

    return return_flg

def game_check():
    game_flg = False
    message = ""
    for index in range(3):
        if count_point_detail("row", index, user_point) == 3 or count_point_detail("cel", index, user_point) == 3:
            message = "you win"
            game_flg = True

        elif count_point_detail("row", index, cpu_point) == 3 or count_point_detail("cel", index, cpu_point) == 3:
            message = "cpu win"
            game_flg = True

        elif check_diagonal("you", "left", user_point) == 3 or check_diagonal("you", "right", user_point) == 3:
            message = "you win"
            game_flg = True
        
        elif check_diagonal("cpu", "left", cpu_point) == 3 or check_diagonal("cpu", "right", cpu_point) == 3:
            message = "cpu win"
            game_flg = True

    empty_count = 0
    for index1 in range(3):
        for index2 in range(3):
            if view_list[index1][index2] == empty_point:
                empty_count += 1

    if empty_count == 0:
        message = "引き分け"
        game_flg = True

    if game_flg:
        titleFontStyle = tkFont.Font(family="System", size=40)
        game_end_msg = tkinter.Label(text=message, font=titleFontStyle)
        game_end_msg.place(x=250, y=370)
        return game_flg

    return game_flg

# CPUターン
def input_cpu():
    global turnFlg
    
    # 攻めの一手
    if defense_and_offence(cpu_point):
        turnFlg = True

    # 守りの一手
    elif defense_and_offence(user_point):
        turnFlg = True

    while not turnFlg:
        row = random.randint(0, 2)
        cel = random.randint(0, 2)

        if view_list[row][cel] == empty_point:
            view_list[row][cel] = cpu_point
            cpu_click(row, cel)
            turnFlg = True

    if game_check():
        turnFlg = False


# ユーザーがクリックした際の処理
def canvas_click(event):
    global turnFlg
    if not turnFlg:
        return

    point_x = 0
    point_y = 0
    row_index = -1
    cel_index = -1
    if 20 <= event.x <= 220:
        cel_index = 0
        point_x = 122
    elif 225 <= event.x <= 425:
        cel_index = 1
        point_x = 322
    elif 430 <= event.x <= 630:
        cel_index = 2
        point_x = 522
    else:
        return

    if 100 <= event.y <= 300:
        row_index = 0
        point_y = 205
    elif 305 <= event.y <= 505:
        row_index = 1
        point_y = 405
    elif 510 <= event.y <= 710:
        row_index = 2
        point_y = 605
    else:
        return

    if row_index == -1 or cel_index == -1:
        return

    if view_list[row_index][cel_index] != empty_point:
        return
    
    turnFlg = False
    view_list[row_index][cel_index] = user_point
    canvas.create_image(point_x, point_y, image=user_click_img)
    if game_check():
        turnFlg = False
        return

    input_cpu()    

if __name__=="__main__":

    root.title("○×ゲーム")
    root.minsize(640, 720)

    bg_img = ImageTk.PhotoImage(file="images/game_bg.jpg")

    # 画像の中心を基準に画面の座標を指定
    canvas = tkinter.Canvas(bg="black", width=640, height=720)
    canvas.place(x=0, y=0)
    canvas.create_image(320, 360, image=bg_img)
    canvas.bind("<Button>", canvas_click)

    # タイトル
    titleFontStyle = tkFont.Font(family="System", size=32)
    title = tkinter.Label(text="○×ゲーム", font=titleFontStyle)
    title.place(x=250, y=0)

    # 説明文
    msgFontStyle = tkFont.Font(family="System", size=16)
    message = tkinter.Label(
        text="これはコンピューターと対戦する３×３の○×ゲームです。\n以下に表示している３×３のマスを使用します。\n先攻はあなたです。それではゲームを始めてください。"
        , font=msgFontStyle)
    message.place(x=120, y=35)

    root.mainloop()
