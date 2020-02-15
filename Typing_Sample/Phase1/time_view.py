# utf-8
# time view

# import群
import tkinter as tk
import time
import math

def time_view(now):
    count_time = math.floor(time.time() - now)
    minutes = math.floor(int(count_time) / 60)
    seconds = int(count_time) % 60
    view_text = "{0} 分 {1} 経過".format(minutes, seconds)
    root = tk.Tk()
    root.title("経過時間")
    root.geometry("300x150+100+100")    
    label = tk.Label(text=view_text)
    label.pack()
    root.mainloop()

if __name__ == "__main__":
    time_view(time.time())
