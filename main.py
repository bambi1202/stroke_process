import sys
import os
import cv2
import time
import numpy as np

from PIL import Image,ImageQt

from ui import Ui_ui
from mouse_event import GraphicsScene

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

class ui(QWidget, Ui_ui):
    def __init__(self):
        super(ui, self).__init__()
        self.setupUi(self)
        self.show()

        self.mode = 0
        # self.size = self.sld.value()

        self.mouse_clicked = False
        self.GotDetails = False
        self.scene = GraphicsScene(self.mode)
        self.scene.setSceneRect(120,20,512,512)
        self.scene.graphicsView = self.graphicsView
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def save_img(self):
        if False:
            if type(self.output_img):
                fileName, _ = QFileDialog.getSaveFileName(self, "Save File",
                        QDir.currentPath())
                cv2.imwrite(fileName+'.jpg',self.output_img)
        else:
            self.scene.strokes_save()

    def curvature(self):
        if False:
            if type(self.output_img):
                fileName, _ = QFileDialog.getSaveFileName(self, "Save File",
                        QDir.currentPath())
                cv2.imwrite(fileName+'.jpg',self.output_img)
        else:
            self.scene.strokes_load1()

    def derivation(self):
        if False:
            if type(self.output_img):
                fileName, _ = QFileDialog.getSaveFileName(self, "Save File",
                        QDir.currentPath())
                cv2.imwrite(fileName+'.jpg',self.output_img)
        else:
            self.scene.strokes_load()


if __name__ == "__main__":
    app = QApplication([])
    widget = ui()
    widget.show()
    sys.exit(app.exec_())