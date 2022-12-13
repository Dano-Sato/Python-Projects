from MyPyLib import *

class Appli(Genesis):
    def initUI(self):
        self.resize(600,600)
        self.setWindowTitle("Test Game")        
        self.scene = XGraphicsScene(0,0,1200,800)
        self.testSqr = XGraphicsRectItem()
        self.testSqr.setRect(30,30,50,50)
        self.testSqr.setColor(QColor(50,50,50))
        self.testSqr.setEdge(QPen(Qt.white,10))
        self.scene.addItem(self.testSqr)
        
        self.scene2 = XGraphicsScene(0,0,1200,800)
        self.sqr2 = XGraphicsRectItem()
        self.sqr2.setRect(50,50,200,200)
        self.sqr2.setColor(QColor(200,10,10))
        self.scene2.addItem(self.sqr2)

        self.layout = XVLayout()
        self.setLayout(self.layout)
        self.currentView = None
        self.changeView(self.scene.view)
        self.x=200
        self.y=200

    def changeView(self,view):
        if self.currentView != None:
            self.currentView.setParent(None)
        self.currentView = view
        self.layout.addWidget(view)
    def update(self):
        super().update()

    '''
    def drawEvent(self, event):
        a = self.drawAction
        a()
        return
    def drawAction(self):
        self.drawString(self.x,self.y,"test")
    '''
            
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            if self.currentView ==self.scene.view:
                self.changeView(self.scene2.view)
            else:
                self.changeView(self.scene.view)
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_W:
            self.y-=4
        if event.key()==Qt.Key_A:
            self.x-=4
        if event.key()==Qt.Key_S:
            self.y+=4
        if event.key()==Qt.Key_D:
            self.x+=4
            

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mwindow = Appli()
    mwindow.show()
    
    app.exec_()