import os,sys
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

#def show_dialog():
#    print('ok')
#    fTyp = [("","*")]
#    iDir = os.path.abspath(os.path.dirname(__file__))
#    filepath =  filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

#=================================================
# main function
#=================================================
if __name__ == '___main__':
    #rootの作成
    root = Tk()
    root.title("ImageLabeling")

    #メニューバー
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu)
    menu.add_cascade(label="ファイル",menu=filemenu)
    filemenu.add_command(label="フォルダを開く", command=show_dialog)

    #ファイルを開く
    #path = 'C:/Users/254994/Desktop/Image_labeling/ikuchan/'
    #ImgName = 'ikuchan.'
    #ext = 'jpg'

    #画象表示
    Pic_Image = ImageTk.PhotoImage(Image.open(filepath))
    #Pic_Image = ImageTk.PhotoImage(Image.open(path + ImgName + ext))
    Pic_Label = Label(root, image = Pic_Image)
    Pic_Label.pack()

    #イベントループ
    root.mainloop()