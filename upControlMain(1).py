import re
import sys
import os
import time
import binascii
import pyqtgraph as pg
import numpy as np
import array
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QDate

index = 0
in_mn = 0
in_kg = 0
alarm = 0
halve = 0
data = array.array('d')  # 可动态改变数组的大小,double型数组
horizontalLength = 120      # 横坐标长度
idx = 0
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(800, 900)
        font = QtGui.QFont()
        font.setFamily("SimHei")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        Form.setFont(font)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Form.setMouseTracking(False)
        Form.setStyleSheet("color: rgb(25, 25, 25);""background-color: rgb(240, 240, 240);""font: 11pt \"SimHei\";")
        # 接收区域标题
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(420, 285, 80, 25))  #430, 350, 251, 181
        self.label1.setObjectName("label1")
        # 发送区域标题
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(40, 285, 80, 25))
        self.label2.setTextFormat(QtCore.Qt.AutoText)
        self.label2.setObjectName("label2")
        # 发送按钮
        self.SendButton = QtWidgets.QPushButton(Form)
        self.SendButton.setGeometry(QtCore.QRect(300, 285, 80, 25))
        self.SendButton.setObjectName("SendButton")
        # 清除按钮
        self.ClearButton = QtWidgets.QPushButton(Form)
        self.ClearButton.setGeometry(QtCore.QRect(680, 285, 80, 25))
        self.ClearButton.setObjectName("ClearButton")
        # 接收区域框
        self.textEdit_Recive = QtWidgets.QTextEdit(Form)
        self.textEdit_Recive.setGeometry(QtCore.QRect(420, 310, 350, 200))
        self.textEdit_Recive.setStyleSheet("background-color: rgb(230, 230, 230);""background-color: rgb(230, 230, 230);")
        self.textEdit_Recive.setObjectName("textEdit_Recive")
        # 发送区域框
        self.textEdit_Send = QtWidgets.QTextEdit(Form)
        self.textEdit_Send.setGeometry(QtCore.QRect(30, 310, 350, 200))
        self.textEdit_Send.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.textEdit_Send.setObjectName("textEdit_Send")

        # 构建一个表格
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 180, 700, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # 串口刷新 标题
        self.ComRefreshLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComRefreshLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComRefreshLabel.setObjectName("ComRefreshLabel")
        self.gridLayout.addWidget(self.ComRefreshLabel, 0, 0, 1, 1)
        # 串口刷新 按钮
        self.ComRefreshButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ComRefreshButton.setObjectName("ComRefreshButton")
        self.gridLayout.addWidget(self.ComRefreshButton, 1, 0, 1, 1)

        # 波特率设置 标题
        self.ComBaudLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComBaudLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComBaudLabel.setObjectName("ComBaudLabel")
        self.gridLayout.addWidget(self.ComBaudLabel, 0, 2, 1, 1)
        # 波特率设置 下拉菜单
        self.ComBaudCombo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.ComBaudCombo.setEditable(True)
        self.ComBaudCombo.setDuplicatesEnabled(False)
        self.ComBaudCombo.setModelColumn(0)
        self.ComBaudCombo.setObjectName("ComBaudCombo")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.ComBaudCombo.addItem("")
        self.gridLayout.addWidget(self.ComBaudCombo, 1, 2, 1, 1)

        # 串口选择 标题
        self.ComNameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComNameLabel.setObjectName("ComNameLabel")
        self.gridLayout.addWidget(self.ComNameLabel, 0, 1, 1, 1)
        # 串口选择 下拉菜单
        self.Com_Name_Combo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.Com_Name_Combo.setObjectName("ComNameCombo")
        self.gridLayout.addWidget(self.Com_Name_Combo, 1, 1, 1, 1)

        # 串口操作 标题
        self.ComStateLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComStateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComStateLabel.setObjectName("ComStateLabel")
        self.gridLayout.addWidget(self.ComStateLabel, 0, 3, 1, 1)
        # 串口打开 按钮
        self.ComOpenButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ComOpenButton.setObjectName("Com_Open_Button")
        self.gridLayout.addWidget(self.ComOpenButton, 0, 4, 1, 1)
        # 关闭 按钮
        self.ComCloseButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ComCloseButton.setDefault(False)
        self.ComCloseButton.setObjectName("ComCloseButton")
        self.gridLayout.addWidget(self.ComCloseButton, 1, 4, 1, 1)
        # 打开/关闭 标题
        self.Com_isOpenOrNot_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Com_isOpenOrNot_Label.setText("")
        self.Com_isOpenOrNot_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Com_isOpenOrNot_Label.setObjectName("Com_isOpenOrNot_Label")
        self.gridLayout.addWidget(self.Com_isOpenOrNot_Label, 1, 3, 1, 1)


        # 以16进制发送 选择框
        self.hexSending_checkBox = QtWidgets.QCheckBox(Form)
        self.hexSending_checkBox.setGeometry(QtCore.QRect(140, 285, 140, 25))
        self.hexSending_checkBox.setObjectName("hexSending_checkBox")
        # 以16进制显示 选择框
        self.hexShowing_checkBox = QtWidgets.QCheckBox(Form)
        self.hexShowing_checkBox.setGeometry(QtCore.QRect(520, 285, 140, 25))
        self.hexShowing_checkBox.setObjectName("hexShowing_checkBox")

        self.figure = QtWidgets.QLabel(Form)
        self.figure.setGeometry(QtCore.QRect(20, 10, 100, 105))
        self.figure.setText("")
        self.figure.setObjectName("figure1")
        cover_img = os.path.abspath('resource/figure1.jpeg')
        image = QtGui.QPixmap(cover_img).scaled(100, 105)
        self.figure.setPixmap(image)

        self.figure2 = QtWidgets.QLabel(Form)
        self.figure2.setGeometry(QtCore.QRect(130, 10, 650, 105))
        self.figure2.setText("")
        self.figure2.setObjectName("figure1")
        cover_img = os.path.abspath('resource/figure2.png')
        image = QtGui.QPixmap(cover_img).scaled(650, 105)
        self.figure2.setPixmap(image)
        # 日历
        # self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        # self.calendarWidget.setGeometry(QtCore.QRect(430, 350, 251, 181))
        # self.calendarWidget.setStyleSheet("alternate-background-color: rgb(0, 0, 0);""background-color: rgb(0, 0, 0);")
        # self.calendarWidget.setFirstDayOfWeek(QtCore.Qt.Sunday)
        # self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        # self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.ISOWeekNumbers)
        # self.calendarWidget.setObjectName("calendarWidget")

        # 时间显示
        self.TimeLabel = QtWidgets.QLabel(Form)
        self.TimeLabel.setGeometry(QtCore.QRect(150, 130, 150, 20))
        self.TimeTitle = QtWidgets.QLabel(Form)
        self.TimeTitle.setGeometry(QtCore.QRect(20, 130, 130, 20))
        # 时间显示 字体定义
        font1 = QtGui.QFont()
        font1.setFamily("SimSun")
        font1.setPointSize(2)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setWeight(500)
        self.TimeLabel.setFont(font1)
        self.TimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TimeLabel.setObjectName("TimeLabel")
        self.TimeTitle.setFont(font1)
        self.TimeTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.TimeTitle.setObjectName("TimeTitle")

        self.AuthorLabel = QtWidgets.QLabel(Form)
        self.AuthorLabel.setGeometry(QtCore.QRect(340, 130, 420, 20))


        # 关于 按钮
        self.AboutButton = QtWidgets.QPushButton(Form)
        self.AboutButton.setGeometry(QtCore.QRect(200, 520, 400, 30))
        # 关于 按钮 字体定义
        font = QtGui.QFont()
        font.setFamily("SimSun")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.AboutButton.setFont(font)
        self.AboutButton.setObjectName("AboutButton")

        # changed!!!
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 550, 800, 350))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.plot_view = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.plot_view.setContentsMargins(0, 0, 0, 0)
        self.plot_view.setObjectName("plot_view")
        #self.plot_view.setStyleSheet("background-color: rgb(230, 230, 230);")
        pg.setConfigOption('background', '#F0F0F0')
        pg.setConfigOption('foreground', 'k')
        win = pg.GraphicsLayoutWidget()  # 建立窗口
        win.setStyleSheet("background-color: rgb(20, 20, 20);")
        data = array.array('d')  # 可动态改变数组的大小,double型数组
        horizontalLength = 120  # 横坐标长度
        p = win.addPlot()  # 把图p加入到窗口中
        p.showGrid(x=True, y=True)  # 把X和Y的表格打开
        p.setRange(xRange=[0, horizontalLength], yRange=[0, 255], padding=0)
        p.setLabel(axis='left', text='y / V')  # 靠左
        p.setLabel(axis='bottom', text='x / point')
        p.setTitle('波形曲线监控区域')  # 表格的名字
        self.curve = p.plot()  # 绘制一个图形
        self.plot_view.addWidget(win)

        self.retranslateUi(Form)
        self.ClearButton.clicked.connect(self.textEdit_Recive.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "计算机系统综合设计：第7组 串口通信工具"))
        self.label1.setText(_translate("Form", "接收区域"))
        self.label2.setText(_translate("Form", "发送区域"))
        self.SendButton.setText(_translate("Form", "发送"))
        self.ClearButton.setText(_translate("Form", "清除"))
        self.textEdit_Recive.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimHei\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\';\"><br /></p></body></html>"))
        self.ComBaudLabel.setText(_translate("Form", "波特率设置"))
        self.ComCloseButton.setText(_translate("Form", "关闭"))
        self.ComNameLabel.setText(_translate("Form", "串口选择"))
        self.ComRefreshLabel.setText(_translate("Form", "串口刷新"))
        self.ComRefreshButton.setText(_translate("Form", "刷新"))
        self.ComStateLabel.setText(_translate("Form", "串口操作"))
        self.ComBaudCombo.setCurrentText(_translate("Form", "9600"))
        self.ComBaudCombo.setItemText(0, _translate("Form", "1200"))
        self.ComBaudCombo.setItemText(1, _translate("Form", "2400"))
        self.ComBaudCombo.setItemText(2, _translate("Form", "4800"))
        self.ComBaudCombo.setItemText(3, _translate("Form", "9600"))
        self.ComBaudCombo.setItemText(4, _translate("Form", "14400"))
        self.ComBaudCombo.setItemText(5, _translate("Form", "19200"))
        self.ComBaudCombo.setItemText(6, _translate("Form", "38400"))
        self.ComBaudCombo.setItemText(7, _translate("Form", "43000"))
        self.ComBaudCombo.setItemText(8, _translate("Form", "57600"))
        self.ComBaudCombo.setItemText(9, _translate("Form", "76800"))
        self.ComBaudCombo.setItemText(10, _translate("Form", "115200"))
        self.ComBaudCombo.setItemText(11, _translate("Form", "128000"))
        self.ComBaudCombo.setItemText(12, _translate("Form", "230400"))
        self.ComBaudCombo.setItemText(13, _translate("Form", "256000"))
        self.ComBaudCombo.setItemText(14, _translate("Form", "460800"))
        self.ComBaudCombo.setItemText(15, _translate("Form", "921600"))
        self.ComBaudCombo.setItemText(16, _translate("Form", "1382400"))
        self.ComOpenButton.setText(_translate("Form", "打开"))
        self.hexSending_checkBox.setText(_translate("Form", "以16进制发送"))
        self.hexShowing_checkBox.setText(_translate("Form", "以16进制显示"))
        self.TimeLabel.setText(_translate("Form", "Time"))
        self.TimeTitle.setText(_translate("Form", "Beijing Time："))
        self.AboutButton.setText(_translate("Form", "Github: Click here to get the source code"))
        self.AuthorLabel.setText(_translate("Form", "Author:尚修为、胡聿鑫、林宇丰、王佳玉、海塞姆"))

    def plotData(self):
        global idx#内部作用域想改变外部域变量
        #tmp = np.cos(np.pi / 50)* idx
        #tmp = in_mn * idx
        tmp = np.sin(np.pi / 50 * idx)*in_mn
        if tmp >= 0:
            if len(data)<horizontalLength:
                data.append(in_mn)
            else:
                data[:-1] = data[1:]#前移
                data[-1] = tmp
        self.curve.setData(data)
        idx = idx + 1

