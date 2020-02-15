# utf-8
import json

## 予約語記録ファイル読み込み
def get_yoyakugo_info(gengo_name):
    with open("yoyakugo.json", "r") as yoyakugo_info:
        yoyakugo_map = json.load(yoyakugo_info)
        print(gengo_name)
        return yoyakugo_map[gengo_name]

## 出力メッセージ読み込み
def get_information_msg():
    msg_list = []
    with open("readme.txt", mode="r", encoding="utf-8") as info_msg:
        for i, line in enumerate(info_msg):
            msg_list.append(line)
        
    return msg_list

## 
def write_history():
    with open("", mode="w", encoding="utf-8") as wr_his:
        wr_his.write("")


## 仮置き
if __name__ == "__main__":
    tmp = get_yoyakugo_info("python")
    print(tmp)
    print()
    for line_txt in get_information_msg():
        print(line_txt)

