
from PyQt5.QtWidgets import QDesktopWidget

from PyQt5 import QtCore, QtGui, QtWidgets
from pymongo import MongoClient
import LoginFace,Admin,MainWindow


class UiLoginWindow(object):
    def __init__(self):

        self.UserNameState = None
        self.PassWordState = None

        uri = "mongodb://localhost:27017/"
        Client = MongoClient(uri)
        DataBase = Client["Thien"]

        self.AdminCollection = DataBase["Admin"]
        self.UserCollection  = DataBase["User"]


    def OpenMainWindow(self):

        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindowUi = MainWindow.Ui_MainWindow(StaffName=self.UserDocument['Name'])
        self.MainWindowUi.setupUi(self.MainWindow)
        self.LogInWindow.close()
        self.MainWindow.show()

    def OpenAdminWindow(self):
        self.AdminWindow = QtWidgets.QMainWindow()
        self.AdminUi = Admin.Ui_AdminWindow()
        self.AdminUi.setupUi(self.AdminWindow)

        self.AdminWindow.show()
        self.LogInWindow.close()

    def OpenFaceWindowFunction(self):
        self.FaceWindow = QtWidgets.QMainWindow()
        self.FaceUi = LoginFace.Ui_LoginFaceWindow()
        self.FaceUi.setupUi(self.FaceWindow)
        self.FaceWindow.show()

    def CheckEnterUsername(self):
        self.Username = self.GetUserLine.text()
        if self.Username == "":
            return False
        else:
            return True

    def CheckEnterPassWord(self):
        self.PassWord = self.GetPassWordLine.text()
        if self.PassWord== "":
            return False
        else:
            return True
    def CheckAccount(self):
        self.UserNameState = None
        self.PassWordState = None
        if self.CheckEnterUsername():

            for self.AdminDocument in self.AdminCollection.find():
                if self.Username == self.AdminDocument['UserName']:
                    self.UserNameState = "Admin"
                    break

            if self.UserNameState == None:
                for self.UserDocument in self.UserCollection.find():
                    if self.Username == self.UserDocument['UserName']:

                        self.UserNameState = "User"
                        break

            if self.CheckEnterPassWord():
                if (self.UserNameState == "Admin") and (self.PassWord == self.AdminDocument["PassWord"]):
                    self.PassWordState = "Admin"
                elif (self.UserNameState == "User") and (self.PassWord == self.UserDocument["PassWord"]):
                    self.PassWordState = "User"
                else:
                    self.PassWordState = "False"
            else:
                self.PassWordState = "Empty"

        else:
            self.UserNameState = "Empty"


    def PressLineEdit(self,event):
        self.CheckAccount()
        if self.UserNameState == "Empty":
            self.WarningUserLabel.setText("Please enter user name")
            self.WarningPassWordLabel.setText("")

        elif self.UserNameState == None:
            self.WarningUserLabel.setText("User name not available")
            self.WarningPassWordLabel.setText("")
        else:
            self.WarningUserLabel.setText(u'\u2713')
            self.WarningPassWordLabel.setText("")


    def LoginFunction(self):
        self.CheckAccount()

        if self.UserNameState == "Empty":
            self.WarningUserLabel.setText("Please enter user name")
            self.WarningPassWordLabel.setText("")

        elif self.UserNameState == None:
            self.WarningUserLabel.setText("User name not available")
            self.WarningPassWordLabel.setText("")
        else:
            self.WarningUserLabel.setText(u'\u2713')
            if self.PassWordState == "Empty":
                self.WarningPassWordLabel.setText("Please enter password")
            elif self.PassWordState == "False":
                self.WarningPassWordLabel.setText("Incorrect password")
            elif self.PassWordState == "Admin":
                self.OpenAdminWindow()
            else:
                self.OpenMainWindow()




    def Center(self,widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())

    def setupUi(self, LogInWindow):
        self.LogInWindow = LogInWindow
        self.Center(LogInWindow)
        LogInWindow.setObjectName("LogInWindow")
        LogInWindow.resize(760, 658)
        LogInWindow.setMaximumSize(QtCore.QSize(760, 658))
        LogInWindow.setStyleSheet("background-color: rgb(211, 215, 207);")

        self.LoginWidget = QtWidgets.QWidget(LogInWindow)
        self.LoginWidget.setStyleSheet("background-color: rgb(129, 199, 195);\n"
"background-color: rgb(222, 226, 226);\n"
"background-color: rgb(12, 93, 123);\n"
"background-color: rgb(18, 16, 61);\n"
"")
        self.LoginWidget.setObjectName("LoginWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.LoginWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MainFrame = QtWidgets.QFrame(self.LoginWidget)
        self.MainFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.MainFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.LogoFrame = QtWidgets.QFrame(self.MainFrame)
        self.LogoFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LogoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LogoFrame.setObjectName("LogoFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.LogoFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.LogoLabel = QtWidgets.QLabel(self.LogoFrame)
        self.LogoLabel.setMaximumSize(QtCore.QSize(150, 150))
        self.LogoLabel.setText("")
        self.LogoLabel.setPixmap(QtGui.QPixmap("./icons/login.png"))
        self.LogoLabel.setScaledContents(True)
        self.LogoLabel.setObjectName("LogoLabel")
        self.verticalLayout_4.addWidget(self.LogoLabel)
        self.verticalLayout_2.addWidget(self.LogoFrame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.AccountFrame = QtWidgets.QFrame(self.MainFrame)
        self.AccountFrame.setMinimumSize(QtCore.QSize(100, 135))
        self.AccountFrame.setStyleSheet("font: 75 12pt \"Ubuntu Condensed\";")
        self.AccountFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AccountFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AccountFrame.setObjectName("AccountFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.AccountFrame)
        self.gridLayout.setHorizontalSpacing(18)
        self.gridLayout.setVerticalSpacing(9)
        self.gridLayout.setObjectName("gridLayout")

        self.GetUserLine = QtWidgets.QLineEdit(self.AccountFrame)
        self.GetUserLine.setMinimumSize(QtCore.QSize(0, 43))
        self.GetUserLine.setMaximumSize(QtCore.QSize(300, 16777215))
        self.GetUserLine.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 255, 255);\n"
"border-width : 1.5px;\n"
"border-style:inset;\n"
"border-radius: 8px;\n"
"padding: 0 5px;")
        self.GetUserLine.setObjectName("GetUserLine")
        self.gridLayout.addWidget(self.GetUserLine, 0, 2, 1, 1, QtCore.Qt.AlignVCenter)

        self.GetPassWordLine = QtWidgets.QLineEdit(self.AccountFrame)
        self.GetPassWordLine.setMinimumSize(QtCore.QSize(0, 43))
        self.GetPassWordLine.setMaximumSize(QtCore.QSize(300, 16777215))
        self.GetPassWordLine.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                           "background-color: rgb(255, 255, 255);\n"
                                           "border-width : 1.5px;\n"
                                           "border-style:inset;\n"
                                           "border-radius: 8px;\n"
                                           "padding: 0 5px;")
        self.GetPassWordLine.setObjectName("GetPassWordLine")
        self.GetPassWordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.GetPassWordLine, 1, 2, 1, 1, QtCore.Qt.AlignVCenter)

        self.PassWordLogo = QtWidgets.QLabel(self.AccountFrame)
        self.PassWordLogo.setMinimumSize(QtCore.QSize(0, 43))
        self.PassWordLogo.setText("")
        self.PassWordLogo.setPixmap(QtGui.QPixmap("./icons/key.svg"))
        self.PassWordLogo.setObjectName("PassWordLogo")
        self.gridLayout.addWidget(self.PassWordLogo, 1, 1, 1, 1, QtCore.Qt.AlignRight)
        self.WarningPassWordLabel = QtWidgets.QLabel(self.AccountFrame)
        self.WarningPassWordLabel.setStyleSheet("color: rgb(239, 41, 41);")
        self.WarningPassWordLabel.setObjectName("WarningPassWordLabel")
        self.gridLayout.addWidget(self.WarningPassWordLabel, 1, 3, 1, 1, QtCore.Qt.AlignLeft)
        self.WarningUserLabel = QtWidgets.QLabel(self.AccountFrame)
        self.WarningUserLabel.setMinimumSize(QtCore.QSize(0, 40))
        self.WarningUserLabel.setStyleSheet("\n"
"color: rgb(239, 41, 41);")
        self.WarningUserLabel.setObjectName("WarningUserLabel")
        self.gridLayout.addWidget(self.WarningUserLabel, 0, 3, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.UserLogo = QtWidgets.QLabel(self.AccountFrame)
        self.UserLogo.setMinimumSize(QtCore.QSize(0, 43))
        self.UserLogo.setText("")
        self.UserLogo.setPixmap(QtGui.QPixmap("./icons/user.svg"))
        self.UserLogo.setObjectName("UserLogo")
        self.gridLayout.addWidget(self.UserLogo, 0, 1, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.AccountFrame, 0, QtCore.Qt.AlignBottom)
        self.LogButtonFrame = QtWidgets.QFrame(self.MainFrame)
        self.LogButtonFrame.setMinimumSize(QtCore.QSize(300, 0))
        self.LogButtonFrame.setMaximumSize(QtCore.QSize(16777215, 180))
        self.LogButtonFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LogButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LogButtonFrame.setObjectName("LogButtonFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.LogButtonFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.LoginButton = QtWidgets.QPushButton(self.LogButtonFrame)
        self.LoginButton.setMinimumSize(QtCore.QSize(164, 43))
        self.LoginButton.setMaximumSize(QtCore.QSize(500, 16777215))
        self.LoginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LoginButton.setStyleSheet("QPushButton{\n"
"    \n"
"border-color: rgb(255 ,255,255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"background-color: rgb(56, 64, 95);\n"
"border-width : 1.5px;\n"
"border-style:inset;\n"
"border-radius: 8px;\n"
"padding: 0 5px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: rgb(122, 155, 153);\n"
"\n"
"}")
        self.LoginButton.setObjectName("LoginButton")
        self.verticalLayout_3.addWidget(self.LoginButton)
        self.LoginFaceButton = QtWidgets.QPushButton(self.LogButtonFrame)
        self.LoginFaceButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LoginFaceButton.setMinimumSize(QtCore.QSize(164, 43))
        self.LoginFaceButton.setMaximumSize(QtCore.QSize(500, 16777215))
        self.LoginFaceButton.setStyleSheet("QPushButton{\n"
"    \n"
"border-color: rgb(255 ,255,255);\n"
"font: 75 15pt \"Ubuntu Condensed\";\n"
"background-color: rgb(56, 64, 95);\n"
"border-width : 1.5px;\n"
"border-style:inset;\n"
"border-radius: 8px;\n"
"padding: 0 5px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(122, 155, 153);\n"
"\n"
"}")
        self.LoginFaceButton.setObjectName("LoginFaceButton")
        self.verticalLayout_3.addWidget(self.LoginFaceButton)
        self.verticalLayout_2.addWidget(self.LogButtonFrame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.MainFrame)
        LogInWindow.setCentralWidget(self.LoginWidget)

        self.retranslateUi(LogInWindow)
        QtCore.QMetaObject.connectSlotsByName(LogInWindow)


    def retranslateUi(self, LogInWindow):
        _translate = QtCore.QCoreApplication.translate
        LogInWindow.setWindowTitle(_translate("LogInWindow", "Parking Management"))
        self.GetPassWordLine.setPlaceholderText(_translate("LogInWindow", "Pass word"))
        self.GetPassWordLine.mouseReleaseEvent= self.PressLineEdit
        self.GetUserLine.setPlaceholderText(_translate("LogInWindow", "User name"))
        self.WarningPassWordLabel.setText(_translate("LogInWindow", ""))
        self.WarningUserLabel.setText(_translate("LogInWindow", ""))
        self.LoginButton.setText(_translate("LogInWindow", "LOGIN"))
        self.LoginFaceButton.setText(_translate("LogInWindow", "LOGIN WITH FACE"))

        self.LoginButton.setShortcut("Return")
        self.LoginFaceButton.setShortcut("Ctrl+F")

        self.LoginFaceButton.clicked.connect(self.OpenFaceWindowFunction)
        self.LoginFaceButton.clicked.connect(LogInWindow.close)
        self.LoginButton.clicked.connect(self.LoginFunction)




if __name__ == "__main__":
    import sys
    

    app = QtWidgets.QApplication(sys.argv)
    LogInWindow = QtWidgets.QMainWindow()
    ui = UiLoginWindow()
    ui.setupUi(LogInWindow)
    LogInWindow.show()
    sys.exit(app.exec_())