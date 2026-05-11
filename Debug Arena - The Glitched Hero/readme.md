# DEBUG ARENA YARIŞMASI: The Glitched Hero

**Tarih:** 11 Mayıs (10:00) - 17 Mayıs (23:59) 2026

---

## 📌 Yarışma Hakkında
**Türkiye Yapay Zeka Topluluğu** bünyesinde düzenlenen **Debug Arena**, yarışmacıların halihazırda var olan ancak teknik bütünlüğü bozulmuş bir yazılım projesini analiz ederek, içerisindeki hataları (bug) onarmalarını amaçlayan bir hata ayıklama (debugging) yarışmasıdır. Amacınız, size verilen bozuk kod tabanını proje kurallarına sadık kalarak tamamen çalışır hale getirmektir.

---

## 📁 Dosya Hiyerarşisi
```text
  main.py              → Oyunun tek başlangıç noktası. Başka iş yapmaz.
  game/
  ├── __init__.py      → game/ klasörünü Python paketi olarak tanımlar. İçi boştur.
  ├── data.py          → Tüm sabit veriler burada. Bölüm bilgileri, level ödülleri.
  ├── item.py          → Tek bir eşyayı temsil eder ve kullanım mantığını taşır.
  ├── inventory.py     → Oyuncunun çantasını yönetir. Item bilmez, slot bilir.
  ├── character.py     → Oyuncu karakteri. Tüm stat ve aksiyonlar burada.
  ├── enemy.py         → Düşman karakteri. Karakterden bağımsız, daha sade.
  ├── battle.py        → İki karakter arasındaki tek savaşı yönetir.
  └── game.py          → Tüm bölümleri sırayla oynatır, oyunun ana akışıdır.
```

---

## 🚀 Nasıl Çalıştırılır?
Bu proje standart hiçbir ek kütüphaneye ihtiyaç duymaz. Bilgisayarınızda **Python 3** yüklü olması yeterlidir.

Size verilen klasörün (`Debug Arena - The Glitched Hero/`) içinde terminal açarak aşağıdaki komutu çalıştırın:

```bash
python main.py
```

> **Not:** Python komutunun çalışmaması durumunda `python3 main.py` komutunu deneyin.

---

## 🎮 Oyunun Sistem Mantığı ve Teorik Altyapısı (DİKKATLE OKUYUNUZ!)
Sistem içerisindeki "Mantık Hataları (Logic Bugs)" salt kod denenerek onarılamaz! Karşılaştığınız sorunların orijinal oyun kurallarına göre nasıl çalışması gerektiğini bilmezseniz, getireceğiniz "patch" çözümleri geçersiz (hardcoded) sayılacaktır. Aşağıdaki kural seti oyunun orijinal matematiksel modelini tanımlar:

### 1. Savaş ve Hasar Matematiği (En Kritik Bölüm)
- **Saldırı (Attack):** Saldırı gücü sabit değildir! Karakterin hasar formülü şu şekildedir: `Temel Hasar + Rastgele Değer (0-5) + Geçici Güçlendirme Buff'ı`. Eğer yetenek veya eşyadan gelen bir "Geçici Güçlendirme" varsa (Örn: Saldırı Tozu), bu buff eklendikten sonra **mutlaka sıfırlanmalıdır** (tek kullanımlık olmalıdır).
- **Savunma (Defend):** Kullanıcı "Savun" komutunu seçtiğinde, ilgili savuma bayrağı aktifleşir ve o tur alınacak hasar **YARI YARIYA (%50)** düşürülür. Ardından bu bayrak sıfırlanmalıdır.
- **Kalkan (Shield):** "Demir Kalkan" çalıştırılırsa, gelen hasar *ilk olarak* kalkanın gücünden düşer, arta kalan hasar oyuncuya yansır. Kalkan hasarı sönümledikten sonra **Sıfırlanmalıdır (Kalıcı bir ölümsüzlük veya koruma zırhı yaratılamaz)**.
- **HP Kontrolleri (Bounds Check):** Oyunun doğası gereği hem düşman hem karakter HP (Can) havuzu **ASLA 0'ın altına düşmemeli** (negatif olmamalı) ve 0'a sabitlenmelidir.

