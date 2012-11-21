#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore, Qt

import smartboard_driver
import thread

class frmMain(QtGui.QWidget):
    
    def __init__(self):
        super(frmMain, self).__init__()
        
        self.initUI()
        self.savenum = 0
        
    def initUI(self):      

        global data

	self.data = data

        self.setGeometry(300, 300, 600, 800)
        self.setWindowTitle('Draw text')
        self.show()

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawData(event, qp)
        qp.end()

    def keyPressEvent(self, event):
         if type(event) == QtGui.QKeyEvent:
             if(event.key() == ord('s') or event.key() == ord('S')):
		print 'spremi'

             event.accept()
         else:
             event.ignore()
        
    def spremiSliku(self):
        img = QtGui.QImage(600, 800, QtGui.QImage.Format_RGB32)
        qp = QtGui.QPainter(img)
        qp.fillRect(0,0,600,800, QtGui.QColor(255,255,255))

        zelena = QtGui.QColor(0,255,0)
        crna = QtGui.QColor(0,0,0)
        
        trenutna = zelena
        qp.setPen(trenutna)

        if(len(self.data) > 2):
          for i in range(0,len(self.data)-1):

            scale_factor = 8

            x1 = float(self.data[i][0])
            y1 = float(self.data[i][1])
            x2 = float(self.data[i+1][0])
            y2 = float(self.data[i+1][1])
            boja1 = int(self.data[i][2])
            boja2 = int(self.data[i+1][2])
            p1 = int(self.data[i][3])
            p2 = int(self.data[i+1][3])

            if(p1 > 0 and p2 > 0):

              if(x1 < -100 and x2 < -100):	#ako je novi dokument
                pass

              else:

                if(boja1 >= 40 and boja1 < 50 and trenutna != zelena):
                  trenutna = zelena
                  qp.setPen(trenutna)

                elif(boja1 >=60 and boja1 < 70 and trenutna != crna):
                  trenutna = crna
                  qp.setPen(trenutna)
                
                if(boja1 >= 40 and boja2 >= 40):
                  qp.drawLine(x1 / scale_factor, y1 / scale_factor, x2 / scale_factor, y2 / scale_factor)

        qp.end()
        img.save('slika' + str(self.savenum) + '.png', 'PNG')
        self.savenum = self.savenum + 1
        print 'save'

    def addPoint(self, pointData):
        pd = pointData.split(';')
        self.data.append([pd[1], pd[2], pd[4], pd[5]])
        self.update()

    def drawData(self, event, qp):

        
        zelena = QtGui.QColor(0,255,0)
        crna = QtGui.QColor(0,0,0)
        
        trenutna = zelena

        qp.setPen(trenutna)

        if(len(self.data) > 2):
          for i in range(0,len(self.data)-1):

            scale_factor = 8

            x1 = float(self.data[i][0])
            y1 = float(self.data[i][1])
            x2 = float(self.data[i+1][0])
            y2 = float(self.data[i+1][1])
            boja1 = int(self.data[i][2])
            boja2 = int(self.data[i+1][2])
            p1 = int(self.data[i][3])
            p2 = int(self.data[i+1][3])

            if(p1 > 0 and p2 > 0):

              if(x1 < -100 and x2 < -100):	#ako je novi dokument
                self.spremiSliku()
                del self.data[0:len(self.data) - 1]
                return

              else:

                if(boja1 >= 40 and boja1 < 50 and trenutna != zelena):
                  trenutna = zelena
                  qp.setPen(trenutna)

                elif(boja1 >=60 and boja1 < 70 and trenutna != crna):
                  trenutna = crna
                  qp.setPen(trenutna)
                
                if(boja1 >= 40 and boja2 >= 40):
                  qp.drawLine(x1 / scale_factor, y1 / scale_factor, x2 / scale_factor, y2 / scale_factor)
    


if __name__ == '__main__':

    global data
    data = []

    app = QtGui.QApplication(sys.argv)
    ex = frmMain()

    #obrada ulaznih argumenta
    if(len(sys.argv) == 1):
      input_file_name = '/dev/usb/hiddev0'
    else:
      input_file_name = sys.argv[1]
    input_file = open(input_file_name, 'rb')

    sbd = smartboard_driver.smartboard_driver(input_file)
    sbd.update = ex.addPoint
    thr = thread.start_new_thread(sbd.run, ())

    
    sys.exit(app.exec_())

    
