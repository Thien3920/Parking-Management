from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
import Login,CreateUser,History,UserList,CustomerList,CreateCustomer

import sys


class Ui_AdminWindow(object):
    def Center(self,widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())

    def setupUi(self, AdminWindow):
        self.Center(AdminWindow)
        AdminWindow.setObjectName("AdminWindow")
        AdminWindow.resize(903, 707)
        self.centralwidget = QtWidgets.QWidget(AdminWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(12, 11, 42);\n")
 
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(12, 11, 42);\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.LogoutButton = QtWidgets.QPushButton(self.frame)
        self.LogoutButton.setMinimumSize(QtCore.QSize(115, 35))
        self.LogoutButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.LogoutButton.setStyleSheet("\n"
"QPushButton {\n"
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
        self.LogoutButton.setIcon(icon)
        self.LogoutButton.setObjectName("LogoutButton")
        self.gridLayout.addWidget(self.LogoutButton, 0, 0, 1, 1)
        self.ExitButton = QtWidgets.QPushButton(self.frame)
        self.ExitButton.setMinimumSize(QtCore.QSize(0, 35))
        self.ExitButton.setMaximumSize(QtCore.QSize(100, 16777215))
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
        self.ExitButton.setObjectName("ExitButton")
        self.gridLayout.addWidget(self.ExitButton, 0, 2, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(12, 11, 42);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setSpacing(38)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setMinimumSize(QtCore.QSize(135, 50))
        self.label.setMaximumSize(QtCore.QSize(100, 50))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 30pt \"Ubuntu Condensed\";")
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_7.addWidget(self.frame_4)
        self.frame_20 = QtWidgets.QFrame(self.frame_3)
        self.frame_20.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.frame_20)
        self.label_5.setMinimumSize(QtCore.QSize(250, 250))
        self.label_5.setMaximumSize(QtCore.QSize(250, 250))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("./icons/Business-Man-Settings-01-256.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout_7.addWidget(self.frame_20)
        self.gridLayout.addWidget(self.frame_3, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_9.setContentsMargins(-1, -1, -1, 42)
        self.horizontalLayout_9.setSpacing(10)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setMinimumSize(QtCore.QSize(296, 0))
        self.frame_5.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(2)
        self.gridLayout_2.setVerticalSpacing(7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_12 = QtWidgets.QFrame(self.frame_5)
        self.frame_12.setStyleSheet("border: none;")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_2 = QtWidgets.QLabel(self.frame_12)
        self.label_2.setMinimumSize(QtCore.QSize(215, 50))
        self.label_2.setMaximumSize(QtCore.QSize(215, 50))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Ubuntu Condensed\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_10.addWidget(self.label_2)
        self.gridLayout_2.addWidget(self.frame_12, 0, 0, 1, 2, QtCore.Qt.AlignBottom)
        self.frame_14 = QtWidgets.QFrame(self.frame_5)
        self.frame_14.setStyleSheet("border: none;")
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 60)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.UsersButton = QtWidgets.QPushButton(self.frame_14)
        self.UsersButton.setMinimumSize(QtCore.QSize(0, 48))
        self.UsersButton.setStyleSheet("QPushButton {\n"
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
        icon2.addPixmap(QtGui.QPixmap("icons/users.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UsersButton.setIcon(icon2)
        self.UsersButton.setIconSize(QtCore.QSize(40, 30))
        self.UsersButton.setObjectName("UserButton")
        self.verticalLayout_5.addWidget(self.UsersButton)
        self.gridLayout_2.addWidget(self.frame_14, 1, 1, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.frame_13 = QtWidgets.QFrame(self.frame_5)
        self.frame_13.setStyleSheet("border: none;")
        self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 60)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.NewUseButton = QtWidgets.QPushButton(self.frame_13)
        self.NewUseButton.setMinimumSize(QtCore.QSize(162, 48))
        self.NewUseButton.setMaximumSize(QtCore.QSize(172, 16777215))
        self.NewUseButton.setStyleSheet("QPushButton {\n"
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
        icon3.addPixmap(QtGui.QPixmap("icons/user-plus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NewUseButton.setIcon(icon3)
        self.NewUseButton.setIconSize(QtCore.QSize(40, 30))
        self.NewUseButton.setObjectName("NewAccButton")
        self.verticalLayout_4.addWidget(self.NewUseButton)
        self.gridLayout_2.addWidget(self.frame_13, 1, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.horizontalLayout_9.addWidget(self.frame_5)
        self.frame_10 = QtWidgets.QFrame(self.frame_2)
        self.frame_10.setMinimumSize(QtCore.QSize(398, 0))
        self.frame_10.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;")
        self.frame_10.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_10)
        self.gridLayout_3.setContentsMargins(5, 0, 5, 0)
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_15 = QtWidgets.QFrame(self.frame_10)
        self.frame_15.setStyleSheet("border: none;")
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 60)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.NewCustomerButton = QtWidgets.QPushButton(self.frame_15)
        self.NewCustomerButton.setMinimumSize(QtCore.QSize(206, 48))
        self.NewCustomerButton.setMaximumSize(QtCore.QSize(149, 16777215))
        self.NewCustomerButton.setStyleSheet("QPushButton {\n"
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
        self.NewCustomerButton.setIcon(icon3)
        self.NewCustomerButton.setIconSize(QtCore.QSize(40, 30))
        self.NewCustomerButton.setObjectName("NewAccButton_2")
        self.horizontalLayout.addWidget(self.NewCustomerButton, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.gridLayout_3.addWidget(self.frame_15, 1, 0, 1, 1, QtCore.Qt.AlignBottom)
        self.frame_16 = QtWidgets.QFrame(self.frame_10)
        self.frame_16.setStyleSheet("border: none;")
        self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 60)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.CustomersButton = QtWidgets.QPushButton(self.frame_16)
        self.CustomersButton.setMinimumSize(QtCore.QSize(170, 48))
        self.CustomersButton.setMaximumSize(QtCore.QSize(99, 16777215))
        self.CustomersButton.setStyleSheet("QPushButton {\n"
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
        self.CustomersButton.setIcon(icon2)
        self.CustomersButton.setIconSize(QtCore.QSize(40, 30))
        self.CustomersButton.setObjectName("UserButton_2")
        self.horizontalLayout_7.addWidget(self.CustomersButton, 0, QtCore.Qt.AlignBottom)
        self.gridLayout_3.addWidget(self.frame_16, 1, 1, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.frame_17 = QtWidgets.QFrame(self.frame_10)
        self.frame_17.setStyleSheet("border: none;")
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_3 = QtWidgets.QLabel(self.frame_17)
        self.label_3.setMinimumSize(QtCore.QSize(215, 50))
        self.label_3.setMaximumSize(QtCore.QSize(215, 50))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Ubuntu Condensed\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_11.addWidget(self.label_3)
        self.gridLayout_3.addWidget(self.frame_17, 0, 0, 1, 2, QtCore.Qt.AlignBottom)
        self.horizontalLayout_9.addWidget(self.frame_10)
        self.frame_11 = QtWidgets.QFrame(self.frame_2)
        self.frame_11.setMaximumSize(QtCore.QSize(166, 16777215))
        self.frame_11.setStyleSheet("border-color: rgb(255,255,255);\n"
"border-style: inset;\n"
"border-width: 1.5px;\n"
"border-radius: 8px;")
        self.frame_11.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_6.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_18 = QtWidgets.QFrame(self.frame_11)
        self.frame_18.setStyleSheet("border: none;")
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_18)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_4 = QtWidgets.QLabel(self.frame_18)
        self.label_4.setMinimumSize(QtCore.QSize(215, 50))
        self.label_4.setMaximumSize(QtCore.QSize(215, 50))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 20pt \"Ubuntu Condensed\";")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_12.addWidget(self.label_4)
        self.verticalLayout_6.addWidget(self.frame_18, 0, QtCore.Qt.AlignBottom)
        self.frame_19 = QtWidgets.QFrame(self.frame_11)
        self.frame_19.setStyleSheet("border: none;")
        self.frame_19.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 60)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.HistoryButton = QtWidgets.QPushButton(self.frame_19)
        self.HistoryButton.setMinimumSize(QtCore.QSize(0, 48))
        self.HistoryButton.setMaximumSize(QtCore.QSize(172, 16777215))
        self.HistoryButton.setStyleSheet("QPushButton {\n"
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
        self.HistoryButton.setIcon(icon3)
        self.HistoryButton.setIconSize(QtCore.QSize(40, 30))
        self.HistoryButton.setObjectName("NewAccButton_3")
        self.horizontalLayout_8.addWidget(self.HistoryButton, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.verticalLayout_6.addWidget(self.frame_19, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.horizontalLayout_9.addWidget(self.frame_11, 0, QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 3, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.frame)
        AdminWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AdminWindow)
        QtCore.QMetaObject.connectSlotsByName(AdminWindow)

    def retranslateUi(self, AdminWindow):
        self.AdminWindow = AdminWindow
        _translate = QtCore.QCoreApplication.translate
        AdminWindow.setWindowTitle(_translate("AdminWindow", "Parking Management"))
        self.LogoutButton.setText(_translate("AdminWindow", "Logout"))
        self.ExitButton.setText(_translate("AdminWindow", "Exit"))
        self.label.setText(_translate("AdminWindow", "ADMIN"))
        self.label_2.setText(_translate("AdminWindow", "USER"))
        self.UsersButton.setText(_translate("AdminWindow", "USERS"))
        self.NewUseButton.setText(_translate("AdminWindow", "NEW USER"))
        self.NewCustomerButton.setText(_translate("AdminWindow", "NEW CUSTOMER"))
        self.CustomersButton.setText(_translate("AdminWindow", "CUSTOMERS"))
        self.label_3.setText(_translate("AdminWindow", "CUSTOMER"))
        self.label_4.setText(_translate("AdminWindow", "HISTORY"))
        self.HistoryButton.setText(_translate("AdminWindow", "History"))
        ##
        self.LogoutButton.clicked.connect(self.Logout)
        self.LogoutButton.clicked.connect(AdminWindow.close)

        self.NewUseButton.clicked.connect(self.NewAcc)
        self.NewUseButton.clicked.connect(AdminWindow.close)

        self.HistoryButton.clicked.connect(self.ViewHistory)
        self.HistoryButton.clicked.connect(AdminWindow.close)

        self.ExitButton.clicked.connect(AdminWindow.close)
        self.UsersButton.clicked.connect(self.ViewUser)
        self.UsersButton.clicked.connect(AdminWindow.close)

        self.NewCustomerButton.clicked.connect(self.OpenNewCustomerWindow)
        self.NewCustomerButton.clicked.connect(AdminWindow.close)

        self.CustomersButton.clicked.connect(self.ViewCustomer)
        self.CustomersButton.clicked.connect(AdminWindow.close)



    def OpenNewCustomerWindow(self):
        self.NewCustomerWindow = QtWidgets.QMainWindow()
        self.NewCustomerUi = CreateCustomer.Ui_MainWindow()
        self.NewCustomerUi.setupUi(self.NewCustomerWindow)
        self.NewCustomerWindow.show()
    
    def ViewCustomer(self):
        self.CustomerWindow = QtWidgets.QMainWindow()
        self.CustomerUi = CustomerList.Ui_MainWindow()
        self.CustomerUi.setupUi(self.CustomerWindow)
        self.CustomerWindow.show()


    def ViewHistory(self):
        self.HistoryWindow = QtWidgets.QMainWindow()
        self.HistoryUi = History.Ui_MainWindow()
        self.HistoryUi.setupUi(self.HistoryWindow)
        self.HistoryWindow.show()



    def ViewUser(self):
        self.UserWindow = QtWidgets.QMainWindow()
        self.UserUi = UserList.Ui_MainWindow()
        self.UserUi.setupUi(self.UserWindow)
        self.UserWindow.show()


    def NewAcc(self):
        self.NewUserWindow = QtWidgets.QMainWindow()
        self.NewUserUi = CreateUser.Ui_MainWindow()
        self.NewUserUi.setupUi(self.NewUserWindow)
        self.NewUserWindow.show()


    def Logout(self):
        self.LoginWindow = QtWidgets.QMainWindow()
        self.LoginUi = Login.UiLoginWindow()
        self.LoginUi.setupUi(self.LoginWindow)
        self.LoginWindow.show()


if __name__ == "__main__":
        
    app = QtWidgets.QApplication(sys.argv)
    AdminWindow = QtWidgets.QMainWindow()
    ui = Ui_AdminWindow()
    ui.setupUi(AdminWindow)
    AdminWindow.show()
    sys.exit(app.exec_())
