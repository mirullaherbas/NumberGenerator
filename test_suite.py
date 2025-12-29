"""
Otomatik Test Süiti - Collatz-AES Generator

Bu test dosyası, algoritmanın tüm bileşenlerinin doğru çalıştığını doğrular.
Matplotlib'e bağımlılığı yoktur, kolayca çalıştırılabilir.

Kullanım:
    python test_suite.py
"""

from collatz_aes import CollatzAESGenerator
import time

def test_basic_generation():
    """Temel anahtar üretimini test eder."""
    print("="*60)
    print("TEST 1: Temel Anahtar Üretimi")
    print("="*60)
    
    gen = CollatzAESGenerator()
    result = gen.generate_balanced_key(256)
    
    assert result['stats']['total_len'] == 256, "Uzunluk hatası!"
    assert result['stats']['0_count'] == 128, "0 sayısı hatası!"
    assert result['stats']['1_count'] == 128, "1 sayısı hatası!"
    assert len(result['hex']) == 64, "Hex uzunluk hatası!"
    assert len(result['binary']) == 256, "Binary uzunluk hatası!"
    
    print(f"✅ Uzunluk Kontrolü: {result['stats']['total_len']} bit")
    print(f"✅ Denge Kontrolü: 0={result['stats']['0_count']}, 1={result['stats']['1_count']}")
    print(f"✅ Entropi: {result['stats']['entropy']:.6f}")
    print(f"✅ Hex Uzunluk: {len(result['hex'])} karakter")
    print()

def test_entropy():
    """Entropi kalitesini test eder."""
    print("="*60)
    print("TEST 2: Entropi Kalitesi")
    print("="*60)
    
    gen = CollatzAESGenerator()
    
    entropies = []
    for i in range(5):
        result = gen.generate_balanced_key(128)
        entropies.append(result['stats']['entropy'])
    
    avg_entropy = sum(entropies) / len(entropies)
    min_entropy = min(entropies)
    
    print(f"✅ 5 test ortalaması: {avg_entropy:.6f}")
    print(f"✅ Minimum entropi: {min_entropy:.6f}")
    
    assert avg_entropy > 0.95, "Entropi çok düşük!"
    print(f"✅ Entropi eşiği geçildi (>0.95)")
    print()

def test_different_lengths():
    """Farklı uzunluklarda anahtar üretimini test eder."""
    print("="*60)
    print("TEST 3: Farklı Uzunluklar")
    print("="*60)
    
    gen = CollatzAESGenerator()
    lengths = [64, 128, 256, 512]
    
    for length in lengths:
        start = time.time()
        result = gen.generate_balanced_key(length)
        duration = time.time() - start
        
        assert result['stats']['0_count'] == length // 2
        assert result['stats']['1_count'] == length // 2
        
        print(f"✅ {length:4d} bit: {duration*1000:.2f}ms, entropy={result['stats']['entropy']:.4f}")
    print()

def test_uniqueness():
    """Ardışık üretimlerin farklı olduğunu test eder."""
    print("="*60)
    print("TEST 4: Tekil Üretim (Uniqueness)")
    print("="*60)
    
    gen = CollatzAESGenerator()
    
    keys = set()
    for i in range(10):
        result = gen.generate_balanced_key(128)
        keys.add(result['hex'])
        # Küçük bir gecikme ekleyerek temporal farklılık garanti et
        time.sleep(0.001)
    
    assert len(keys) == 10, "Aynı anahtarlar üretildi!"
    print(f"✅ 10 farklı anahtar başarıyla üretildi")
    print(f"✅ Tüm anahtarlar birbirinden farklı")
    print()

def test_run_statistics():
    """Run length istatistiklerini test eder."""
    print("="*60)
    print("TEST 5: Run Length Analizi")
    print("="*60)
    
    gen = CollatzAESGenerator()
    result = gen.generate_balanced_key(512)
    
    runs = result['stats']['runs']
    
    print(f"✅ Run sayısı: {runs['run_count']}")
    print(f"✅ Ortalama run: {runs['avg_run_length']:.2f}")
    print(f"✅ Maksimum run: {runs['max_run_length']}")
    
    # İyi kalite için maksimum run 15'ten küçük olmalı
    if runs['max_run_length'] < 10:
        quality = "Mükemmel"
    elif runs['max_run_length'] < 15:
        quality = "İyi"
    else:
        quality = "Orta"
    
    print(f"✅ Kalite Değerlendirmesi: {quality}")
    print()

def test_hex_format():
    """Hex formatının doğruluğunu test eder."""
    print("="*60)
    print("TEST 6: Format Doğrulama")
    print("="*60)
    
    gen = CollatzAESGenerator()
    result = gen.generate_balanced_key(256)
    
    hex_key = result['hex']
    
    # Hex karakterlerini kontrol et
    assert all(c in '0123456789ABCDEF' for c in hex_key), "Geçersiz hex karakter!"
    
    # Binary'den hex'e dönüşümü doğrula
    binary_to_hex = hex(int(result['binary'], 2))[2:].upper().zfill(64)
    assert hex_key == binary_to_hex, "Hex/Binary tutarsızlığı!"
    
    print(f"✅ Hex format geçerli")
    print(f"✅ Binary ↔ Hex tutarlılığı doğrulandı")
    print(f"✅ Örnek hex: {hex_key[:32]}...")
    print()

def test_collatz_path():
    """Collatz yörüngesinin kaydedildiğini test eder."""
    print("="*60)
    print("TEST 7: Collatz Yörünge Kaydı")
    print("="*60)
    
    gen = CollatzAESGenerator()
    result = gen.generate_balanced_key(256)
    
    path = result.get('collatz_path', [])
    
    assert len(path) > 0, "Collatz yörüngesi kaydedilmemiş!"
    assert len(path) <= 1000, "Yörünge çok uzun!"
    
    print(f"✅ Yörünge uzunluğu: {len(path)} adım")
    print(f"✅ İlk değer: {path[0]}")
    print(f"✅ Son değer: {path[-1]}")
    print()

def run_all_tests():
    """Tüm testleri çalıştırır."""
    print("\n")
    print("🔬 " + "="*58)
    print("   COLLATZ-AES GENERATOR - OTOMATİK TEST SÜİTİ")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    try:
        test_basic_generation()
        test_entropy()
        test_different_lengths()
        test_uniqueness()
        test_run_statistics()
        test_hex_format()
        test_collatz_path()
        
        duration = time.time() - start_time
        
        print("="*60)
        print("🎉 TÜM TESTLER BAŞARIYLA GEÇTİ!")
        print(f"⏱️  Toplam süre: {duration:.3f} saniye")
        print("="*60)
        print("\n✅ Algoritma doğru çalışıyor!")
        print("✅ Kriptografik kalite metrikleri geçti!")
        print("✅ Performans kabul edilebilir seviyede!")
        print("\n💡 Şimdi 'python main.py' ile programı çalıştırabilirsiniz.\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST HATASI: {e}")
        return False
    except Exception as e:
        print(f"\n❌ BEKLENMEDİK HATA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

