# -*- coding: utf-8 -*-

import sys
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OGmeituan import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import xlwt


import pythread
import copy
from insert2mysql import Write2mysql




class ChildWindow(QMainWindow, Ui_MainWindow):
    """
    创建窗口
    界面树依赖OGmeituan.py QT基础知识。
    """
    close_singnal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

        self.thread = MyThread()
        self.thread.result_thread.connect(self.showtable)
        # self.thread.result_thread.connect(self.savemysql)
        self.thread.error_thread.connect(self.showerror)
        self.thread.state_thread.connect(self.not_click)
        self.Write2mysql = Write2mysql()

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '确认',
                                               "程序爬取的内容需要右下角手动保存!!\n是否确认退出？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.thread.stop_thread()
            self.close_singnal.emit("sayasora")
        else:
            event.ignore()


    def initUI(self):
        #子窗口名字修改
        self.setWindowTitle("欢迎使用美团美食的爬取程序")
        #子窗口最大化
        # self.showMaximized()
        self.textBrowser_3.append("欢迎使用美团美食的爬取程序，请设置爬虫参数\r")

        # 设置表格
        self.model = QStandardItemModel(0, 10)
        # 设置水平方向十个头标签文本内容
        self.model.setHorizontalHeaderLabels(
            ['页码', '个数', '店名', '店铺编号', '评分', '评论数', '地址', '人均消费', '是否为广告', '商品图片']
        )

        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.model)
        self.horizontalLayout_3.addWidget(self.tableView)

        #本程序不需要导入数据
        self.pushButton_8.setEnabled(False)
        # 存储所有相关数据为列表
        self.alldata = []
        #定义接口数据
        self.interface_data = []
        self.interface_data_state = True
        self.pushButton_1.clicked.connect(lambda: self.check_data())

        #更改swichbtn状态
        self.select_btn = 1
        self.select_btn_translate = "综合默认"
        self.radioButton_1.setChecked(True)
        self.radioButton_1.clicked.connect(lambda: self.selectbtn(1))
        self.radioButton_2.clicked.connect(lambda: self.selectbtn(2))
        self.radioButton_3.clicked.connect(lambda: self.selectbtn(3))

        #价格 页码可输入范围
        self.spinBox_3.setRange(1, 67)
        self.spinBox_4.setRange(1, 67)

        #创建导入导出文件位置
        self.in_address = ""
        self.out_address = ""
        self.pushButton_8.clicked.connect(self.getfile)
        self.pushButton_9.clicked.connect(self.savefile)

        #设置开始按钮
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.clicked.connect(self.start_btn)

        #设置中止按钮
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.clicked.connect(self.main_stop_thread)

        #设置清空参数按钮
        self.pushButton_2.clicked.connect(self.clean_frame_6)

        #设置清除提示窗口
        self.pushButton_3.clicked.connect(self.clean_textBrowser_3)

        #数据保存按钮，保存为excel
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.clicked.connect(self.save_excel)
        #数据存入数据库操作
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.clicked.connect(self.savemysql)
        #数据分析结果
        self.pushButton_10.setEnabled(False)
        self.pushButton_10.clicked.connect(self.showdata)
    #选择商品排序槽函数
    def selectbtn(self, i):
        self.select_btn = i
        #翻译按钮
        self.translate_radio(i)

    #导入文件按钮槽函数
    def getfile(self):
        a = QFileDialog.getOpenFileName(self, '请选择要打开的文件', 'meituan', "Data files (*.xlsx *.xls *.csv)")
        self.pushButton_8.setText(a[0])
        self.in_address = a[0]

    #导出文件按钮槽函数
    def savefile(self):
        a = QFileDialog.getSaveFileName(self, '请选择要保存的位置', 'meituan', "Data files (*.xls)")
        self.pushButton_9.setText(a[0])
        self.out_address = a[0]

    #状态选择翻译
    def translate_radio(self, i):
        a = {"1": "默认排序", "2": "销量最多", "3": "好评最多"}
        self.select_btn_translate = a[str(i)]

    #清空参数函数
    def clean_frame_6(self):
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.spinBox_3.setValue(1)
        self.spinBox_4.setValue(1)
        self.pushButton_9.setText("点击选择")
        self.out_address = ''

        self.textBrowser_3.append("已成功清除参数\r")

    #清除提示窗口函数
    def clean_textBrowser_3(self):
        self.textBrowser_3.clear()

    #检查按钮对应槽函数
    def check_data(self):
        if self.pushButton_1.text() == "取消":
            self.frame_6.setEnabled(True)
            self.pushButton_1.setText("检查参数")
            self.pushButton_4.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.textBrowser_3.append("请重新输入需要修改的参数\r")
        else:
            self.interface_data = [self.comboBox_3.currentText(), self.select_btn, self.comboBox_4.currentText(), self.comboBox_5.currentText(), self.spinBox_3.text(), self.spinBox_4.text(), self.in_address, self.out_address]
            print(self.interface_data)
            if int(self.interface_data[4]) > int(self.interface_data[5]):
                self.textBrowser_3.append("商品页码搜索区间有误\r")
                self.interface_data_state = False
            if self.interface_data[7] == "":
                self.textBrowser_3.append("请设置导出文件的位置\r")
                self.interface_data_state = False

            self.textBrowser_1.setText(
                "选择城市：" + self.interface_data[0] +
                "\r\r搜索规则：" + self.select_btn_translate +
                "\r\r搜索区域：" + self.interface_data[2] +
                "\r\r用餐人数：" + self.interface_data[3] +
                "\r\r搜索页数：" + self.interface_data[4] + " 到 " + self.interface_data[5] + " 页" +
                "\r\r导入位置：" + self.interface_data[6] +
                "\r\r导出位置：" + self.interface_data[7]
            )

            if self.interface_data_state:
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(False)
                self.frame_6.setEnabled(False)
                self.pushButton_1.setText("取消")
                self.textBrowser_3.append("爬虫参数设置无误，准备开始\r")
            else:
                self.pushButton_4.setEnabled(False)

            self.interface_data_state = True

    #开始按钮槽函数
    def start_btn(self):

        #准备创建Excel
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('Sheet1', cell_overwrite_ok=True)
        a = ['title', 'poiId', 'avgScore', 'allCommentNum', 'address', 'avgPrice', 'hasAds', 'frontImg']
        for i in range(len(a)):
            self.sheet.write(0, i, a[i])

        # 设置变量excel排数
        self.book_row = 1

        # #清空表格
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            ['页码', '个数', '店名', '店铺编号', '评分', '评论数', '地址', '人均消费', '是否为广告', '商品图片']
        )

        #开启另一个线程
        self.thread.setidentity(self.interface_data)
        self.thread.start()

    def main_stop_thread(self):
        print("main_stop_thread")
        self.textBrowser_3.append("正在中止程序，请稍等...\r")
        self.pushButton_5.setEnabled(False)
        self.thread.stop_thread()


    #显示表格函数
    def showtable(self, a):
        line = {}
        self.model.appendRow(
            [QStandardItem(str(a["page"])),
             QStandardItem(str(a["x"])),
             QStandardItem(str(a["title"])),
             QStandardItem(str(a["poiId"])),
             QStandardItem(str(a["avgScore"])),
             QStandardItem(str(a["allCommentNum"])),
             QStandardItem(str(a["address"])),
             QStandardItem(str(a["avgPrice"])),
             QStandardItem(str(a["hasAds"])),
             QStandardItem(str(a["frontImg"]))
             ]
        )

        if a['hasAds'] == True:
            a['hasAds'] = 1.0
        else:
            a['hasAds'] = 2.0
        self.sheet.write(self.book_row, 0, a["title"])
        self.sheet.write(self.book_row, 1, a["poiId"])
        self.sheet.write(self.book_row, 2, a["avgScore"])
        self.sheet.write(self.book_row, 3, a["allCommentNum"])
        self.sheet.write(self.book_row, 4, a["address"])
        self.sheet.write(self.book_row, 5, a["avgPrice"])
        self.sheet.write(self.book_row, 6, a["hasAds"])
        self.sheet.write(self.book_row, 7, a["frontImg"])

        self.book_row = self.book_row + 1

        self.alldata.append(a)
    #显示报错
    def showerror(self, a):
        self.textBrowser_3.append(a)
    def del_item(self,data):
        for c in ['x','page']:
            try:
                del data[c]
            except:
                pass
        try:
         data['dealList'] = str(data['dealList'])
        except:
            pass

        return data

    def savemysql(self):
        # 保存内容到数据库
        count = 0
        self.textBrowser_3.append("正在保存到mysql，耐心等待")
        for i,data in enumerate(self.alldata):
            self.textBrowser_3.append("正在保存第{}条".format(i + 1))
            data = self.del_item(data)
            print(data)
            self.Write2mysql.processitem(data)
            self.pushButton_7.setEnabled(False)
            count =i
        self.textBrowser_3.append("数据全部保存到mysql,共{}条： ".format(count+1))
    def showdata(self):
        # 显示数据分析结果
        import os
        from pltimg import save_image
        self.textBrowser_3.append("图标生成中，耐心等待")
        # 生成分析图像
        data_anlyize = save_image("./meituan.xls")
        data_anlyize.save_all()
        # 调用另外界面展示分析结果
        os.system("python OGimg.py")
        self.pushButton_10.setEnabled(False)

    #子线程状态，按钮禁用
    def not_click(self, a):
        if a == 1:
            self.pushButton_1.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(True)
            self.pushButton_10.setEnabled(True)
            self.pushButton_5.setEnabled(True)
        else:
            self.pushButton_1.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.pushButton_10.setEnabled(True)
            self.pushButton_5.setEnabled(False)

    #确认保存为excel函数
    def save_excel(self):
        self.book.save(self.interface_data[7])
        self.textBrowser_3.append("已经成功保存到"+self.interface_data[7]+'\r')
        self.pushButton_6.setEnabled(False)
    #存入数据库




