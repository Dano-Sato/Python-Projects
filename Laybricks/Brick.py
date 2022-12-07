from MyPyLib import *
from RoutineManager import *

BrickTitleFont = QFont('Arial',20)
BrickTitleFont.setBold(True)
BrickTextFont = QFont('Arial',15)


class Brick(XGraphicsRectItem):
    def __init__(self,_title='Title',_text='',_color=None):
        super().__init__()
        self.title = QGraphicsTextItem(_title)
        self.title.setFont(BrickTitleFont)
        self.title.setParentItem(self)
        self.text = QGraphicsTextItem(_text)
        self.text.setFont(BrickTextFont)
        self.text.setParentItem(self)
        self.foldButton = QGraphicsTextItem('⬆')
        self.foldButton.setFont(BrickTextFont)
        self.foldButton.setParentItem(self)
        self.pinButton = QGraphicsTextItem('📌')
        self.pinButton.setFont(BrickTextFont)
        self.pinButton.setParentItem(self)
        self.pinButton.hide()
        if _color == None:
            _color = QColor(random.randint(0,75),random.randint(0,75),random.randint(0,75))
        self.color = _color
        self.setBrush(self.color) # 배경색 정함
        self.setPen(QPen(Qt.white,1))
    def setRect(self,x,y,w,h):
        super().setRect(0,0,w,h)
        self.title.setPos(5,5)
        self.text.setPos(10,40)
        self.foldButton.setPos(w-35,8)
        self.pinButton.setPos(w-60,8)
        self.text.setTextWidth(self.rect().width()-20)
        self.setPos(x,y) # Coordinate를 망가뜨리지 않기 위해 이렇게 설계
    def fold(self):
        if self.foldButton.toPlainText()=='⬆':
            self.foldButton.setPlainText('⬇')
            self.text.hide()
        else:
            self.foldButton.setPlainText('⬆')
            #self.text.show()
            
            
    def setTitle(self,str):
        self.title.setPlainText(str)
    def setText(self,str):
        self.text.setPlainText(str)
    def heightUpdate(self):
        if self.foldButton.toPlainText()=='⬆':
            h1 = self.title.boundingRect().height()
            h2 = self.text.boundingRect().height()
            rect = self.rect()
            rect.setHeight(min(rect.height()*1.15,h1+h2+10))
            self.setRect(rect.x(),rect.y(),rect.width(),rect.height())
            if rect.height() == h1+h2+10:
                self.text.show()
        else:
            h1 = self.title.boundingRect().height()
            rect = self.rect()
            rect.setHeight(max(rect.height()*0.85,h1+10))
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
    # 내부 브릭들의 위치를 정렬한다.     
    def update(self): 
        self.Bricks.sort(key = lambda x:x.rect().y())
        temp = self.rect().y()
        temp += 70
        lastUnFoldBrick = None
        for b in self.Bricks:
            b.moveTo(self.rect().x()+self.delta,temp)
            if b.foldButton.toPlainText()=='⬆':
                lastUnFoldBrick = b
            temp+=b.rect().height()
            temp+=self.delta
        if temp>self.rect().height():
            if lastUnFoldBrick != None:
                lastUnFoldBrick.fold()

    #보드에 새로운 브릭을 추가한다.
    def addBrick(self,scene):
        b = Brick()
        b.setRect(self.pos().x(),self.pos().y(),self.rect().width()-self.delta*2,self.minimal_brick_height)
        b.heightUpdate()

        self.Bricks.append(b)
        self.isSaved = False
        self.update()
        scene.addItem(b)

    #[title,text,color] 리스트 형태의 데이터를 받아서 브릭을 구성한다.
    def addBrickFromData(self,scene,data):
        b = Brick(data[0],data[1],data[2])
        b.setRect(self.pos().x(),self.pos().y(),self.rect().width()-self.delta*2,self.minimal_brick_height)
        b.heightUpdate()

        self.Bricks.append(b)
        self.isSaved = False
        self.update()
        scene.addItem(b)
        
    def dataExport(self):
        l = []
        for b in self.Bricks:
            l.append([b.title.toPlainText(),b.text.toPlainText(),b.color])
        return l
    def dataImport(self,scene,data):
        data.reverse()
        for d in data:
            self.addBrickFromData(scene,d)