### 2. Eşyalar ve Envanter Döngüsü
- **Tüketim Limitleri:** Bir eşya kullanıldığında kullanım sayısı  mutlak suretle **1 adet eksilmelidir**.
- **Boş Çanta Kontrolü:** Eğer oyuncunun envanterinde kullanım hakkı (`uses > 0`) olan hiçbir eşya kalmadıysa, sistem "Envanterde kullanılabilir item yok!" uyarısı vermeli ve menüyü açmamalıdır.
- **Felç Etkisi (Stun):** Eşya kullanılarak düşman uyuşturulduğunda, düşmanın o tur hasarı 0 olmalı ve saldırı atlandıktan sonra durum sıfırlanarak düşman normale dönmelidir.
- **Tur Önceliği:** Oyuncu çantasını (Envanter) açıp kullandığında/kapattığında, hamle sırasını **kaybetmez**. Yani iksir içtiğinizde, sistem size "Tekrar saldırmak veya savunmak için" komut sormalı, düşman sistem boşluğundan faydalanıp aniden size (bedavaya) hasar vurmamalıdır!
- **Erişilebilir Eşyalar ve Seviyeleri:** Oyunda kullanılan eşyalar seviye atladıkça belirli bir sırayla oyuncunun envanterine eklenir. Oyuncu maceraya 2 kullanımlık **İksir** (+30 HP) ile başlar. Sonrasında kazanacağı seviye ödülleri şunlardır:
  - **Level 2:** Güçlü İksir (İyileşme - +50 HP yeniler)
  - **Level 3:** Saldırı Tozu (Saldırı Güçlendirme - Sonraki vuruşunuza +8 Hasar ekler)
  - **Level 4:** Demir Kalkan (Kalkan - Gelen hasarın ilk 20 birimini tamamen emer)
  - **Level 5:** Uyuşturma Ruhu (Felç - Düşmanı 1 tur boyunca felç ederek saldırmasını engeller)

### 3. Kaçma ve Karşılaşma (Flee Mechanics)
- **Cezalı Durum:** Eğer kaçış başarısız olursa, düşman oyuncudan bir intikam hamlesi olarak hasar çarpanını (multiplier) 1.5 kat artırıp tekil bir saldırı yapar.
- **Geri Dönüş (Encounter):** Bir düşmandan başarılı şekilde kaçarsanız, o bölümün (chapter) son eşleşmesinde aynı düşman oyuncuyu tekrar bulup karşısına çıkar. Ancak bu geri dönüşte düşman **canı (HP) fullenmiş olarak gelmemelidir!** En son ilk savaştan "yaralı kaçtığınız" anki HP değeri ne ise, %100 aynı HP ile mücadeleye devam ettirmelidir.

### 4. Deneyim (XP) ve Karakter İlerlemesi
Bir bölüm tamamlandığında oyuncu XP sınırını aşar ve seviye (level) atlar. Tüm seviye geçiş özellikleri **AYNI ANDA** kurgulanmalıdır:
- **XP Sıfırlama:** Toplanmış olan XP tutarı tamamen **SIFIRLANIR (0 olur)** ve bir sonraki seviye için tabandan birikmeye başlar (Sıfırlanmazsa bir kere level atlayan sonsuz döngüye girip tekrar tekrar atlar).
- **Can Yenileme:** Karakterin Max HP değeri 20 birim artar ve anlık canı (current HP) bu **yeni maksimum değere** şarj edilmelidir.
- **Güç Artışı:** Karakterin taban saldırı gücü (damage) kalıcı olarak 2 artar.
- **Kapasite:** Çantanın sınır taşıma kapasitesi (+1 slot) genişlemeli ve seviye ödülü envantere eklenmelidir.

