import matplotlib.pyplot as plt
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
    def ivme_hesapla(self, vx, vy, yuk_agirlik, surunme_kuvveti, g):
        toplam_hiz = (vx**2 + vy**2)**0.5
        x_ivme = - (surunme_kuvveti/yuk_agirlik) * (vx/toplam_hiz)
        y_ivme = -g - (surunme_kuvveti/yuk_agirlik)  * (vy/toplam_hiz)
        return x_ivme, y_ivme
    def hiz_guncelle(self, vx, vy, x_ivme, y_ivme, dt):
        vx += x_ivme * dt
        vy += y_ivme * dt
        return vx, vy
    def konum_guncelle(self, x, y, vx, vy, dt):
        x += vx * dt
        y += vy * dt
        return x, y
    
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
            
            vx , vy = self.hiz_guncelle(vx, vy, x_ivme, y_ivme, dt)
            
            x, y = self.konum_guncelle(x, y, vx, vy, dt)
        return x

    def ters_dusme_hesapla(self, uav, yuk, cevre, hedef_x, tol = 0.01):
        uav_iter=UAV(irtifa=uav.irtifa, hiz_x=uav.hiz_x, hiz_y=uav.hiz_y)
        tahmini_vx = uav.hiz_x

        hata = float('inf')
        max_iter = 100

        ayarlama_carpani = 0.5

        for i in range(max_iter):
            uav_iter.hiz_x = tahmini_vx

            gerceklesen_x = self.dusme_hesapla(uav_iter, yuk, cevre)

            hata = hedef_x - gerceklesen_x

            if abs(hata) < tol:
                print("basarili iterasyon")

                return tahmini_vx
            
            ayarlama_miktari = hata* ayarlama_carpani / hedef_x

            tahmini_vx += ayarlama_miktari * tahmini_vx

            if (i == max_iter - 1):
                print("maksimum iterasyona ulasildi, istenen tolerans saglanamadi.")

        return tahmini_vx
    



    def dusme_grafikli(self, uav, yuk, cevre):
        g = cevre.yercekimi_ivmesi
        rho = cevre.hava_yogunlugu
        Cd = yuk.Cd
        alan = yuk.alan
        yuk_agirlik = yuk.kutle / g
        
        # başlangıç hızları
        vx, vy = self.bagil_hiz_hesapla(uav, cevre)

        # başlangıç konumu
        x, y = 0, uav.irtifa
        dt = 0.1

        # grafik için listeler
        xs, ys = [x], [y]
        speeds = []
        times = [0]
        t = 0

        while y > 0:
            toplam_hiz = (vx**2 + vy**2)**0.5
            surunme = self.surunme_kuvveti_hesapla(rho, Cd, alan, toplam_hiz)

            x_ivme = - (surunme/yuk_agirlik) * (vx/toplam_hiz)
            y_ivme = - g - (surunme/yuk_agirlik) * (vy/toplam_hiz)

            vx, vy = self.hiz_guncelle(vx, vy, x_ivme, y_ivme, dt)
            x, y = self.konum_guncelle(x, y, vx, vy, dt)

            xs.append(x)
            ys.append(max(y, 0))    # yer altına düşmesin
            speeds.append((vx**2 + vy**2)**0.5)

            t += dt
            times.append(t)

        # --- TRAJEKTORİ GRAFİĞİ ---
        plt.figure(figsize=(10,6))
        plt.plot(xs, ys)
        plt.xlabel("X (metre)")
        plt.ylabel("Y (metre)")
        plt.title("Balistik Düşüş Trajektorisi")
        plt.grid(True)
        plt.show()

        # --- HIZ GRAFİĞİ ---
        plt.figure(figsize=(10,6))
        plt.plot(times[:-1], speeds)
        plt.xlabel("Zaman (saniye)")
        plt.ylabel("Hız (m/s)")
        plt.title("Yük'ün Hızının Zamana Göre Değişimi")
        plt.grid(True)
        plt.show()

        return xs[-1]  # yere temas X noktası
    

uav = UAV(irtifa=200, hiz_x=20, hiz_y=0)
yuk = Yuk(kutle=2, Cd=0.4, alan=0.03)
cevre = Cevre(ruzgar_Vx=2, ruzgar_Vy=0)

hesap = BalistikHesap()

hesap.dusme_grafikli(uav, yuk, cevre)