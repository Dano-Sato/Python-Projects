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
        self.layout = XVLayout()
        self.layout.addWidget(self.scene.view)
        self.setLayout(self.layout)
        
        self.x=200
        self.y=200
        
    def update(self):
        super().update()

    def drawEvent(self, event):
        a = self.drawAction
        a()
        return
    def drawAction(self):
        self.drawString(self.x,self.y,"test")
        
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            print('test')
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