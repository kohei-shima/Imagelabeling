import os,sys
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

#rootの作成
root = Tk()
root.title("ImageLabeling")
root.geometry("500x500")

def show_dialog():

    #ファイルを開く
    fTyp = [("","*.jpg;*.bmp")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath =  filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

    #画象表示
    Pic_Image = ImageTk.PhotoImage(Image.open(filepath))
    Pic_Label = Label(root, image = Pic_Image)
    print("ok")
    Pic_Label.pack()

#メニューバー
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu,tearoff=False)
menu.add_cascade(label="ファイル",menu=filemenu)
filemenu.add_command(label="フォルダを開く", command=show_dialog)

root.mainloop()