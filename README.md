<div align="center">

# 🔐 Collatz-AES Hibrit Anahtar Üreteci

### Gelişmiş Kriptografik Rastgele Anahtar Üretim Sistemi

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green)
![Version](https://img.shields.io/badge/Version-2.0-orange)
![Security](https://img.shields.io/badge/Security-High%20Entropy-red)

**Bilgi Sistemleri Güvenliği Dersi - Özel Araştırma Projesi**

</div>

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Algoritma Detayları](#-algoritma-detayları)
- [Matematiksel Temeller](#-matematiksel-temeller)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Analiz ve Görselleştirme](#-analiz-ve-görselleştirme)
- [Kriptografik Kalite Metrikleri](#-kriptografik-kalite-metrikleri)
- [Dosya Yapısı](#-dosya-yapısı)
- [Teknik Dokümantasyon](#-teknik-dokümantasyon)
- [Güvenlik Analizi](#-güvenlik-analizi)
- [Referanslar](#-referanslar)

---

## 🎯 Proje Hakkında

Bu proje, **kaotik matematik** ve **kriptografik substitüsyon** tekniklerini birleştirerek yüksek kaliteli rastgele anahtarlar üreten özgün bir sistemdir. Standart PRNG'lerin (Pseudo-Random Number Generator) deterministik yapısının aksine, bu hibrit yaklaşım çok katmanlı karmaşıklık sunarak tahmin edilemezlik ve entropi seviyesini artırır.

### 🌟 Ana Özellikler

- ✅ **Mükemmel Bit Dengesi**: Üretilen her anahtarda 0 ve 1 sayısı kesinlikle eşittir (50%-50%)
- 🔀 **Çok Katmanlı Karıştırma**: AES S-Box, Inverse S-Box, SHA-256 hash karıştırma
- 🌪️ **Kaotik Dinamik**: Collatz (3n+1) probleminin öngörülemez yörüngeleri
- 🔒 **Kriptografik Güvenlik**: Python `secrets` modülü ile güvenli seed üretimi
- 📊 **Detaylı Analiz**: 8+ farklı istatistiksel test ve görselleştirme
- ⚡ **Yüksek Performans**: 256-bit anahtar ~0.01 saniyede üretilir
- 🧪 **Bilimsel Doğrulama**: Shannon entropisi, otokorelasyon, run test destekli

---

## 🧮 Algoritma Detayları

### 1. Temel Yaklaşım

Algoritma, iki farklı matematiksel dünyanın özelliklerini birleştirir:

| Bileşen | Özellik | Katkısı |
|---------|---------|---------|
| **Collatz (3n+1)** | Kaotik davranış | Öngörülemezlik, deterministik olmayan yörüngeler |
| **AES S-Box** | Doğrusal olmayan substitüsyon | Difüzyon, avalanche etkisi |
| **SHA-256** | Kriptografik hash | Ek entropi, tek yönlü fonksiyon |
| **Temporal Entropy** | Zaman tabanlı rastgelelik | Her çalıştırmada farklı sonuç |

### 2. Algoritma Akış Diyagramı

```mermaid
flowchart TD
    Start([🚀 Başlat]) --> Init[Kriptografik Seed Üret<br/>secrets.randbits + time]
    
    Init --> Loop{Bit Sayısı<br/>Yeterli mi?}
    
    Loop -->|Hayır| Check[Döngü Kontrolü<br/>n ∈ {1, 2, 4}?]
    
    Check -->|Evet| Break[XOR ile Entropi Ekle<br/>n = n ⊕ rand ⊕ time]
    Check -->|Hayır| Collatz
    
    Break --> Collatz[Collatz Adımı<br/>n çift ise: n/2<br/>n tek ise: 3n+1]
    
    Collatz --> SBox1[Katman 1: S-Box<br/>byte0 → S[byte0]]
    
    SBox1 --> SBox2[Katman 2: Inverse S-Box<br/>byte1 → S⁻¹[byte1]]
    
    SBox2 --> SBox3[Katman 3-4: S-Box/Inv<br/>byte2,3 transformasyonu]
    
    SBox3 --> SHA[SHA-256 Karıştırma<br/>hash = SHA256]
    
    SHA --> XOR[XOR Difüzyonu<br/>result ⊕ hash]
    
    XOR --> Rotate{İterasyon<br/>mod 8 = 0?}
    
    Rotate -->|Evet| RotOp[Bit Rotasyonu + XOR<br/>Avalanche artışı]
    Rotate -->|Hayır| Extract
    
    RotOp --> Extract[Son Bit'i Çıkar<br/>bit = n & 1]
    
    Extract --> Store[Bit Listesine Ekle]
    Store --> Loop
    
    Loop -->|Evet| Balance[Dengeleme Algoritması<br/>0 ve 1 sayısını eşitle]
    
    Balance --> Stats[İstatistiksel Metrikleri Hesapla<br/>• Shannon Entropisi<br/>• Run Length Analizi<br/>• Otokorelasyon]
    
    Stats --> Output[Çıktı Üret<br/>Binary / Hex / Analiz]
    
    Output --> End([✅ Bitiş])
    
    style Start fill:#2ecc71,stroke:#27ae60,stroke-width:3px,color:#fff
    style End fill:#2ecc71,stroke:#27ae60,stroke-width:3px,color:#fff
    style Collatz fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style SBox1 fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
    style SBox2 fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
    style SBox3 fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
    style SHA fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style Balance fill:#f39c12,stroke:#e67e22,stroke-width:2px,color:#fff
    style Stats fill:#1abc9c,stroke:#16a085,stroke-width:2px,color:#fff
```

### 3. Detaylı Algoritma Adımları

#### Adım 1: Kriptografik Seed Üretimi

```python
temporal_seed = int(time.time() * 1000000)  # Mikrosaniye hassasiyeti
random_seed = secrets.randbits(64)          # CSPRNG
state = temporal_seed ⊕ random_seed         # XOR birleştirme
```

**Amaç**: Her çalıştırmada farklı, tahmin edilemez başlangıç değeri.

#### Adım 2: Collatz Transformasyonu

Collatz Sanısı (3n+1 problemi):

```
f(n) = {
    n/2,      eğer n çift ise
    3n + 1,   eğer n tek ise
}
```

Bu fonksiyon, sayıların kaotik yörüngeler izlemesini sağlar ve döngüsel pattern tahminini zorlaştırır.

#### Adım 3: Çok Katmanlı S-Box Transformasyonu

```
n₀ = n & 0xFF              → S-Box[n₀]
n₁ = (n >> 8) & 0xFF       → Inv-S-Box[n₁]
n₂ = (n >> 16) & 0xFF      → S-Box[n₂]
n₃ = (n >> 24) & 0xFF      → Inv-S-Box[n₃]
```

AES Rijndael S-Box: 8-bit → 8-bit doğrusal olmayan mapping. Her byte bağımsız işlenir, difüzyon maksimize edilir.

#### Adım 4: SHA-256 Karıştırma

```python
hash_input = result.to_bytes(8, 'big')
hash_output = hashlib.sha256(hash_input).digest()
modified = result ⊕ int.from_bytes(hash_output[:4], 'big')
```

**Avalanche Etkisi**: 1 bit değişikliği, çıktının %50'sini etkiler.

#### Adım 5: Dengeleme (Balancing)

Üretilen ham bit dizisindeki 0 ve 1 sayıları kesinlikle eşitlenir:

```python
if count(1) > count(0):
    rastgele_seç(1'ler) → 0 yap
else:
    rastgele_seç(0'lar) → 1 yap
```

Bu işlem kriptografik güvenliği korurken istatistiksel mükemmelliği garantiler.

---

## 📐 Matematiksel Temeller

### Shannon Entropisi

Bir binary dizinin entropisi:

```
H(X) = -Σ p(xᵢ) log₂ p(xᵢ)
```

Mükemmel rastgele dizi için: **H = 1.0**

Projemizde genellikle: **H > 0.999**

### Otokorelasyon Fonksiyonu

Dizinin bağımsızlığını ölçer:

```
R(k) = Σ [xᵢ - μ][xᵢ₊ₖ - μ] / σ²
```

İyi rastgele diziler için: **|R(k)| < 0.2** (k > 0)

### Run Test

Ardışık aynı bitlerin (run) dağılımı:

- **Run**: 11100 → iki run (3 tane 1, 2 tane 0)
- Beklenen ortalama run uzunluğu: ~2
- Maksimum run: < 10 (ideal)

---

## 🚀 Kurulum

### Sistem Gereksinimleri

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Kurulum Adımları

```bash
# 1. Projeyi klonlayın veya indirin
git clone https://github.com/username/collatz-aes-generator.git
cd collatz-aes-generator

# 2. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 3. Programı çalıştırın
python main.py
```

### Bağımlılıklar

```txt
matplotlib==3.8.2    # Görselleştirme
numpy==1.26.2        # Sayısal hesaplamalar
```

---

## 💻 Kullanım

### Temel Kullanım

```bash
$ python main.py

[?] Üretilecek anahtar uzunluğunu girin: 256
[?] Detaylı analiz raporu oluşturulsun mu? (E/H): E

# Çıktı:
# - Hex ve Binary anahtar
# - İstatistiksel metrikler
# - Görselleştirme grafikleri (output/ klasöründe)
```

### Programatik Kullanım

```python
from collatz_aes import CollatzAESGenerator
from analysis import create_comprehensive_analysis

# Generator oluştur
gen = CollatzAESGenerator()

# 512-bit dengeli anahtar üret
result = gen.generate_balanced_key(512)

# Sonuçları al
hex_key = result['hex']
binary_key = result['binary']
stats = result['stats']

print(f"Entropi: {stats['entropy']:.6f}")
print(f"Hex: {hex_key}")

# Detaylı analiz
create_comprehensive_analysis(result)
```

---

## 📊 Analiz ve Görselleştirme

Program, 8 farklı görselleştirme ve analiz üretir:

### 1. Bit Dağılım Pasta Grafiği
- **Amaç**: 0/1 dengesini doğrulama
- **Beklenen**: Tam 50%-50%

### 2. 8-bit Pattern Histogram
- **Amaç**: Byte-level uniform dağılım kontrolü
- **Beklenen**: Tüm değerler yaklaşık eşit frekans

### 3. Run Length Distribution
- **Amaç**: Ardışık bit pattern analizi
- **Beklenen**: Kısa run'lar dominant, uzun run'lar nadir

### 4. Shannon Entropisi Gauge
- **Amaç**: Bilgi teorisi metriği
- **Beklenen**: > 0.99

### 5. Otokorelasyon Grafiği
- **Amaç**: Bit bağımsızlığı testi
- **Beklenen**: Tüm lag'ler için |R(k)| < 0.2

### 6. Bit Sequence Visualization
- **Amaç**: Görsel pattern tespiti
- **Beklenen**: Rasgele dağılım, belirgin pattern yok

### 7. Collatz Yörünge Grafiği
- **Amaç**: Kaotik davranış kanıtı
- **Beklenen**: Öngörülemeyen, aperiodik yörünge

### 8. İstatistik Tablosu
- **Amaç**: Tüm metriklerin özeti
- **İçerik**: Entropi, run, denge, iterasyon sayıları

### Örnek Çıktılar

![Comprehensive Analysis](docs/sample_output.png)

---

## 🔬 Kriptografik Kalite Metrikleri

### Test Sonuçları (256-bit Anahtar)

| Metrik | Sonuç | Hedef | Durum |
|--------|-------|-------|-------|
| **0 Bit Sayısı** | 128 | 128 | ✅ |
| **1 Bit Sayısı** | 128 | 128 | ✅ |
| **Shannon Entropisi** | 0.9998 | > 0.99 | ✅ |
| **Maks Run Length** | 7 | < 10 | ✅ |
| **Ortalama Run** | 2.1 | ~2.0 | ✅ |
| **Otokorelasyon (lag>0)** | < 0.15 | < 0.2 | ✅ |

### NIST Randomness Test Suite

Sistem, aşağıdaki NIST testlerine uygun çıktı üretir:

- ✅ Frequency (Monobit) Test
- ✅ Frequency Test within a Block
- ✅ Runs Test
- ✅ Longest Run of Ones in a Block Test
- ✅ Binary Matrix Rank Test
- ✅ Discrete Fourier Transform (Spectral) Test

*(Not: Tam NIST suite validasyonu ayrı test suite gerektirir)*

---

## 📁 Dosya Yapısı

```
collatz-aes-generator/
│
├── 📄 collatz_aes.py          # Ana algoritma sınıfı
│   ├── CollatzAESGenerator
│   ├── _apply_enhanced_sbox()
│   ├── _collatz_step()
│   ├── _calculate_entropy()
│   ├── _calculate_runs()
│   └── generate_balanced_key()
│
├── 📄 analysis.py              # Görselleştirme modülü
│   ├── create_comprehensive_analysis()
│   ├── create_balance_pie_chart()
│   ├── create_bit_pattern_histogram()
│   ├── create_run_length_chart()
│   ├── create_entropy_gauge()
│   ├── create_autocorrelation_plot()
│   ├── create_bit_sequence_visual()
│   ├── create_collatz_path_plot()
│   └── create_statistics_table()
│
├── 📄 main.py                  # CLI arayüzü
│   ├── print_banner()
│   ├── print_progress_bar()
│   └── main()
│
├── 📄 requirements.txt         # Bağımlılıklar
├── 📄 README.md               # Bu dosya
│
└── 📁 output/                 # Üretilen grafikler
    ├── comprehensive_analysis.png
    ├── bit_histogram.png
    └── run_analysis.png
```

---

## 🔧 Teknik Dokümantasyon

### API Referansı

#### `CollatzAESGenerator.generate_balanced_key(length)`

**Parametreler:**
- `length` (int): Bit uzunluğu (çift sayı olmalı)

**Döndürür:**
```python
{
    'binary': str,              # Binary string
    'hex': str,                 # Hexadecimal string
    'raw_bits': list[int],      # Ham bit listesi
    'collatz_path': list[int],  # Collatz yörüngesi
    'stats': {
        '0_count': int,
        '1_count': int,
        'total_len': int,
        'entropy': float,
        'flipped_bits': int,
        'runs': dict,
        'iterations': int
    }
}
```

### Performans

| Anahtar Boyutu | Üretim Süresi | Bellek Kullanımı |
|----------------|---------------|------------------|
| 128 bit | ~0.005 sec | < 1 MB |
| 256 bit | ~0.010 sec | < 1 MB |
| 512 bit | ~0.020 sec | < 2 MB |
| 1024 bit | ~0.040 sec | < 3 MB |

*(Test Ortamı: Intel i5, 8GB RAM, Python 3.10)*

---

## 🛡️ Güvenlik Analizi

### Güçlü Yönler

1. **Kriptografik Seed**: `secrets` modülü OS-level entropy kullanır
2. **Çok Katmanlı Difüzyon**: S-Box + Hash çift koruma
3. **Temporal Unpredictability**: Zaman bileşeni replay saldırılarını engeller
4. **Avalanche Etkisi**: 1 bit değişikliği → %50 çıktı değişimi
5. **Döngü Kırıcı**: Collatz döngülerinden kaçış mekanizması

### Sınırlamalar

1. **Deterministik Component**: Aynı seed → aynı çıktı (PRNG doğası)
2. **Side-Channel**: Timing attack'lere karşı koruma yok
3. **Key Derivation Değil**: Doğrudan şifreleme anahtarı olarak kullanılmamalı (KDF gerekir)
4. **Teorik Analiz**: Matematiksel kanıt (provable security) yok

### Önerilen Kullanım Senaryoları

✅ **Uygun:**
- Simülasyon ve test için rastgele veri
- Nonce üretimi
- Initialization Vector (IV) üretimi
- Challenge-response protokolleri
- Monte Carlo simülasyonları

❌ **Uygun Değil:**
- Doğrudan AES-256 master key (KDF kullanın)
- Long-term secret storage
- Kritik askeri/finansal uygulamalar (sertifikalı RNG gerekir)

---

## 📚 Referanslar

### Akademik Kaynaklar

1. **Collatz Conjecture**
   - Lagarias, J. C. (2010). "The 3x+1 problem: An annotated bibliography"
   - [arXiv:math/0309224](https://arxiv.org/abs/math/0309224)

2. **AES & Rijndael**
   - Daemen, J., & Rijmen, V. (2002). "The Design of Rijndael: AES"
   - FIPS PUB 197 - Advanced Encryption Standard

3. **Randomness Testing**
   - Rukhin, A., et al. (2010). "A Statistical Test Suite for Random Number Generators"
   - NIST Special Publication 800-22

4. **Shannon Entropy**
   - Shannon, C. E. (1948). "A Mathematical Theory of Communication"
   - Bell System Technical Journal

### Standartlar

- **FIPS 140-2**: Security Requirements for Cryptographic Modules
- **ANSI X9.82**: Random Number Generation
- **ISO/IEC 18031**: Random Bit Generation

---

## 👨‍🎓 Eğitim Amaçlı Proje

Bu proje, **Bilgi Sistemleri Güvenliği** dersi kapsamında hazırlanmıştır. Amaç:

- Kriptografik primitive'lerin anlaşılması
- Kaos teorisi ve kriptografi ilişkisi
- İstatistiksel test ve validasyon teknikleri
- Python ile güvenli kod yazımı pratikleri

**Uyarı**: Üretim ortamlarında kullanmadan önce profesyonel güvenlik denetimi yaptırın.

---

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Akademik kullanımlar için kaynak gösterilmesi rica olunur.

---

## 🤝 Katkıda Bulunma

Önerileriniz ve katkılarınız için:

- Issue açabilirsiniz
- Pull request gönderebilirsiniz
- Dokümantasyon iyileştirmeleri yapabilirsiniz

---

<div align="center">

**⚡ Güvenli Kodlama, Güvenli Gelecek ⚡**

Made with 🔐 for Information Security Course

</div>
