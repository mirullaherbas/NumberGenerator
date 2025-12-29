# Kurulum ve Çalıştırma Kılavuzu

## Hızlı Başlangıç

### 1. Sistem Gereksinimleri

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Terminal/Command Prompt erişimi

### 2. Kurulum Adımları

```bash
# Adım 1: Proje dizinine gidin
cd NumberGenerator

# Adım 2: Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Veya manuel olarak:
pip install matplotlib==3.8.2 numpy==1.26.2
```

### 3. Programı Çalıştırma

```bash
python main.py
```

**Etkileşimli Kullanım:**
1. Program çalıştığında size anahtar uzunluğunu soracaktır (örn: 128, 256, 512)
2. Detaylı analiz isteyip istemediğinizi soracaktır (E/H)
3. Sonuçlar ekranda gösterilecek ve `output/` klasörüne kaydedilecektir

### 4. Test Çalıştırma

Algoritmanın doğru çalıştığını doğrulamak için:

```bash
python test_suite.py
```

Çıktı:
```
🔬 COLLATZ-AES GENERATOR - OTOMATİK TEST SÜİTİ
✅ TEST 1: Temel Anahtar Üretimi - BAŞARILI
✅ TEST 2: Entropi Kalitesi - BAŞARILI
✅ TEST 3: Farklı Uzunluklar - BAŞARILI
✅ TEST 4: Tekil Üretim - BAŞARILI
✅ TEST 5: Run Length Analizi - BAŞARILI
✅ TEST 6: Format Doğrulama - BAŞARILI
🎉 TÜM TESTLER BAŞARIYLA GEÇTİ!
```

## Örnek Kullanım

### Örnek 1: 256-bit Dengeli Anahtar Üretimi

```bash
$ python main.py

[?] Üretilecek anahtar uzunluğunu girin: 256
[?] Detaylı analiz raporu oluşturulsun mu? (E/H): E

🚀 ANAHTAR ÜRETME SÜRECİ BAŞLATILIYOR...

🔑 HEX ANAHTAR:
   A3F5C892 7D4E1B6A 93C2F058 E4B7D2A1
   5F8C3E19 B6A4D7F2 C1E93A58 7D2B4F6E

📊 DETAYLI İSTATİSTİKSEL ANALİZ
   Toplam Uzunluk : 256 bit
   0 Bitleri      : 128 (50.00%)
   1 Bitleri      : 128 (50.00%)
   ✓ Mükemmel Denge Sağlandı!
   
   Shannon Entropisi  : 1.000000 (Mükemmel)
   
✅ İŞLEM BAŞARIYLA TAMAMLANDI

📁 Çıktı Dosyaları:
   • output/comprehensive_analysis.png
   • output/bit_histogram.png
   • output/run_analysis.png
```

### Örnek 2: Programatik Kullanım

```python
from collatz_aes import CollatzAESGenerator

# Generator oluştur
gen = CollatzAESGenerator()

# 512-bit dengeli anahtar üret
result = gen.generate_balanced_key(512)

# Sonuçları kullan
print(f"Hex Anahtar: {result['hex']}")
print(f"Entropi: {result['stats']['entropy']:.6f}")
print(f"0/1 Dengesi: {result['stats']['0_count']}/{result['stats']['1_count']}")
```

## Çıktı Dosyaları

Program çalıştırıldıktan sonra `output/` klasöründe şu dosyalar oluşur:

1. **comprehensive_analysis.png** - Ana analiz raporu (8 farklı grafik)
2. **bit_histogram.png** - Detaylı histogram analizi
3. **run_analysis.png** - Run length frekans dağılımı

## Sorun Giderme

### Hata: ModuleNotFoundError: No module named 'matplotlib'

**Çözüm:**
```bash
pip install matplotlib numpy
```

### Hata: pip: command not found

**Çözüm:**
```bash
# macOS/Linux
python3 -m pip install matplotlib numpy

# Windows
python -m pip install matplotlib numpy
```

### Grafik gösterilmiyor

Grafik dosyaları `output/` klasöründe PNG formatında kaydedilir. Bir resim görüntüleyici ile açın:

```bash
# macOS
open output/comprehensive_analysis.png

# Linux
xdg-open output/comprehensive_analysis.png

# Windows
start output\comprehensive_analysis.png
```

## Performans İpuçları

- **128-bit anahtar**: ~0.005 saniye, test ve geliştirme için ideal
- **256-bit anahtar**: ~0.010 saniye, standart kullanım için önerilen
- **512-bit anahtar**: ~0.020 saniye, yüksek güvenlik gereksinimleri için
- **1024-bit anahtar**: ~0.040 saniye, maksimum güvenlik

## Sistem Gereksinimleri (Minimum)

- **CPU**: 1 GHz veya üzeri
- **RAM**: 512 MB (1 GB önerilen)
- **Disk**: 50 MB boş alan (kütüphaneler dahil)
- **OS**: Windows 7+, macOS 10.12+, Linux (herhangi bir modern dağıtım)

## Notlar

- İlk çalıştırmada matplotlib font önbelleği oluşturulacağı için 2-3 saniye gecikme yaşanabilir
- Çok büyük anahtar boyutları (>2048 bit) için bellek kullanımı artabilir
- Grafik oluşturma detaylı analizde ~0.5 saniye ek süre alır

## Destek

Sorun yaşıyorsanız:
1. Test suite'i çalıştırın (`python test_suite.py`)
2. Python sürümünü kontrol edin (`python --version` - 3.8+ olmalı)
3. Bağımlılıkları yeniden yükleyin (`pip install -r requirements.txt --upgrade`)

---

**Son Güncelleme**: 2024  
**Versiyon**: 2.0

