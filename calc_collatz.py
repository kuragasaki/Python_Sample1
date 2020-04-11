# 計算用関数
def collatz(num):
    if num % 2 == 0:
        return int(num / 2)
    else:
        return num * 3 + 1

if __name__ == "__main__":
    num = -1
    while num == -1:
        try:
            num = int(input("整数を入力してください : "))
        except ValueError:
            print("もう一度、", sep=" ")
           
    print(num)
    while num != 1:
        num = collatz(num)
        print(num)
