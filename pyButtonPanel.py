#Python3 test script for EFCO button panel
#Build by Sam Lee

import tkinter as tk
import os

root = tk.Tk()
root.title('EFCO Button Panel Demo')
#root.configure(bg="#02DF82")    #可以直接打顏色名稱或是找色碼表的代號
root.configure(bg="#000000")    #可以直接打顏色名稱或是找色碼表的代號
w=620  #width
r=300  #height
x=200  #與視窗左上x的距離
y=300  #與視窗左上y的距離
root.geometry('%dx%d+%d+%d' % (w,r,x,y))
root.resizable(False, False)
#root.iconbitmap('icon.ico')

canvas = tk.Canvas(root, width=620, height=300, bg="#000000")
#canvas = tk.Canvas(root, width=620, height=300)

#標題
#canvas.create_text(20, 20, text='test1', anchor='nw', fill='#0a0', font=('Arial', 18, 'bold','italic'))
canvas.create_text(50, 30, text='test1', fill='#0a0', font=('Arial', 18))
canvas.create_text(150, 30, text='test2', fill='#0a0', font=('Arial', 18))
canvas.create_text(250, 30, text='test3', fill='#0a0', font=('Arial', 18))
canvas.create_text(350, 30, text='test4', fill='#0a0', font=('Arial', 18))
canvas.create_text(450, 30, text='test5', fill='#0a0', font=('Arial', 18))
canvas.create_text(550, 30, text='test6', fill='#0a0', font=('Arial', 18))


#按鈕
canvas.create_oval(10, 50, 100, 140, width=3, fill='#dcdcdc')
canvas.create_oval(110, 50, 200, 140, width=3, fill='#00ff00')
canvas.create_oval(210, 50, 300, 140, width=3, fill='#ff0000')
canvas.create_oval(310, 50, 400, 140, width=3, fill='#ffff00')
canvas.create_oval(410, 50, 500, 140, width=3, fill='#dcdcdc')
canvas.create_oval(510, 50, 600, 140, width=3, fill='#ff0000')

#分隔線
canvas.create_line(20, 160, 600, 160, width=5, fill='#0a0')

#狀態
os.environ.setdefault('BLINKA_FT232H', '1')
import board
import digitalio
C0 = digitalio.DigitalInOut(board.C0)
C1 = digitalio.DigitalInOut(board.C1)
C2 = digitalio.DigitalInOut(board.C2)
C3 = digitalio.DigitalInOut(board.C3)
C4 = digitalio.DigitalInOut(board.C4)
C5 = digitalio.DigitalInOut(board.C5)
C6 = digitalio.DigitalInOut(board.C6)
C7 = digitalio.DigitalInOut(board.C7)
for i in range(8):
    locals()['C' + str(i)].direction = digitalio.Direction.INPUT

canvas.create_text(50, 200, text='test1', fill='#0a0', font=('Arial', 18))
canvas.create_text(150, 200, text='test2', fill='#0a0', font=('Arial', 18))
canvas.create_text(250, 200, text='test3', fill='#0a0', font=('Arial', 18))
canvas.create_text(350, 200, text='test4', fill='#0a0', font=('Arial', 18))
canvas.create_text(450, 200, text='test5', fill='#0a0', font=('Arial', 18))
canvas.create_text(550, 200, text='test6', fill='#0a0', font=('Arial', 18))

canvas.pack()

'''
L1=tk.Label(root,text='Thank1',bg='#FFFACD',fg="#DAA520",
            font=("Arial",18,"bold"))
L2=tk.Label(root,text='Thank2',bg='#FFFACD',fg="#DAA520",
            font=("Arial",18,"bold"))
L3=tk.Label(root,text='Thank3',bg='#FFFACD',fg="#DAA520",
            font=("Arial",18,"bold"))
L4=tk.Label(root,text='Thank',bg='#FFFACD',fg="#DAA520",
            font=("Arial",18,"bold"))
L5=tk.Label(root,text='Thank',bg='#FFFACD',fg="#DAA520",
            font=("Arial",18,"bold"))
L6=tk.Label(root,text='Thank',bg='#FFFACD',fg="#DAA520",
            font=("Arial",18,"bold"))

L1.place(x=20,y=20,height=40,width=80)#位置在(150,150)，高150寬200
L2.place(x=120,y=20,height=40,width=80)
L3.place(x=220,y=20,height=40,width=80)
L4.place(x=320,y=20,height=40,width=80)
L5.place(x=420,y=20,height=40,width=80)
L6.place(x=520,y=20,height=40,width=80)

horizontal =tk.Frame(root, bg='gray', height=2,width=600)
horizontal.place(x=10, y=80)



C1 = tk.Frame(root, width=320, height=200, pady=100) #畫布
C1.create_oval(10, 10, 100, 100) # 圓形
C1.create_oval(110, 10, 200, 100, fill='red') # 圓形
C1.create_oval(210, 10, 300, 100, outline='blue') # 圓形
C1.create_oval(10, 10, 100, 120) # 橢圓
C1.pack()
'''


root.mainloop()