class MyThread(QThread):

    #定义thread信号,传递结果字典
    result_thread = pyqtSignal(dict)
    error_thread = pyqtSignal(str)
    state_thread = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

        self.identity = []
        self.working = True

    def stop_thread(self):
        self.working = False
#
    def setidentity(self, list):
        self.identity = list

    def translate_list(self, list):
        """
        字段声明
        通过不同字段可以构建不同的URL
        """
        b = [None, None, None, None, None, None, None, None]

        # 商品分类参数
        cs = ["cd"]
        b[0] = cs[0]

        # 商品搜索规则
        gz = ["", "sales", "rating"]
        b[1] = gz[list[1] - 1]

        # 商品区域
        qu = {
            "武侯区": "b38", "青羊区": "b36", "成华区": "b37", "金牛区": "b35", "锦江区": "b34", "郫县": "b3805",
            "温江区": "b3798", "龙泉驿区": "b3795", "青白江区": "b3796", "彭州市": "b3800", "新津县": "b3808", "都江堰市": "b3799",
            "新都区": "b3797", "邛崃市": "b3801", "崇州市": "b3802", "金堂县": "b3803", "大邑县": "b3806", "蒲江县": "b3807",
            "简阳市": "b3906", "高新区": "b5895", "双流区": "b5896", "不限": ""
        }
        b[2] = qu[list[2]]

        # 商品人数
        rs = {
            "单人餐": "?attrs=65:152", "双人餐": "?attrs=65:152", "3-4人": "?attrs=65:152", "5-6人": "?attrs=65:152",
            "7-8人": "?attrs=65:152", "9-10人": "?attrs=65:152", "10人以上": "?attrs=65:152", "其他": "?attrs=65:152",
            "不限": ""
        }
        b[3] = rs[list[3]]

        b[4] = list[4]
        b[5] = list[5]
        b[6] = list[6]
        b[7] = list[7]
        print(b)
        return b

    def get_commemts(self, text, page):
        """

        :param text: 传入已爬取的数据 进行字段提取
        :param page: 页码
        :return:
        """
        self.error_thread.emit("需爬取 " + str(self.identity[5]) + " 页，正在爬取第 " + str(page+1) + " 页\r")
        json_str = re.findall(r'poiInfos":(.*?)},"comHeader', text, re.S)
        json_str = json_str[0].replace("false", "False")
        json_str = json_str.replace("true", "True")
        food_list = eval(json_str)
        gs = 1
        for x in food_list:
            x.update({"page": page, "x": gs})
            gs = gs + 1
            self.result_thread.emit(x)
        return food_list


    def run(self):
        """
        :pythread为多线程爬取类获取所有爬取结果
        :遍历后展示在页面上
        :return:
        """
        content = pythread.get_data(int(self.identity[5]))
        for i,text in enumerate(content):
            # print(i,text)
            if self.get_commemts(text, i) == []:
                self.error_thread.emit("此页商品数目不足,，或超过筛选条件页数，请扩大筛选条件或减少搜索页数。\r")
                break

            if self.working == False:
                break
        if self.working:
            self.error_thread.emit("已完成爬取\r")
        else:
            self.error_thread.emit("已中止程序\r")
            self.working = True
        # 信号量传递，，爬取数据通过线程传给主界面
        self.state_thread.emit(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ChildWindow()
    form.show()
    sys.exit(app.exec_())