class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置实例
        self.CreateItems()
        # 设置信号与槽
        self.CreateSignalSlot()
        # changed!!!
        my_timer = QTimer(self)
        my_timer.timeout.connect(self.plotData)  # 定时调用plotData函数
        my_timer.start(50)  # 多少ms调用一次

    # 设置实例
    def CreateItems(self):
        # Qt 串口类
        self.com = QSerialPort()
        # Qt 定时器类
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.ShowTime)  # 计时结束调用operate()方法
        self.timer.start(100)  # 设置计时间隔 100ms 并启动

    # 设置信号与槽
    def CreateSignalSlot(self):
        self.ComOpenButton.clicked.connect(self.Com_Open_Button_clicked)
        self.ComCloseButton.clicked.connect(self.Com_Close_Button_clicked)
        self.SendButton.clicked.connect(self.SendButton_clicked)
        self.ComRefreshButton.clicked.connect(self.Com_Refresh_Button_Clicked)
        self.com.readyRead.connect(self.Com_Receive_Data)  # 接收数据
        self.hexSending_checkBox.stateChanged.connect(self.hexShowingClicked)
        self.hexSending_checkBox.stateChanged.connect(self.hexSendingClicked)
        self.AboutButton.clicked.connect(self.Goto_GitHub)

    # 跳转到 GitHub 查看源代码
    def Goto_GitHub(self):
        self.browser = QWebEngineView()
        self.browser.load(QUrl('https://github.com/Oslomayor/PyQt5-SerialPort-Stable'))
        self.setCentralWidget(self.browser)

    # 显示时间
    def ShowTime(self):
        self.TimeLabel.setText(time.strftime("%B %d, %H:%M:%S", time.localtime()))

        # 串口发送数据

    def Com_Send_Data(self):
        global halve
        global alarm
        # 优先处理报警
        if alarm == 1:
            txData = str(8)
            alarm = 0

        # 处理减半或正常读取
        else:
            if halve == 1:
                txData = str(in_mn / 2 + 128)
            else:  # 从命令窗口取命令
                # 根据命令判断是否减半,txData字符串类型
                txData = self.textEdit_Send.toPlainText()
                if int(txData) >> 4 == 1:
                    halve = 1

        if len(txData) == 0:
            return
        if self.hexSending_checkBox.isChecked() == False:
            self.com.write(txData.encode('UTF-8'))
        else:
            Data = txData.replace(' ', '')
            # 如果16进制不是偶数个字符, 去掉最后一个, [ ]左闭右开
            if len(Data) % 2 == 1:
                Data = Data[0:len(Data) - 1]
            # 如果遇到非16进制字符
            if Data.isalnum() is False:
                QMessageBox.critical(self, '错误', '输入非十六进制数')
            try:
                hexData = binascii.a2b_hex(Data)
            except:
                QMessageBox.critical(self, '错误', '转换编码错误')
                return
            # 发送16进制数据, 发送格式如 ‘31 32 33 41 42 43’, 代表'123ABC'
            try:
                self.com.write(hexData)
            except:
                QMessageBox.critical(self, '异常', '发送十六进制错误')
                return

                # 串口接收数据
                # 一直收没停止过，循环读取并组装，最后判断报警or传数据

    def Com_Receive_Data(self):
        global index
        global in_mn
        global in_kg
        global alarm
        try:
            rxData = bytes(self.com.readAll())
        except:
            QMessageBox.critical(self, '严重错误', '串口接收数据错误')
        if self.hexShowing_checkBox.isChecked() == False:
            try:

                self.textEdit_Recive.insertPlainText(rxData.decode('UTF-8'))
                if index >= 1 and index <= 3:
                    in_mn = in_mn * 10 + int(rxData.decode('UTF-8'))

                if index == 5:
                    in_kg = int(rxData.decode("utf-8"))

                if index < 7:
                    index = index + 1
                # 采集完毕
                else:
                    # print(in_mn,"-",in_kg)
                    # print("alarm:", alarm, "mn:", in_mn)
                    # 优先处理报警
                    if in_mn > 260 or halve == 1:
                        alarm = 1
                        self.Com_Send_Data()
                    in_kg = 0
                    in_mn = 0
                    index = 0
            except:
                pass
        else:
            Data = binascii.b2a_hex(rxData).decode('ascii')
            # re 正则表达式 (.{2}) 匹配两个字母
            hexStr = ' 0x'.join(re.findall('(.{2})', Data))
            # 补齐第一个 0x
            hexStr = '0x' + hexStr
            self.textEdit_Recive.insertPlainText(hexStr)
            self.textEdit_Recive.insertPlainText(' ')
    # 串口刷新
    def Com_Refresh_Button_Clicked(self):
        self.Com_Name_Combo.clear()
        com = QSerialPort()
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            com.setPort(info)
            if com.open(QSerialPort.ReadWrite):
                self.Com_Name_Combo.addItem(info.portName())
                com.close()

    # 16进制显示按下
    def hexShowingClicked(self):
        if self.hexShowing_checkBox.isChecked() == True:
            # 接收区换行
            self.textEdit_Recive.insertPlainText('\n')

    # 16进制发送按下
    def hexSendingClicked(self):
        if self.hexSending_checkBox.isChecked() == True:
            pass

    # 发送按钮按下
    def SendButton_clicked(self):
        self.Com_Send_Data()

    # 串口刷新按钮按下
    def Com_Open_Button_clicked(self):
        #### com Open Code here ####
        comName = self.Com_Name_Combo.currentText()
        comBaud = int(self.ComBaudCombo.currentText())
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critical(self, '严重错误', '串口打开失败')
                return
        except:
            QMessageBox.critical(self, '严重错误', '串口打开失败')
            return
        self.ComCloseButton.setEnabled(True)
        self.ComOpenButton.setEnabled(False)
        self.ComRefreshButton.setEnabled(False)
        self.Com_Name_Combo.setEnabled(False)
        self.ComBaudCombo.setEnabled(False)
        self.Com_isOpenOrNot_Label.setText('  已打开')
        self.com.setBaudRate(comBaud)

    def Com_Close_Button_clicked(self):
        self.com.close()
        self.ComCloseButton.setEnabled(False)
        self.ComOpenButton.setEnabled(True)
        self.ComRefreshButton.setEnabled(True)
        self.Com_Name_Combo.setEnabled(True)
        self.ComBaudCombo.setEnabled(True)
        self.Com_isOpenOrNot_Label.setText('  已关闭')

if __name__ == '__main__':


    app1 = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()

    # app = QtWidgets.QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    # ui = Ui_Form()
    # ui.setupUi(Form)
    # Form.show()
    # sys.exit(app.exec_())

    app1.exec_()
    sys.exit(app1.exec_())