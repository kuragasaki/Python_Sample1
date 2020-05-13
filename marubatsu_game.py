#! Python3
# marubatus.py
import random

user_point = "○"
cpu_point = "×"
empty_point = " "
view_list = [[empty_point, empty_point, empty_point], [empty_point, empty_point, empty_point], [empty_point, empty_point, empty_point]]

def show():
    template = "| {} | {} | {} |"
    print("-" * 13)
    for output_list in view_list:
        print(template.format(output_list[0], output_list[1], output_list[2]))
        print("-" * 13)

    if game_check():
        print("ゲーム終了")
        exit()

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

def count_point(check, check_point):
    count_map = {}
    for index in range(3):
        count_map[index] = count_point_detail(check, index, check_point)

    return count_map


def check_empty_space(player, count_map):
    for key, value in count_map.items():
        if value == 3:
            print(player.join(" win"))
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
        else:
            if view_list[index2][index1] == empty_point:
                view_list[index2][index1] = cpu_point

def cpu_diagonal_turn(base_point):
    for index in range(3):
        if base_point == "left":
            if view_list[index][index] == empty_point:
                view_list[index][index] = cpu_point
        else:
            if view_list[index][2 - index] == empty_point:
                view_list[index][2 - index] = cpu_point

def defense_and_offence(check_point):
    ## ユーザーの勝利回避のためのチェック
    row_count_map = count_point("row", check_point)
    cel_count_map = count_point("cel", check_point)

    row_index = check_empty_space("cpu", row_count_map)
    cel_index = check_empty_space("cpu", cel_count_map)

    left_to_right_count = check_diagonal("cpu", "left", check_point)
    right_to_left_count = check_diagonal("cpu", "right", check_point)

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


def input_cpu():
    print("cpu ターン")

    # 攻めの一手
    if defense_and_offence(cpu_point):
        return

    # 守りの一手
    if defense_and_offence(user_point):
        return

    while True:
        row = random.randint(0, 2)
        cel = random.randint(0, 2)

        if view_list[row][cel] == empty_point:
            view_list[row][cel] = cpu_point
            return

def user_input(message):
    while True:
        print(message)
        input_num = input()

        if input_num.isalnum() and input_num.isdecimal():
            if 1 <= int(input_num) <= 3:
                return int(input_num) - 1

            print("範囲外の数値が入力されています。")
            continue

        print("正しく入力されていません。")

def game_check():
    for index in range(3):
        if count_point_detail("row", index, user_point) == 3 or count_point_detail("cel", index, user_point) == 3:
            print("you win")
            return True

        elif count_point_detail("row", index, cpu_point) == 3 or count_point_detail("cel", index, cpu_point) == 3:
            print("cpu win")
            return True

        elif check_diagonal("you", "left", user_point) == 3 or check_diagonal("you", "left", user_point) == 3:
            return True
        
        elif check_diagonal("cpu", "left", cpu_point) == 3 or check_diagonal("cpu", "left", cpu_point) == 3:
            return True

    empty_count = 0
    for index1 in range(3):
        for index2 in range(3):
            if view_list[index1][index2] == empty_point:
                empty_count += 1

    if empty_count == 0:
        print("引き分け")
        return True

    return False

if __name__ == "__main__":

    print("これはコンピューターと対戦する３×３の○×ゲームです。")
    print("以下のように３×３のマスが表示されます。")
    show()

    print("あなたが印を付けたいマスを指定する場合、")
    print("左上のマス（１行、１列）を基準に行と列番号を")
    print("指定してください。")
    
    print("先行はあなたです。")
    print("Game Start")

    while True:
        row = user_input("行番号１〜３を半角数字で入力してください。")
        cel = user_input("列番号１〜３を半角数字で入力してください。")

        if view_list[row][cel] != " ":
            print("すでにチェックされています。")
            print("再度、入力してください。")
            continue

        view_list[row][cel] = user_point
        show()

        input_cpu()
        show()