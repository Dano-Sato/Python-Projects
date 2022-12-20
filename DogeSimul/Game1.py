from MyPyLib import *

class OrderBook(QWidget):
    def __init__(self,_isBuy = True,_count = 10):
        super().__init__()
        self.labels = []
        self.orders = {}
        self.isBuy = _isBuy # 구매 오더북인지, 판매 오더북인지 확인하는 인자
        self.labelUpdateTimer = 0
        if self.isBuy:
            self.color = 'green'
        else:
            self.color = 'red'
        self.layout = XVLayout()
        self.count = _count
        for i in range(_count):
            l = QLabel()
            l.setFont(QFont('Monaco',12))
            self.labels.append(l)
            self.layout.addWidget(l)
        if not self.isBuy:
            self.labels.reverse()
        self.setLayout(self.layout)
    def generate(self,curPrice,range,count):
        r = random.randint(-range,range)
        price = max(0,curPrice+r)
        c = random.randint(int(count/10),count)
        if price in list(self.orders):
            self.orders[price]+=c
        else:
            self.orders[price]=c
            
        
        
    def update(self,matchPrice,amount,delta):
        
        l = list(self.orders)
        if len(l)==0:
            self.generate(matchPrice,delta,amount)            
            return
        l.sort()
        if self.isBuy:
            l.reverse()
            
        self.labelUpdateTimer+=1
        if self.labelUpdateTimer>=10:
            self.labelUpdateTimer=0    
            #Label Update
            for i, la in enumerate(self.labels):
                if i < len(self.orders):
                    _o = str(self.orders[l[i]])
                    _space = '&nbsp;'
                    _r = (10-len(_o))*_space+_o

                    la.setText("<font color='{0}'> {1} </font> {2}".format(self.color,l[i]/10.0,_r))
        if random.random()<0.3:
            self.generate(matchPrice,delta,amount)


        #Demolishing process
        
        for order in l:
            c = abs(matchPrice-order)/matchPrice
            c*=100
            d = random.random()*c
            if random.random()<0.1:
                self.orders[order] = int(self.orders[order]*(1-d))
                if self.orders[order] <=0:
                    del self.orders[order] 
        for order in l[500:]:
            del self.orders[order]
            
    

class Appli(Genesis):
    def initUI(self):
        self.resize(600,600)
        self.setWindowTitle("Test Game")
        indicator = QLabel("<font color=#AAAAAA>Price(Cent) &nbsp; Amount(HDG)</font>")
        self.buyOrder = OrderBook(True)
        self.sellOrder = OrderBook(False)
        
        self.buyOrder.orders ={5121:3}
        self.sellOrder.orders = {5122:5}
        self.priceLabel = QLabel('>1')
        self.priceLabel.setFont(QFont('Monaco',20))
        self.priceUpdateTimer = 0 
        self.priceColor = 'white'
        self.matchPrice = 5121
        self.curPrice = 512
        self.OrderBook = XVLayout(indicator,self.sellOrder,self.priceLabel,self.buyOrder)
        self.setLayout(self.OrderBook)
    def update(self):
        super().update()
        self.priceUpdateTimer+=1
        if self.priceUpdateTimer%5==0:
            self.priceLabel.setText("<font color='{0}'> &nbsp; {1} </font>".format(self.priceColor,str(self.matchPrice/10)))
        if self.priceUpdateTimer%10==0:
            newPrice = int(self.matchPrice/10)
            if self.curPrice<newPrice:
                self.priceColor = 'green'
            elif self.curPrice == newPrice:
                self.priceColor = 'white'
            else:
                self.priceColor = 'red'
            self.curPrice = int(self.matchPrice / 10)
            
        self.buyOrder.update(self.matchPrice,1000,10)
        self.sellOrder.update(self.matchPrice,1000,10)

        while self.match():
            True

    # Buy order과 Sell order의 오더를 상쇄한다.
    def match(self):
        try:
            m = max(list(self.buyOrder.orders))
            n = min(list(self.sellOrder.orders))
            self.matchPrice = m
            if m>=n:
                count = min(self.buyOrder.orders[m],self.sellOrder.orders[n])
                self.buyOrder.orders[m] -= count
                if self.buyOrder.orders[m] <= 0:
                    del self.buyOrder.orders[m]
                self.sellOrder.orders[n] -= count
                if self.sellOrder.orders[n] <=0:
                    del self.sellOrder.orders[n]
                return True
            else:
                return False
        except:
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