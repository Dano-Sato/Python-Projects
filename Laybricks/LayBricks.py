from MyPyLib import *
from RoutineManager import *
from Brick import *



assessment = ['Did a few😔','Not Enough😢','Normal🙂','Well Done!👍','Excellent!😎']

home_path = os.path.expanduser('~')
directoryName = home_path+"/Library/Application\ Support/LayBricks"
saveFilePath = (directoryName+'/currentData.laybricks')
configFilePath = (directoryName+'/currentConfig.config')


            
        
class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.showMaximized()
        self.resize(1440,800)
        self.setWindowTitle("🧱LayBricks")
        self.toolbar = self.addToolBar('toolbar')

        self.exportButton = QPushButton('Save Data')
        self.toolbar.addWidget(self.exportButton)
    
        self.importButton = QPushButton('Load Data')
        self.toolbar.addWidget(self.importButton)

        self.toolbar.addSeparator()
        self.routineManager = RoutineManager()
        self.routineManagerButton = QPushButton('Routine Manager')
        self.routineManagerButton.clicked.connect(self.openRoutineManager)
        self.toolbar.addWidget(self.routineManagerButton)        

        self.supplyButton = QPushButton('Supply Routines')
        self.toolbar.addWidget(self.supplyButton)        
        
        self.toolbar.addSeparator()

        self.removeButton = QPushButton('Remove All')
        self.toolbar.addWidget(self.removeButton)
        
        
    def openRoutineManager(self):
        self.routineManager.show()
        

