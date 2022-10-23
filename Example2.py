from MyPyLib import *

BrickTitleFont = QFont('Arial',15)
BrickTitleFont.setBold(True)

class Brick(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.title = QGraphicsTextItem('Title')
        self.title.setFont(BrickTitleFont)
        self.text = QGraphicsTextItem('text')
        self.text.setTextWidth(130)
        self.setBrush(QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))) # 배경색 정함
        self.setPen(QPen(Qt.white,1))
    def setRect(self,x,y,w,h):
        super().setRect(x,y,w,h)
        self.setPos(x,y)
    def setPos(self,x,y):
        super().setPos(x,y)
        self.title.setPos(x+10,y+10)
        self.text.setPos(x+15,y+35)
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


class Board(QGraphicsRectItem):
    def __init__(self,color):
        self.setBrush(color)
        self.Bricks = []

class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.setWindowTitle("LayBricks")
        self.toolbar = self.addToolBar('toolbar')
        self.resetTimeEdit = QTimeEdit() # 매일 루틴 리셋 시간을 지정하는 Editor
        self.resetTimeEdit.setUpdatesEnabled(True)
        self.toolbar.addWidget(QLabel('Reset at'))
        self.toolbar.addWidget(self.resetTimeEdit)


class App(Genesis):
    def initUI(self):

        self.b = Brick()
        self.b.setRect(10,10,150,150)


        self.scene = QGraphicsScene()
        self.b.addToScene(self.scene)


        self.Todo = []
        self.Ongoing = []
        self.Done = []
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.viewport().installEventFilter(self)
        self.view.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.editorFrame = QFrame()
        self.textEdit = QPlainTextEdit()

        self.layout = XHLayout(self.view)
        self.setLayout(self.layout)

        
        self.draggedObject = None

    def eventFilter(self, obj, event):
        if obj is self.view.viewport():
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() & Qt.LeftButton:
                    #Mouse Press Event 
                    print('mouse press event = ', event.pos())
                    self.draggedObject=self.b
                    
            elif event.type() == QEvent.MouseButtonRelease:
                #Mouse Release Event
                print('mouse release event = ', event.pos())
                self.draggedObject = None

        return QWidget.eventFilter(self, obj, event)

    def update(self):
        super().update()
        if self.draggedObject != None:
            self.draggedObject.setPos(self.getCursorPos().x(),self.getCursorPos().y())

        #Brick들을 정렬, Dragging되는 오브젝트 처리





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = MWindow()
    Appli = App()
    mwindow.setCentralWidget(Appli)
    mwindow.show()
    
    app.exec_()