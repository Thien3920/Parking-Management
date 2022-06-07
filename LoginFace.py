# from re import I

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from pymongo import MongoClient
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
import imutils
import Login
import MainWindow
import cv2

import numpy as np
from bson.objectid import ObjectId
from PIL import Image
import io
import time
from insightface.model_zoo.retinaface import RetinaFace
from insightface.model_zoo.arcface_onnx import ArcFaceONNX


class Ui_LoginFaceWindow(object):
    def __init__(self):
        self.source = 0
        self.ID = None
        self.ss = "False"
        self.StateNext = False
        self.StaffName = None
 


        ## Database
        uri = "mongodb://localhost:27017/"
        Client = MongoClient(uri)
        DataBase = Client["Thien"]
        self.UserCollection = DataBase["User"]

        #face reg

        self.codes = []
        self.ids = []
        for self.UserDocument in self.UserCollection.find():
            self.codes.append(self.UserDocument["Code"])
            self.ids.append(str(self.UserDocument["_id"]))

        self.detector = RetinaFace(model_file='/home/thien/.insightface/models/buffalo_l/det_10g.onnx')
        self.recognizer = ArcFaceONNX(model_file='/home/thien/.insightface/models/buffalo_l/w600k_r50.onnx')

    def Default(self):
        self.CODES = []
        self.IDS = []
        for UserDocument in self.UserCollection.find():
            self.CODES.append(UserDocument["Code"])
            self.IDS.append(str(UserDocument["_id"]))

    def OpenMainWindow(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainUi = MainWindow.Ui_MainWindow(StaffName=self.StaffName)
        self.MainUi.setupUi(self.MainWindow)
        self.MainWindow.show()

    def Next(self):
        if self.StateNext:
            self.OpenMainWindow()
            self.LoginFaceWindow.close()



    def Logout(self):
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        self.LoginWindow = QtWidgets.QMainWindow()
        self.LoginUi = Login.UiLoginWindow()
        self.LoginUi.setupUi(self.LoginWindow)
        self.LoginWindow.show()

    def Center(self,widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())

    def LoadImage(self, image):
        image = imutils.resize(image, width=500)
        frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.GetFaceLabel.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def drawbox(self):
        if len(self.bboxes)> 0:
            xmin,ymin,xmax,ymax,score = [int(_) for _ in self.bboxes[0]][:5]
            FaceImage = self.image[ymin:ymax,xmin:xmax]
            cv2.rectangle(self.image, (xmin, ymin ), (xmax ,ymax), (0,255,0), 1, cv2.LINE_AA)
            
            return FaceImage


    def View_video(self):
        ret, self.image = self.cap.read()
        
        image = self.image.copy()
        self.bboxes, self.kpss = self.detector.detect(self.image, input_size =(640, 640))
        self.FaceImage = self.drawbox()


        image,self.Name,self.ID  = self.RecognizeFace()
        self.LoadImage(self.image)
        self.CheckAndShowInfo(image,self.Name,self.ID)
    
 

    def RecognizeFace(self):
        Name = None
        Id = None
        TestImage = None

        if len(self.bboxes)> 0:
            
            
            self.Distance = []
            EncodeTest = self.recognizer.get(self.image, self.kpss[0])
            for CodeOb in self.CODES:
                ds = []
                for code in CodeOb:
                    distance = self.recognizer.compute_sim(EncodeTest,np.array(code))
                    ds.append(distance)
                d = max(ds) 
                self.Distance.append(d)
            maxvalue = max(self.Distance)
            print(maxvalue)
            indexmax = np.argmax(self.Distance)
            id = self.IDS[indexmax]
            
            if  maxvalue > 0.3:
                Id = id
                object = self.UserCollection.find_one({"_id":ObjectId(Id)})
                Name = object["Name"]
                img = object["Images"][0]
                TestImage = np.asarray(Image.open(io.BytesIO(img)))



        return TestImage,Name,Id


    def CheckAndShowInfo(self,image,Name,ID):
        if(Name != None) and (ID != None) :
        
            self.CheckNameLabel.setText("{}".format(Name))
            self.CheckIDLabel.setText("{}".format(ID))
            bboxes, kpss = self.detector.detect(image, input_size =(640, 640))
      
            xmin,ymin,xmax,ymax,score = [int(_) for _ in bboxes[0]][:5]
            FaceImage = image[ymin:ymax,xmin:xmax]
            
            self.LoadImage(FaceImage)
            self.StateNext = True
            self.StaffName = self.UserCollection.find_one({"_id":ObjectId(ID)})["Name"]
            self.timer.stop()
            self.cap.release()


    def Run(self):
        self.cap = cv2.VideoCapture(self.source)
        self.timer = QTimer()
        self.timer.timeout.connect(self.View_video)
        self.timer.start(60)


    def setupUi(self, LoginFaceWindow):
        self.Center(LoginFaceWindow)
        LoginFaceWindow.setObjectName("LoginFaceWindow")
        LoginFaceWindow.resize(760, 658)
        LoginFaceWindow.setMaximumSize(QtCore.QSize(760, 658))
        LoginFaceWindow.setStyleSheet("background-color: rgb(18, 16, 61);\n"
"")
        self.LoginFaceWidget = QtWidgets.QWidget(LoginFaceWindow)
        self.LoginFaceWidget.setObjectName("LoginFaceWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.LoginFaceWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main = QtWidgets.QWidget(self.LoginFaceWidget)
        self.main.setObjectName("main")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout_2.setContentsMargins(9, 0, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TopFrame = QtWidgets.QFrame(self.main)
        self.TopFrame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.TopFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TopFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TopFrame.setObjectName("TopFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.TopFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BackButton = QtWidgets.QPushButton(self.TopFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BackButton.sizePolicy().hasHeightForWidth())
        self.BackButton.setSizePolicy(sizePolicy)
        self.BackButton.setMinimumSize(QtCore.QSize(100, 40))
        self.BackButton.setMaximumSize(QtCore.QSize(100, 40))
        self.BackButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BackButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icons/chevrons-left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BackButton.setIcon(icon)
        self.BackButton.setIconSize(QtCore.QSize(35, 35))
        self.BackButton.setObjectName("BackButton")
        self.horizontalLayout.addWidget(self.BackButton)
        self.TitleLabel = QtWidgets.QLabel(self.TopFrame)
        self.TitleLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 30pt \"Ubuntu Condensed\";")
        self.TitleLabel.setObjectName("TitleLabel")
        self.horizontalLayout.addWidget(self.TitleLabel, 0, QtCore.Qt.AlignHCenter)
        self.NextButton = QtWidgets.QPushButton(self.TopFrame)
        self.NextButton.setMinimumSize(QtCore.QSize(0, 40))
        self.NextButton.setMaximumSize(QtCore.QSize(100, 40))
        self.NextButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.NextButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NextButton.setStyleSheet("QPushButton {\n"
"border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"padding: 0 12px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./icons/chevrons-right.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NextButton.setIcon(icon1)
        self.NextButton.setIconSize(QtCore.QSize(35, 35))
        self.NextButton.setObjectName("NextButton")
        self.horizontalLayout.addWidget(self.NextButton)
        self.verticalLayout_2.addWidget(self.TopFrame)
        self.CenterFrame = QtWidgets.QFrame(self.main)
        self.CenterFrame.setMinimumSize(QtCore.QSize(500, 500))
        self.CenterFrame.setMaximumSize(QtCore.QSize(500, 500))
        self.CenterFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.CenterFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CenterFrame.setObjectName("CenterFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.CenterFrame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.GetFaceLabel = QtWidgets.QLabel(self.CenterFrame)
        self.GetFaceLabel.setMinimumSize(QtCore.QSize(500, 500))
        self.GetFaceLabel.setMaximumSize(QtCore.QSize(500, 500))

        self.GetFaceLabel.setStyleSheet("border: none;")
        self.GetFaceLabel.setText("")
        self.GetFaceLabel.setScaledContents(True)
        self.GetFaceLabel.setWordWrap(False)

        self.GetFaceLabel.setObjectName("GetFaceLabel")


        self.verticalLayout_3.addWidget(self.GetFaceLabel, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.CenterFrame, 0, QtCore.Qt.AlignHCenter)
        self.BottomFrame = QtWidgets.QFrame(self.main)
        self.BottomFrame.setMaximumSize(QtCore.QSize(16777215, 140))
        self.BottomFrame.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Ubuntu Condensed\";")
        self.BottomFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BottomFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BottomFrame.setObjectName("BottomFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.BottomFrame)
        self.gridLayout.setHorizontalSpacing(50)
        self.gridLayout.setObjectName("gridLayout")
        self.CheckNameLabel = QtWidgets.QLabel(self.BottomFrame)
        self.CheckNameLabel.setObjectName("CheckNameLabel")
        self.gridLayout.addWidget(self.CheckNameLabel, 0, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.NameLabel = QtWidgets.QLabel(self.BottomFrame)
        self.NameLabel.setObjectName("NameLabel")
        self.gridLayout.addWidget(self.NameLabel, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.IDLabel = QtWidgets.QLabel(self.BottomFrame)
        self.IDLabel.setObjectName("IDLabel")
        self.gridLayout.addWidget(self.IDLabel, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.CheckIDLabel = QtWidgets.QLabel(self.BottomFrame)
        self.CheckIDLabel.setObjectName("CheckIDLabel")
        self.gridLayout.addWidget(self.CheckIDLabel, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.verticalLayout_2.addWidget(self.BottomFrame)
        self.verticalLayout.addWidget(self.main)
        LoginFaceWindow.setCentralWidget(self.LoginFaceWidget)

        self.retranslateUi(LoginFaceWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginFaceWindow)

    def retranslateUi(self, LoginFaceWindow):
        self.LoginFaceWindow = LoginFaceWindow
        _translate = QtCore.QCoreApplication.translate
        LoginFaceWindow.setWindowTitle(_translate("LoginFaceWindow", "Parking Management"))
        self.BackButton.setText(_translate("LoginFaceWindow", "Back"))
        self.TitleLabel.setText(_translate("LoginFaceWindow", "LOGIN WITH FACE"))
        self.NextButton.setText(_translate("LoginFaceWindow", "Next"))
        self.CheckNameLabel.setText(_translate("LoginFaceWindow", "Unknow"))
        self.NameLabel.setText(_translate("LoginFaceWindow", "Name"))
        self.IDLabel.setText(_translate("LoginFaceWindow", "ID"))
        self.CheckIDLabel.setText(_translate("LoginFaceWindow", "None"))
        self.Run()

        self.BackButton.setShortcut("Ctrl+B")
        self.NextButton.setShortcut("Ctrl+N")
        self.BackButton.clicked.connect(self.Logout)
        self.BackButton.clicked.connect(LoginFaceWindow.close)
        self.NextButton.clicked.connect(self.Next)

        #default
        self.Default()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginFaceWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginFaceWindow()
    ui.setupUi(LoginFaceWindow)
    LoginFaceWindow.show()
    sys.exit(app.exec_())
