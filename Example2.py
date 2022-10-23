from MyPyLib import *

BrickTitleFont = QFont('Arial',15)
BrickTitleFont.setBold(True)

class Brick(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.title = QGraphicsTextItem("Title")
        self.title.setFont(BrickTitleFont)
        self.text = QGraphicsTextItem("testetsettsetstsetsetstetstststs")
        self.text.setTextWidth(130)
        self.setBrush(Qt.black)
        self.setPen(QPen(Qt.white,2))
    def setRect(self,x,y,w,h):
        super().setRect(x,y,w,h)
        self.title.setPos(x+5,y+5)
        self.text.setPos(x+10,y+30)
    def addToScene(self,scn):
        scn.addItem(self)
        scn.addItem(self.text)
        scn.addItem(self.title)
    def removeFromScene(self,scn):
        scn.removeItem(self)
        scn.removeItem(self.text)
        scn.removeItem(self.title)

class Game(Genesis):
    def initUI(self):
        b = Brick()
        b.setRect(10,10,150,150)
        scene = QGraphicsScene()
        b.addToScene(scene)
        self.view = QGraphicsView()
        self.view.setScene(scene)

        self.resize(400,400)
        self.setWindowTitle("LayBricks")
        self.layout = XVLayout(QPushButton("Hello World"))
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = Game()
    mwindow.show()
    
    app.exec_()