from MyPyLib import *

class RoutineManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Routine Manager')
        self.setWindowModality(Qt.NonModal)
        self.resize(800,800)
        self.routineList = QListWidget()
        self.addButton = QPushButton("+Make Routine")
        self.titleEdit = QLineEdit()
        self.textEdit = QPlainTextEdit()
        self.layout = XHLayout(XVLayout(QLabel('Routines'),self.routineList,self.addButton),XVLayout(QLabel('Title'),self.titleEdit,QLabel('Text'),self.textEdit))
        self.setLayout(self.layout)
