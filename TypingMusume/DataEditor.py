##어플리케이션의 기본 디폴트 형태를 담음.
##새 프로젝트를 만들 때 이것을 복사해서 쓰면 좋다.

from MyPyLib import *

class Game(Genesis):
    def initUI(self):
        self.resize(600,600)
        self.setWindowTitle("Test Game")        
        self.x=200
        self.y=200

    def drawEvent(self, event):
        a = self.drawAction
        a()
        return
    def drawAction(self):
        self.drawString(self.x,self.y,"test")
    def update(self):
        super().update()
        
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            print('test')
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_W:
            self.y-=4
        if event.key()==Qt.Key_A:
            self.x-=4
        if event.key()==Qt.Key_S:
            self.y+=4
        if event.key()==Qt.Key_D:
            self.x+=4
            

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mwindow = Game()
    mwindow.show()
    
    app.exec_()