### 5. Düşman Mantığı ve Durum Yönetimi
- **Ölüm Kontrolü:** Canı 0 veya altına düşen bir düşman anında "yenilmiş" sayılmalı ve savaş sonlanmalıdır.
- **Felç (Stun) Etkisi:** Düşman felç edildiğinde o tur hasar veremez. Bu tur atlandıktan sonra düşman **normale dönmeli** ve bir sonraki tur saldırabilmelidir.

---

## ⚠️ Yarışma Kuralları
1. **Orijinalite:** Sınıf (Class) yapılarını, dosya isimlerini veya ana oyun döngüsünü tamamen baştan kendi bildiğiniz gibi yazmak ZORUNLU OLMADIKÇA yasaktır. Amaç bozulanı orijinal mantığıyla onarmaktır.
2. **Raporlama Zorunluluğu:** Bulup düzelttiğiniz her hata, bu README dosyasının alt kısmındaki şablona DOLDURULMALIDIR! Sadece kodda onarılan ama burada bahsedilmeyen hatalar kopya/şüpheli işlem şüphesiyle geçersiz sayılır.

---

## 🛠️ ÇÖZÜLEN HATALAR FORMU
> *Lütfen bulduğunuz ve düzelttiğiniz hataları aşağıdaki şablona uygun olarak ekleyiniz.*

### 1- Saldırı Hasarı
* **Dosya Adı ve Satır Aralığı:** `game/character.py` (L23 - L26)
* **Hatanın Sebebi:** `attack()` metodu için README'de belirtilen hasar formülü çalışmıyordu.
* **Nasıl Çözdünüz:** Oyuncunun temel hasarına `0-5` arası rastgele değer ve geçici saldırı güçlendirmesi eklendi.

---

### 2- Savunma Durumu ve Negatif HP
* **Dosya Adı ve Satır Aralığı:** `game/character.py` (L28 - L43)
* **Hatanın Sebebi:** `defend()` metodunda savunma durumunu hatalıydı ve hasar alındığında can `0` altına düşebiliyordu.
* **Nasıl Çözdünüz:** `is_defending` kullanıldı. Savunma aktifse gelen hasar yarıya indi ve can `0` altına düşmeyecek şekilde ayarlandı.

---

### 3- Seviye Atlama Kuralları ve Max Slot Genişletmesi
* **Dosya Adı ve Satır Aralığı:** `game/character.py` (L53 - L72), `game/inventory.py` (L21 - L22)
* **Hatanın Sebebi:** Seviye atlandığında XP sıfırlanmıyor , max hp kurala göre artmıyor ve envanter kapasitesi genişlemiyordu.
* **Nasıl Çözdünüz:** Seviye atlanırken XP `0` olarak ayarlandı , max HP `20` kurala göre ayarlandı ve `Inventory.expand_slot()` `1` artıracak şekilde ayarlandı.

---

### 4- Karakter İstatistiği Yazdırma Hatası
* **Dosya Adı ve Satır Aralığı:** `game/character.py` (L79 - L81)
* **Hatanın Sebebi:** `show_stats()`'da `print` ifadesinde tırnak işareti eksikti.
* **Nasıl Çözdünüz:** Tırnak işareti ile düzeltildi.

---

### 5- Item Kullanım Hakkının Azalmaması
* **Dosya Adı ve Satır Aralığı:** `game/item.py` (L9 - L36)
* **Hatanın Sebebi:** Item kullanıldıktan sonra değeri düşürülmediği için eşyalar sonsuz kez kullanılabiliyordu.
* **Nasıl Çözdünüz:** İtem kullanıldıktan sonra `self.uses -= 1` olarak ayarlandı.

---

### 6- Felç
* **Dosya Adı ve Satır Aralığı:** `game/item.py` (L28 - L33)
* **Hatanın Sebebi:** `stun` için TODO bölümü için istenilen yapıldı.
* **Nasıl Çözdünüz:** TODO'ya göre `felç` ayarlandı.

---

### 7- Item Dosyası Sözdizimi Hatası
* **Dosya Adı ve Satır Aralığı:** `game/item.py` (L39 - L45)
* **Hatanın Sebebi:** `type_labels`'de elemanlar arasında virgül eksikleri vardı.
* **Nasıl Çözdünüz:** Eksik virgüller eklendi.

