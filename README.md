# Collatz-AES Hibrit Anahtar Üreteci

**Bilgi Sistemleri Güvenliği Dersi - Özel Araştırma Projesi**

Bu proje, kaotik matematik (Collatz Problemi) ve modern kriptografik teknikleri (AES S-Box) birleştirerek yüksek güvenlikli ve istatistiksel olarak dengeli rastgele anahtarlar üretir.

![License](https://img.shields.io/badge/License-Educational-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

---

## Proje Amacı

Standart rastgele sayı üreteçlerinin ötesine geçerek, kaotik dinamikler ve doğrusal olmayan dönüşümlerle tahmin edilmesi zor anahtarlar üretmek. Sistem, üretilen her anahtarın %50 sıfır ve %50 bir içermesini garanti eder (Mükemmel Denge).

## Özellikler

- **Hibrit Yapı:** Collatz kaosu ve AES S-Box/Inverse S-Box karıştırması.
- **Tam Denge:** Üretilen anahtarlarda 0 ve 1 sayısı her zaman eşittir.
- **Yüksek Entropi:** Shannon entropisi > 0.99.
- **Görsel Analiz:** Detaylı histogramlar, run testleri ve denge grafikleri.
- **Güvenli Başlangıç:** Python `secrets` modülü ile CSPRNG tabanlı seed.

## Algoritma Akış Şeması

Aşağıdaki şema, anahtar üretim sürecinin mantıksal akışını göstermektedir:

```mermaid
graph TD
    Start[Baslat] --> Init[Guvenli Seed Uretimi]
    Init --> CheckLoop{Bit Sayisi Yeterli mi?}
    
    CheckLoop -- Hayir --> LoopCheck{Dongu Kontrolu}
    LoopCheck -- Evet --> Entropy[Entropi Ekle]
    LoopCheck -- Hayir --> Collatz[Collatz Adimi: 3n+1 veya n/2]
    
    Entropy --> Collatz
    Collatz --> SBox[AES S-Box Karistirma]
    SBox --> SHA[SHA-256 Hash Karistirma]
    SHA --> Extract[Bit Cikarimi]
    Extract --> Store[Listeye Ekle]
    Store --> CheckLoop
    
    CheckLoop -- Evet --> Balance[Dengeleme Algoritmasi]
    Balance --> Analyze[Istatistiksel Analiz]
    Analyze --> Visuals[Gorsellestirme]
    Visuals --> End[Bitis]
```

## Kurulum ve Kullanım

### Gereksinimler

- Python 3.8+
- matplotlib, numpy

### Kurulum

```bash
git clone https://github.com/username/collatz-aes-generator.git
cd collatz-aes-generator
pip install -r requirements.txt
```

### Çalıştırma

```bash
python main.py
```

Program çalıştığında anahtar uzunluğunu (örn. 256) girin. Sonuçlar terminalde ve `output/` klasöründe görüntülenecektir.

## Analiz ve Görseller

Algoritma, üretilen anahtarların kalitesini kanıtlamak için çeşitli grafikler oluşturur.

### 1. Kapsamlı Analiz Raporu
Denge, entropi, otokorelasyon ve run testlerini içeren genel bakış:

![Kapsamlı Analiz](output/comprehensive_analysis.png)

### 2. Bit Dağılımı ve Histogram
Bitlerin uniform dağılımını gösteren grafikler:

![Bit Histogramı](output/bit_histogram.png)

### 3. Run Length Analizi
Ardışık gelen bitlerin (000, 111 gibi) frekans analizi:

![Run Analizi](output/run_analysis.png)

## Dosya Yapısı

- `collatz_aes.py`: Ana algoritma ve sınıf yapısı.
- `analysis.py`: Grafik oluşturma ve istatistiksel test modülü.
- `main.py`: Kullanıcı arayüzü ve çalıştırıcı.
- `output/`: Oluşturulan grafiklerin kaydedildiği klasör.

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Akademik kullanımlarda kaynak gösteriniz.
