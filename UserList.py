

from PyQt5 import QtCore, QtGui, QtWidgets
from bson.objectid import ObjectId
from pymongo import MongoClient
from PyQt5.QtWidgets import QDesktopWidget
import sys
import Admin





class Ui_MainWindow(object):
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        Client = MongoClient(uri)
        DataBase = Client["Thien"]
        self.UserCollection = DataBase["User"]

    def Center(self,widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())

    def setupUi(self, MainWindow):
        self.Center(MainWindow)
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(12, 11, 42);\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(12, 11, 42);\n"
"")

        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.BackButton = QtWidgets.QPushButton(self.frame_2)
        self.BackButton.setMinimumSize(QtCore.QSize(75, 35))
        self.BackButton.setStyleSheet("\n"
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
        self.BackButton.setIcon(icon)
        self.BackButton.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.BackButton, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setMinimumSize(QtCore.QSize(300, 50))
        self.label.setMaximumSize(QtCore.QSize(300, 50))
        self.label.setStyleSheet("font: 75 30pt \"Ubuntu Condensed\";\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.ExitButton = QtWidgets.QPushButton(self.frame_2)
        self.ExitButton.setMinimumSize(QtCore.QSize(75, 35))
        self.ExitButton.setStyleSheet("\n"
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/power.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExitButton.setIcon(icon1)
        self.ExitButton.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.ExitButton, 0, 2, 1, 1, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 576))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setMinimumSize(QtCore.QSize(800, 552))
        self.frame_4.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_4)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 15pt \"Ubuntu Condensed\";")
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setObjectName("tableWidget")
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
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget.verticalHeader().setDefaultSectionSize(37)
        self.tableWidget.verticalHeader().setMinimumSectionSize(37)
        self.horizontalLayout_5.addWidget(self.tableWidget)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.DeleteButton = QtWidgets.QPushButton(self.frame_5)
        self.DeleteButton.setMinimumSize(QtCore.QSize(108, 38))
        self.DeleteButton.setMaximumSize(QtCore.QSize(106, 30))
        self.DeleteButton.setStyleSheet("\n"
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon2)
        self.DeleteButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.DeleteButton)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.verticalLayout.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Parking Management"))
        self.BackButton.setText(_translate("MainWindow", "Back"))
        self.label.setText(_translate("MainWindow", "USERS"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "UserName"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "PassWord"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))
        ##
        self.loaddata()
        self.DeleteButton.clicked.connect(self.Delete)
        self.BackButton.clicked.connect(self.Back)
        self.ExitButton.clicked.connect(MainWindow.close)



    def Back(self):
        self.AdminWindow = QtWidgets.QMainWindow()
        self.AdminUi = Admin.Ui_AdminWindow()
        self.AdminUi.setupUi(self.AdminWindow)
        self.AdminWindow.show()
        self.MainWindow.close()

    def Delete(self):
        idx = self.tableWidget.currentRow()

        if idx >= 0:
            ID = self.tableWidget.item(idx,0).text()
            x = self.UserCollection.find_one({'_id': ObjectId(ID)})
            self.UserCollection.delete_one(x)
            self.tableWidget.removeRow(idx)


    def loaddata(self):
        Dataset = []
        for UserDocument in self.UserCollection.find():
            Dataset.append(UserDocument)

        row = 0
        self.tableWidget.setRowCount(len(Dataset))
        for Data in Dataset:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(Data["_id"])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(Data['Name']))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(Data["UserName"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(Data["PassWord"]))

            row = row + 1



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
