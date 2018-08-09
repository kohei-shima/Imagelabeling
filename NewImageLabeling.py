import os,sys
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk

root = Tk()
canvas = tk.Canvas(root,width=300,height=300,relief=tk.RIDGE,bd=2)

canvas.place(x=200,y=100)

class App(Frame):
    def quit(self): 
        self.master.destroy()
 
    def show_dialog(self):
        fTyp = [("","*.jpg;*.bmp")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filename = filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)

        if filename != "":
            im = Image.open(filename)
            resize_im = im
            #resize_im = im.resize((int(im.width / 2), int(im.height / 2)))
            #resize_im = im.resize((int(im.width * 2), int(im.height * 2)))
            self.image1 = ImageTk.PhotoImage(resize_im)
            canvas.create_image(150,150,image=self.image1)

    def init(self):
        self.image1 = PhotoImage()

        canvas.create_image(0,0,image=self.image1,anchor=tk.NW)
        #label = self.label = Label(root,image = self.image1)
        #label.pack()

        m0 = Menu(root)
        root.config(menu = m0)

        m1 = Menu(m0,tearoff=0)
        m1.add_command(label="フォルダを開く",under=0,command=self.show_dialog)
        m1.add_command(label="終了",under=0,command=quit)
        m0.add_cascade(label="ファイル",under=0,menu=m1)
 
    def __init__(self, master=None):
        Frame.__init__(self, master)
        root.geometry('800x600')
        self.master.title(u'ImageLabeling')
        self.init()
        self.pack()
 
if __name__ == "__main__":
    app = App()
    app.mainloop()