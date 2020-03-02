# utf-8
# time view

# import群
import tkinter as tk
import tkinter.font as font
import time
import math
import threading

root = tk.Tk()
root.title("経過時間")
root.geometry("400x75+500+100")    
my_font = font.Font(root,family="System",size=50,weight="bold")

def time_view(now):
    count_time = math.floor(time.time() - now)
    minutes = math.floor(int(count_time) / 60)
    seconds = int(count_time) % 60
    view_text = "{0} 分 {1} 経過".format(minutes, seconds)
    label = tk.Label(text=view_text, font=my_font)
    label.pack()
    root.mainloop()

def window_close():
    root.destroy()

if __name__ == "__main__":
    time_view(time.time())
