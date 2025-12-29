import secrets
import time
import hashlib

class CollatzAESGenerator:
    """
    Gelişmiş Collatz-AES Hibrit Anahtar Üreteci.
    
    Bu sınıf, Collatz (3n+1) probleminin kaotik doğasını ve AES (Rijndael) şifrelemesinin
    doğrusal olmayan S-Box yapısını birleştirerek kriptografik olarak güçlü ve 
    dengeli (eşit sayıda 0 ve 1 içeren) rastgele anahtarlar üretir.
    
    Gelişmiş Özellikler:
    - Çift katmanlı S-Box transformasyonu
    - Avalanche etkisi (küçük değişiklikler büyük farklılıklar yaratır)
    - Temporal entropi enjeksiyonu
    - SHA-256 karıştırma katmanı
    - İstatistiksel kalite metrikleri
    """

    # Rijndael (AES) S-Box Table (Substitution Box)
    # 8-bitlik bir değeri doğrusal olmayan başka bir 8-bitlik değere dönüştürür.
    S_BOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]
    
    # Inverse S-Box (Ters S-Box) - Ek karıştırma için
    INV_S_BOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]

    def __init__(self):
        """Generator sınıfını başlatır ve istatistik kayıtlarını oluşturur."""
        self.state = 0
        self.iteration_count = 0
        self.collatz_path = []  # Collatz yörüngesi kaydı (analiz için)

    def _apply_enhanced_sbox(self, number):
        """
        Gelişmiş çok katmanlı S-Box transformasyonu uygular.
        Her 4 byte'ı farklı katmanlardan geçirerek daha güçlü difüzyon sağlar.
        
        Args:
            number (int): İşlenecek sayı.
            
        Returns:
            int: Geliştirilmiş S-Box ile modifiye edilmiş sayı.
        """
        # 1. Katman: İlk byte'ı S-Box'tan geçir
        byte0 = number & 0xFF
        sbox_val0 = self.S_BOX[byte0]
        
        # 2. Katman: İkinci byte'ı Inverse S-Box'tan geçir (ek karmaşıklık)
        byte1 = (number >> 8) & 0xFF
        sbox_val1 = self.INV_S_BOX[byte1]
        
        # 3. Katman: Üçüncü byte'ı tekrar S-Box'tan geçir
        byte2 = (number >> 16) & 0xFF
        sbox_val2 = self.S_BOX[byte2]
        
        # 4. Katman: Dördüncü byte'ı Inverse S-Box'tan geçir
        byte3 = (number >> 24) & 0xFF
        sbox_val3 = self.INV_S_BOX[byte3]
        
        # Tüm katmanları birleştir ve XOR ile extra difüzyon ekle
        result = sbox_val0 | (sbox_val1 << 8) | (sbox_val2 << 16) | (sbox_val3 << 24)
        
        # SHA-256 karıştırma (Avalanche etkisi için)
        # Küçük değişiklikler çıktıda büyük farklılıklara yol açar
        hash_input = result.to_bytes(8, 'big')
        hash_output = hashlib.sha256(hash_input).digest()
        hash_int = int.from_bytes(hash_output[:4], 'big')
        
        # Original number ile hash'i XOR'la
        modified_number = result ^ hash_int
        
        return modified_number

    def _collatz_step(self, n):
        """
        Gelişmiş Collatz adımı: Kaotik matematiği ve kriptografik karıştırmayı birleştirir.
        
        Bu fonksiyon:
        1. Döngü kırma mekanizması ile durağan durumları önler
        2. Temporal entropi enjeksiyonu yapar (zaman tabanlı rastgelelik)
        3. Collatz transformasyonu uygular
        4. Çok katmanlı S-Box karıştırması yapar
        5. Avalanche etkisi için ek XOR rotasyonu ekler
        
        Args:
            n (int): Mevcut sayı.
            
        Returns:
            int: Bir sonraki sayı.
        """
        self.iteration_count += 1
        
        # Döngü Kırıcı: Klasik 4-2-1 döngüsü veya 1'e ulaşma durumunda
        if n in [1, 2, 4] or n < 100:
            # Yüksek entropili rastgele değer + temporal component
            temporal_entropy = int(time.time() * 1000000) & 0xFFFF
            random_entropy = secrets.randbits(32)
            n = (n ^ random_entropy ^ temporal_entropy) | 0x10000
            
        # Collatz yörüngesini kaydet (analiz için)
        if len(self.collatz_path) < 1000:  # İlk 1000 adımı kaydet
            self.collatz_path.append(n)

        # Collatz Algoritması Adımı
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
            
        # Gelişmiş AES Karıştırma (Kritik Adım)
        n = self._apply_enhanced_sbox(n)
        
        # Ek rotasyon ve XOR (Avalanche etkisi artırımı)
        # Her 8 iterasyonda bir ekstra karıştırma
        if self.iteration_count % 8 == 0:
            rotation_amount = (self.iteration_count % 32)
            n = ((n << rotation_amount) | (n >> (32 - rotation_amount))) & 0xFFFFFFFF
            n ^= secrets.randbits(32)
        
        return n

    def _calculate_entropy(self, bits):
        """
        Shannon entropisi hesaplar (bilgi teorisi metriği).
        Mükemmel rastgele diziler için entropi 1.0'a yakın olmalıdır.
        
        Args:
            bits (list): Binary bit listesi (0 ve 1'ler).
            
        Returns:
            float: Shannon entropisi (0.0 - 1.0 arası).
        """
        if not bits:
            return 0.0
            
        n = len(bits)
        ones = sum(bits)
        zeros = n - ones
        
        if ones == 0 or zeros == 0:
            return 0.0
            
        p1 = ones / n
        p0 = zeros / n
        
        import math
        entropy = -(p0 * math.log2(p0) + p1 * math.log2(p1))
        return entropy
    
    def _calculate_runs(self, bits):
        """
        Runs Test: Ardışık aynı bitlerin (run) dağılımını analiz eder.
        Rastgele dizilerde run uzunlukları belli bir pattern izler.
        
        Args:
            bits (list): Binary bit listesi.
            
        Returns:
            dict: Run istatistikleri.
        """
        runs = []
        current_run = 1
        
        for i in range(1, len(bits)):
            if bits[i] == bits[i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)
        
        return {
            'run_count': len(runs),
            'avg_run_length': sum(runs) / len(runs) if runs else 0,
            'max_run_length': max(runs) if runs else 0,
            'run_distribution': runs[:50]  # İlk 50 run'ı kaydet
        }

    def generate_balanced_key(self, length=256):
        """
        Belirtilen uzunlukta dengeli (eşit sayıda 0 ve 1) ve yüksek entropili bir anahtar üretir.
        
        Bu fonksiyon:
        1. Kriptografik güvenli seed kullanır
        2. Collatz-AES hibrit algoritmasını uygular
        3. Mükemmel denge sağlar (50% sıfır, 50% bir)
        4. İstatistiksel kalite metrikleri hesaplar
        5. Detaylı analiz verisi döndürür
        
        Args:
            length (int): Üretilecek anahtarın bit uzunluğu (örn: 128, 256, 512).
            
        Returns:
            dict: {
                'binary': str (binary string),
                'hex': str (hexadecimal string),
                'stats': dict (detaylı istatistikler),
                'raw_bits': list (ham bit listesi - analiz için),
                'collatz_path': list (Collatz yörüngesi - ilk 1000 adım)
            }
        """
        if length % 2 != 0:
            raise ValueError("Dengeli bir anahtar için uzunluk çift sayı olmalıdır.")

        # 1. Başlangıç (Seed) Belirleme
        # Kriptografik olarak güvenli bir başlangıç değeri
        # Temporal component ekleyerek her çalıştırmada farklı sonuç garanti edilir
        temporal_seed = int(time.time() * 1000000)
        random_seed = secrets.randbits(64)
        self.state = temporal_seed ^ random_seed
        self.iteration_count = 0
        self.collatz_path = []
        
        bits = []
        
        # İstenen uzunluğa kadar bit üretimi
        while len(bits) < length:
            self.state = self._collatz_step(self.state)
            
            # Sayının birden fazla bitini kullanarak daha fazla entropi elde et
            # Ancak dengesizlik yaratmamak için dikkatli ol
            bits.append(self.state & 1)
            
        # 2. Dengeleme (Balancing) Algoritması
        # 0 ve 1 sayılarının tam eşit olmasını garanti eder.
        current_ones = sum(bits)
        target_ones = length // 2
        flipped_count = 0
        
        if current_ones != target_ones:
            diff = current_ones - target_ones
            
            rng = secrets.SystemRandom()
            
            if diff > 0:
                # 1'ler fazla, rastgele 'diff' kadar 1'i 0 yapmalıyız.
                ones_indices = [i for i, b in enumerate(bits) if b == 1]
                to_flip = rng.sample(ones_indices, diff)
                for idx in to_flip:
                    bits[idx] = 0
                    flipped_count += 1
            else:
                # 0'lar fazla (diff negatif), rastgele '|diff|' kadar 0'ı 1 yapmalıyız.
                zeros_indices = [i for i, b in enumerate(bits) if b == 0]
                to_flip = rng.sample(zeros_indices, abs(diff))
                for idx in to_flip:
                    bits[idx] = 1
                    flipped_count += 1
        
        # 3. İstatistiksel Metrikleri Hesapla
        entropy = self._calculate_entropy(bits)
        runs_data = self._calculate_runs(bits)
                    
        # 4. Sonuçları Formatla
        binary_string = "".join(map(str, bits))
        
        # Binary string'i integer'a çevirip hex formatına dönüştür
        integer_value = int(binary_string, 2)
        hex_string = hex(integer_value)[2:].upper()
        
        # Hex uzunluğunu düzelt (gerekirse başına 0 ekle)
        expected_hex_len = length // 4
        hex_string = hex_string.zfill(expected_hex_len)
        
        return {
            'binary': binary_string,
            'hex': hex_string,
            'raw_bits': bits,
            'collatz_path': self.collatz_path,
            'stats': {
                '0_count': bits.count(0),
                '1_count': bits.count(1),
                'total_len': length,
                'entropy': entropy,
                'flipped_bits': flipped_count,
                'runs': runs_data,
                'iterations': self.iteration_count
            }
        }

