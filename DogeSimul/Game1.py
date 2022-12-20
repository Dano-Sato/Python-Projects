from MyPyLib import *

class OrderBook(QWidget):
    def __init__(self,_isBuy = True,_count = 10):
        super().__init__()
        self.labels = []
        self.orders = {1121:3,1124:4,1125:5,1140:4,1150:3,1161:16}
        self.isBuy = _isBuy # 구매 오더북인지, 판매 오더북인지 확인하는 인자
        if self.isBuy:
            self.color = 'green'
        else:
            self.color = 'red'
        self.layout = XVLayout()
        self.count = _count
        for i in range(_count):
            l = QLabel()
            self.labels.append(l)
            self.layout.addWidget(l)
        if not self.isBuy:
            self.labels.reverse()
        self.setLayout(self.layout)
    def generate(self,curPrice,range,count):
        r = random.randint(-range,range)
        price = max(0,curPrice+r)
        c = random.randint(1,count)
        if price in list(self.orders):
            self.orders[price]+=c
        else:
            self.orders[price]=c
        
    def update(self):
        l = list(self.orders)
        l.sort()
        if self.isBuy:
            l.reverse()
        for i, la in enumerate(self.labels):
            if i < len(self.orders):
                la.setText("<font color='{0}'> {1} </font> \t\t {2}".format(self.color,l[i]/10.0,self.orders[l[i]]))
        self.generate(l[0],10,10)
            
        
    

class Appli(Genesis):
    def initUI(self):
        self.resize(600,600)
        self.setWindowTitle("Test Game")
        self.buyOrder = OrderBook(True)
        self.sellOrder = OrderBook(False)
        self.layout = XVLayout(self.sellOrder,self.buyOrder)
        self.setLayout(self.layout)
    def update(self):
        super().update()
        self.buyOrder.update()
        self.sellOrder.update()
        while self.match():
            True

    # Buy order과 Sell order의 오더를 상쇄한다.
    def match(self):
        m = max(list(self.buyOrder.orders))
        n = min(list(self.sellOrder.orders))
        if m>=n:
            count = min(self.buyOrder.orders[m],self.sellOrder.orders[n])
            self.buyOrder.orders[m] -= count
            if self.buyOrder.orders[m] == 0:
                del self.buyOrder.orders[m]
            self.sellOrder.orders[n] -= count
            if self.sellOrder.orders[n] ==0:
                del self.sellOrder.orders[n]
            return True
        else:
            return False
            
        
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
    mwindow = Appli()
    mwindow.show()
    
    app.exec_()