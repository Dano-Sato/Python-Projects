from MyPyLib import *
class Game(Genesis):
    def initUI(self):
        self.resize(200,100)
        self.setWindowTitle("Test App")
        self.layout = XVLayout(QPushButton("Hello World"))
        self.layout
        self.setLayout(self.layout)

class Brick():
    def __init__(self):
        self.rect = QGraphicsRectItem()
        self.text = QGraphicsTextItem("test")
        self.rect.setBrush(Qt.black)
        self.rect.setPen(QPen(Qt.white,2))

    def setRect(self,x,y,w,h):
        self.rect.setRect(x,y,w,h)
        self.text.setPos(x+10,y+10)

    def addToScene(self,scn):
        scn.addItem(self.rect)
        scn.addItem(self.text)

    def removeFromScene(self,scn):
        scn.removeItem(self.rect)
        scn.removeItem(self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #mwindow = Game()
    #mwindow.show()
    b = Brick()
    b.setRect(10,10,50,50)
    scene = QGraphicsScene()
    b.addToScene(scene)
    view = QGraphicsView()
    view.setScene(scene)
    view.show()

    app.exec_()