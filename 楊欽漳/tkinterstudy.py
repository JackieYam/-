import tkinter as tk
win= tk.Tk()
#---------------------#
#關於視窗界面的設計
win.title("trade management")
win.geometry("400x500+850+200")#850+ 200 生成在中間 
win.minsize(width=400,height=500)
win.maxsize(width=400,height=500)
#resizable(0,0)
win.config(background="skyblue")#界面背景顔色
win.attributes("-topmost",True)

#按鈕
btn1=tk.Button(text="TP")
btn2=tk.Button(text="SL")
btn3=tk.Button(text="Partial Close")
btn1.config(bg="grey",width=3, height=10)
btn2.config(bg="grey",width=15, height=10)
btn3.config(bg="grey",width=20, height=20)
btn1.pack()
btn2.pack()
btn3.pack()
lb=tk.Label()
#輸入框
en=tk.Entry()
en.pack()
win.mainloop()
#----------------------#
#pyperclip


