from MyPyLib import *

BrickTitleFont = QFont('Arial',15)
BrickTitleFont.setBold(True)

class Brick(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.title = QGraphicsTextItem('Title')
        self.title.setFont(BrickTitleFont)
        self.title.setParentItem(self)
        self.text = QGraphicsTextItem('text')
        self.text.setParentItem(self)
        self.text.setTextWidth(130)
        self.setBrush(QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))) # 배경색 정함
        self.setPen(QPen(Qt.white,1))
    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.setPos(x,y)
        self.title.setPos(x+5,y+5)
        self.text.setPos(x+10,y+30)
    def setTitle(str):
        self.title.setPlainText(str)
    def setText(str):
        self.text.setPlainText(str)
    def addToScene(self,scn):
        scn.addItem(self)
    def removeFromScene(self,scn):
        scn.removeItem(self)
    def rect(self):
        rect = super().rect()
        rect.moveTo(self.pos().x(),self.pos().y())
        return rect


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





        self.Todo = []
        self.Ongoing = []
        self.Done = []
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0,0,1200,800)
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.viewport().installEventFilter(self)
        self.view.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.zero = QGraphicsRectItem()
        self.zero.setPos(0,0)
        self.scene.addItem(self.zero)
        self.view.setFocusPolicy(Qt.NoFocus)
        self.editorFrame = QFrame()
        self.textEdit = QPlainTextEdit()



        self.layout = XHLayout(self.view)
        self.setLayout(self.layout)

        self.b = Brick()
        self.b.setRect(0,0,150,150)
        self.b.setPos(150,0)
        self.a = Brick()
        self.a.setRect(0,0,150,150)
        self.a.setPos(300,0)
        self.b.addToScene(self.scene)
        self.c = Brick()
        self.c.setRect(0,0,150,150)

        self.a.addToScene(self.scene)
        self.c.addToScene(self.scene)

        
        self.draggedObject = None

    def eventFilter(self, obj, event):
        if obj is self.view.viewport():
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() & Qt.LeftButton:
                    #Mouse Press Event 
                    #print('mouse press event = ', event.pos())
                    for brick in [self.a,self.b,self.c]:
                        pos = self.view.mapToScene(self.getCursorPos())
                        if brick.rect().contains(pos.x(),pos.y()):                
                            self.draggedObject=brick
                    
            elif event.type() == QEvent.MouseButtonRelease:
                #Mouse Release Event
                #print('mouse release event = ', event.pos())
                self.draggedObject = None

        return QWidget.eventFilter(self, obj, event)

    def update(self):
        super().update()
        if self.draggedObject != None:
            pos = self.view.mapToScene(self.getCursorPos())
            self.draggedObject.setPos(pos.x(),pos.y())
            for brick in [self.a,self.b,self.c]:
                print('brick:',brick.rect())
            print('cursor:',self.getCursorPos())
            #print('cursor(Scene)',)


        #Brick들을 정렬, Dragging되는 오브젝트 처리





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = MWindow()
    Appli = App()
    mwindow.setCentralWidget(Appli)
    mwindow.show()
    
    app.exec_()