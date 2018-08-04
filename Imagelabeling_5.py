import sys
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import *
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter,QColor,QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import glob
from PIL import Image

__appname__ = 'Image_labeling'
global ImgList,ImgName
global button1,button2,labelbutton
global Dirpath
global Imgtot,Imgnumber

ImgName = None
Imgtot = 0

sys.setrecursionlimit(10000000)

class Application(QMainWindow,QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(__appname__)

        # UIの初期化
        self.initUI()

        # Figureの初期化
        self.initFigure()

        # ファイルを変更した時のイベント
        ImgList.itemSelectionChanged.connect(self.FileList_Changed)

        # ボタンをクリックした時のイベント
        labelbutton.clicked.connect(self.labelbuttonClicked)

    # UIの初期化
    def initUI(self):
        global ImgList,button1,button2,labelbutton

        # ファイルのリスト
        ImgList = QtWidgets.QListWidget(self)

        # メニューバーの設定
        openFile = QAction('Open', self)
        # ショートカット設定
        openFile.setShortcut('Ctrl+O')
        # ステータスバー設定
        openFile.setStatusTip('フォルダを開く')
        openFile.triggered.connect(self.showDialog_showimage)

        # メニューバー作成
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       

        # Figure用のWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # FigureWidgetにLayoutを追加
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # Marginを消す
        self.FigureLayout.setContentsMargins(0,0,0,0)

        # ラベル作成ボタン用のWidget
        self.LabelButtonWidget = QtWidgets.QWidget(self)
        # LabelButtonWidgetにLayoutを追加
        self.LabelButtonLayout = QtWidgets.QVBoxLayout(self.LabelButtonWidget)
        # Marginを消す
        self.LabelButtonLayout.setContentsMargins(0,0,0,0)

        # 入力フォーム用のWidget
        self.InputWidget = QtWidgets.QWidget(self)
        # InputWidgetにLayoutを追加
        self.InputLayout = QtWidgets.QVBoxLayout(self.InputWidget)
        # Marginを消す
        self.InputLayout.setContentsMargins(0,0,0,0)

        # button用のWidget
        self.ButtonWidget = QtWidgets.QWidget(self)
        # ButtonWidgetにLayoutを追加
        self.ButtonLayout = QtWidgets.QVBoxLayout(self.ButtonWidget)
        # Marginを消す
        self.ButtonLayout.setContentsMargins(0,0,0,0)

        # ボタンを画面に追加
        # ボタンのラベルを設定
        labelbutton = QPushButton('ラベル作成',self)
        #ボタンを配置
        self.LabelButtonLayout.addWidget(labelbutton)

        # 入力フォームを画面に追加
        self.input = QLineEdit()
        self.InputLayout.addWidget(self.input)

        self.statusBar()
 
        # 配置
        #self.setGeometry(0,0,1200,800)
        self.setFixedSize(1200,800)
        ImgList.setGeometry(0,26,200,754)
        self.FigureWidget.setGeometry(300,50,600,600)
        self.ButtonWidget.setGeometry(1000,25,150,625)
        self.InputWidget.setGeometry(1000,650,150,50)
        self.LabelButtonWidget.setGeometry(1025,650,100,120)

    # Figureの初期化
    def initFigure(self):
        # Figureを作成
        self.Figure = plt.figure()
        # FigureをFigureCanvasに追加
        self.FigureCanvas = FigureCanvas(self.Figure)
        # LayoutにFigureCanvasを追加
        self.FigureLayout.addWidget(self.FigureCanvas)

        self.axis = self.Figure.add_subplot(1,1,1)
        plt.axis('off')

    # ファイルを配置
    def set_FileList(self):
        global Imgtot
        # ファイルの読み込み
        Files = glob.glob(self.root+'*.'+self.ext)
        # ソート
        self.Files = sorted(Files)
        Imgtot = len(self.Files)
        #print(Imgtot)

        # ファイルリストに追加
        ImgList.clear()
        for file in self.Files: 
            ImgList.addItem(os.path.basename(file))
        
    # ファイルを変更した時の関数
    def FileList_Changed(self):
        global ImgName

        if len(ImgList) == 1:
            pass
        else:
            # 選択しているファイルの名前を取得
            ImgName = ImgList.selectedItems()[0].text()
            # 画像を読み込み
            self.load_ImageFile()
            # Figureを更新
            self.update_Figure()
            # "表示されている画像番号/画像の総数"の表示
            self.display_Imgnumber()
            self.update()

    # 画像ファイルを読み込む
    def load_ImageFile(self):
        # 画像を開く
        image = Image.open(self.root + ImgName)
        # numpy.ndarrayに
        self.image = np.asarray(image)

    # Figureを更新
    def update_Figure(self):
        self.axis_image = self.axis.imshow(self.image, cmap='gray')
        self.axis_image.set_data(self.image)
        self.FigureCanvas.draw()

    # ラベルボタンクリック後のイベント
    def buttonClicked(self):
        global ImgName
        sender = self.sender()

        #ラベルフォルダにすでに同じ名前の画像があるときのエラー回避のためのif
        if os.path.exists(sender.text() + '/' + ImgName) :
            #pass
            self.statusBar().showMessage('同じ名前の画像ファイルが存在します')
        else:
        # フォルダを選ぶ前にラベルボタンを押した時のエラーを回避するためのif
            if ImgName is None:
                pass
            else:
                shutil.copy(self.root + ImgName,sender.text())

                currIndex = [i for i, e in enumerate(self.Files) if ImgName in e]
                # ラベル付けした画像をリストから消す
                ImgList.takeItem(currIndex[0]) 
                del self.Files[currIndex[0]]
                self.display_Imgnumber()

                # 次のファイルの名前を取得
                if currIndex[0] + 1 < len(ImgList):
                    ImgName = ImgList.item(currIndex[0]).text()

                    # 画像を読み込み
                    self.load_ImageFile()
                    # Figureを更新
                    self.update_Figure()
                    # "表示されている画像番号/画像の総数"の表示
                    self.display_Imgnumber()
                    self.update()

            # ステータスバーへメッセージの表示
            self.statusBar().showMessage(sender.text() + ' が押されました')
 
    #フォルダを開く機能
    def showDialog_showimage(self):
        global Dirpath,ImgName

        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        Dirpath = QFileDialog.getExistingDirectory(self, 'Open Directory', '/home')

        # rootディレクトリ
        self.root = Dirpath + '/'
        # 拡張子
        self.ext = 'bmp'
        #self.ext = 'jpg'

        # ファイルを配置
        self.set_FileList()

        #開いたフォルダに指定した拡張子の画像が無いときのエラー回避のif
        if ImgList.item(0) == None:
            self.statusBar().showMessage('指定した拡張子の画像ファイルが存在しません')
        else:
            # 画像
            ImgName = ImgList.item(0).text()

            # 画像を読み込む
            self.load_ImageFile()

            # Figureを更新
            self.update_Figure()

            # "表示されている画像番号/画像の総数"の表示
            self.display_Imgnumber()
            self.update()    

    # ラベル作成ボタンクリック後のイベント
    def labelbuttonClicked(self):

        #すでに同じ名前のディレクトリがある時のmkdirのエラーを回避するためのif
        if os.path.exists(self.input.text()):
            # ボタンのラベルを設定
            button = QPushButton(self.input.text(),self)
            #ボタンを配置
            self.ButtonLayout.addWidget(button)

            button.clicked.connect(self.buttonClicked)
        elif self.input.text() != "":
            # ボタンのラベルを設定
            button = QPushButton(self.input.text(),self)
            #ボタンを配置
            self.ButtonLayout.addWidget(button)

            os.mkdir(self.input.text())
            button.clicked.connect(self.buttonClicked)
        else:
            pass

        self.input.clear()
    
    # Enterキーを押すとラベル作成ボタンが押されるようにする
    def keyPressEvent(self,e):

       if e.key() == Qt.Key_Return:
           # labelbuttonClickedと同じ文
           if os.path.exists(self.input.text()):
               button = QPushButton(self.input.text(),self)
               self.ButtonLayout.addWidget(button)

               button.clicked.connect(self.buttonClicked)
           else:
               button = QPushButton(self.input.text(),self)
               self.ButtonLayout.addWidget(button)

               os.mkdir(self.input.text())
               button.clicked.connect(self.buttonClicked)

       self.input.clear()

    # "表示されている画像のindex/画像の総数","画像のファイル名"の表示
    def paintEvent(self,event):
        qp = QPainter(self)
        self.settingText(event,qp)

    def settingText(self,event,qp):
        qp.setFont(QFont(u'メイリオ',15,QFont.Bold,False))
        if Imgtot == 0 :
            pass
        else:
            display_number = str(Imgnumber) + '/' + str(Imgtot) 
            qp.drawText(575,750,display_number)
            qp.drawText(300,700,'ファイル名：' + ImgName)

    def display_Imgnumber(self):
        global Imgtot,Imgnumber
        if len(ImgList) == 0:
            pass
        else:
            #Imgtot = len(ImgList)
            currIndex = [i for i, e in enumerate(self.Files) if ImgName in e]
            Imgnumber = currIndex[0] + 1

QApp = QtWidgets.QApplication(sys.argv)
app = Application()
app.show()
sys.exit(QApp.exec_())