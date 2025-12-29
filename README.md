# 🔐 Collatz-AES Hibrit Anahtar Üreteci

**Bilgi Sistemleri Güvenliği Dersi - Özel Araştırma Projesi**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-High-red?style=for-the-badge)

Bu proje, matematikteki **Collatz Problemi'nin (3n+1)** kaotik doğasını ve modern kriptografinin **AES S-Box** (Substitüsyon) tekniklerini birleştirerek, **yüksek entropili** ve **istatistiksel olarak dengeli** rastgele anahtarlar üretir.

---

## 🌟 Öne Çıkan Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🧬 **Hibrit Yapı** | Kaotik matematik ve Kriptografik standartların (AES, SHA-256) birleşimi. |
| ⚖️ **Mükemmel Denge** | Üretilen her anahtarın **%50 '0'** ve **%50 '1'** içermesi garanti edilir. |
| 🎲 **Yüksek Entropi** | Shannon entropisi **> 0.99** ile tahmin edilemezlik sağlar. |
| 📊 **Görsel Analiz** | Üretim sonrası detaylı grafikler ve raporlar sunar. |
| 🛡️ **Güvenli Seed** | CSPRNG ve zamansal bileşenler kullanılarak güvenli başlangıç yapılır. |

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

Projenin çalışması için Python 3.8+ ve aşağıdaki kütüphaneler gereklidir:
- `matplotlib` (Grafik çizimi için)
- `numpy` (Sayısal işlemler için)

### 2. Kurulum

Terminal veya komut satırında şu komutları çalıştırın:

```bash
# Projeyi klonlayın (veya indirin)
git clone https://github.com/username/collatz-aes-generator.git

# Proje dizinine gidin
cd collatz-aes-generator

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

### 3. Çalıştırma

```bash
python main.py
```

Program çalıştığında sizden **anahtar uzunluğunu** (örn: 256, 512, 1024) girmenizi isteyecektir.

---

## 🧠 Algoritma Nasıl Çalışır?

Sistem, rastgeleliği artırmak için çok katmanlı bir mimari kullanır:

```mermaid
graph TD
    Start[🚀 Başlat] --> Seed[🔐 Güvenli Seed (CSPRNG + Time)]
    Seed --> Loop{Döngü}
    
    subgraph "Kaotik & Kriptografik Katmanlar"
        Loop --> Collatz[📉 Collatz Dönüşümü (3n+1 veya n/2)]
        Collatz --> SBox[📦 AES S-Box Karıştırma]
        SBox --> SHA[🔑 SHA-256 Hash & XOR]
    end
    
    SHA --> Extract[Bit Çıkarımı]
    Extract --> Check{Yeterli Bit?}
    Check -- Hayır --> Loop
    Check -- Evet --> Balance[⚖️ Dengeleme Algoritması]
    
    Balance --> Analyze[📈 İstatistiksel Analiz]
    Analyze --> Report[📄 Raporlama & Görseller]
```

---

## 📊 Görsel Analiz ve Çıktılar

Algoritma, üretilen anahtarın kalitesini kanıtlamak için `output/` klasörüne detaylı grafikler kaydeder. İşte örnek bir analiz raporu:

### 1. Kapsamlı Analiz Raporu
Denge, entropi, otokorelasyon ve run testlerini tek bir görselde özetler.
> **Dosya:** `output/comprehensive_analysis.png`

![Kapsamlı Analiz](output/comprehensive_analysis.png)

---

### 2. Bit Dağılımı (Histogram)
0 ve 1 bitlerinin dağılımını gösterir. İdeal bir anahtarda bu çubuklar eşit olmalıdır.
> **Dosya:** `output/bit_histogram.png`

![Bit Histogramı](output/bit_histogram.png)

---

### 3. Run Length (Ardışıklık) Analizi
Ardışık gelen aynı bitlerin (örneğin arka arkaya gelen '1'ler) uzunluk frekansını gösterir. Kriptografik olarak güvenli bir dağılım, üstel olarak azalan bir eğri izlemelidir.
> **Dosya:** `output/run_analysis.png`

![Run Analizi](output/run_analysis.png)

---

## 📁 Dosya Yapısı

- `main.py`: 🖥️ Programın ana giriş noktası ve kullanıcı arayüzü.
- `collatz_aes.py`: ⚙️ Anahtar üretim algoritmasının çekirdek kodları.
- `analysis.py`: 📈 İstatistiksel analiz ve grafik çizim modülü.
- `ALGORITHM.md`: 📝 Algoritmanın detaylı teknik dokümantasyonu.
- `output/`: 📂 Oluşturulan anahtar analiz görsellerinin kaydedildiği klasör.

---

## ⚠️ Lisans ve Sorumluluk Reddi

Bu proje **eğitim ve araştırma amaçlı** geliştirilmiştir. Gerçek dünyadaki yüksek güvenlik gerektiren kriptografik sistemlerde (bankacılık vb.) sertifikalı standart kütüphanelerin kullanılması önerilir.

---
**Geliştirici:** Mirullah Erbaş
**Ders:** Bilgi Sistemleri Güvenliği
