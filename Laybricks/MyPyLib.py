## My Python Library

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,QtWidgets
import sys, random,time, glob,pickle,os

from Lib_PyHigh import PythonHighlighter


##Print Log, substitute for print debugging
##In Goorm IDE Qt, You can't use print function, It doesn't show up

logPath = 'log.txt'
def printLog(s):
    if len(glob.glob(logPath))==0:
        os.system('touch '+logPath)
    f = open(logPath,'a')
    f.write(s+'\n')
    f.close()
    
def clearLog(s):
    f = open(logPath,'w')
    f.write("")
    f.close()
    

##safeCommand is substitute of os.system function. if the command doesn't ends, safecommand kills the process after the timeout.
## use like : if safeCommand(yourcommand):
##                ## do your things


def safeCommand(cmd,timeout):
    from subprocess import Popen
    proc = Popen(cmd,shell=True)
    startTime = time.time()
    while True:
        if not (proc.poll() is None):
            return True ##means success
        if time.time()-startTime>timeout:
            proc.kill()
            return False ## means killed by timeout
        



#30ms당 한번씩 signal 배출하는 쓰레드
class Updater(QThread):
    update_signal = pyqtSignal()
    def run(self):
        while True:
            self.update_signal.emit()
            time.sleep(1/60)


#Genesis class is Base class of window. You can define your own windows as its base as Genesis.
#It has useful Drawing functions, and cleaned up messy things.

class Genesis(QWidget):

    def __init__(self):
        super(Genesis,self).__init__()
        
        ## Make UI
        self.initUI()
        self.update_thread = Updater()
        self.update_thread.update_signal.connect(self.update)
        self.update_thread.start()
        ###Paint Setting
        self.painter = QPainter()
        self.color = 0xFFFFFF
        self.font = ['Arial',20]
        
    def paintEvent(self, event):

        self.painter.begin(self)
        self.drawEvent(event) 
        self.painter.end()
    
    ## Will Be Overloaded
    def initUI(self):
        return
    def drawEvent(self, event):
        return

    def getCursorPos(self):
            return self.mapFromGlobal(QCursor.pos())
    
    ## Painting Functions 
    def drawString(self,x,y,s):
        self.painter.setPen(QColor(self.color))
        self.painter.setFont(QFont(self.font[0],self.font[1]))
        self.painter.drawText(x,y, s)
    def drawSquare(self, x, y, size):
        
        color = QColor(self.color)
        self.painter.fillRect(x + 1, y + 1, size - 2, size - 2, color)

        self.painter.setPen(color.lighter())
        self.painter.drawLine(x, y + size - 1, x, y)
        self.painter.drawLine(x, y, x + size - 1, y)

        self.painter.setPen(color.darker())
        self.painter.drawLine(x + 1, y + size - 1, x + size - 1, y + size - 1)
        self.painter.drawLine(x + size - 1, y + size - 1, x + size - 1, y + 1)
    def drawPushedSquare(self, x, y, size):
        
        color = QColor(self.color)
        self.painter.fillRect(x + 1, y + 1, size - 2, size - 2, color)

        self.painter.setPen(color.darker())
        self.painter.drawLine(x, y + size - 1, x, y)
        self.painter.drawLine(x, y, x + size - 1, y)

        self.painter.setPen(color.lighter())
        self.painter.drawLine(x + 1, y + size - 1, x + size - 1, y + size - 1)
        self.painter.drawLine(x + size - 1, y + size - 1, x + size - 1, y + 1)

        

###Easy, Excellent GUI###
##List that has search bar
class SearchList(QWidget):
    def listUpdate(self):
        self.list.clear()
        try:
            for k in self.WholeList:
                if k.upper().count(str(self.search.text()).upper())>0:
                    self.list.addItem(QListWidgetItem(k))
        except:
            pass
                
    def __init__(self,name):
        super(SearchList,self).__init__()
        self.label = QLabel(name)
        self.search = QLineEdit()
        self.search.textChanged.connect(self.listUpdate)
        self.list = QListWidget()
        self.layout = QVBoxLayout()
        self.WholeList=[]
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)
        self.listUpdate()

#Test

class XColorDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self.color = None

    def setColor(self, color):
        self.color = QColor(color)
        self.update()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        if self.color is not None:
            painter.setBrush(QBrush(self.color))
            painter.drawRect(self.rect())

    def getColorName(self):
        return unicode(self.color.name())



def XButton(buttonName, function):
    button = QPushButton(buttonName)
    button.clicked.connect(function)
    return button

def XVLayout(*components):
    return _XBoxLayout('V',components)

def XHLayout(*components):
    return _XBoxLayout('H',components)
    
def _XBoxLayout(type, components):
    if type=='V':
        layout = QVBoxLayout()
    else:
        layout = QHBoxLayout()
    for component in components:
        try:
            ##if component is integer, it is considered as a stretch factor.
            layout.addStretch(component)
            continue
        except:
            pass
        try:
            layout.addWidget(component)
        except:
            layout.addLayout(component)
    return layout   


class Xt():
    @classmethod
    def rect(cls,graphicsItem):
        try:
            rect = graphicsItem.rect()
        except:
            rect = graphicsItem.boundingRect()
        rect.moveTo(graphicsItem.pos().x(),graphicsItem.pos().y())
        if graphicsItem.parentItem() != None:
            rect.moveTo(graphicsItem.pos().x()+graphicsItem.parentItem().rect().x(),graphicsItem.pos().y()+graphicsItem.parentItem().rect().y())
        return rect
    
    @classmethod
    def showError(cls,errMessage):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(errMessage)
            msg.setWindowTitle("Error")
            msg.exec_()
    @classmethod
    def norm(cls,vec):
        result = 0
        for v in vec:
            result += (v*v)
        import math
        return math.sqrt(result)
        
        

class XGraphicsRectItem(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.setPos(x,y)
    def rect(self):
        rect = super().rect()
        rect.moveTo(self.pos().x(),self.pos().y())
        if self.parentItem() != None:
            rect.moveTo(self.pos().x()+self.parentItem().rect().x(),self.pos().y()+self.parentItem().rect().y())
        return rect

    def moveTo(self,x,y):
        vec = [x-self.pos().x(),y-self.pos().y()]
        n = Xt.norm(vec)
        if n>10:
            self.setPos(self.pos().x()+vec[0]/2,self.pos().y()+vec[1]/2)
        else:
            self.setPos(x,y)     



##Horizontal Table with header labels
def XTableView(*headerLabels):
    table = QTableWidget()
    table.setColumnCount(len(headerLabels))
    table.setHorizontalHeaderLabels(headerLabels)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
    #table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) # Other header resizing option
    #table.horizontalHeader().setSectionResizeMode(len(headerLabels)-1, QHeaderView.Stretch) # Stretch Last header
    return table
###Excellent GUI####

## Show Python Editor
class PythonEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.highlight=PythonHighlighter(self.document())

