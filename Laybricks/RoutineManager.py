from MyPyLib import *


class Routine():
    def __init__(self,_title = 'New Routine',_text = '',_color= None):
        self.title = QListWidgetItem(_title)
        self.text = _text
        if _color == None:
            self.color = QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))
        else:
            self.color = _color
    def setTitle(self,_title):
        self.title.setText(_title)

    #브릭의 형태로 추출
    def export(self):
        return [self.title.text(),self.text,self.color]


class RoutineManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Routine Manager')
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(600,800)
        self.routineList = QListWidget()
        self.routines = []
        self.addButton = QPushButton("+Make Routine")
        self.addButton.clicked.connect(self.addRoutine)
        self.routineList.currentItemChanged.connect(self.selectRoutine)
        self.isSaved = True        
        
        self.editorFrame = QFrame()
        self.titleEdit = QLineEdit()
        self.titleEdit.textChanged.connect(self.titleUpdate)
        self.textEdit = QPlainTextEdit()
        self.textEdit.setTabStopWidth(15)
        self.textChanged = False
        self.textEdit.textChanged.connect(self.textUpdate)
        self.removeButton = QPushButton('Remove Routine')
        self.removeButton.clicked.connect(self.removeRoutine)
        self.colorButton = QPushButton('Pick Color')
        self.colorButton2 = QPushButton('Random Color')
        self.colorButton.clicked.connect(self.changeColor)
        self.colorButton2.clicked.connect(self.randomColor)
        self.colorDisplay = XColorDisplay()
        self.colorPicker = XHLayout(self.colorDisplay,self.colorButton,self.colorButton2)
        self.colorPicker.setStretchFactor(self.colorDisplay,1)
        self.colorPicker.setStretchFactor(self.colorButton,3)
        self.editorFrame.setLayout(XVLayout(QLabel('Title'),self.titleEdit,QLabel('Text'),self.textEdit,self.colorPicker,self.removeButton))
        self.currentRoutine = None
        self.editorFrame.hide()
        self.routineLayout = XVLayout(QLabel('Routines'),self.routineList,self.addButton)
        self.layout = XHLayout(self.routineLayout,self.editorFrame)
        self.layout.setStretchFactor(self.routineLayout,1)
        self.layout.setStretchFactor(self.editorFrame,2)
        self.setLayout(self.layout)
    def changeColor(self):
        if self.currentRoutine != None:
            color = QColorDialog.getColor()
            self.show()
            if color.isValid():
                self.currentRoutine.color = color
                self.colorDisplay.setColor(color)
    def randomColor(self):
        if self.currentRoutine != None: 
            color = QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))            
            self.currentRoutine.color = color
            self.colorDisplay.setColor(color)


    def removeRoutine(self):
        if self.currentRoutine != None:
            self.routines.remove(self.currentRoutine)
            item = self.routineList.takeItem(self.routineList.currentRow())
            item = None
            self.selectRoutine()
    def textUpdate(self):
        self.currentRoutine.text = self.textEdit.toPlainText()
        self.textChanged = True
    def titleUpdate(self):
        self.currentRoutine.title.setText(self.titleEdit.text())
    def selectRoutine(self):
        item = self.routineList.currentItem()
        if item != None:
            for r in self.routines:
                if r.title is item:
                    self.currentRoutine = r
                    break
            if self.currentRoutine != None:
                self.titleEdit.setText(item.text())
                self.textEdit.setPlainText(r.text)
                self.colorDisplay.setColor(r.color)
                self.editorFrame.show()
        else:
            self.editorFrame.hide()
    def addRoutine(self):
        r = Routine()
        self.routines.append(r)
        self.routineList.addItem(r.title)
    def export(self):
        _routines = []
        for r in self.routines:
            data = [r.title.text(),r.text,r.color]
            _routines.append(data)
        return _routines
    def load(self,_routines): # 저장된 루틴들 불러오기
        self.routines = []
        for r in _routines:
            routine = Routine(r[0],r[1],r[2])
            self.routines.append(routine)
            self.routineList.addItem(routine.title)
    def closeEvent(self,event):
        self.isSaved = False
        #Save가 필요하다는 것을 보여주어야 한다.
