Sen Kıdemli bir Kriptografi Mühendisi ve Python Uzmanısın. Üniversite düzeyinde "Bilgi Sistemleri Güvenliği" dersi için, hocanın özel isteklerine göre modifiye edilmiş, özgün bir "Collatz-AES Hibrit Anahtar Üreteci" projesi yazmanı istiyorum.

Projenin temel amacı: Collatz (3n+1) algoritmasının kaotik yapısını, AES şifrelemesinin S-Box (Substitution Box) yapısı ile birleştirerek güvenli ve *dengeli* anahtarlar üretmektir.

Lütfen aşağıdaki dosya yapısını ve teknik kuralları birebir uygula:

### 1. `collatz_aes.py` (Ana Modül)
Bu dosyada `CollatzAESGenerator` sınıfı olmalı:
- **Algoritma Mantığı:**
  1. Başlangıç (Seed) olarak `secrets` modülünü kullan.
  2. **Collatz Adımı:** Sayı çiftse `n/2`, tekse `3n+1` uygula.
  3. **AES Karıştırma (Kritik):** Her adımdan sonra, oluşan sayının son 8 bitini alıp, Rijndael (AES) S-Box tablosundan geçirerek sayıyı modifiye et. Bu, hocanın "AES ekleme" isteğini karşılayacak ve Collatz'ın lineerliğini bozacak.
  4. **Döngü Kırıcı:** Eğer sayı 1, 2 veya 4 (klasik döngü) olursa, XOR işlemi ile rastgele bir entropi ekleyerek döngüden çıkar.
- **`generate_balanced_key(length)` Metodu (Çok Önemli):**
  - Belirtilen uzunlukta (örn: 256 bit) bir anahtar üretmeli.
  - **ZORUNLU KURAL:** Üretilen anahtardaki **0'ların sayısı ile 1'lerin sayısı birbirine TAM OLARAK EŞİT OLMALIDIR.** (Örn: 128 tane '1', 128 tane '0').
  - Bunu sağlamak için üretimden sonra bir dengeleme (balancing) algoritması çalıştır. Fazla olan bitleri rastgele seçip tersine çevir.
  - Çıktı olarak hem Binary string, hem Hex string hem de 0/1 sayılarını içeren bir sözlük (dict) döndür.

### 2. `analysis.py` (Kanıt ve Görselleştirme)
Bu dosya hocaya projenin çalıştığını kanıtlamak içindir:
- `matplotlib` kullanarak bir **Pasta Grafiği (Pie Chart)** çizdir.
- Bu grafik, üretilen anahtardaki 0 ve 1 oranının tam %50-%50 olduğunu görsel olarak kanıtlamalıdır.
- Grafiği `output/` klasörüne kaydetmeli.

### 3. `main.py` (Çalıştırıcı)
- Kullanıcıdan bit uzunluğunu (örn: 128, 256) isteyen şık bir CLI arayüzü hazırla.
- Algoritmayı çalıştır, Hex anahtarı ve Binary halini ekrana renkli ve düzenli yazdır.
- "0 Sayısı" ve "1 Sayısı" istatistiklerini göstererek eşitliği vurgula.
- Analiz grafiğini oluştur.

### 4. `README.md` (Dokümantasyon ve Akış Diyagramı)
- Projenin amacını ve kurulumunu anlatan profesyonel bir Markdown dosyası.
- **Akış Diyagramı:** Algoritmanın çalışma mantığını (Seed -> Collatz -> AES S-Box -> Denge Kontrolü -> Çıktı) gösteren **Mermaid** formatında detaylı bir grafik kodu ekle.

**Teknik Gereksinimler:**
- Kodlar PEP8 standartlarına uygun ve modüler olmalı.
- Her fonksiyonun ne işe yaradığını anlatan detaylı Docstring'ler ve yorum satırları ekle (Hoca inceleyecek).
- Kod bloklarını tek parça halinde veya dosya dosya net bir şekilde ver.