# -*- coding: utf-8 -*-
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import os

import cv2
import sys
import time
import math

import pandas as pd

import pickle#load,save list

color_list = [QColor(0, 0, 0), QColor(204, 0, 0), QColor(76, 153, 0), QColor(204, 204, 0), QColor(204, 0, 204), QColor(51, 51, 255), QColor(0, 255, 255), QColor(51, 255, 255), QColor(255, 0, 0), QColor(102, 51, 0), QColor(102, 204, 0), QColor(255, 255, 0), QColor(0, 0, 153), QColor(0, 0, 204), QColor(255, 51, 153), QColor(0, 204, 204), QColor(0, 51, 0), QColor(255, 153, 51), QColor(0, 204, 0)]

class GraphicsScene(QGraphicsScene):
    def __init__(self, mode,parent=None):
        QGraphicsScene.__init__(self, parent)

        self.PosX=120
        self.PosY=20
        self.mode = mode

        self.drawCnt = 0
        self.prev_pt = None

        self.this_mouse_stroke=[]
        self.this_mouse_strokes=[]
        self.this_mouse_strokes_mark=[]
        self.line_size=[]#.append(self.size)
        self.line_color_list=[]
        self.current_color=(0, 0, 0)

        self.strokeptx = []
        self.strokepty = []
        self.stroke_cur = []
        self.stroke_k = []
        self.stroke = []
        self.strokes = []

        # save the points
        self.mask_points = []
        for i in range(len(color_list)):
            self.mask_points.append([])

        # save the size of points
        self.size_points = []
        for i in range(len(color_list)):
            self.size_points.append([])

        # save the history of edit
        self.history = []
        
        self.strokes_path="temp/strokes_save"#
        self.strokes_width_path="temp/strokes_width_save"#
        self.strokes_color_path="temp/strokes_color_save"
        # self.callbk= None
        self.mouse_left=False
        self.mouse_right=False
        
        

    def mousePressEvent(self, event):
        #self.mouse_clicked = True
        self.this_mouse_stroke=[]
        if(event.buttons() == Qt.LeftButton):
            self.mouse_left=True
        elif(event.buttons() == Qt.RightButton):
            self.mouse_right=True
            self.stroke_del(event)
        #if self.prev_pt is None:
        #   self.prev_pt = event.scenePos()
            #print(self.prev_pt)
    def setShadowImage(self):
        if(self.shadow_pil is None):
            return
        im = self.shadow_pil
        data = im.tobytes('raw', 'RGB')
        qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGB888)
        pix = QPixmap.fromImage(qim)
        pix=self.set_pixmap_alpha(pix)
        tst=self.addPixmap(pix)
        tst.setPos(self.PosX, self.PosY)  

    def mouseReleaseEvent(self, event):
        if self.mouse_right:
            self.mouse_right=False
            return
        if not self.mouse_left:
            return
            
        self.mouse_left=False
        
        self.prev_pt = None
        #self.mouse_clicked = False
        if(len(self.this_mouse_stroke)==0):
            return
        self.this_mouse_strokes.append(self.this_mouse_stroke)
        self.line_size.append(1)
        self.line_color_list.append(self.current_color)
        self.this_mouse_stroke=[]
        self.save_tmp_img(path=os.path.join(os.getcwd(),'temp','query_img.png'))

    def strokes_save(self):
        # print("save")
        
        px = self.strokeptx
        py = self.strokepty
        # print(len(px))

        for i in range(len(px)):
            self.stroke.append((px[i],py[i]))
            
            if i > 0:
                up =  abs(px[i-1]*py[i] - px[i]*py[i-1])
                down = np.power(np.square(px[i-1]) + np.square(py[i]),3/2)
                k = up/down
                self.stroke_k.append(k)
        # print(len(self.stroke_k))

        self.strokes.append(self.stroke)
        print(self.this_mouse_strokes)
        if len(self.this_mouse_strokes) > 1:
            stroke1 = self.this_mouse_strokes[1]
            stroke2 = self.this_mouse_strokes[0]
            print(stroke1)
            print(stroke2)
            result = self.frechet_distance(stroke1, stroke2)
            print(result)


        strokedata = pd.DataFrame(self.this_mouse_strokes)
        # print(strokedata)
        strokedata.to_csv("temp/stroke.csv")
       
    def strokes_load1(self):
        print("Curvature")
        px = self.strokeptx
        py = self.strokepty
        # print(len(px))

        for i in range(len(px)):
            self.stroke.append((px[i],py[i]))
            
            if i > 0:
                up =  abs(px[i-1]*py[i] - px[i]*py[i-1])
                down = np.power(np.square(px[i-1]) + np.square(py[i]),3/2)
                k = up/down
                self.stroke_cur.append(k)
        # print(len(self.stroke_k))

        self.strokes.append(self.stroke)
        print(self.stroke_cur)


        strokedata = pd.DataFrame(self.this_mouse_strokes)
        # print(strokedata)
        strokedata.to_csv("temp/stroke.csv")

    def strokes_load(self):
        print("Derivation")
        px = self.strokeptx
        py = self.strokepty
        # print(len(px))

        for i in range(len(px)):
            self.stroke.append((px[i],py[i]))
            
            if i > 0:
                dx = px[i] - px[i-1]
                dy = py[i] - py[i-1]
                if dy == 0:
                    k = 0
                else:
                    k = dx/dy
                self.stroke_k.append(k)
        # print(len(self.stroke_k))

        self.strokes.append(self.stroke)
        print(self.stroke_k)


        strokedata = pd.DataFrame(self.this_mouse_strokes)
        # print(strokedata)
        strokedata.to_csv("temp/stroke.csv")


    def euc_dist(self, pt1, pt2):
        return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))
 

    def _c(self, ca,i,j,P,Q):
        if ca[i,j] > -1:
            return ca[i,j]
        elif i == 0 and j == 0:
            ca[i,j] = self.euc_dist(P[0],Q[0])
        elif i > 0 and j == 0:
            ca[i,j] = max(self._c(ca,i-1,0,P,Q),self.euc_dist(P[i],Q[0]))
        elif i == 0 and j > 0:
            ca[i,j] = max(self._c(ca,0,j-1,P,Q),self.euc_dist(P[0],Q[j]))
        elif i > 0 and j > 0:
            ca[i,j] = max(min(self._c(ca,i-1,j,P,Q),self._c(ca,i-1,j-1,P,Q),self._c(ca,i,j-1,P,Q)),self.euc_dist(P[i],Q[j]))
        else:
            ca[i,j] = float("inf")
        return ca[i,j]
    
    def frechet_distance(self, P,Q):
        ca = np.ones((len(P),len(Q)))
        ca = np.multiply(ca,-1)
        return self._c(ca, len(P) - 1, len(Q) - 1, P, Q)  # ca是a*b的矩阵(3*4),2,3

    def mouseMoveEvent(self, event): # drawing
        if self.mouse_left:#self.mouse_clicked:
            this_pt=event.scenePos()
            #print(this_pt)
            point=(this_pt.x()-120.0,this_pt.y()-20.0)
            #print(point)
            pointx = this_pt.x()-120
            pointy = this_pt.y()-20
            self.strokeptx.append(pointx)
            self.strokepty.append(pointy)

            self.this_mouse_stroke.append(point)
            if self.prev_pt:
                
                #print('drawMask')
                #self.drawMask(self.prev_pt, event.scenePos(), color_list[self.mode], self.size)
                #self.drawMask(self.prev_pt, this_pt, color_list[0], self.size)
                self.drawMask(self.prev_pt, this_pt, QColor(self.current_color[0],self.current_color[1],self.current_color[2]), 1)
                pts = {}
                pts['prev'] = (int(self.prev_pt.x()),int(self.prev_pt.y()))
                pts['curr'] = (int(this_pt.x()),int(this_pt.y()))
        
                self.size_points[self.mode].append(1)
                self.mask_points[self.mode].append(pts)
                self.history.append(self.mode)
                self.prev_pt = this_pt
            else:
                self.prev_pt = this_pt

    def drawMask(self, prev_pt, curr_pt, color, size):
        self.drawCnt+=1
        if(False):
            return
        else:

            lineItem = QGraphicsLineItem()
            lineItem.setFlag(QGraphicsItem.ItemIsMovable)
            lineItem.setPen(QPen(color, size, Qt.SolidLine)) 
            lineItem.setLine(prev_pt.x(),prev_pt.y(),curr_pt.x(),curr_pt.y()) # rect

            self.addItem(lineItem)
            #I don't know why this will happen #setSceneRect!!!!
            if(self.drawCnt<0):
                self.undo()
                if(self.drawCnt==1):
                    #lineItem2 = QGraphicsLineItem(QLineF(prev_pt, curr_pt))
                    lineItem.setPen(QPen(QColor(255, 255, 255), size, Qt.SolidLine))
                    self.addItem(lineItem)
                #self.removeItem(lineItem)
        self.update()
        #self.save_tmp_img()
                        
    def drawStrokes(self,strokes,thicknessList,colorList):
        img = np.ones((512, 512, 3), np.uint8)*255#np.zeros((512, 512, 3), np.uint8)
        ptStart=None
        ptEnd=None
        point_color = (0, 0, 0) # BGR
        point_color2 = (255, 255, 255)
        lineType = 4
        idx=0
        for stroke in strokes:
            thickness=thicknessList[idx]
            point_color=colorList[idx]
            for point in stroke:
                point_int=(int(point[0]),int(point[1]))
                if(ptStart is None):
                    ptStart=point_int
                    continue
                ptEnd=point_int
                cv2.line(img, ptStart, ptEnd, point_color, thickness, lineType)
                ptStart=ptEnd
            ptStart=None
            idx+=1
            
        return img

    def Refresh(self):
        if len(self.items())>0:
            for i in range(len(self.items())):
                item = self.items()[0]
                self.removeItem(item)
                if len(self.history)>0:
                    if self.history[-1] == self.mode:
                        #print(self.mask_points[self.mode][-1])
                        self.mask_points[self.mode].pop()
                        self.size_points[self.mode].pop()
                        self.history.pop()         
        if len(self.this_mouse_strokes)>0:
            self.redraw()
    def redraw(self):
        cv_mat=self.drawStrokes(self.this_mouse_strokes,self.line_size,self.line_color_list)
        mat_img = cv2.cvtColor(np.array(cv_mat),cv2.COLOR_RGB2BGR)
        Qimage_new= QImage(mat_img, 512, 512, QImage.Format_RGB888)
        pix = QPixmap.fromImage(Qimage_new)
        tst=self.addPixmap(pix)
        tst.setPos(self.PosX, self.PosY)   

    def save_tmp_img(self,path): 
        self.Refresh()
        # Create a QImage to render to and fix up a QPainter for it.
        area= QRectF(0.0, 0.0, 512.0, 512.0)
        area2= QRectF(120.0, 20.0, 512.0, 512.0)
        image = QImage(area.width(), area.height(), QImage.Format_ARGB32_Premultiplied)

        painter = QPainter(image)

        # Render the region of interest to the QImage.
        self.render(painter, area, area2)
        painter.end()

        # Save the image to a file.
        #path=os.path.join(os.getcwd(),'temp','query_img.png')
        image.save(path)
        #image.save("capture.png")

