from MyPyLib import *


ArrCha = '⇐⇑⇒⇓'
RectColors = ['255,0,0','0,255,0','0,0,255','200,200,0']

class ArrowLine(QWidget):

    def __init__(self):
        super().__init__()
        self.Arrows=[]
        self.layout = XVLayout()
        self.setLayout(self.layout)
    def addArrow(self,c):
        l = QLabel(c)
        l.setFont(QFont('Arial',60))
        self.Arrows.append(l)
        self.layout.addWidget(l)

class Appli(Genesis):
    def addArrow(self,c):
            self.AL.addArrow(c)
            #self.arrow.setText(self.AL.Arrows[0].text())
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self,score):
        self.scoreLabel.setText("SCORE: "+str(score))
        self._score = score
        
    @property
    def curIndex(self):
        return self._curIndex
    @curIndex.setter
    def curIndex(self,curIndex):
        if curIndex >= len(self.AL.Arrows):
            curIndex = 0
        self._curIndex = curIndex
    def initUI(self):
        self.setWindowTitle("⇑Dance with Bishoujo")
        

        
        self.scoreLabel = QLabel('SCORE:0')
        self.GameEnd = False


        self.dancer = QLabel()
        self.dancer.setScaledContents(True)
        self.dancer.setFixedSize(400,600)
        self.movie = QMovie('zerotwo01.gif')
        self.dancer.setMovie(self.movie)
        self.movie.start()
        self._score = 0
        self._curIndex = 0
        self.setLayout(XVLayout(self.scoreLabel,self.dancer))
        self.notMoveTimer = 0
        self.endTimer = 0
        
        #self.rect.setStyleSheet('QLabel{background-color: red}')

        self.rect = QLabel(self.dancer)
        self.rectTimer = 0
        self.rect.setFixedSize(50,50)
        self.rect.setStyleSheet('QLabel {background-color: rgba(255,0,0,80%); border-radius:20px}')
        self._rectColor=[0,0,0]
        
        
        self.AL = ArrowLine()
        self.AL.setParent(self.dancer)        
        self.AL.move(QPoint(10,30))
        '''
        self.arrow = QLabel(self.dancer)
        self.arrow.setText('a')
        self.arrow.setFont(QFont('Arial',30))
        self.arrow.setStyleSheet('QLabel {color:black}')
        self.arrow.move(QPoint(150,400))
        '''
        for i in range(6):
            self.addArrow(random.choice(ArrCha))


    def setRectColor(self,r,g,b):
        str = ','.join(str(r),str(g),str(b))
        self.rect.setStyleSheet('QLabel {background-color: rgba('+str+',80%); border-radius:20px}')
        
        

        
    def update(self):
        super().update()
        self.endTimer+=1
        if self.endTimer==3140:
            self.GameEnd = True
        self.rectTimer +=1
        self.notMoveTimer+=1
        if self.notMoveTimer>40:
            self.movie.setPaused(True)
        else:
            if self.movie.state()==QMovie.MovieState.Paused:
                self.movie.setPaused(False)
        m = 30
        if self.rectTimer ==m:
            self.rectTimer = 0
        d = min(self.rectTimer,m-self.rectTimer)//4
        self.rect.setFixedSize(self.AL.Arrows[self.curIndex].size()+QSize(d,2*d))
        Xt.moveTo(self.rect,self.AL.Arrows[self.curIndex].pos()+self.AL.pos()-QPoint(d,d))
    def Match(self,c):
        if self.AL.Arrows[self.curIndex].text() == c:
            self.score +=100
            self.notMoveTimer=0
            #self.movie.jumpToNextFrame()
            a = self.AL.Arrows[self.curIndex]
            a.setText(random.choice(ArrCha))
            #self.addArrow(random.choice(ArrCha))
            self.curIndex+=1
            if self.curIndex == len(self.AL.Arrows):
                self.curIndex = 0
            t = self.AL.Arrows[self.curIndex].text()
            i = ArrCha.index(t)
        else:
            self.score = max(0,self.score-1000)
            path = os.getcwd()+"/error.wav"
            QSound.play(path)
        
    '''
    def drawEvent(self, event):
        a = self.drawAction
        a()
        return
    def drawAction(self):
        self.drawString(self.x,self.y,"test")
    '''
            
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            print('leftButton')
    def keyPressEvent(self,event):
        if not self.GameEnd:
            if event.key()==Qt.Key_W or event.key()==Qt.Key_Up:
                self.Match('⇑')
            if event.key()==Qt.Key_A or event.key()==Qt.Key_Left:
                self.Match('⇐')
            if event.key()==Qt.Key_S or event.key()==Qt.Key_Down:
                self.Match('⇓')
            if event.key()==Qt.Key_D or event.key()==Qt.Key_Right:
                self.Match('⇒')

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mwindow = Appli()
    mwindow.show()
    playlist = QMediaPlaylist()
    path = os.path.join(os.getcwd(), 'dance1.mp3')
    url = QUrl.fromLocalFile(path)
    playlist.addMedia(QMediaContent(url))
    #playlist.setPlaybackMode(QMediaPlaylist.Loop)

    player = QMediaPlayer()
    player.setPlaylist(playlist)
    player.play()

    
    app.exec_()