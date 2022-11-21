from MyPyLib import *

class RoutineManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Routine Manager')
        self.setWindowModality(Qt.NonModal)
        self.resize(1200,800)        
        self.layout = XHLayout(XVLayout())
        self.setLayout(self.layout)
