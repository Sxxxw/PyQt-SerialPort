import re
import sys
import os
import time
import array
import binascii
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *
from PyQt5.QtWebEngineWidgets import *

data = array.array('d')
horizontalLength = 120
num = 0
idx = 0
class SerialForm(object):
    def UiSet(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(800, 900)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setFamily("SimHei")
        font.setPointSize(10)
        font.setWeight(50)
        Form.setFont(font)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Form.setMouseTracking(False)
        Form.setStyleSheet("color: rgb(25, 25, 25);""background-color: rgb(240, 240, 240);""font: 11pt \"SimHei\";")
        # Receiving Area    Title
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(420, 285, 80, 25))
        self.label1.setObjectName("label1")
        # Sending Area      Title
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(40, 285, 80, 25))
        self.label2.setTextFormat(QtCore.Qt.AutoText)
        self.label2.setObjectName("label2")
        # Sending Button
        self.SendButton = QtWidgets.QPushButton(Form)
        self.SendButton.setGeometry(QtCore.QRect(300, 285, 80, 25))
        self.SendButton.setObjectName("SendButton")
        # Clear  Button
        self.ClearButton = QtWidgets.QPushButton(Form)
        self.ClearButton.setGeometry(QtCore.QRect(680, 285, 80, 25))
        self.ClearButton.setObjectName("ClearButton")
        # Receiving Area Box
        self.textEdit_Recive = QtWidgets.QTextEdit(Form)
        self.textEdit_Recive.setGeometry(QtCore.QRect(400, 310, 385, 200))
        self.textEdit_Recive.setStyleSheet("background-color: rgb(230, 230, 230);""background-color: rgb(230, 230, 230);")
        self.textEdit_Recive.setObjectName("textEdit_Recive")
        # Sending Area Box
        self.textEdit_Send = QtWidgets.QTextEdit(Form)
        self.textEdit_Send.setGeometry(QtCore.QRect(30, 310, 350, 200))
        self.textEdit_Send.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.textEdit_Send.setObjectName("textEdit_Send")

        # Build a table
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(15, 180, 770, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # SerialPort Refresh    Title
        self.RefreshLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RefreshLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RefreshLabel.setObjectName("ComRefreshLabel")
        self.gridLayout.addWidget(self.RefreshLabel, 0, 0, 1, 1)    # 0 0
        # SerialPort Refresh   Button
        self.RefreshButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.RefreshButton.setObjectName("ComRefreshButton")
        self.gridLayout.addWidget(self.RefreshButton, 1, 0, 1, 1)   # 1 0

        # SerialPort Select    Title
        self.ComNameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComNameLabel.setObjectName("ComNameLabel")
        self.gridLayout.addWidget(self.ComNameLabel, 0, 1, 1, 1)    # 0 1
        # SerialPort Select    Drop Down List
        self.ComNameCombo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.ComNameCombo.setObjectName("ComNameCombo")
        self.gridLayout.addWidget(self.ComNameCombo, 1, 1, 1, 1)    # 1 1

        # Baud Rate Setting   Title
        self.BaudLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.BaudLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.BaudLabel.setObjectName("BaudLabel")
        self.gridLayout.addWidget(self.BaudLabel, 0, 2, 1, 1)      # 0 2
        # Baud Rate Setting   Drop Down List
        self.BaudCombo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.BaudCombo.setEditable(True)
        self.BaudCombo.setDuplicatesEnabled(False)
        self.BaudCombo.setModelColumn(0)
        self.BaudCombo.setObjectName("BaudCombo")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.BaudCombo.addItem("")
        self.gridLayout.addWidget(self.BaudCombo, 1, 2, 1, 1)    # 1 2

        # SerialPort Operation Title
        self.ComStateLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComStateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComStateLabel.setObjectName("ComStateLabel")
        self.gridLayout.addWidget(self.ComStateLabel, 0, 3, 1, 1)  # 0 3

        # Open/Close Title
        self.ComWhetherOpenLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ComWhetherOpenLabel.setText("")
        self.ComWhetherOpenLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ComWhetherOpenLabel.setObjectName("ComWhetherOpenLabel")
        self.gridLayout.addWidget(self.ComWhetherOpenLabel, 1, 3, 1, 1)  # 1 3

        # SerialPort Open Button
        self.ComOpenButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ComOpenButton.setObjectName("ComOpenButton")
        self.gridLayout.addWidget(self.ComOpenButton, 0, 4, 1, 1)  # 0 4
        # SerialPort Close Button
        self.ComCloseButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ComCloseButton.setDefault(False)
        self.ComCloseButton.setObjectName("ComCloseButton")
        self.gridLayout.addWidget(self.ComCloseButton, 1, 4, 1, 1)  # 1 4

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

        # Show Time
        self.TimeLabel = QtWidgets.QLabel(Form)
        self.TimeLabel.setGeometry(QtCore.QRect(150, 130, 150, 20))
        self.TimeTitle = QtWidgets.QLabel(Form)
        self.TimeTitle.setGeometry(QtCore.QRect(20, 130, 130, 20))

        # Show Time   Font Definition
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

        # Author Title
        self.AuthorLabel = QtWidgets.QLabel(Form)
        self.AuthorLabel.setGeometry(QtCore.QRect(340, 130, 420, 20))


        # Github Button
        self.GithubButton = QtWidgets.QPushButton(Form)
        self.GithubButton.setGeometry(QtCore.QRect(200, 520, 400, 30))
        # Github Button  Font Definition
        font = QtGui.QFont()
        font.setFamily("SimSun")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.GithubButton.setFont(font)
        self.GithubButton.setObjectName("AboutButton")

        # Waveform Curve Monitoring Area
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 550, 800, 350))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.plot_view = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.plot_view.setContentsMargins(0, 0, 0, 0)
        self.plot_view.setObjectName("plot_view")
        pg.setConfigOption('background', '#F0F0F0')
        pg.setConfigOption('foreground', 'k')
        win = pg.GraphicsLayoutWidget()  # Create Window
        win.setStyleSheet("background-color: rgb(20, 20, 20);")
        data = array.array('d')  # Dynamically Change the Size of the Array
        horizontalLength = 120  # Abscissa length
        p = win.addPlot()  # Add Figure P to the Window
        p.showGrid(x=True, y=True)  # Open the X and Y Tables
        p.setRange(xRange=[0, horizontalLength], yRange=[0, 255], padding=0)
        p.setLabel(axis='left', text='')  # Keep to the Left
        p.setLabel(axis='bottom', text='')
        p.setTitle('Waveform Curve Monitoring Area')  # Set the Name of the Table
        self.curve = p.plot(pen='r')  # Draw a Graph
        self.plot_view.addWidget(win)

        self.UItranslate(Form)
        self.ClearButton.clicked.connect(self.textEdit_Recive.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def UItranslate(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Computer Integrated System Design：Group 7-Serial Port Communication Tools"))
        self.label1.setText(_translate("Form", "Receiving Area"))
        self.label2.setText(_translate("Form", "Sending Area"))
        self.SendButton.setText(_translate("Form", "Send Out"))
        self.ClearButton.setText(_translate("Form", "Clear up"))
        self.RefreshLabel.setText(_translate("Form", "SerialPort Reflesh"))
        self.RefreshButton.setText(_translate("Form", "Refresh"))
        self.ComNameLabel.setText(_translate("Form", "SerialPort Select"))
        self.BaudLabel.setText(_translate("Form", "Set Baud Rate"))
        self.BaudCombo.setCurrentText(_translate("Form", "9600"))
        self.BaudCombo.setItemText(0, _translate("Form", "1200"))
        self.BaudCombo.setItemText(1, _translate("Form", "2400"))
        self.BaudCombo.setItemText(2, _translate("Form", "4800"))
        self.BaudCombo.setItemText(3, _translate("Form", "9600"))
        self.BaudCombo.setItemText(4, _translate("Form", "14400"))
        self.BaudCombo.setItemText(5, _translate("Form", "19200"))
        self.BaudCombo.setItemText(6, _translate("Form", "38400"))
        self.BaudCombo.setItemText(7, _translate("Form", "43000"))
        self.BaudCombo.setItemText(8, _translate("Form", "57600"))
        self.BaudCombo.setItemText(9, _translate("Form", "76800"))
        self.BaudCombo.setItemText(10, _translate("Form", "115200"))
        self.BaudCombo.setItemText(11, _translate("Form", "128000"))
        self.BaudCombo.setItemText(12, _translate("Form", "230400"))
        self.BaudCombo.setItemText(13, _translate("Form", "256000"))
        self.BaudCombo.setItemText(14, _translate("Form", "460800"))
        self.ComStateLabel.setText(_translate("Form", "SerialPort Switch"))
        self.ComCloseButton.setText(_translate("Form", "Close"))
        self.ComOpenButton.setText(_translate("Form", "Open"))
        self.textEdit_Recive.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'SimHei\'; font-size:9pt; font-weight:400; font-style:normal;\">\n""<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\';\"><br /></p></body></html>"))
        self.TimeLabel.setText(_translate("Form", "Time"))
        self.TimeTitle.setText(_translate("Form", "Beijing Time："))
        self.GithubButton.setText(_translate("Form", "Github: Click here to get the source code"))
        self.AuthorLabel.setText(_translate("Form", "Author:尚修为、胡聿鑫、林宇丰、王佳玉、海塞姆"))

    def WavePlot(self):
        global idx
        tmp = np.sin(np.pi / 50 * idx) * num
        if tmp >= 0:
            if len(data)<horizontalLength:
                data.append(num)
            else:
                data[:-1] = data[1:]
                data[-1] = tmp
        self.curve.setData(data)
        idx = idx + 1

ind = 0
ink = 0
halve = 0
alarm = 0
class MyMainWindow(QMainWindow, SerialForm):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.UiSet(self)
        # Set Instance
        self.CreateItems()
        # Set Signals and Slots
        self.CreateSignalSlot()

        my_timer = QTimer(self)
        my_timer.timeout.connect(self.WavePlot)  # Call WavePlot Function Regularly
        my_timer.start(50)  # Call Once in 50ms

    # Set Instance
    def CreateItems(self):
        # Qt Serial Port Class
        self.com = QSerialPort()
        # Qt Timer class
        self.timer = QTimer(self)  # Initialization Timer
        self.timer.timeout.connect(self.DisplayTime)  # When the Timing Ends, Call the DisplayTime() method
        self.timer.start(100)  # Call Once in 100ms

    # Set Signals and Slots
    def CreateSignalSlot(self):
        self.ComOpenButton.clicked.connect(self.ComOpenButton_Clicked)
        self.ComCloseButton.clicked.connect(self.ComCloseButton_Clicked)
        self.SendButton.clicked.connect(self.SendButton_clicked)
        self.RefreshButton.clicked.connect(self.RefreshButton_Clicked)
        self.com.readyRead.connect(self.DataReceive)  # Receive Data
        self.GithubButton.clicked.connect(self.SkipGitHub)

    # Jump to GitHub to View the Source Code
    def SkipGitHub(self):
        self.browser = QWebEngineView()
        self.browser.load(QUrl('https://github.com/Sxxxw/PtQt-SerialPort'))
        self.setCentralWidget(self.browser)

    # Show Beijing Time
    def DisplayTime(self):
        self.TimeLabel.setText(time.strftime("%H:%M:%S,%B,%d", time.localtime()))

    # Serial Port Sending Data
    def DataSend(self):
        global halve
        global alarm
        # Priority Alarm
        if alarm == 1:
            txData = str(8)
            print(txData)
            alarm = 0

        # Halving or Normal Reading
        else:
            if halve == 1:
                txData = str(num / 2 + 128)
            else:  # Get commands from the command window
                # Determine whether to halve according to the command. Txdata string type
                txData = self.textEdit_Send.toPlainText()
                if int(txData) >> 4 == 1:
                    halve = 1

        if len(txData) == 0:
            return
        self.com.write(txData.encode('UTF-8'))

    # Serial Port Receiving Data
    def DataReceive(self):
        global ind
        global num
        global ink
        global alarm
        try:
            rxData = bytes(self.com.readAll())
        except:
            QMessageBox.critical(self, 'Error', 'Serial port data receiving error')

        try:
            self.textEdit_Recive.insertPlainText(rxData.decode('UTF-8'))
            if ind == 5:
                ink = int(rxData.decode("utf-8"))
            if ind >= 1 and ind <= 3:
                num = num * 10 + int(rxData.decode('UTF-8'))
            if ind < 7:
                ind = ind + 1
            # Collection completed
            else:
                # Alarm
                if num > 250 or halve == 1:
                    alarm = 1
                    self.DataSend()
                ink = 0
                num = 0
                ind = 0
        except:
            pass
    # Serial Port Refresh _ Clicked
    def RefreshButton_Clicked(self):
        self.ComNameCombo.clear()
        com = QSerialPort()
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            com.setPort(info)
            if com.open(QSerialPort.ReadWrite):
                self.ComNameCombo.addItem(info.portName())
                com.close()

    # Data Send Button _ Clicked
    def SendButton_clicked(self):
        self.DataSend()

    # Serial Port Open Button _ Clicked
    def ComOpenButton_Clicked(self):
        #### com Open Code here ####
        comName = self.ComNameCombo.currentText()
        comBaud = int(self.BaudCombo.currentText())
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critical(self, 'Error', 'Failed to open serial port')
                return
        except:
            QMessageBox.critical(self, 'Error', 'Failed to open serial port')
            return
        self.ComCloseButton.setEnabled(True)
        self.ComOpenButton.setEnabled(False)
        self.RefreshButton.setEnabled(False)
        self.ComNameCombo.setEnabled(False)
        self.BaudCombo.setEnabled(False)
        self.ComWhetherOpenLabel.setText('Opened')
        self.com.setBaudRate(comBaud)

    # Serial Port Close Button _ Clicked
    def ComCloseButton_Clicked(self):
        self.com.close()
        self.ComCloseButton.setEnabled(False)
        self.ComOpenButton.setEnabled(True)
        self.RefreshButton.setEnabled(True)
        self.ComNameCombo.setEnabled(True)
        self.BaudCombo.setEnabled(True)
        self.ComWhetherOpenLabel.setText('Closed')

if __name__ == '__main__':

    app1 = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()

    app1.exec_()
    sys.exit(app1.exec_())