# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ui(object):
    def setupUi(self, ui):
        ui.setObjectName("ui")
        ui.resize(660, 555)
        self.graphicsView = QtWidgets.QGraphicsView(ui)
        self.graphicsView.setGeometry(QtCore.QRect(120, 20, 512, 512))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtWidgets.QPushButton(ui)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 80, 25))
        self.pushButton.setObjectName("save_stroke")
        self.pushButton_2 = QtWidgets.QPushButton(ui)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 60, 80, 25))
        self.pushButton_2.setObjectName("Curvature")
        self.pushButton_3 = QtWidgets.QPushButton(ui)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 100, 80, 25))
        self.pushButton_3.setObjectName("Derivation")

        self.pushButton = QtWidgets.QPushButton(ui)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 80, 25))
        self.pushButton.setObjectName("save_stroke")




        self.retranslateUi(ui)
        QtCore.QMetaObject.connectSlotsByName(ui)

        self.pushButton.clicked.connect(ui.save_img)
        self.pushButton_2.clicked.connect(ui.curvature)
        self.pushButton_3.clicked.connect(ui.derivation)

    def retranslateUi(self, ui):
        _translate = QtCore.QCoreApplication.translate
        ui.setWindowTitle(_translate("ui", "ui"))
        self.pushButton.setText(_translate("ui", "Frechet"))
        self.pushButton_2.setText(_translate("ui", "Curvature"))
        self.pushButton_3.setText(_translate("ui", "Derivation"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_ui()
#     ui.setupUi(ui)
#     ui.show()
#     sys.exit(app.exec_())