from MyPyLib import *

BrickTitleFont = QFont('Arial',15)
BrickTitleFont.setBold(True)

class Brick(XGraphicsRectItem):
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
        self.title.setPos(5,5)
        self.text.setPos(10,30)
        self.setPos(x,y) # Coordinate를 망가뜨리지 않기 위해 이렇게 설계
    def setTitle(self,str):
        self.title.setPlainText(str)
    def setText(self,str):
        self.text.setPlainText(str)


class Board(XGraphicsRectItem):
    delta = 15
    def __init__(self,color):
        super().__init__()
        self.setBrush(color)
        self.Bricks = []
        self.addButton = XGraphicsRectItem()
        self.addButton.setBrush(color.lighter())
        self.addButton.setParentItem(self)
        self.title = QGraphicsTextItem('')
        self.title.setParentItem(self)
        self.title.setFont(BrickTitleFont)
        self.addButtonLabel = QGraphicsTextItem("+ add Brick")
        self.addButtonLabel.setParentItem(self.addButton)

    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.addButtonLabel.setPos(50,8)
        self.addButton.setRect(w/3-20,h-60,200,40)
        self.title.setPos(5,5)
        self.setPos(x,y)
    def setTitle(self,str):
        self.title.setPlainText(str)
    def update(self): # 내부 브릭들의 위치를 정렬한다.
        self.Bricks.sort(key = lambda x:x.rect().y())
        temp = self.rect().y()
        temp += 100
        for b in self.Bricks:
            b.setPos(self.rect().x()+self.delta,temp)
            temp+=b.rect().height()
            temp+=self.delta

    def addBrick(self,scene):
        b = Brick()
        b.setRect(0,0,self.rect().width()-30,60)
        self.Bricks.append(b)
        self.update()
        scene.addItem(b)
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


        #Board 객체들 구성

        width = 400
        d = 20

        self.Todo = Board(QColor(50,25,25))
        self.Todo.setRect(d,50,width,1200)
        self.Todo.setTitle('Todo')
        
        self.Ongoing = Board(QColor(25,50,25))
        self.Ongoing.setRect(2*d+width,50,width,1200)
        self.Ongoing.setTitle('Ongoing')

        self.Done = Board(QColor(25,25,50))
        self.Done.setRect(3*d+2*width,50,width,1200)
        self.Done.setTitle('Done')


        self.scene.addItem(self.Todo)
        self.scene.addItem(self.Ongoing)
        self.scene.addItem(self.Done)


        '''
        self.b = Brick()
        self.b.setRect(150,0,150,150)
        self.a = Brick()
        self.a.setRect(300,0,150,150)
        self.scene.addItem(self.b)
        self.c = Brick()
        self.c.setRect(0,0,150,150)

        self.scene.addItem(self.a)
        self.scene.addItem(self.c)
        '''
        
        self.draggedObject = None

    def eventFilter(self, obj, event):
        if obj is self.view.viewport():
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() & Qt.LeftButton:
                    #Mouse Press Event 
                    #print('mouse press event = ', event.pos())

                    offset = -16
                    for board in [self.Todo,self.Ongoing,self.Done]:
                        #버튼을 눌렀을 때 행동
                        button = board.addButton
                        pos = self.getCursorPos()
                        print(pos)
                        print(button.rect().topLeft())
                        pos.setX(pos.x()+offset)
                        pos.setY(pos.y()+offset)
                        if button.rect().contains(pos.x(),pos.y()):
                            print('add brick')
                            print(button.rect())
                            board.addBrick(self.scene)
                        for brick in board.Bricks:
                            if brick.rect().contains(pos.x(),pos.y()):                
                                self.draggedObject=brick

                    
            elif event.type() == QEvent.MouseButtonRelease:
                #Mouse Release Event
                #print('mouse release event = ', event.pos())
                self.draggedObject = None

        return QWidget.eventFilter(self, obj, event)

    def update(self):
        super().update()
        for board in [self.Todo,self.Ongoing,self.Done]:
            board.update()
        if self.draggedObject != None:
            self.draggedObject.setPos(self.getCursorPos().x()-40,self.getCursorPos().y()-40)
            for board in [self.Todo,self.Ongoing,self.Done]:
                if self.draggedObject in board.Bricks:
                    currentBoard = board
                    break
            for board in [self.Todo,self.Ongoing,self.Done]:            
                if board.rect().contains(self.draggedObject.rect().center()):
                    if currentBoard != board:
                        board.Bricks.append(self.draggedObject)
                        currentBoard.Bricks.remove(self.draggedObject)
            #print('cursor(Scene)',)
        


        #Brick들을 정렬, Dragging되는 오브젝트 처리





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = MWindow()
    Appli = App()
    mwindow.setCentralWidget(Appli)
    mwindow.show()
    
    app.exec_()