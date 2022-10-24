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
        self.color = QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))
        self.setBrush(self.color) # 배경색 정함
        self.setPen(QPen(Qt.white,1))
    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.title.setPos(5,5)
        self.text.setPos(10,30)
        self.text.setTextWidth(self.rect().width()-20)
        self.setPos(x,y) # Coordinate를 망가뜨리지 않기 위해 이렇게 설계
    def setTitle(self,str):
        self.title.setPlainText(str)
    def setText(self,str):
        self.text.setPlainText(str)
    def heightUpdate(self):
        h1 = self.title.boundingRect().height()
        h2 = self.text.boundingRect().height()
        rect = self.rect()
        rect.setHeight(h1+h2+10)
        self.setRect(rect.x(),rect.y(),rect.width(),rect.height())



class Board(XGraphicsRectItem):
    delta = 15
    minimal_brick_height = 60

    
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
        b.setRect(0,0,self.rect().width()-30,self.minimal_brick_height)
        b.heightUpdate()

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

    def textUpdate(self):
        texts = self.textEdit.toPlainText().replace('\t','    ').split('\n')
        #Brick Update
        if self.currentObject != None:
            if len(texts)>0:
                head = texts[0]
                self.currentObject.title.setPlainText(head)
            else:
                self.currentObject.title.setPlainText('')
            if len(texts)>1:
                text = '\n'.join(texts[1:])
                self.currentObject.text.setPlainText(text)
            else:
                self.currentObject.text.setPlainText('')
            self.currentObject.heightUpdate()
            cursor = self.textEdit.textCursor()
            if cursor.blockNumber()==0:
                self.textEdit.setCurrentCharFormat(self.titleFormat)
            else:
                self.textEdit.setCurrentCharFormat(self.textFormat)
            self.prevBN = cursor.blockNumber()

        
    def initUI(self):





        #QGraphicsView 구성
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

        #Brick Editor 구성 
        self.editorFrame = QFrame()
        self.textEdit = QPlainTextEdit()
        self.textEdit.textChanged.connect(self.textUpdate)
        self.textEdit.setTabStopWidth(self.textEdit.fontMetrics().width(' ') * 4)        
        self.titleFormat = QTextCharFormat()
        self.prevBN = -1
        TitleFont = QFont('Arial',22)
        TitleFont.setBold(True)
        self.titleFormat.setFont(TitleFont)
        self.textFormat = QTextCharFormat()
        self.textFormat.setFont(QFont('Arial',14))
        self.editorFrame.setLayout(XVLayout(QLabel("Brick Editor"),self.textEdit))
        self.editorFrame.hide()


        self.layout = XHLayout(self.view,self.editorFrame)
        self.layout.setStretchFactor(self.view,3)
        self.layout.setStretchFactor(self.editorFrame,1)
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
        self.draggingOffset = None
        self.currentObject = None


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
                                if self.currentObject != None:
                                    self.currentObject.setBrush(self.currentObject.color)
                                    self.currentObject.setPen(QPen(Qt.white,1))

                                if self.editorFrame.isHidden():
                                    self.editorFrame.show()
                                self.currentObject=brick
                               # str = brick.title.toPlainText()+'\n'+brick.text.toPlainText()
                               # self.textEdit.setPlainText(str)
                                title = brick.title.toPlainText()
                                text = brick.text.toPlainText()
                                self.textEdit.clear()
                                self.textEdit.setCurrentCharFormat(self.titleFormat)
                                self.textEdit.insertPlainText(title+'\n')
                                self.textEdit.setCurrentCharFormat(self.textFormat)
                                self.textEdit.insertPlainText(text)
                                self.currentObject.setBrush(self.currentObject.color.lighter().lighter())
                                self.currentObject.setPen(QPen(Qt.black,1))

                                self.draggedObject=brick
                                self.draggingOffset = [self.getCursorPos().x()-self.draggedObject.rect().x(),self.getCursorPos().y()-self.draggedObject.rect().y()]

                    
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
            self.draggedObject.setPos(self.getCursorPos().x()-self.draggingOffset[0],self.getCursorPos().y()-self.draggingOffset[1])
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