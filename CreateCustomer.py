from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import os
from PyQt5.QtWidgets import QDesktopWidget
import cv2

from PyQt5.QtCore import QTimer

import time
import shutil
from glob import glob
from pymongo import MongoClient
import Admin
import io
import PIL
import numpy as np

from insightface.model_zoo.retinaface import RetinaFace
from insightface.model_zoo.arcface_onnx import ArcFaceONNX


class Ui_MainWindow(object):
    def __init__(self):
        self.cap = None
        self.timer = None
        self.image = None
        self.FaceImage = None
        self.bb = None
        self.StateCapture = False
        self.files = [[]]
        self.idx = 0
        self.record = None
        self.license = None


        uri = "mongodb://localhost:27017/"
        Client = MongoClient(uri)
        DataBase = Client["Thien"]

        ## Model
        self.detector = RetinaFace(model_file='/home/thien/.insightface/models/buffalo_l/det_10g.onnx')
        self.recognizer = ArcFaceONNX(model_file='/home/thien/.insightface/models/buffalo_l/w600k_r50.onnx')

        self.CustomerDBCollection = DataBase["CustomerDB"]
    def Back(self):
        if self.timer !=None and self.cap!=None:
            self.timer.stop()
            self.cap.release()
        self.AdminWindow = QtWidgets.QMainWindow()
        self.AdminUi = Admin.Ui_AdminWindow()
        self.AdminUi.setupUi(self.AdminWindow)
        self.AdminWindow.show()

    def Center(self, widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())
    def setupUi(self, MainWindow):
        self.Center(MainWindow)
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1133, 851)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(12, 11, 42);\n"
"color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_8 = QtWidgets.QFrame(self.frame_5)
        self.frame_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.BackButton = QtWidgets.QPushButton(self.frame_8)
        self.BackButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/chevrons-left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BackButton.setIcon(icon)
        self.BackButton.setIconSize(QtCore.QSize(30, 30))
        self.BackButton.setObjectName("BackButton")
        self.horizontalLayout_6.addWidget(self.BackButton)
        self.horizontalLayout_3.addWidget(self.frame_8, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_5, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_9 = QtWidgets.QFrame(self.frame_6)
        self.frame_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_n = QtWidgets.QLabel(self.frame_9)
        self.label_n.setStyleSheet("font: 75 25pt \"Ubuntu Condensed\";")
        self.label_n.setAlignment(QtCore.Qt.AlignCenter)
        self.label_n.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label_n)
        self.horizontalLayout_4.addWidget(self.frame_9, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_6, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_7 = QtWidgets.QFrame(self.frame_2)
        self.frame_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_10 = QtWidgets.QFrame(self.frame_7)
        self.frame_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.ExitButton = QtWidgets.QPushButton(self.frame_10)
        self.ExitButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/power.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExitButton.setIcon(icon1)
        self.ExitButton.setIconSize(QtCore.QSize(30, 30))
        self.ExitButton.setObjectName("ExitButton")
        self.horizontalLayout_8.addWidget(self.ExitButton)
        self.horizontalLayout_5.addWidget(self.frame_10, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_7, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignTop)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 568))
        self.frame_3.setStyleSheet("")
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(11)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.frame_13 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"")
        self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_15 = QtWidgets.QFrame(self.frame_13)
        self.frame_15.setStyleSheet("border:none;")
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_3 = QtWidgets.QLabel(self.frame_15)
        self.label_3.setStyleSheet("font: 75 20pt \"Ubuntu Condensed\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_12.addWidget(self.label_3)
        self.verticalLayout_3.addWidget(self.frame_15, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_16 = QtWidgets.QFrame(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy)
        self.frame_16.setStyleSheet("border:none;\n"
"\n"
"")
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_16)
        self.verticalLayout_5.setContentsMargins(0, 11, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_19 = QtWidgets.QFrame(self.frame_16)
        self.frame_19.setMaximumSize(QtCore.QSize(450, 450))
        self.frame_19.setStyleSheet("border:none;")
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.VideoLabel = QtWidgets.QLabel(self.frame_19)
        self.VideoLabel.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.VideoLabel.setText("")
        self.VideoLabel.setPixmap(QtGui.QPixmap("icons/face-scan.png"))
        self.VideoLabel.setScaledContents(True)
        self.VideoLabel.setObjectName("VideoLabel")
        self.horizontalLayout_14.addWidget(self.VideoLabel)
        self.verticalLayout_5.addWidget(self.frame_19, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_20 = QtWidgets.QFrame(self.frame_16)
        self.frame_20.setStyleSheet("border:none;")
        self.frame_20.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.frame_26 = QtWidgets.QFrame(self.frame_20)
        self.frame_26.setStyleSheet("border:none;")
        self.frame_26.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_26)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.StartButton = QtWidgets.QPushButton(self.frame_26)
        self.StartButton.setMinimumSize(QtCore.QSize(115, 51))
        self.StartButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/play-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StartButton.setIcon(icon2)
        self.StartButton.setIconSize(QtCore.QSize(30, 30))
        self.StartButton.setObjectName("StartButton")
        self.horizontalLayout_18.addWidget(self.StartButton)
        self.horizontalLayout_17.addWidget(self.frame_26, 0, QtCore.Qt.AlignRight)
        self.frame_27 = QtWidgets.QFrame(self.frame_20)
        self.frame_27.setStyleSheet("border:none;")
        self.frame_27.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_27)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.CaptureButton = QtWidgets.QPushButton(self.frame_27)
        self.CaptureButton.setMinimumSize(QtCore.QSize(115, 51))
        self.CaptureButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/camera.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CaptureButton.setIcon(icon3)
        self.CaptureButton.setIconSize(QtCore.QSize(30, 30))
        self.CaptureButton.setObjectName("CaptureButton")
        self.horizontalLayout_19.addWidget(self.CaptureButton)
        self.horizontalLayout_17.addWidget(self.frame_27, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_5.addWidget(self.frame_20)
        self.verticalLayout_3.addWidget(self.frame_16)
        self.horizontalLayout_11.addWidget(self.frame_13)
        self.frame_14 = QtWidgets.QFrame(self.frame_3)
        self.frame_14.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"")
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_17 = QtWidgets.QFrame(self.frame_14)
        self.frame_17.setStyleSheet("border:none;")
        self.frame_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_4 = QtWidgets.QLabel(self.frame_17)
        self.label_4.setStyleSheet("font: 75 20pt \"Ubuntu Condensed\";")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_13.addWidget(self.label_4)
        self.verticalLayout_4.addWidget(self.frame_17)
        self.frame_32 = QtWidgets.QFrame(self.frame_14)
        self.frame_32.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_32.setStyleSheet("border:none;\n"
"")
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_32)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.ChooseFileButton = QtWidgets.QPushButton(self.frame_32)
        self.ChooseFileButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ChooseFileButton.setIcon(icon4)
        self.ChooseFileButton.setObjectName("pushButton")
        self.verticalLayout_10.addWidget(self.ChooseFileButton)
        self.verticalLayout_4.addWidget(self.frame_32, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.frame_18 = QtWidgets.QFrame(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_18.sizePolicy().hasHeightForWidth())
        self.frame_18.setSizePolicy(sizePolicy)
        self.frame_18.setStyleSheet("border:none;")
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_18)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 0)
        self.verticalLayout_6.setSpacing(11)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_21 = QtWidgets.QFrame(self.frame_18)
        self.frame_21.setStyleSheet("border:none;")
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_21)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.PicLabel = QtWidgets.QLabel(self.frame_21)
        self.PicLabel.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.PicLabel.setText("")
        self.PicLabel.setPixmap(QtGui.QPixmap("./icons/face-scan.png"))
        self.PicLabel.setScaledContents(True)
        self.PicLabel.setMaximumSize(250,250)
        self.PicLabel.setObjectName("PicLabel")
        self.horizontalLayout_15.addWidget(self.PicLabel)
        self.verticalLayout_6.addWidget(self.frame_21, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_22 = QtWidgets.QFrame(self.frame_18)
        self.frame_22.setStyleSheet("border:none;")
        self.frame_22.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_22)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.frame_23 = QtWidgets.QFrame(self.frame_22)
        self.frame_23.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_23)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.BackPicButton = QtWidgets.QPushButton(self.frame_23)
        self.BackPicButton.setMinimumSize(QtCore.QSize(90, 40))
        self.BackPicButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        self.BackPicButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/skip-back.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BackPicButton.setIcon(icon5)
        self.BackPicButton.setIconSize(QtCore.QSize(25, 25))
        self.BackPicButton.setObjectName("BackPicButton")
        self.verticalLayout_8.addWidget(self.BackPicButton)
        self.horizontalLayout_16.addWidget(self.frame_23, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.frame_24 = QtWidgets.QFrame(self.frame_22)
        self.frame_24.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_24)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.DeletePicButton = QtWidgets.QPushButton(self.frame_24)
        self.DeletePicButton.setMinimumSize(QtCore.QSize(90, 40))
        self.DeletePicButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        self.DeletePicButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeletePicButton.setIcon(icon6)
        self.DeletePicButton.setIconSize(QtCore.QSize(25, 25))
        self.DeletePicButton.setObjectName("DeletePicButton")
        self.verticalLayout_7.addWidget(self.DeletePicButton)
        self.horizontalLayout_16.addWidget(self.frame_24, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_25 = QtWidgets.QFrame(self.frame_22)
        self.frame_25.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_25)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.NextPicButton = QtWidgets.QPushButton(self.frame_25)
        self.NextPicButton.setMinimumSize(QtCore.QSize(90, 40))
        self.NextPicButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        self.NextPicButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/skip-forward.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NextPicButton.setIcon(icon7)
        self.NextPicButton.setIconSize(QtCore.QSize(25, 25))
        self.NextPicButton.setObjectName("NextPicButton")
        self.verticalLayout_9.addWidget(self.NextPicButton)
        self.horizontalLayout_16.addWidget(self.frame_25, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.verticalLayout_6.addWidget(self.frame_22, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.verticalLayout_4.addWidget(self.frame_18)
        self.horizontalLayout_11.addWidget(self.frame_14)
        self.verticalLayout.addWidget(self.frame_3, 0, QtCore.Qt.AlignTop)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(11)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_12 = QtWidgets.QFrame(self.frame_4)
        self.frame_12.setMinimumSize(QtCore.QSize(0, 57))
        self.frame_12.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"")
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setContentsMargins(-1, -1, -1, 11)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_28 = QtWidgets.QFrame(self.frame_12)
        self.frame_28.setMinimumSize(QtCore.QSize(569, 0))
        self.frame_28.setStyleSheet("border:none;")
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_28)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 1)
        self.horizontalLayout_20.setSpacing(12)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.frame_30 = QtWidgets.QFrame(self.frame_28)
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_30)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.Plate = QtWidgets.QLabel(self.frame_30)
        self.Plate.setMinimumSize(QtCore.QSize(0, 34))
        self.Plate.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";")
        self.Plate.setObjectName("Plate")
        self.horizontalLayout_21.addWidget(self.Plate)
        self.horizontalLayout_20.addWidget(self.frame_30)
        self.frame_31 = QtWidgets.QFrame(self.frame_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_31.sizePolicy().hasHeightForWidth())
        self.frame_31.setSizePolicy(sizePolicy)
        self.frame_31.setMinimumSize(QtCore.QSize(0, 54))
        self.frame_31.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_31.setObjectName("frame_31")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_31)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_31)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 34))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"font: 75 15pt \"Ubuntu Condensed\";")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_23.addWidget(self.lineEdit)
        self.horizontalLayout_20.addWidget(self.frame_31)
        self.horizontalLayout_10.addWidget(self.frame_28, 0, QtCore.Qt.AlignLeft)
        self.frame_29 = QtWidgets.QFrame(self.frame_12)
        self.frame_29.setStyleSheet("border:none;")
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_29)
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label = QtWidgets.QLabel(self.frame_29)
        self.label.setStyleSheet("color: rgb(239, 41, 41);\n"
"font: 75 15pt \"Ubuntu Condensed\";")
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label_2")
        self.horizontalLayout_22.addWidget(self.label)
        self.horizontalLayout_10.addWidget(self.frame_29)
        self.verticalLayout_2.addWidget(self.frame_12)
        self.frame_11 = QtWidgets.QFrame(self.frame_4)
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 20)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.SaveButton = QtWidgets.QPushButton(self.frame_11)
        self.SaveButton.setMinimumSize(QtCore.QSize(130, 50))
        self.SaveButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 5px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveButton.setIcon(icon8)
        self.SaveButton.setIconSize(QtCore.QSize(30, 30))
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout_9.addWidget(self.SaveButton)
        self.verticalLayout_2.addWidget(self.frame_11, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Parking Management"))
        self.BackButton.setText(_translate("MainWindow", "Back"))
        self.label_n.setText(_translate("MainWindow", "REGISTER CUSTOMER"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))
        self.label_3.setText(_translate("MainWindow", "CAMERA"))
        self.StartButton.setText(_translate("MainWindow", "Start"))
        self.CaptureButton.setText(_translate("MainWindow", "Capture"))
        self.label_4.setText(_translate("MainWindow", "FACE"))
        self.ChooseFileButton.setText(_translate("MainWindow", "Choose File"))
        self.Plate.setText(_translate("MainWindow", "License Plate"))
        self.SaveButton.setText(_translate("MainWindow", "SAVE"))
        #Button connect function


        self.ChooseFileButton.clicked.connect(self.LinkPic)
        self.BackPicButton.clicked.connect(self.BackPic)
        self.NextPicButton.clicked.connect(self.NextPic)
        self.DeletePicButton.clicked.connect(self.DeletePic)
        self.StartButton.clicked.connect(self.StartVideo)
        self.CaptureButton.clicked.connect(self.Capture)
        self.SaveButton.clicked.connect(self.Save)

        self.BackButton.clicked.connect(self.Back)
        self.BackButton.clicked.connect(MainWindow.close)
        self.ExitButton.clicked.connect(MainWindow.close)

        

    def Save(self):
        self.license = self.lineEdit.text()
        if self.license != "" and self.license != None:
            for CustomerDB in self.CustomerDBCollection.find():
                if self.license == CustomerDB["License Plate"]:
                    self.label.setText("License available")
                    return 0
            
            if len(self.files[0]) > 0:
                codes = []
                Images = []
                for ImageName in self.files[0]:
                    image = cv2.imread(ImageName)
                    im = PIL.Image.fromarray(np.uint8(image))
                    image_bytes = io.BytesIO()
                    im.save(image_bytes, format='JPEG')
                    Images.append(image_bytes.getvalue())
                    bboxes, kpss = self.detector.detect(image, input_size =(640, 640))
                    if len(bboxes)> 0:
                        code = self.recognizer.get(image, kpss[0])
                        codes.append(code.tolist())
                self.CustomerDBCollection.insert_one({"License Plate":self.license,"Code":codes,"Images":Images})
                self.label.setText("OK")
                
            else:
                self.label.setText("No face")
        else:
            self.label.setText("Please Enter License Plate")




    def StartVideo(self):
        if self.record == None or self.record == "STOP":
            self.default()
            self.record ="RUNNING"
            self.cap = cv2.VideoCapture(0)
            self.timer = QTimer()
            self.timer.timeout.connect(self.ShowVideo)
            self.timer.start(60)
            self.StartButton.setText("Finish")

        elif self.record =="RUNNING":
            self.record = "STOP"
            self.VideoLabel.setPixmap(QtGui.QPixmap("./icons/face-scan.png"))
            self.timer.stop()
            self.cap.release()
            self.StartButton.setText("Start")

    def ShowVideo(self):
        ret, self.image = self.cap.read()
        self.bboxes, self.kpss = self.detector.detect(self.image, input_size =(640, 640))
        self.FaceImage = self.drawbox()
        self.LoadImage(self.image,self.VideoLabel)
    
    def drawbox(self):
        if len(self.bboxes)> 0:
            xmin,ymin,xmax,ymax,score = [int(_) for _ in self.bboxes[0]][:5]
            FaceImage = self.image[ymin:ymax,xmin:xmax]
            cv2.rectangle(self.image, (xmin, ymin ), (xmax ,ymax), (0,255,0), 1, cv2.LINE_AA)
            
            return FaceImage

    def Capture(self):
        if self.timer != None:
            xtime = int(float(time.time()))
            cv2.imwrite("./images/image_{}.jpg".format(xtime),self.image)
            self.ListImage()



    # def CheckFace(self):
    #     if len(self.bb) > 0:
    #         x0, y0, x1, y1 = [int(_) for _ in self.bb[0]][:4]
    #         self.FaceImage = self.image[y0:y1, x0:x1]
    #         image = self.FaceImage.copy()
    #         if image .shape[0] > 0 and image .shape[1] > 0:
    #             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #             lankmasrks = face_recognition.face_landmarks(image)
    #             if len(lankmasrks) >0:
    #                 code = face_recognition.face_encodings(image)
    #                 if len(code) >0 :
    #                     self.code = code[0]
    #                     self.StateCapture = True
    #                     cv2.putText(self.image, "OK", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 255, 0), 2, cv2.LINE_AA)
    #                     return 0
    #     cv2.putText(self.image, "No landmasks", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL,
    #                 1, (0, 0, 255), 2, cv2.LINE_AA)
    #     self.StateCapture = False

    def ListImage(self):
        list = glob('./images' + '/*.jpg') + glob('./images' + '/*.png')
        list.sort()
        self.files=[list]
        self.idx = len(self.files[0])
        self.ShowImage(self.idx -1)

    def default(self):
        if os.path.exists('./images'):
            shutil.rmtree('./images')
        os.makedirs('./images')

        self.license = ""
        self.image = None
        self.FaceImage = None
        self.files = [[]]
        self.idx = 0
        self.license = None
        self.PicLabel.setPixmap(QtGui.QPixmap("./icons/face-scan.png"))
        self.lineEdit.clear()
        self.label.setText("")


    def DeletePic(self):
        if len(self.files[0])>0:

            self.idx = len(self.files[0])-1
            self.files[0].pop(self.idx)
            if self.idx ==0:
                path = "icons/face-scan.png"
                I = cv2.imread(path)
                self.LoadImage(I, self.PicLabel)
            else:
                self.BackPic()

    def BackPic(self):
        if len(self.files[0]) > 0:
            if self.idx >0:
                self.idx -=1
            else:
                self.idx = len(self.files[0]) -1

            self.ShowImage(self.idx)
    def NextPic(self):
        if len(self.files[0]) > 0:
            if self.idx < len(self.files[0]) -1:
                self.idx+=1
            else:
                self.idx = 0
            self.ShowImage(self.idx)

    def LinkPic(self):
        kwargs = {}
        if 'SNAP' in os.environ:
            kwargs['options'] = QFileDialog.DontUseNativeDialog

        self.files = QFileDialog.getOpenFileNames(None,"","", "image file (*.png, *.jpg)",**kwargs)
        self.idx = len(self.files[0])

        self.ShowImage(self.idx-1)
    
    def ShowImage(self,idx):
   
        if len(self.files) > 0:
            path = self.files[0][idx]
            image = cv2.imread(path)
            bboxes, kpss = self.detector.detect(image, input_size =(640, 640))
      
            xmin,ymin,xmax,ymax,score = [int(_) for _ in bboxes[0]][:5]
            image = image[ymin:ymax,xmin:xmax]

        else:
            path = "./icons/face-scan-small.png"
            image = cv2.imread(path)
        
        self.LoadImage(image,self.PicLabel)

   




    def LoadImage(self, image,Label):
        frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        Label.setPixmap(QtGui.QPixmap.fromImage(image))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
