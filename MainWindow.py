
# from detect_plate import predict
from plate.alpr import ALPR
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QTimer
from pymongo import MongoClient
import cv2
# from FaceReconition import DetectFace
# import face_recognition
import time
from datetime import timedelta
import numpy as np
import Login
import shutil
from skimage import exposure
from bson.objectid import ObjectId
from PIL import Image
from insightface.model_zoo.retinaface import RetinaFace
from insightface.model_zoo.arcface_onnx import ArcFaceONNX
import io



class Ui_MainWindow(object):
    def __init__(self,StaffName = None):
        self.StaffName = StaffName
        self.cap = None
        self.timer = None
        self.myFrameNumber = 0
        self.initial = False
        self.Checklp = ''
        self.VideoBienSo = "./videos/videodemo.mp4"
        self.VideoFace = 0
        ## Database
        uri = "mongodb://localhost:27017/"
        Client = MongoClient(uri)
        DataBase = Client["Thien"]

        self.CustomersCollection = DataBase["Customers"]
        self.HistoryCollection = DataBase["History"]
        self.CustomerDBcollection = DataBase["CustomerDB"]

        #license plate recognize
        self.ALPR = ALPR()
        #facerecognize
        self.codes = []
        self.ids = []
        for self.UserDocument in self.CustomerDBcollection.find():
            self.codes.append(self.UserDocument["Code"])
            self.ids.append(str(self.UserDocument["_id"]))

        self.detector = RetinaFace(model_file='/home/thien/.insightface/models/buffalo_l/det_10g.onnx')
        self.recognizer = ArcFaceONNX(model_file='/home/thien/.insightface/models/buffalo_l/w600k_r50.onnx')
    


        

    def Logout(self):
        self.initial = True
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        self.LoginWindow = QtWidgets.QMainWindow()
        self.LoginUi = Login.UiLoginWindow()
        self.LoginUi.setupUi(self.LoginWindow)
        self.timer.stop()
        self.cap.release()
        self.LoginWindow.show()

    def Center(self, widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())


    def LoadImage(self, image,Label):
        try:
            frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        except:
            pass
        image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        Label.setPixmap(QtGui.QPixmap.fromImage(image))

    def SetDefault(self):
        self.LicensePlate = ''
        totalFrames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if self.myFrameNumber >= 0 & self.myFrameNumber <= totalFrames:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.myFrameNumber)
        self.LicensePlateValueLabel.setText("Unknow")
        self.IDValuelabel.setText("None")
        self.TimeInValueLabel.setText("None")
        self.LBValueLabel.setText("Unknow")
        self.IDValueLabel.setText("None")
        self.TimeOutValueLabel.setText("None")
        self.TotalTimeValueLabel.setText("None")
        self.CostValueLabel.setText("0 VND")
        self.FaceLabel.setPixmap(QtGui.QPixmap("icons/face-scan.png"))
        self.ShowFaceOutLabel.setPixmap(QtGui.QPixmap("icons/face-scan.png"))

        


    def GetLicencePlate(self):
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        self.cap = cv2.VideoCapture(self.VideoBienSo)
        self.timer = QTimer()
        self.SetDefault()
        self.timer.timeout.connect(self.VideoLicencePlateStream)
        self.timer.start(60)

    def VideoLicencePlateStream(self):
        self.myFrameNumber +=1
        ret, self.image = self.cap.read()
        
        self.LicensePlate = self.ALPR.predict(self.image,self.initial)

        cv2.rectangle(self.image, (0, 0), (270, 40), (0, 0, 0), -1)

        if self.Checklp == self.LicensePlate:
            cv2.putText(self.image,"", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(self.image,self.LicensePlate, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        

        self.initial = False
        print("pllllll:",self.LicensePlate)
        
        self.LoadImage(self.image,self.CarCameraLabel)
        self.CheckLicencePlate()
        self.Checklp = self.LicensePlate

    def CheckLicencePlate(self):
        state = False
        if self.LicensePlate != None and self.LicensePlate != "":
            for CustomersDocument in self.CustomersCollection.find():
                if self.LicensePlate == CustomersDocument["License Plate"]:
                    self.LicensePlateValueLabel.setText("Exist")
                    return 0

            for CustomerDB in self.CustomerDBcollection.find():
                if self.LicensePlate == CustomerDB["License Plate"]:
                    state = True

            if state:
                self.LicensePlateValueLabel.setText("{}".format(self.LicensePlate))
                self.GetFace()
            else:
                self.LicensePlateValueLabel.setText("Unregistered vehicles")


    def GetFace(self):
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        self.cap = cv2.VideoCapture(self.VideoFace)
        self.timer = QTimer()
        self.timer.timeout.connect(self.VideoFaceStream)
        self.timer.start(60)

    def VideoFaceStream(self):
        ret, self.image = self.cap.read()
        self.bboxes, self.kpss = self.detector.detect(self.image, input_size =(640, 640))
        check = self.CheckFace()
        self.LoadImage(self.image, self.FaceLabel)
        if check:
            object = self.CustomerDBcollection.find_one({"License Plate":self.LicensePlate})
            img = object["Images"][0]
            image = np.asarray(Image.open(io.BytesIO(img)))
            bboxes, kpss = self.detector.detect(image, input_size =(640, 640))
            xmin,ymin,xmax,ymax,score = [int(_) for _ in bboxes[0]][:5]
            FaceImage = image[ymin:ymax,xmin:xmax]

            self.LoadImage(FaceImage, self.FaceLabel)
            self.Save()


    def CheckFace(self):
        if len(self.bboxes) > 0:
            xmin,ymin,xmax,ymax,score = [int(_) for _ in self.bboxes[0]][:5]
            self.FaceImage = self.image[ymin:ymax,xmin:xmax]
            cv2.rectangle(self.image, (xmin, ymin ), (xmax ,ymax), (0,255,0), 1, cv2.LINE_AA)
            
         

            EncodeTest = self.recognizer.get(self.image, self.kpss[0])
            
            CustomerDB = self.CustomerDBcollection.find_one({"License Plate":self.LicensePlate})
            ds = []
            for code in CustomerDB["Code"]:
                distance = self.recognizer.compute_sim(EncodeTest,np.array(code))
                ds.append(distance) 
            maxvalue = max(ds)
            if maxvalue > 0.3:
                cv2.putText(self.image, "OK", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 0, 255), 2, cv2.LINE_AA)
                return True
            else:
                cv2.putText(self.image, "The face doesn't match the license plate", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2,cv2.LINE_AA)
        return False


    def NumberCustomers(self):
        LB = []
        for CustomersDocument in self.CustomersCollection.find():
            LB.append(CustomersDocument["License Plate"])
        return len(LB)

    def Save(self):

        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        now = time.time()
        object =  self.CustomersCollection.insert_one({"License Plate": self.LicensePlate,"TimeIN": now,"StaffName":self.StaffName})
        self.ID = object.inserted_id

        self.IDValuelabel.setText("{}".format(self.ID))
        self.TimeInValueLabel.setText("{}".format(time.ctime(now)))



    def GetLicencePlateOut(self):
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()

        self.cap = cv2.VideoCapture(self.VideoBienSo)
        self.timer = QTimer()
        self.SetDefault()
        self.timer.timeout.connect(self.VideoLicencePlateStreamOut)
        self.timer.start(60)


    def VideoLicencePlateStreamOut(self):
        self.myFrameNumber += 1
        ret, self.image = self.cap.read()
        self.LicensePlate = self.ALPR.predict(self.image,self.initial)
        self.initial = False
        self.LoadImage(self.image,self.LPCameraOutLabel)
        self.CheckLicencePlateOut()

    def CheckLicencePlateOut(self):
        if self.LicensePlate != "" and self.LicensePlate != None:
            for self.CustomersDocument in self.CustomersCollection.find():
                if self.LicensePlate == self.CustomersDocument["License Plate"]:
                    self.LBValueLabel.setText("{}".format(self.LicensePlate))
                    self.GetFaceOut()
                    return 0

            self.LBValueLabel.setText("Not exist")
        else:
            self.LBValueLabel.setText("None")

    def GetFaceOut(self):
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()

        self.cap = cv2.VideoCapture(self.VideoFace)
        self.timer = QTimer()
        self.timer.timeout.connect(self.VideoFaceStreamOut)
        self.timer.start(60)

    def VideoFaceStreamOut(self):
        ret, self.image = self.cap.read()
        self.bboxes, self.kpss = self.detector.detect(self.image, input_size =(640, 640))
        check = self.CheckFace()
        self.LoadImage(self.image, self.ShowFaceOutLabel)
        if check:
            object = self.CustomerDBcollection.find_one({"License Plate":self.LicensePlate})
            img = object["Images"][0]
            image = np.asarray(Image.open(io.BytesIO(img)))
            bboxes, kpss = self.detector.detect(image, input_size =(640, 640))
            xmin,ymin,xmax,ymax,score = [int(_) for _ in bboxes[0]][:5]
            FaceImage = image[ymin:ymax,xmin:xmax]
            self.LoadImage(FaceImage, self.ShowFaceOutLabel)
            self.Pay()

   

    def Pay(self):

        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        now = time.time()
        Customer = self.CustomersCollection.find_one({"License Plate": self.LicensePlate})
        total = now - Customer['TimeIN']
        time_del = timedelta(seconds=total)
        Cost = self.CaculateCost(str(time_del))
        self.TotalTimeValueLabel.setText("{}".format(time_del))
        self.ID = Customer['_id']
        self.IDValueLabel.setText("{}".format(self.ID))
        self.TimeOutValueLabel.setText("{}".format(time.ctime(now)))
        self.CostValueLabel.setText("{} VND".format(Cost))
        self.HistoryCollection.insert_one(
            {"License Plate": Customer["License Plate"], "TimeIN": Customer["TimeIN"],
             "TimeOUT": now, "TotalTime": str(time_del), "Cost": Cost,"StaffName":Customer["StaffName"]})
        self.CustomersCollection.delete_one({"License Plate": Customer["License Plate"]})

    def CaculateCost(self,x):
        time = x.split(":")
        hours = int(time[0])
        if hours <=5:
            cost_value = 5000
        else:
            cost_value =5000 +(hours -5)*2000
        return cost_value

    def ChangeTab(self):

        self.initial = True
        if self.cap != None and self.timer != None:
            self.cap.release()
            self.timer.stop()
        self.myFrameNumber = 0
        self.CurrentTab = self.tabWidget.currentIndex()
        if self.CurrentTab == 0:
            self.GetLicencePlate()
        elif self.CurrentTab == 1:
            self.GetLicencePlateOut()
        else:
            self.loaddata()

    def Delete(self):
        idx = self.tableWidget.currentRow()

        if idx >= 0:
            ID = self.tableWidget.item(idx, 0).text()
            x = self.CustomersCollection.find_one({'_id': ObjectId(ID)})
            self.CustomersCollection.delete_one(x)
            self.tableWidget.removeRow(idx)

    def loaddata(self):
        Dataset = []
        for CustomerDocument in self.CustomersCollection.find():
            Dataset.append(CustomerDocument)

        row = 0
        self.tableWidget.setRowCount(len(Dataset))
        for Data in Dataset:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(Data["_id"])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(Data['License Plate']))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(time.ctime(Data["TimeIN"]))))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(Data["StaffName"]))
            row = row + 1




    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1035, 855)
        MainWindow.setStyleSheet("background-color: rgb(18, 16, 61);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("font: 75 15pt \"Ubuntu Condensed\";\n"
                                     "color: rgb(255, 255, 255);")
        self.tabWidget.setObjectName("tabWidget")
        self.IncomeTab = QtWidgets.QWidget()
        self.IncomeTab.setObjectName("IncomeTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.IncomeTab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TopFrame = QtWidgets.QFrame(self.IncomeTab)
        self.TopFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TopFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TopFrame.setObjectName("TopFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.TopFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LeftFrame = QtWidgets.QFrame(self.TopFrame)
        self.LeftFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LeftFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LeftFrame.setObjectName("LeftFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.LeftFrame)
        self.verticalLayout_2.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TitleLabel = QtWidgets.QLabel(self.LeftFrame)
        self.TitleLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_2.addWidget(self.TitleLabel)
        self.CarCameraLabel = QtWidgets.QLabel(self.LeftFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CarCameraLabel.sizePolicy().hasHeightForWidth())
        self.CarCameraLabel.setSizePolicy(sizePolicy)
        self.CarCameraLabel.setMinimumSize(QtCore.QSize(640, 640))
        self.CarCameraLabel.setStyleSheet("border-color: rgb(255,255,255);\n"
                                          "border-style: inset;\n"
                                          "border-width: 1.5px;\n"
                                          "border-radius: 8px;\n"
                                          "color: rgb(255, 255, 255);")
        self.CarCameraLabel.setObjectName("CarCameraLabel")
        self.CarCameraLabel.setScaledContents(True)
        self.verticalLayout_2.addWidget(self.CarCameraLabel)
        self.horizontalLayout_2.addWidget(self.LeftFrame)
        self.RightFrame = QtWidgets.QFrame(self.TopFrame)
        self.RightFrame.setMaximumSize(QtCore.QSize(700, 16777215))
        self.RightFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.RightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RightFrame.setObjectName("RightFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.RightFrame)
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.InforStaffFrame = QtWidgets.QFrame(self.RightFrame)
        self.InforStaffFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.InforStaffFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.InforStaffFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.InforStaffFrame.setObjectName("InforStaffFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.InforStaffFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.StaffNameLabel = QtWidgets.QLabel(self.InforStaffFrame)
        self.StaffNameLabel.setStyleSheet("padding: 0 5px;")
        self.StaffNameLabel.setObjectName("StaffNameLabel")
        self.horizontalLayout_3.addWidget(self.StaffNameLabel, 0, QtCore.Qt.AlignLeft)
        self.ShowStaffNameLabel = QtWidgets.QLabel(self.InforStaffFrame)
        self.ShowStaffNameLabel.setObjectName("ShowStaffNameLabel")
        self.horizontalLayout_3.addWidget(self.ShowStaffNameLabel, 0, QtCore.Qt.AlignLeft)
        self.LogoutButton = QtWidgets.QPushButton(self.InforStaffFrame)
        self.LogoutButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.LogoutButton.setStyleSheet("QPushButton {\n"
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
        icon.addPixmap(QtGui.QPixmap("./icons/log-out.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LogoutButton.setIcon(icon)
        self.LogoutButton.setObjectName("LogoutButton")
        self.horizontalLayout_3.addWidget(self.LogoutButton, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_3.addWidget(self.InforStaffFrame)
        self.FaceCameralabel = QtWidgets.QFrame(self.RightFrame)
        self.FaceCameralabel.setStyleSheet("border-color: rgb(255,255,255);\n"
                                           "border-style: inset;\n"
                                           "border-width: 1.5px;\n"
                                           "border-radius: 8px;\n"
                                           "color: rgb(255, 255, 255);")
        self.FaceCameralabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FaceCameralabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FaceCameralabel.setObjectName("FaceCameralabel")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.FaceCameralabel)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.FaceLabel = QtWidgets.QLabel(self.FaceCameralabel)
        self.FaceLabel.setScaledContents(True)
        self.FaceLabel.setMinimumSize(QtCore.QSize(500, 500))
        self.FaceLabel.setMaximumSize(QtCore.QSize(500, 500))
        self.FaceLabel.setStyleSheet("border: none;\n"
        "background-color: rgb(255, 255, 255);\n")
        self.FaceLabel.setObjectName("FaceLabel")
        self.verticalLayout_4.addWidget(self.FaceLabel)
        self.verticalLayout_3.addWidget(self.FaceCameralabel)
        self.InforFrame = QtWidgets.QFrame(self.RightFrame)
        self.InforFrame.setStyleSheet("QFrame {\n"
                                      "border-color: rgb(255,255,255);\n"
                                      "border-style: inset;\n"
                                      "border-width: 1.5px;\n"
                                      "border-radius: 8px;\n"
                                      "}")
        self.InforFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.InforFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.InforFrame.setObjectName("InforFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.InforFrame)
        self.gridLayout.setContentsMargins(30, -1, 15, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.LicensePlateLabel = QtWidgets.QLabel(self.InforFrame)
        self.LicensePlateLabel.setStyleSheet("border: none;")
        self.LicensePlateLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LicensePlateLabel.setObjectName("LicensePlateLabel")
        self.gridLayout.addWidget(self.LicensePlateLabel, 0, 0, 1, 1)
        self.LicensePlateValueLabel = QtWidgets.QLabel(self.InforFrame)
        self.LicensePlateValueLabel.setStyleSheet("border: none;")
        self.LicensePlateValueLabel.setObjectName("LicensePlateValueLabel")
        self.gridLayout.addWidget(self.LicensePlateValueLabel, 0, 1, 1, 1)
        self.IDLabel = QtWidgets.QLabel(self.InforFrame)
        self.IDLabel.setStyleSheet("border: none;")
        self.IDLabel.setObjectName("IDLabel")
        self.gridLayout.addWidget(self.IDLabel, 1, 0, 1, 1)
        self.IDValuelabel = QtWidgets.QLabel(self.InforFrame)
        self.IDValuelabel.setStyleSheet("border: none;")
        self.IDValuelabel.setObjectName("IDValuelabel")
        self.gridLayout.addWidget(self.IDValuelabel, 1, 1, 1, 1)
        self.TimeInLabel = QtWidgets.QLabel(self.InforFrame)
        self.TimeInLabel.setStyleSheet("border: none;")
        self.TimeInLabel.setObjectName("TimeInLabel")
        self.gridLayout.addWidget(self.TimeInLabel, 2, 0, 1, 1)
        self.TimeInValueLabel = QtWidgets.QLabel(self.InforFrame)
        self.TimeInValueLabel.setStyleSheet("border: none;")
        self.TimeInValueLabel.setObjectName("TimeInValueLabel")
        self.gridLayout.addWidget(self.TimeInValueLabel, 2, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.InforFrame)
        self.horizontalLayout_2.addWidget(self.RightFrame)
        self.verticalLayout.addWidget(self.TopFrame)
        self.BottomFrame = QtWidgets.QFrame(self.IncomeTab)
        self.BottomFrame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.BottomFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BottomFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BottomFrame.setObjectName("BottomFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.BottomFrame)
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setSpacing(9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.StartButton = QtWidgets.QPushButton(self.BottomFrame)
        self.StartButton.setMinimumSize(QtCore.QSize(0, 91))
        self.StartButton.setStyleSheet("QPushButton {\n"
                                       "border-color: rgb(255,255,255);\n"
                                       "border-style: inset;\n"
                                       "border-width: 1.5px;\n"
                                       "border-radius: 5px;\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "font: 75 20pt \"Ubuntu Condensed\";\n"
                                       "padding: 0 10px;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color: rgb(122, 155, 153);\n"
                                       "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./icons/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StartButton.setIcon(icon1)
        self.StartButton.setIconSize(QtCore.QSize(30, 30))
        self.StartButton.setObjectName("StartButton")
        self.horizontalLayout_4.addWidget(self.StartButton)


        self.verticalLayout.addWidget(self.BottomFrame)
        self.tabWidget.addTab(self.IncomeTab, "")


        self.OutcomeTab = QtWidgets.QWidget()
        self.OutcomeTab.setObjectName("OutcomeTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.OutcomeTab)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.TopFrame_2 = QtWidgets.QFrame(self.OutcomeTab)
        self.TopFrame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TopFrame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TopFrame_2.setObjectName("TopFrame_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.TopFrame_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.LeftFrame_2 = QtWidgets.QFrame(self.TopFrame_2)
        self.LeftFrame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LeftFrame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LeftFrame_2.setObjectName("LeftFrame_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.LeftFrame_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.CameraOutFrame = QtWidgets.QFrame(self.LeftFrame_2)
        self.CameraOutFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.CameraOutFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.CameraOutFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CameraOutFrame.setObjectName("CameraOutFrame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.CameraOutFrame)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.CameraOutTitle = QtWidgets.QLabel(self.CameraOutFrame)
        self.CameraOutTitle.setObjectName("CameraOutTitle")
        self.horizontalLayout_7.addWidget(self.CameraOutTitle)
        self.verticalLayout_6.addWidget(self.CameraOutFrame)
        self.ShowCameraOutFrame = QtWidgets.QFrame(self.LeftFrame_2)
        self.ShowCameraOutFrame.setStyleSheet("border-color: rgb(255,255,255);\n"
                                              "border-style: inset;\n"
                                              "border-width: 1.5px;\n"
                                              "border-radius: 8px;\n"
                                              "color: rgb(255, 255, 255);")
        self.ShowCameraOutFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ShowCameraOutFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ShowCameraOutFrame.setObjectName("ShowCameraOutFrame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.ShowCameraOutFrame)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.LPCameraOutLabel = QtWidgets.QLabel(self.ShowCameraOutFrame)
        sizePolicy.setHeightForWidth(self.LPCameraOutLabel.sizePolicy().hasHeightForWidth())
        self.LPCameraOutLabel.setSizePolicy(sizePolicy)
        self.LPCameraOutLabel.setMinimumSize(QtCore.QSize(640, 640))

        self.LPCameraOutLabel.setStyleSheet("border-color: rgb(255,255,255);\n"
                                          "border-style: inset;\n"
                                          "border-width: 1.5px;\n"
                                          "border-radius: 8px;\n"
                                          "color: rgb(255, 255, 255);")

        self.LPCameraOutLabel.setScaledContents(True)
        self.LPCameraOutLabel.setObjectName("LPCameraOutLabel")
        self.horizontalLayout_8.addWidget(self.LPCameraOutLabel)
        self.verticalLayout_6.addWidget(self.ShowCameraOutFrame)
        self.horizontalLayout_6.addWidget(self.LeftFrame_2)
        self.RightFrame2 = QtWidgets.QFrame(self.TopFrame_2)
        self.RightFrame2.setMaximumSize(QtCore.QSize(700, 16777215))
        self.RightFrame2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.RightFrame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RightFrame2.setObjectName("RightFrame2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.RightFrame2)
        self.verticalLayout_7.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.InfoStaffTitleFrame = QtWidgets.QFrame(self.RightFrame2)
        self.InfoStaffTitleFrame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.InfoStaffTitleFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.InfoStaffTitleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.InfoStaffTitleFrame.setObjectName("InfoStaffTitleFrame")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.InfoStaffTitleFrame)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.StaffNameOutLabel = QtWidgets.QLabel(self.InfoStaffTitleFrame)
        self.StaffNameOutLabel.setStyleSheet("padding: 0 5px;\n"
                                             "font: 75 15pt \"Ubuntu Condensed\";")
        self.StaffNameOutLabel.setObjectName("StaffNameOutLabel")
        self.horizontalLayout_9.addWidget(self.StaffNameOutLabel, 0, QtCore.Qt.AlignLeft)
        self.NameStaffOut = QtWidgets.QLabel(self.InfoStaffTitleFrame)
        self.NameStaffOut.setObjectName("NameStaffOut")
        self.horizontalLayout_9.addWidget(self.NameStaffOut)
        self.LogOut2Button = QtWidgets.QPushButton(self.InfoStaffTitleFrame)
        self.LogOut2Button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.LogOut2Button.setStyleSheet("QPushButton {\n"
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
        self.LogOut2Button.setIcon(icon)
        self.LogOut2Button.setObjectName("LogOut2Button")
        self.horizontalLayout_9.addWidget(self.LogOut2Button, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_7.addWidget(self.InfoStaffTitleFrame)
        self.FaceOutFrame = QtWidgets.QFrame(self.RightFrame2)
        self.FaceOutFrame.setStyleSheet("border-color: rgb(255,255,255);\n"
                                        "border-style: inset;\n"
                                        "border-width: 1.5px;\n"
                                        "border-radius: 8px;\n"
                                        "color: rgb(255, 255, 255);")
        self.FaceOutFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FaceOutFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FaceOutFrame.setObjectName("FaceOutFrame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.FaceOutFrame)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ShowFaceOutLabel = QtWidgets.QLabel(self.FaceOutFrame)
        self.ShowFaceOutLabel.setScaledContents(True)
        self.ShowFaceOutLabel.setMinimumSize(QtCore.QSize(500, 500))
        self.ShowFaceOutLabel.setMaximumSize(QtCore.QSize(500, 500))

        self.ShowFaceOutLabel.setStyleSheet("border: none;\n"
        "background-color: rgb(255, 255, 255);\n")
        self.ShowFaceOutLabel.setObjectName("ShowFaceOutLabel")
        self.verticalLayout_8.addWidget(self.ShowFaceOutLabel)
        self.verticalLayout_7.addWidget(self.FaceOutFrame)
        self.InForOutFrame = QtWidgets.QFrame(self.RightFrame2)
        self.InForOutFrame.setStyleSheet("border-color: rgb(255,255,255);\n"
                                         "border-style: inset;\n"
                                         "border-width: 1.5px;\n"
                                         "border-radius: 8px;\n"
                                         "color: rgb(255, 255, 255);")
        self.InForOutFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.InForOutFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.InForOutFrame.setObjectName("InForOutFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.InForOutFrame)
        self.gridLayout_2.setContentsMargins(30, -1, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LPOutLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.LPOutLabel.setStyleSheet("border: none;")
        self.LPOutLabel.setObjectName("LPOutLabel")
        self.gridLayout_2.addWidget(self.LPOutLabel, 0, 0, 1, 1)
        self.IDValueLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.IDValueLabel.setStyleSheet("border: none;")
        self.IDValueLabel.setObjectName("IDValueLabel")
        self.gridLayout_2.addWidget(self.IDValueLabel, 1, 1, 1, 1)
        self.CostLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.CostLabel.setStyleSheet("border: none;")
        self.CostLabel.setObjectName("CostLabel")
        self.gridLayout_2.addWidget(self.CostLabel, 5, 0, 1, 1)
        self.CostValueLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.CostValueLabel.setStyleSheet("border: none;")
        self.CostValueLabel.setObjectName("CostValueLabel")
        self.gridLayout_2.addWidget(self.CostValueLabel, 5, 1, 1, 1)
        self.TimeOutValueLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.TimeOutValueLabel.setStyleSheet("border: none;")
        self.TimeOutValueLabel.setObjectName("TimeOutValueLabel")
        self.gridLayout_2.addWidget(self.TimeOutValueLabel, 3, 1, 1, 1)
        self.TotalTimeLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.TotalTimeLabel.setStyleSheet("border: none;")
        self.TotalTimeLabel.setObjectName("TotalTimeLabel")
        self.gridLayout_2.addWidget(self.TotalTimeLabel, 4, 0, 1, 1)
        self.LBValueLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.LBValueLabel.setStyleSheet("border: none;")
        self.LBValueLabel.setObjectName("LBValueLabel")
        self.gridLayout_2.addWidget(self.LBValueLabel, 0, 1, 1, 1)
        self.TimeOutLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.TimeOutLabel.setStyleSheet("border: none;")
        self.TimeOutLabel.setObjectName("TimeOutLabel")
        self.gridLayout_2.addWidget(self.TimeOutLabel, 3, 0, 1, 1)
        self.IDOutLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.IDOutLabel.setStyleSheet("border: none;")
        self.IDOutLabel.setObjectName("IDOutLabel")
        self.gridLayout_2.addWidget(self.IDOutLabel, 1, 0, 1, 1)
        self.TotalTimeValueLabel = QtWidgets.QLabel(self.InForOutFrame)
        self.TotalTimeValueLabel.setStyleSheet("border: none;")
        self.TotalTimeValueLabel.setObjectName("TotalTimeValueLabel")
        self.gridLayout_2.addWidget(self.TotalTimeValueLabel, 4, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.InForOutFrame)
        self.horizontalLayout_6.addWidget(self.RightFrame2)
        self.verticalLayout_5.addWidget(self.TopFrame_2)
        self.BottomFrame_2 = QtWidgets.QFrame(self.OutcomeTab)
        self.BottomFrame_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.BottomFrame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BottomFrame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BottomFrame_2.setObjectName("BottomFrame_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.BottomFrame_2)
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.StartOutButton = QtWidgets.QPushButton(self.BottomFrame_2)
        self.StartOutButton.setMinimumSize(QtCore.QSize(0, 91))
        self.StartOutButton.setStyleSheet("QPushButton {\n"
                                          "border-color: rgb(255,255,255);\n"
                                          "border-style: inset;\n"
                                          "border-width: 1.5px;\n"
                                          "border-radius: 5px;\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "font: 75 20pt \"Ubuntu Condensed\";\n"
                                          "padding: 0 10px;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:pressed{\n"
                                          "    background-color: rgb(122, 155, 153);\n"
                                          "}")
        self.StartOutButton.setIcon(icon1)
        self.StartOutButton.setIconSize(QtCore.QSize(30, 30))
        self.StartOutButton.setObjectName("StartOutButton")
        self.horizontalLayout_10.addWidget(self.StartOutButton)


        self.verticalLayout_5.addWidget(self.BottomFrame_2)
        self.tabWidget.addTab(self.OutcomeTab, "")


        self.CustomerTab =  QtWidgets.QWidget()
        self.CustomerTab .setObjectName("CustomerTab")
        ###
        self.gridLayout_3 = QtWidgets.QGridLayout(self.CustomerTab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame = QtWidgets.QFrame(self.CustomerTab)
        self.frame.setStyleSheet("background-color: rgb(18, 16, 61);\n"
                                 "")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setMinimumSize(QtCore.QSize(300, 50))
        self.label_3.setMaximumSize(QtCore.QSize(300, 50))
        self.label_3.setStyleSheet("font: 75 30pt \"Ubuntu Condensed\";\n"
                                   "color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_18.addWidget(self.label_3)
        self.verticalLayout_11.addWidget(self.frame_6, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.frame_11 = QtWidgets.QFrame(self.frame)
        self.frame_11.setMinimumSize(QtCore.QSize(0, 576))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.frame_12 = QtWidgets.QFrame(self.frame_11)
        self.frame_12.setMinimumSize(QtCore.QSize(800, 552))
        self.frame_12.setStyleSheet("\n"
                                    "background-color: rgb(255, 255, 255);")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_12)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "font: 75 15pt \"Ubuntu Condensed\";")
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setObjectName("tableWidget_3")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.horizontalLayout_20.addWidget(self.tableWidget)
        self.horizontalLayout_19.addWidget(self.frame_12)
        self.frame_13 = QtWidgets.QFrame(self.frame_11)
        self.frame_13.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.DeleteButton = QtWidgets.QPushButton(self.frame_13)
        self.DeleteButton.setMinimumSize(QtCore.QSize(108, 38))
        self.DeleteButton.setMaximumSize(QtCore.QSize(106, 30))
        self.DeleteButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 75 15pt \"Ubuntu Condensed\";")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon5)
        self.DeleteButton.setObjectName("pushButton_3")
        self.horizontalLayout_21.addWidget(self.DeleteButton)
        self.horizontalLayout_19.addWidget(self.frame_13)
        self.verticalLayout_11.addWidget(self.frame_11)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)
        ###
        self.tabWidget.addTab(self.CustomerTab, "")


        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        self.Center(MainWindow)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Parking Management"))
        self.TitleLabel.setText(_translate("MainWindow", "Camera In"))
        self.CarCameraLabel.setText(_translate("MainWindow", "Camera"))
        self.StaffNameLabel.setText(_translate("MainWindow", "Name Staff"))
        self.ShowStaffNameLabel.setText(_translate("MainWindow", self.StaffName))
        self.LogoutButton.setText(_translate("MainWindow", "Logout"))
        self.FaceLabel.setText(_translate("MainWindow", "Face"))
        self.LicensePlateLabel.setText(_translate("MainWindow", "License Plates"))
        self.LicensePlateValueLabel.setText(_translate("MainWindow", "Unknow"))
        self.IDLabel.setText(_translate("MainWindow", "ID"))
        self.IDValuelabel.setText(_translate("MainWindow", "None"))
        self.TimeInLabel.setText(_translate("MainWindow", "Time In"))
        self.TimeInValueLabel.setText(_translate("MainWindow", "None"))
        self.StartButton.setText(_translate("MainWindow", "NEW"))


        self.tabWidget.setTabText(self.tabWidget.indexOf(self.IncomeTab), _translate("MainWindow", "Incoming"))
        self.CameraOutTitle.setText(_translate("MainWindow", "Camera Out"))
        self.LPCameraOutLabel.setText(_translate("MainWindow", "Camera"))
        self.StaffNameOutLabel.setText(_translate("MainWindow", "Name Staff"))
        self.NameStaffOut.setText(_translate("MainWindow", self.StaffName))
        self.LogOut2Button.setText(_translate("MainWindow", "Logout"))
        self.ShowFaceOutLabel.setText(_translate("MainWindow", "Face"))
        self.LPOutLabel.setText(_translate("MainWindow", "License Plates"))
        self.IDValueLabel.setText(_translate("MainWindow", "None"))
        self.CostLabel.setText(_translate("MainWindow", "Cost"))
        self.CostValueLabel.setText(_translate("MainWindow", "0 VND"))
        self.TimeOutValueLabel.setText(_translate("MainWindow", "None"))
        self.TotalTimeLabel.setText(_translate("MainWindow", "Total Time"))
        self.LBValueLabel.setText(_translate("MainWindow", "Unknow"))
        self.TimeOutLabel.setText(_translate("MainWindow", "Time Out"))
        self.IDOutLabel.setText(_translate("MainWindow", "ID"))
        self.TotalTimeValueLabel.setText(_translate("MainWindow", "None"))
        self.StartOutButton.setText(_translate("MainWindow", "NEW"))


        self.tabWidget.setTabText(self.tabWidget.indexOf(self.OutcomeTab), _translate("MainWindow", "Outcoming"))

        self.label_3.setText(_translate("MainWindow", "CUSTOMERS"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Licence Plate"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Time In"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Staff Name"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CustomerTab), _translate("MainWindow", "Customers"))

        ###
        self.GetLicencePlate()
        self.StartButton.clicked.connect(self.GetLicencePlate)
        self.StartOutButton.clicked.connect(self.GetLicencePlateOut)
        self.tabWidget.currentChanged.connect(self.ChangeTab)

        self.StartButton.setShortcut("Ctrl+N")
        self.StartOutButton.setShortcut("Ctrl+N")

        ###
        self.LogoutButton.setShortcut("Ctrl+L")
        self.LogoutButton.clicked.connect(self.Logout)
        self.LogoutButton.clicked.connect(MainWindow.close)

        self.LogOut2Button.setShortcut("Ctrl+L")
        self.LogOut2Button.clicked.connect(self.Logout)
        self.LogOut2Button.clicked.connect(MainWindow.close)

        self.DeleteButton.clicked.connect(self.Delete)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
