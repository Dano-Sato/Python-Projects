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
        self.setBrush(QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))) # 배경색 정함
        self.setPen(QPen(Qt.white,1))
    def setRect(self,x,y,w,h):
        super().setRect(x,y,w,h)
        self.title.setPos(x+5,y+5)
        self.text.setPos(x+10,y+30)
    def setTitle(str):
        self.title.setPlainText(str)
    def setText(str):
        self.text.setPlainText(str)
    def addToScene(self,scn):
        scn.addItem(self)
        scn.addItem(self.text)
        scn.addItem(self.title)
    def removeFromScene(self,scn):
        scn.removeItem(self)
        scn.removeItem(self.text)
        scn.removeItem(self.title)

class App(Genesis):
    def initUI(self):

        self.resize(1200,800)
        self.setWindowTitle("LayBricks")
        b = Brick()
        b.setRect(10,10,150,150)
        scene = QGraphicsScene()
        b.addToScene(scene)
        self.Todo = []
        self.Ongoing = []
        self.Done = []
        self.view = QGraphicsView()
        self.view.setScene(scene)
        self.view.viewport().installEventFilter(self)

        self.layout = XVLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        
        self.draggedObject = None

    def eventFilter(self, obj, event):
        if obj is self.view.viewport():
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() & Qt.LeftButton:
                    #Mouse Press Event 
                    print('mouse press event = ', event.pos())
            elif event.type() == QEvent.MouseButtonRelease:
                #Mouse Release Event
                print('mouse release event = ', event.pos())

        return QWidget.eventFilter(self, obj, event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = App()
    mwindow.show()
    
    app.exec_()