class App(Genesis):
    default_size = [2560,1286]
    scale = 1
    charNum = 0

    def exportData(self):
        now = QDate.currentDate().toString('yyyy.MM.dd')
        FileSave = QFileDialog.getSaveFileName(self,'Save file',directoryName.replace('\\','')+'/'+now,'*.laybricks')
        if FileSave[0]:
            data = {'Todo':self.Todo.dataExport(),'Ongoing':self.Ongoing.dataExport(),'Done':self.Done.dataExport()}
            with open(FileSave[0].replace('\\',''), 'wb') as f:
                pickle.dump(data,f)                        
            
    def importData(self):
        '''
        ret = QMessageBox.question(self,'','If you import data,\nAll of current data would be removed.\nIs it okay?', QMessageBox.No | QMessageBox.Yes)
        if ret == QMessageBox.No:
            return
        '''
        FileLoad = QFileDialog.getOpenFileName(self,"Open File",directoryName.replace('\\',''),'*.laybricks')
        if FileLoad[0]:
            try:
                for board in [Appli.Todo,Appli.Ongoing,Appli.Done]:
                    for b in board.Bricks:
                        b.pinButton.hide()
                self.removeAll()
                data = pickle.load(open(FileLoad[0],'rb'))            
                todo = data['Todo']
                ongoing = data['Ongoing']
                done = data['Done']
                Appli.Todo.dataImport(Appli.scene,todo)
                Appli.Ongoing.dataImport(Appli.scene,ongoing)
                Appli.Done.dataImport(Appli.scene,done)

            except:
                Xt.showError("File Load Error")
    def textUpdate(self):
        #if self.isTextChanged == False:
        self.saveTimer = 0
        self.isSaved = False
        self.isTextChanged = True

    def removeAll(self):
        self.isSaved = False
        l = [self.Todo,self.Ongoing,self.Done]
        for board in l:
            remains = []
            for b in board.Bricks:
                if not b.pinButton.isVisible():
                    self.scene.removeItem(b)
                else:
                    remains.append(b)
                    
            board.Bricks=remains
        self.currentObject = None
    def supplyRoutines(self):
        for r in self.mw.routineManager.routines:
            self.Todo.addBrickFromData(self.scene,r.export())
    def self_assessment_changed(self):
        if self.slider.value()>0:
            newLine = 'Self-Assessment: '+assessment[self.slider.value()-1]
            self.assessment_label.setText(newLine)
            title = self.currentObject.title.toPlainText()
            text = self.currentObject.text.toPlainText()
            l = text.split('\n')
            text_changed = False
            for idx,line in enumerate(l):
                if '#Self-Assessment' in line:
                    l[idx] = '#'+newLine
                    text_changed = True
            if not text_changed:
                l.append('#'+newLine)
            newText = '\n'.join(l)
            self.textEdit.clear()
            self.textEdit.setCurrentCharFormat(self.titleFormat)
            self.textEdit.insertPlainText(title+'\n')
            self.textEdit.setCurrentCharFormat(self.textFormat)
            self.textEdit.insertPlainText(newText)

        else:
            self.assessment_label.setText('Self-Assessment Checker')            
            title = self.currentObject.title.toPlainText()
            text = self.currentObject.text.toPlainText()
            l = text.split('\n')
            for line in l:
                if '#Self-Assessment' in line:
                    l.remove(line)
            newText = '\n'.join(l)
            self.textEdit.clear()
            self.textEdit.setCurrentCharFormat(self.titleFormat)
            self.textEdit.insertPlainText(title+'\n')
            self.textEdit.setCurrentCharFormat(self.textFormat)
            self.textEdit.insertPlainText(newText)
            
            
    def saveData(self):
        data = {'Todo':self.Todo.dataExport(),'Ongoing':self.Ongoing.dataExport(),'Done':self.Done.dataExport()}
        config = {'Routines':self.mw.routineManager.export()}
        with open(saveFilePath.replace('\\',''), 'wb') as f:
            pickle.dump(data,f)   
        with open(configFilePath.replace('\\',''),'wb') as f:
            pickle.dump(config,f)
    def removeBrick(self):
        if self.currentObject != None:
            self.isSaved = False
            for board in [self.Todo,self.Ongoing,self.Done]:
                if self.currentObject in board.Bricks:
                    if not self.currentObject.pinButton.isVisible():
                        board.Bricks.remove(self.currentObject)
                        self.scene.removeItem(self.currentObject)
                        self.currentObject = None
    def changeColor(self):
        if self.currentObject != None:
            color = QColorDialog.getColor()
            if color.isValid():
                self.currentObject.color = color
                self.currentObject.setBrush(self.currentObject.color) # 배경색 정함
                self.colorDisplay.setColor(color)
    def randomColor(self):
        if self.currentObject != None: 
            color = QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))            
            self.currentObject.color = color
            self.currentObject.setBrush(self.currentObject.color) # 배경색 정함
            self.colorDisplay.setColor(color)
            
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
        self.removeButton = QPushButton('Remove Brick')
        self.removeButton.clicked.connect(self.removeBrick)
        self.assessment_label = QLabel('Self-Assessment Checker')
        self.slider = QSlider(Qt.Horizontal,self)
        self.slider.setRange(0,5)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.self_assessment_changed)
        self.colorButton = QPushButton('Pick Color')
        self.colorButton2 = QPushButton('Random Color')
        self.colorButton.clicked.connect(self.changeColor)
        self.colorButton2.clicked.connect(self.randomColor)
        self.colorDisplay = XColorDisplay()
        self.colorPicker = XHLayout(self.colorDisplay,self.colorButton,self.colorButton2)
        self.colorPicker.setStretchFactor(self.colorDisplay,1)
        self.colorPicker.setStretchFactor(self.colorButton,3)
        self.pinButton = QCheckBox()
        self.pinButton.setText('Don\'t remove this')
        self.pinButton.stateChanged.connect(self.pinBrick)
        self.editorFrame.setLayout(XVLayout(QLabel("Brick Editor"),self.textEdit,self.assessment_label,self.slider,self.colorPicker,self.pinButton,self.removeButton,1))
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
        _height = 1240
        d = 0
        n = 25
        

        self.Todo = Board(QColor(n+35,n-5,15))
        self.Todo.setRect(d,0,_width,_height)
        self.Todo.setTitle('Todo')
        
        self.Ongoing = Board(QColor(n,n+25,n+10))
        self.Ongoing.setRect(2*d+_width,0,_width,_height)
        self.Ongoing.setTitle('Ongoing')

        self.Done = Board(QColor(n,n+10,n+25))
        self.Done.setRect(3*d+2*_width,0,_width,_height)
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
        self.saveInterval = 30

    def pinBrick(self,state):
        self.isSaved = False
        if state == Qt.Checked:
            self.currentObject.pinButton.show()
        else:
            self.currentObject.pinButton.hide()

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
                            if len(board.Bricks)<15:
                                board.addBrick(self.scene)
                                self.isSaved = False
                        for brick in board.Bricks:
                            if brick.rect().contains(pos.x(),pos.y()):
                                if Xt.rect(brick.foldButton).contains(pos.x(),pos.y()):
                                    brick.fold()
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
                               
                                self.colorDisplay.setColor(brick.color)
                                title = brick.title.toPlainText()
                                text = brick.text.toPlainText()
                                self.textEdit.clear()
                                self.textEdit.setCurrentCharFormat(self.titleFormat)
                                self.textEdit.insertPlainText(title+'\n')
                                self.textEdit.setCurrentCharFormat(self.textFormat)
                                self.textEdit.insertPlainText(text)
                                self.currentObject.setBrush(self.currentObject.color.lighter().lighter())
                                self.currentObject.setPen(QPen(Qt.black,1))
                                if self.currentObject.pinButton.isVisible():
                                    self.pinButton.setChecked(True)
                                else:
                                    self.pinButton.setChecked(False)
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
            for b in board.Bricks:
                b.heightUpdate()
        if self.draggedObject != None:
            self.draggedObject.setPos(self.cursorPos().x()-self.draggingOffset[0],self.cursorPos().y()-self.draggingOffset[1])
            for board in [self.Todo,self.Ongoing,self.Done]:
                if self.draggedObject in board.Bricks:
                    currentBoard = board
                    break
            for board in [self.Todo,self.Ongoing,self.Done]:            
                if board.rect().contains(self.draggedObject.rect().center()) and len(board.Bricks)<15:
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
                
        if not self.mw.routineManager.isSaved:
            self.mw.routineManager.isSaved = True
            self.isSaved = False

        if not self.isSaved:
            #Save
            if self.saveTimer < self.saveInterval:
                self.saveTimer+=1
            else:                
                self.saveData()
                self.saveTimer = 0
                self.isSaved = True
        

        #Brick들을 정렬, Dragging되는 오브젝트 처리





