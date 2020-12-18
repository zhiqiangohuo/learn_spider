import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class picture(QWidget):
    def __init__(self,img_path=None):
        super(picture, self).__init__()
        if img_path:
            self.img_path = img_path
        else:
            self.img_path = './'
        self.resize(1500, 1000)
        self.setWindowTitle("label显示图片")

        self.label = QLabel(self)
        self.label.setText("   显示图片")
        self.label.setFixedSize(1000, 500)
        self.label.move(160, 160)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(255,255,255,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        btn = QPushButton(self)
        btn1 = QPushButton(self)
        btn2 = QPushButton(self)
        btn.setText("热力图")
        btn1.setText("评价分布直方图")
        btn2.setText("广告散点图")
        btn.move(10, 30)
        btn1.move(10, 60)
        btn2.move(10, 90)
        btn.clicked.connect(self.openimage)
        btn1.clicked.connect(self.hist)
        btn2.clicked.connect(self.scatter)
    def openimage(self):
        imgName = self.img_path+"img/hot.png"
        imgType ='png'
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
    def hist(self):
        imgName = self.img_path+"img/hist.png"
        imgType ='png'
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
    def scatter(self):
        imgName = self.img_path+"img/scatter.png"
        imgType ='png'
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    sys.exit(app.exec_())