---

### 8- Boş Envanter Kontrolü
* **Dosya Adı ve Satır Aralığı:** `game/inventory.py` (L36 - L38), `game/battle.py` (L80 - L83)
* **Hatanın Sebebi:** `Inventory.has_items()` her durumda `True` şeklindeydi.
* **Nasıl Çözdünüz:** `has_items()` metodu kontrol edilecek şekilde ayarlandı.

---

### 9- Envanter Kullanımından Sonra Oyuncunun Turuna Devam Etmesi
* **Dosya Adı ve Satır Aralığı:** `game/battle.py` (L62 - L66)
* **Hatanın Sebebi:** Oyuncu envanteri açıp bir işlem yaptıktan sonra sırasını kaybetmeden turuna devam etmesi gerekiyordu.
* **Nasıl Çözdünüz:** Envanter işlemi tamamlandıktan sonra `player_turn()` tekrar çağrılarak oyuncunun turuna devam etmesi sağlandı.

---

### 10- Enemy_turn Metodunun Sonundaki Noktalama İşareti Eksiği
* **Dosya Adı ve Satır Aralığı:** `game/battle.py` (L100)
* **Hatanın Sebebi:** `enemy_turn()` metodunun satırında iki nokta üst üste (`:`) eksikti.
* **Nasıl Çözdünüz:** Metod sonuna `:` eklendi.

---

### 11- Düşman Constructor Parametreleri
* **Dosya Adı ve Satır Aralığı:** `game/enemy.py` (L4 - L12)
* **Hatanın Sebebi:** TODO'da nesne başlatıcı (constructor) içindeki eksik parametrelerin tamamlanması istenmişti.
* **Nasıl Çözdünüz:** Uygun parametrelerini alacak şekilde tamamlandı.

---

### 12- Felç Etkisi Altındaki Düşman Saldırısı ve Hasar Hesaplaması
* **Dosya Adı ve Satır Aralığı:** `game/enemy.py` (L14 - L19)
* **Hatanın Sebebi:** Düşman saldırısı her zaman `0` döndürüyordu ve felç etkisindeki düşman turunu atladıktan sonra `stunned` durumu sıfırlanmıyordu. Ayrıca TODO'da (-1 ile +3 aralığında) rastgele bir hasar değeri hesaplanıp ve döndürülmesi istenmişti.
* **Nasıl Çözdünüz:** Düşman felç etkisindeyse saldırı `0` olarak ayarlandı ve `stunned` `False` yapılarak normale dönmesi sağlandı. İkinci TODO boşluğunda ise -1,3 arasında rastgele bir hasar değeri hesaplayıp döndürüldü.

---

### 13- Düşman Ölüm Kontrolü
* **Dosya Adı ve Satır Aralığı:** `game/enemy.py` (L26 - L27)
* **Hatanın Sebebi:** `is_alive()` her durumda `True` döndürüyordu.
* **Nasıl Çözdünüz:** `is_alive()` metodu `current_hp > 0` kontrolü yapacak şekilde ayarlandı.

---

### 14- Gerekli Importların Yapılması
* **Dosya Adı ve Satır Aralığı:** `game/game.py` (L1 - L6)
* **Hatanın Sebebi:** Importlar eksikti.
* **Nasıl Çözdünüz:** Gerekli importlar eklendi.

---

### 15- Kaçılan Düşmanın HP Değerinin Fullenmesi
* **Dosya Adı ve Satır Aralığı:** `game/game.py` (L58 - L60)
* **Hatanın Sebebi:** Oyuncu düşmandan kaçınca düşmanın canı tamamen yenilenip max değerini alıyordu.
* **Nasıl Çözdünüz:** `enemy.current_hp = enemy.max_hp` satırı kaldırıldı.

---

