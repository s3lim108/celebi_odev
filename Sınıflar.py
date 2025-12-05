class UAV:
    def __init__(self, irtifa, hiz_x=0, hiz_y=0):
        self.hiz_x = hiz_x
        self.hiz_y = hiz_y
        self.irtifa = irtifa
    def anlik_hiz(self):
        return (self.hiz_x**2 + self.hiz_y**2)**0.5

class Yuk:
    def __init__(self, kutle=0, Cd=0, alan=0):
        self.kutle = kutle
        self.Cd = Cd
        self.alan = alan
    
class Cevre:
    def __init__(self, ruzgar_Vx=0, ruzgar_Vy=0, yercekimi_ivmesi=9.81, hava_yogunlugu=1.225):
        self.ruzgar_Vx = ruzgar_Vx
        self.ruzgar_Vy = ruzgar_Vy
        self.yercekimi_ivmesi = yercekimi_ivmesi
        self.hava_yogunlugu = hava_yogunlugu
    def anlik_ruzgar(self):
        return (self.ruzgar_Vx**2 + self.ruzgar_Vy**2)**0.5
    
class BalistikHesap:
    def __init__(self):
        pass

    def bagil_hiz_hesapla(self, uav, cevre):
        vx = uav.hiz_x - cevre.ruzgar_Vx
        vy = uav.hiz_y - cevre.ruzgar_Vy
        return vx, vy 

    def surunme_kuvveti_hesapla(self, rho, Cd, alan, toplam_hiz):
        return 0.5 * rho * toplam_hiz**2 * Cd * alan
    
    def dusme_hesapla(self, uav, yuk, cevre):
        g = cevre.yercekimi_ivmesi
        rho = cevre.hava_yogunlugu
        Cd = yuk.Cd
        yuk_alan = yuk.alan
        yuk_agirlik = yuk.kutle / g
        
        vx, vy= self.bagil_hiz_hesapla(uav, cevre)
        
        x, y = 0, uav.irtifa
        
        dt = 0.1

        while y > 0:
            toplam_hiz = (vx**2 + vy**2)**0.5
            surunme_kuvveti = self.surunme_kuvveti_hesapla(rho, Cd, yuk_alan, toplam_hiz)
            
            x_ivme = - (surunme_kuvveti/yuk_agirlik) * (vx/toplam_hiz)
            y_ivme = -g - (surunme_kuvveti/yuk_agirlik)  * (vy/toplam_hiz)
            
            vx += x_ivme * dt
            vy += y_ivme * dt
            
            x += vx * dt
            y += vy * dt
            
        return x