if __name__ == '__main__':

    #폴더 생성
    if len(glob.glob(directoryName.replace('\\','')))<1:
        os.system('mkdir -p '+directoryName)
    
    
    app = QApplication(sys.argv)
    mwindow = MWindow()
    Appli = App()
    Appli.mw = mwindow
    Appli.mw.removeButton.clicked.connect(Appli.removeAll)
    Appli.mw.supplyButton.clicked.connect(Appli.supplyRoutines)
    Appli.mw.exportButton.clicked.connect(Appli.exportData)
    Appli.mw.importButton.clicked.connect(Appli.importData)
    #세이브 데이터 생성
    if len(glob.glob(saveFilePath.replace('\\','')))<1:
        os.system('touch '+saveFilePath)
    else:
        try: #존재할 경우 데이터를 불러온다.
            data = pickle.load(open(saveFilePath.replace('\\',''),'rb'))
            todo = data['Todo']
            ongoing = data['Ongoing']
            done = data['Done']
            Appli.Todo.dataImport(Appli.scene,todo)
            Appli.Ongoing.dataImport(Appli.scene,ongoing)
            Appli.Done.dataImport(Appli.scene,done)
            mwindow.routineManager.load(data['Routines'])
        except:
            pass
        try:
            config = pickle.load(open(configFilePath.replace('\\',''),'rb'))
            mwindow.routineManager.load(config['Routines'])
        except:
            pass               
    mwindow.setCentralWidget(Appli)
    mwindow.show()    
    
    
    app.exec_()