### 16- Ana Giriş Noktasının Ayarlanması
* **Dosya Adı ve Satır Aralığı:** `main.py` (L1 - L6)
* **Hatanın Sebebi:** TODO'da oyun motorunu başlatacak olan ana giriş noktasının kurgulanması ve sistemi tetiklenmesi isteniyordu.
* **Nasıl Çözdünüz:** Game klasöründen Game sınıfı import edildi ve oyunu başlatmak için gerekli satırlar eklendi.

---

### 17- Hasar Çıktısı
* **Dosya Adı ve Satır Aralığı:** `game/character.py` (L32 - L43), `game/enemy.py` (L21 - L24)
* **Hatanın Sebebi:** Düşen can miktarı yanlış görünüyordu.
* **Nasıl Çözdünüz:** `self.current_hp = max(0, self.current_hp - damage)` ayarlanarak doğru bir şekilde düşen can miktarının gösterilmesi sağlandı.


---

### 18- Savunmanın Felçli Düşman Turunda Sıfırlanmaması
* **Dosya Adı ve Satır Aralığı:** `game/battle.py` (L100 - L104)
* **Hatanın Sebebi:** Düşman saldırısı `0` dönse bile `is_defending` durumu bir sonraki tura kalıyordu. Oysa oyun kurallarına göre savunma sadece o tur için geçerli olmalı.
* **Nasıl Çözdünüz:** Düşman saldırısı `0` dönse bile turun sonunda `self.player.is_defending = False` yapılarak savunma durumu sıfırlandı.

*(Not: Bu listeyi aşağıya doğru dilediğiniz kadar uzatabilirsiniz.)*

---

## 🌟 EKLENEN BONUS ÖZELLİKLER (İsteğe Bağlı)
*Oyundaki hataları başarıyla ayıkladıktan sonra projeye kendi yaratıcı kodlarınızı eklemekte özgürsünüz! Yaptığınız ekstra geliştirmeleri jüriye buradan tanıtabilirsiniz.*

**🎯 Ekstra Puan Getirebilecek Geliştirme Fikirleri (İlham Almanız İçin):**
- **Loot (Ganimet) Sistemi:** Öldürülen düşmanların üzerinden rastgele eşya (İksir, Güçlendirme) düşmesi.
- **Kritik Vuruş Şansı:** Karakterin saldırılarında %10 ihtimalle normalin 2 katı (Kritik) hasar çıkarması.
- **Özel Yetenekler (Skills):** Savaşta belli turlarda geri sayımı dolan (Cooldown) ateş topu vb. özel bir vuruş yeteneği.
- **Dükkan (Shop/Tüccar):** Yaratıklardan düşen altınlarla bölüm geçişlerinde envantere eşya alınabilen bir sistem.
- **Birim Testleri (Unit Tests):** Kodunuzun doğruluğunu kanıtlamak için `unittest` veya `pytest` kullanarak fonksiyonlara test yazılması (Profesyonel bir yazılımcı dokunuşu!).

### Bonus Özellik 1: Savaş Özeti Sistemi
* **Nasıl Çalışıyor:** Her savaşın sonunda sonuç , toplam tur sayısı , oyuncunun verdiği hasar , aldığı hasar ve savaşta kullandığı itemler ekrana özet olarak yazdırılır. Bu özellik için `Battle.__init__` içinde `damage_dealt`, `damage_taken` ve `items_used` değişkenleri eklendi. Savaş sırasında bu değişkenler güncellenerek savaş bittiğinde `show_battle_summary()` ile yazdırılır.
* **Dosya ve Konum Bilgisi:** 
    * **Mevcut Dosya ise:** `game/battle.py` (L5 - L12, L25 - L26, L50 - L56, L92 - L97, L105 - L113, L122 - L137)

---

> **💡 Yarışma İpucu:** 
> Kodun içinde her hata için bir `TODO` etiketi bulunmayabilir. Bazı mantık hatalarını bulmak için yukarıdaki **"Oyunun Sistem Mantığı"** bölümünü rehber edinmeli ve kodun bu kurallara uyup uymadığını bizzat test ederek (oyunu oynayarak) keşfetmelisiniz.
