from MyPyLib import *


ArrCha = '⇐⇑⇒⇓'
RectColors = ['255,0,0','0,255,0','0,0,255','200,200,0']
InitialData = 'Isab02'
DataSet = {'Isab01':[50,None,60],'Isab02':[100,None,64],'Ziba02':[150,None,63]}

class ArrowLine(QWidget):

    def __init__(self):
        super().__init__()
        self.Arrows=[]
        self.layout = XVLayout()
        self.setLayout(self.layout)
    def addArrow(self,c,b):
        l = QLabel(c)
        l.setFont(QFont('Arial',60*b))
        l.setFixedSize(75*b,75*b)
        self.Arrows.append(l)
        self.layout.addWidget(l)

class Appli(Genesis):
    def addArrow(self,c):
            self.AL.addArrow(c,self.big)
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
    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self,direction):
        if direction==1:
            self.setRectColor(255,0,0)
        else:
            self.setRectColor(0,255,255)
        self._direction = direction
    def initUI(self):
        self.setWindowTitle("⇑Bishoujo Dance Club")
        
        self.scoreLabel = QLabel('SCORE:0')
        self.scoreLabel.setFont(QFont('Arial',20))
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        self.GameEnd = False


        self.dancer = QLabel()
        self.dancer.setScaledContents(True)
        self.movie = QMovie(InitialData+'.gif')
        self.dancer.setMovie(self.movie)
        
        self.big = 1

        self.showMaximized()
        if self.size().height()>1000:
            self.dancer.setFixedSize(800,1200)
            self.big=2
            self.setFixedHeight(1250)
            self.setFixedWidth(850)
        else:
            self.dancer.setFixedSize(400,600)
            self.big=1
            self.setFixedHeight(650)
            self.setFixedWidth(450)
        
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


        self.movie.start()
        self._score = 0
        self._curIndex = 0
        self.setLayout(XVLayout(self.scoreLabel,self.dancer))

        self.notMoveTimer = 100
        self.currectTimer = 0        
        self.startTime = time.time()
        
        #self.rect.setStyleSheet('QLabel{background-color: red}')

        self.rect = QLabel(self.dancer)
        self.rectTimer = 0
        self.rect.setFixedSize(50*self.big,50*self.big)
        self.rect.setStyleSheet('QLabel {background-color: rgba(255,0,0,80%); border-radius:20px}')
        self._rectColor=[0,0,0]
        self._direction = 1
        
        
        self.AL = ArrowLine()
        self.AL.setParent(self.dancer)        
        self.AL.move(QPoint(10*self.big,30*self.big))
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
        s = ','.join([str(r),str(g),str(b)])
        self.rect.setStyleSheet('QLabel {background-color: rgba('+s+',80%); border-radius:20px}')
        
    def update(self):
        super().update()
        if self.currectTimer>0:
            self.currectTimer-=1
        if time.time()-self.startTime>DataSet[InitialData][2]:
            self.GameEnd = True
        self.rectTimer +=1
        self.notMoveTimer+=1
        if self.notMoveTimer>50:
            self.movie.setPaused(True)
        else:
            if self.movie.state()==QMovie.MovieState.Paused:
                self.movie.setPaused(False)
        m = 30
        if self.rectTimer ==m:
            self.rectTimer = 0
        d = min(self.rectTimer,m-self.rectTimer)//4
        self.rect.setFixedSize(self.AL.Arrows[self.curIndex].size()+QSize(d,2*d)-8*QSize(self.currectTimer,self.currectTimer))
        for a in self.AL.Arrows:
            a.setFont(QFont('Arial',(60+d)*self.big))
        Xt.moveTo(self.rect,self.AL.Arrows[self.curIndex].pos()+self.AL.pos()-QPoint(0,d)+QPoint(-10*self.big,0)+4*QPoint(self.currectTimer,self.currectTimer))
    def Match(self,c):
        if self.AL.Arrows[self.curIndex].text() == c:
            self.score +=DataSet[InitialData][0]
            self.notMoveTimer=0
            DataSet[InitialData][1]()
            path = os.getcwd()+"/beat.wav"
            QSound.play(path)
            self.currectTimer=6

            '''
            t = self.AL.Arrows[self.curIndex].text()
            i = ArrCha.index(t)
            self.setRectColor()
            '''
        else:
            self.score = max(0,self.score-5*DataSet[InitialData][0])
            path = os.getcwd()+"/error.wav"
            QSound.play(path)
            

        
        
    '''
    def drawEvent(self, event):
        a = self.drawAction
        a()
        return
    def drawAction(self):
        self.drawString(self.x,self.y,"test")
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            print('leftButton')
    '''
            
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

    def Match_Isab01(self):
            a = self.AL.Arrows[self.curIndex]
            a.setText(random.choice(ArrCha))
            if self.curIndex == 0:
                self.direction = 1
            elif self.curIndex ==len(self.AL.Arrows)-1:
                self.direction = -1
            self.curIndex+=self.direction
                
    def Match_Isab02(self):
            a = self.AL.Arrows[self.curIndex]
            a.setText(random.choice(ArrCha))
            if random.random()<0.1:
                self.direction = -self.direction
            self.curIndex+=self.direction
            if self.curIndex >= len(self.AL.Arrows):
                self.curIndex = 0
            if self.curIndex <= -1:
                self.curIndex = len(self.AL.Arrows)-1
    def Match_Ziba02(self):
            self.direction = -1
            a = self.AL.Arrows[self.curIndex]
            a.setText(random.choice(ArrCha))
            r = -1
            while(True):
                r =random.randint(0,len(self.AL.Arrows)-1)
                if r != self.curIndex:
                    break
            self.curIndex=r
        

class Game():
    @classmethod
    def playMusic(cls,musicName):
        cls.playlist = QMediaPlaylist()
        path = os.path.join(os.getcwd(), musicName)
        url = QUrl.fromLocalFile(path)
        cls.playlist.addMedia(QMediaContent(url))
        #playlist.setPlaybackMode(QMediaPlaylist.Loop)

        cls.player = QMediaPlayer()
        cls.player.setPlaylist(cls.playlist)
        cls.player.play()

        
if __name__ == '__main__':
    CharList = ['Isab01','Isab02','Ziba02']
    print('Choose from: '+str(CharList))
    while(True):
        x = input()
        try:
            i = int(x)
            if i< len(CharList):
                InitialData = CharList[i]
                break
        except:
            pass
    
    app = QApplication(sys.argv)
    danceGame = Appli()
    DataSet['Isab01'][1]=danceGame.Match_Isab01
    DataSet['Isab02'][1]=danceGame.Match_Isab02
    DataSet['Ziba02'][1]=danceGame.Match_Ziba02
    danceGame.show()
    Game.playMusic(InitialData+'_m.mp3')
    
    app.exec_()