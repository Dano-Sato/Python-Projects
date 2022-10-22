from MyPyLib import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(200,100)
        self.setWindowTitle("Test App")
        self.layout = QVBoxLayout()
        self.layout.addWidget(QPushButton("Hello World"))
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwindow = MainWindow()
    mwindow.show()
    app.exec_()