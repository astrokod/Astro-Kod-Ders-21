# Gemi ve Engeller listesi
ship = None
pipes = []

# Skor değişkeni
SCORE = 0

# Setup Fonksiyonu
def setup():
    # Gemi ve Borular değişkenini global scope'tan al
    global ship, pipes
    # 750x750'lik bir pencere oluştur
    size(750, 750)
    # Gemi nesnesi oluştur
    ship = Ship()
    # Engeller listesine bir engel ekle
    pipes.append(Pipe())
    
# Draw fonksiyonu
def draw():
    # SCORE değişkenini global scope'tan al
    global SCORE
    # Arka tarafı siyah yap
    background(0)
    # Gemiyi göster
    ship.show()
    # Gemi ekranın kenarına veya engellerden birine çaptı mı?
    ship.die(pipes)
    
    # Engelleri seçen bir döngü (Tersten döner)
    for i in range(len(pipes) - 1, -1, -1):
        # Engeli göster
        pipes[i].show()
        # Engeklin ekranın dışına çıkıp çıkmadığını kontrol et
        if pipes[i].die():
            # Çıktıysa engeli listesden çıkar
            del pipes[i]
            # Skor'u arttır
            SCORE += 1
        
    # her 120. framede engeller klistesine yeni bie engel ekle
    if frameCount%120 == 0:
        pipes.append(Pipe())
        
        
    # Skor'u göster
    textSize(25)
    fill(0, 255, 0)
    text("SCORE {}".format(SCORE), 50, 50)
    
# Tuşa basıldığında çalışan fonksiyon
def keyPressed():
    # Gemiyi yukarıya doğru ittir.
    ship.lift()
    
    
# Engeller sınıfı
class Pipe:
    # Constructor metod
    def __init__(self):
        # Başlangıç pozisyonu
        self.pos = PVector(width, 0)
        # iki boru arasındaki boşluğun başlangıç değeri
        self.gap_start = random(150, 450)
        # iki boru arasındaki böşluk
        self.gap = random(150, 200)
        # Boru genişliği
        self.w = 50
        
    # Boruyu ekranda gösterme metodu
    def show(self):
        # Boruyu hareket ettir
        self.move()
        # Gerekli ayarlar
        noStroke()
        fill(127, 78, 0)
        # Üst boyu
        rect(self.pos.x, self.pos.y, self.w, self.gap_start)
        # Alt boru
        rect(self.pos.x, self.gap_start + self.gap, self.w, height)
        
    # Boruyu hareket ettirme metodu
    def move(self):
        # Borunun pozisyonunun x ekseninden 3 çıkar
        self.pos.add(PVector(-3, 0))
        
    # Boruyu öldürme metodu
    def die(self):
        # Boru kendi genişliği kadar ekranın dışında mı?
        return self.pos.x <= -self.w
    
    
# Uzay gemisi metodu
class Ship:
    # Constructor metod
    def __init__(self):
        # Başlangıç pozisyonu
        self.pos = PVector(width/6, height/2)
        # Başlangıç hızı
        self.vel = PVector(0, 0)
        # Uygulanacak yer çekim ivmesi
        self.g = PVector(0, 0.3)
        # Geminin yarıçapı
        self.r = 75
        
    # Gemiyi ekranda gösterme metodu
    def show(self):
        # Gemiyi hareket ettir
        self.move()
        # Ayarlar
        noStroke()
        fill(128)
        # Gemiyi ekrana çiz
        ellipse(self.pos.x, self.pos.y, self.r, self.r/3)
        # Ayarlar
        fill(94, 255, 255)
        # Geminin penceresini çiz
        circle(self.pos.x, self.pos.y - self.r/5, self.r/3)
        
    # Gemiyi hareket ettirme metodu
    def move(self):
        # Geminin hızına ivmeyi ekle
        self.vel.add(self.g)
        # Geminin pozisyonuna hızı ekle
        self.pos.add(self.vel)
        
    # Gemiyi yukarıya doğru hareket ettirme
    def lift(self):
        # Geminin y ekseni hızından 10 çıkar. - yukarı demek
        self.vel.add(PVector(0, -10))
        
    # Gemi öldü mğ? metodu
    def die(self, pipes):
        # Gemi ekranın kenarına çarptı mı?
        if not self.r/3 <= self.pos.y <= height - self.r/3:
            # draw döngüsünü durdur
            noLoop()
            
        # Tüm boruları tarayan döngü
        for pipe in pipes:
            # Eğer benim x ekseni pozisyonun borunun içindeyse
            if pipe.pos.x - self.r/3 <= self.pos.x <= pipe.pos.x + pipe.w + self.r/3:
                # Eğer üst borunun boyundan daha yukarıda
                # veya alt borunun boyundan daha aşağıdaysam
                if self.pos.y <= pipe.gap_start + self.r/3 or self.pos.y >= pipe.gap_start + pipe.gap - self.r/3 :
                    # draw döngüsünü durdur
                    noLoop()
