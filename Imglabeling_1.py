import sys
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import glob
from PIL import Image

__appname__ = 'Image_labeling'

class Application(QMainWindow,QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(__appname__)

        # UIの初期化
        self.initUI()

        # rootディレクトリ
        self.root = 'とり/'
        # 拡張子
        self.ext = 'jpg'

        # ファイルを配置
        self.set_FileList()

        # 画像
        global ImgName,ImgList
        ImgName = ImgList.item(0).text()

        # 画像を読み込む
        self.load_ImageFile()

        # Figureの初期化
        self.initFigure()

        # ファイルを変更した時のイベント
        ImgList.itemSelectionChanged.connect(self.FileList_Changed)

        # ボタンをクリックした時のイベント
        global button1,button2
        button1.clicked.connect(self.buttonClicked)
        button2.clicked.connect(self.buttonClicked)

    # UIの初期化
    def initUI(self):
        # Figure用のWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # FigureWidgetにLayoutを追加
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # Marginを消す
        self.FigureLayout.setContentsMargins(0,0,0,0)

        # button用のWidget
        self.ButtonWidget = QtWidgets.QWidget(self)
        # ButtonWidgetにLayoutを追加
        self.ButtonLayout = QtWidgets.QVBoxLayout(self.ButtonWidget)
        # Marginを消す
        self.ButtonLayout.setContentsMargins(0,0,0,0)

        # ボタンを画面に追加
        # ボタンのラベルを設定
        global button1,button2
        button1 = QPushButton('ひよこ',self)
        button2 = QPushButton('にわとり',self)
        #ボタンを配置
        self.ButtonLayout.addWidget(button1)
        self.ButtonLayout.addWidget(button2)

        self.statusBar()
        # ファイルのリスト
        global ImgList
        ImgList = QtWidgets.QListWidget(self)

        # 配置
        self.setGeometry(0,0,1200,800)
        ImgList.setGeometry(0,0,200,770)
        self.FigureWidget.setGeometry(200,0,800,770)
        self.ButtonWidget.setGeometry(1000,0,200,770)

    # Figureの初期化
    def initFigure(self):
        # Figureを作成
        self.Figure = plt.figure()
        # FigureをFigureCanvasに追加
        self.FigureCanvas = FigureCanvas(self.Figure)
        # LayoutにFigureCanvasを追加
        self.FigureLayout.addWidget(self.FigureCanvas)

        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis_image = self.axis.imshow(self.image, cmap='gray')
        plt.axis('off')

    # ファイルを配置
    def set_FileList(self):
        # ファイルの読み込み
        Files = glob.glob(self.root+'*.'+self.ext)
        # ソート
        self.Files = sorted(Files)

        # ファイルリストに追加
        global ImgList
        for file in self.Files: 
            ImgList.addItem(os.path.basename(file))

    # ファイルを変更した時の関数
    def FileList_Changed(self):
        global ImgName,ImgList
        # 選択しているファイルの名前を取得
        ImgName = ImgList.selectedItems()[0].text()
        # 画像を読み込み
        self.load_ImageFile()
        # Figureを更新
        self.update_Figure()

    # 画像ファイルを読み込む
    def load_ImageFile(self):
        global ImgName
        # 画像を開く
        image = Image.open(self.root + ImgName)
        # numpy.ndarrayに
        self.image = np.asarray(image)

    # Figureを更新
    def update_Figure(self):
        self.axis_image.set_data(self.image)
        self.FigureCanvas.draw()

    # ボタンクリック後のイベント
    def buttonClicked(self):
        global ImgName,ImgList
        sender = self.sender()
        shutil.copy(self.root + ImgName,sender.text())

        print(self.Files)
        # 次のファイルの名前を取得
        currIndex = [i for i, e in enumerate(self.Files) if ImgName in e]
        print(currIndex)

        if currIndex[0] + 1 < len(ImgList):
            ImgName = ImgList.item(currIndex[0] + 1).text()

            # 画像を読み込み
            self.load_ImageFile()
            # Figureを更新
            self.update_Figure()

        # ステータスバーへメッセージの表示
        self.statusBar().showMessage(sender.text() + ' was pressed')        

QApp = QtWidgets.QApplication(sys.argv)
app = Application()
app.show()
sys.exit(QApp.exec_())