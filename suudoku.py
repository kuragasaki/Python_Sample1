#! Python3
# suudoku.py

import copy
import numpy

suudoku = [
    [   1,    7,    2,    9,    5, None, None,    8,    6],
    [   9, None, None,    4,    8, None, None,    3,    7],
    [   8, None,    3, None,    1,    7,    9,    5, None],
    [None, None,    6, None, None,    8,    7,    4, None], 
    [   3,    1, None,    5, None, None,    2, None, None],
    [None, None,    4,    7,    9,    1,    5,    6, None], 
    [None,    2, None,    1, None, None,    8, None,    5],
    [None, None, None, None, None, None,    6,    1,    9],
    [None, None, None, None,    7, None,    3, None, None]
]

# None変換情報を保持するクラス
class NoneToNumber:
    row_index = -1
    cel_index_list = []
    candidate_list = []

    def __init__(self, row_number):
        self.row_index = row_number

# 盤面チェック
def check_number(check_list):
    # 1行づつ
    for row in check_list:
        # Noneチェック
        if None in row:
            return True

        # １から９までの合計値チェック
        if sum(row) != 45:
            return True

        # 1から９の数字が使用されているかチェック
        count = 1
        for num in sorted(row):
            if count != num:
                return True

            count += 1
    return False


# 行から数字が埋まっていない箇所を探す（列番号を押さえる）
# 使用されていない数字をピックアップ
def pickUp_none():
    pickUpMap = {}
    for row_index in range(len(suudoku)):
        cel_number_list = []
        candidate_list = []
        for cel_index in range(len(suudoku[row_index])):

            # 行から数字が埋まっていない箇所を探す（列番号を押さえる）
            if suudoku[row_index][cel_index] == None:
                cel_number_list.append(cel_index)
        
        for number in range(1, 10):
            # 使用されていない数字をピックアップ
            if number not in suudoku[row_index]:
                candidate_list.append(number)

        # 数字が埋まっていない箇所が存在する
        if len(cel_number_list) > 0:
            tmpClass = NoneToNumber(row_index)
            tmpClass.cel_index_list = copy.copy(cel_number_list)
            tmpClass.candidate_list = copy.copy(candidate_list)

            pickUpMap[row_index] = tmpClass

    return pickUpMap

def pickUp_none_cel():
    pickUpMap = {}
    for cel_index in range(len(suudoku[0])):
        row_number_list = []
        candidate_list = []
        for row_index in range(len(suudoku[0])):

            # 行から数字が埋まっていない箇所を探す（列番号を押さえる）
            if suudoku[row_index][cel_index] == None:
                cel_number_list.append(cel_index)
        
        for number in range(1, 10):
            # 使用されていない数字をピックアップ
            if number not in suudoku[row_index]:
                candidate_list.append(number)

        # 数字が埋まっていない箇所が存在する
        if len(cel_number_list) > 0:
            tmpClass = NoneToNumber(row_index)
            tmpClass.cel_index_list = copy.copy(cel_number_list)
            tmpClass.candidate_list = copy.copy(candidate_list)

            pickUpMap[row_index] = tmpClass

    return pickUpMap


#  埋まっていない箇所が少ない行を探す（行番号を押さえる）
def getNoneMinCount(pickUpMap):

    noneToNumber = pickUpMap[list(pickUpMap.keys())[0]]
    count = len(noneToNumber.candidate_list)
    for value in pickUpMap.values():
        if noneToNumber.row_index != value.row_index and count > len(value.candidate_list):
            noneToNumber = value
            count = len(value.candidate_list)

    return noneToNumber

# １列分のリストを取得する
def getCelList(cel_index):
    cel_list = []
    for row in suudoku:
        cel_list.append(row[cel_index])

    return cel_list

# 埋まっていない場所に、使用されていない数字を入れる
# 埋まっていない列に使用されていない数字が存在するかどうかチェック
# すでに存在していたら、数字を変更してもう一度実施
def writeNumber(noneToNumber):

    checkMap = {}
    # 行の中で使用されていない数字を全て取得
    for num in noneToNumber.candidate_list:
    
        checkList = []
        # 数字が埋まっていない列番号分繰り返す
        for cel_index in noneToNumber.cel_index_list:
            # 対象列の全要素を取得
            #cel_list = getCelList(cel_index)
            cel_list = numpy.array(suudoku).T[cel_index]

            if num not in cel_list:
                checkList.append(cel_index)
        checkMap[num] = copy.copy(checkList)

    # 存在しない場合
    if not checkMap:
        return

    count = len(checkMap)
    check_key_list = list(checkMap.keys())
    del_cel_number = -1
    del_key_number = -1
    while True:

        # 候補の数字が存在する行がない
        if not check_key_list:
            break

        # 候補の数字を当てられる列を探す
        for candidate_number in check_key_list:

            # すでに埋めた列番号が他の候補番号にも存在する場合、列番号を削除
            if del_cel_number != -1 and del_cel_number in checkMap[candidate_number]:
                checkMap[candidate_number].remove(del_cel_number)

            # 列番号取得
            if 1 == len(checkMap[candidate_number]):
                suudoku[noneToNumber.row_index][checkMap[candidate_number][0]] = candidate_number
                del_cel_number = checkMap[candidate_number][0]
                del_key_number = candidate_number
        
        # 使用した候補番号を削除
        if del_key_number > -1:
            del checkMap[del_key_number]
            check_key_list.remove(del_key_number)
            del_key_number = -1

        if count == len(checkMap):
            break
        else:
            count = len(checkMap)

if __name__ == "__main__":
    none_count = -1
    #  ２次元配列をチェック（None、１−９の存在、合計値）
    while check_number(suudoku):
        #  行から数字が埋まっていない箇所を探す（列番号を押さえる）
        #  使用されていない数字をピックアップ
        pickUpMap = pickUp_none()
        none_count_list = []
        if len(pickUpMap) > 0:
            # 埋まっていない場所に、使用されていない数字を入れる
            # 埋まっていない列に使用されていない数字が存在するかどうかチェック
            # すでに存在していたら、数字を変更してもう一度実施
            for noneToNumber in pickUpMap.values():
                writeNumber(noneToNumber)
                none_count_list.append(len(noneToNumber.cel_index_list))

        # 埋められる数値が重複状態になってしまった場合の処置
        if none_count > 0 and none_count == sum(none_count_list):
            index = list(pickUpMap.keys())[0]
            noneToNumber = pickUpMap[index]
            suudoku[index][noneToNumber.cel_index_list[0]] = noneToNumber.candidate_list[0]
        else:
            none_count = sum(none_count_list)

        # 行列入れ替え
        suudoku = numpy.array(suudoku).T

    print(suudoku)    
