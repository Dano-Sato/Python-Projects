from MyPyLib import *

BrickTitleFont = QFont('Arial',20)
BrickTitleFont.setBold(True)
BrickTextFont = QFont('Arial',15)

home_path = os.path.expanduser('~')
directoryName = home_path+"/Library/Application\ Support/LayBricks"

resetTime = "05:00:00"

class Brick(XGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.title = QGraphicsTextItem('Title')
        self.title.setFont(BrickTitleFont)
        self.title.setParentItem(self)
        self.text = QGraphicsTextItem('text')
        self.text.setFont(BrickTextFont)
        self.text.setParentItem(self)
        self.color = QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))
        self.setBrush(self.color) # 배경색 정함
        self.setPen(QPen(Qt.white,1))
    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.title.setPos(5,5)
        self.text.setPos(10,40)
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
    delta = 20
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
        self.addButtonLabel.setFont(QFont('Arial',20))
        self.addButtonLabel.setParentItem(self.addButton)

    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.addButtonLabel.setPos(50,8)
        self.addButton.setRect(w/3-20,h-60,200,40)
        self.title.setPos(20,15)
        self.setPos(x,y)
    def setTitle(self,str):
        self.title.setPlainText(str)
    def update(self): # 내부 브릭들의 위치를 정렬한다.
        self.Bricks.sort(key = lambda x:x.rect().y())
        temp = self.rect().y()
        temp += 70
        for b in self.Bricks:
            b.moveTo(self.rect().x()+self.delta,temp)
            temp+=b.rect().height()
            temp+=self.delta

    def addBrick(self,scene):
        b = Brick()
        b.setRect(self.pos().x(),self.pos().y(),self.rect().width()-self.delta*2,self.minimal_brick_height)
        b.heightUpdate()

        self.Bricks.append(b)
        self.isSaved = False
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
    default_size = [2560,1286]
    scale = 1

    def textUpdate(self):
        if self.isTextChanged == False:
            self.isSaved = False
            self.isTextChanged = True
            
    def saveData(self):
        data = {'Todo':self.Todo,'Ongoing':self.Ongoing,'Done':self.Done,'reset':resetTime}
        pickle.dump
        
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
        self.editorFrameMotionTimer = -1
        self.editorFrameMotionTimerTime = 15
        self.editorFrameIsHide = True
        self.setLayout(self.layout)
        self.isTextChanged = False


        #Board 객체들 구성

        _width = 600
        _height = 1200
        d = 20

        self.Todo = Board(QColor(50,25,25))
        self.Todo.setRect(d,50,_width,_height)
        self.Todo.setTitle('Todo')
        
        self.Ongoing = Board(QColor(25,50,25))
        self.Ongoing.setRect(2*d+_width,50,_width,_height)
        self.Ongoing.setTitle('Ongoing')

        self.Done = Board(QColor(25,25,50))
        self.Done.setRect(3*d+2*_width,50,_width,_height)
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
        self.isSaved = False # 자동저장 여부를 확인
        self.saveTimer = 0 # 세이브 할때 사용하는 타이머 
        self.saveInterval = 200

    def cursorPos(self):
        pos = self.getCursorPos()
        return QPointF(pos.x()/self.scale,pos.y()/self.scale)
    def eventFilter(self, obj, event):
        if obj is self.view.viewport():
            if event.type() == QEvent.MouseButtonPress:
                if event.buttons() & Qt.LeftButton:
                    #Mouse Press Event 
                    #print('mouse press event = ', event.pos())

                    offset = -16
                    clickedBrick = False

                    for board in [self.Todo,self.Ongoing,self.Done]:
                        #버튼을 눌렀을 때 행동
                        button = board.addButton
                        pos = self.cursorPos()
                        pos.setX(pos.x()+offset)
                        pos.setY(pos.y()+offset)
                        if button.rect().contains(pos.x(),pos.y()):
                            board.addBrick(self.scene)
                        for brick in board.Bricks:
                            if brick.rect().contains(pos.x(),pos.y()):
                                clickedBrick = True
                                if self.currentObject != None:
                                    self.currentObject.setBrush(self.currentObject.color)
                                    self.currentObject.setPen(QPen(Qt.white,1))

                                if self.editorFrame.isHidden():
                                    self.editorFrameIsHide = False
                                    self.editorFrameMotionTimer = self.editorFrameMotionTimerTime
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
                                self.draggingOffset = [self.cursorPos().x()-self.draggedObject.rect().x(),self.cursorPos().y()-self.draggedObject.rect().y()]
                    if not clickedBrick:
                        if self.currentObject != None:
                            self.currentObject.setBrush(self.currentObject.color)
                            self.currentObject.setPen(QPen(Qt.white,1))
                        self.currentObject = None
                        self.textEdit.clear()
                        self.editorFrameIsHide = True
                        self.editorFrameMotionTimer = self.editorFrameMotionTimerTime


                    
            elif event.type() == QEvent.MouseButtonRelease:
                #Mouse Release Event
                #print('mouse release event = ', event.pos())
                if self.draggedObject != None:
                    self.draggedObject = None
                    self.isSaved = False

        return QWidget.eventFilter(self, obj, event)

    def resizeEvent(self,event):
        w,h = self.size().width(),self.size().height()
        r_w,r_h = w/self.default_size[0],h/self.default_size[1]
        r = min(r_w,r_h)
        tr = QTransform()
        tr.scale(r,r)
        self.scale = r
        self.view.setTransform(tr)
        return
    def update(self):
        super().update()
        for board in [self.Todo,self.Ongoing,self.Done]:
            board.update()
        if self.draggedObject != None:
            self.draggedObject.setPos(self.cursorPos().x()-self.draggingOffset[0],self.cursorPos().y()-self.draggingOffset[1])
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
            
        if self.editorFrameMotionTimer >= 0:
            _d = 60
            if self.editorFrameMotionTimer>0:
                r = self.editorFrameMotionTimer/self.editorFrameMotionTimerTime
                if self.editorFrameIsHide:#숨기려고 하는중
                    self.layout.setStretchFactor(self.view,3*_d)
                    self.layout.setStretchFactor(self.editorFrame,max(int(((1-(1-r)**2)*_d)),1))
                else:
                    self.layout.setStretchFactor(self.view,3*_d)
                    self.layout.setStretchFactor(self.editorFrame,int((1-(r**2))*_d))
                if self.editorFrameMotionTimer == self.editorFrameMotionTimerTime-3:
                    if not self.editorFrameIsHide:
                        self.editorFrame.show()

            else:
                if self.editorFrameIsHide:
                    self.editorFrame.hide()
                
            self.editorFrameMotionTimer-=1

        if self.isTextChanged:
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
                self.isTextChanged = False

        if not self.isSaved:
            #Save
            if self.saveTimer < self.saveInterval:
                self.saveTimer+=1
            else:                
                print('save')
                self.saveTimer = 0
                self.isSaved = True
        


        #Brick들을 정렬, Dragging되는 오브젝트 처리





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = MWindow()
    Appli = App()
    mwindow.setCentralWidget(Appli)
    mwindow.show()    
    
    #resetTime 수정, 현재 파일이 있을경우 싹 받아와야 한다
    mwindow.resetTimeEdit.setTime(QTime.fromString(resetTime,"hh:mm:ss"))
    
    app.exec_()