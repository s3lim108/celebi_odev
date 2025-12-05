class DusmeHesap:
    def __init__(self):
        self.g=9.87
        
    def dusecekKonumBul(self,x0,y0,vx0,vy0,m,k):
        x,y = x0,y0
        vx,vy=vx0,vy0
        
        while y>0:
            ax = -(k/m) * vx
            ay = -9.81 - (k/m) * vy
            
            vx+=ax*0.1
            vy+=ay*0.1
            
            x+=vx*0.1
            y+=vy*0.1
        return x
    

sonuc = DusmeHesap()
hit = sonuc.dusecekKonumBul(0,100,10,5,2.0,0.5)
print(hit)