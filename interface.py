# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pykseno.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 838)
        font = QtGui.QFont()
        font.setFamily("Ink Free")
        font.setPointSize(6)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("color: rgb(255, 255, 255);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(22, 21, 21);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft PhagsPa")
        font.setPointSize(20)
        self.btnStop.setFont(font)
        self.btnStop.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnStop.setObjectName("btnStop")
        self.gridLayout.addWidget(self.btnStop, 2, 1, 1, 1)
        self.console = QtWidgets.QListWidget(self.centralwidget)
        self.console.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(99, 99, 99);")
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.console, 1, 0, 1, 2)
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft PhagsPa")
        font.setPointSize(20)
        self.btnStart.setFont(font)
        self.btnStart.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnStart.setObjectName("btnStart")
        self.gridLayout.addWidget(self.btnStart, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Sitka Text Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Голосовой помощник"))
        self.btnStop.setText(_translate("MainWindow", "Стоп"))
        self.btnStart.setText(_translate("MainWindow", "Пуск"))
        self.label.setText(_translate("MainWindow", "                                                                 Голосовой помощник Ксено"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
