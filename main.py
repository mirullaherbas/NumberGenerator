import sys
import time
from collatz_aes import CollatzAESGenerator
from analysis import create_comprehensive_analysis

# ANSI Renk Kodları (Terminal görselliği için)
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

def print_banner():
    """Program başlangıcında şık bir banner yazdırır."""
    banner = f"""
    {CYAN}{BOLD}╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🔐 COLLATZ-AES HİBRİT ANAHTAR ÜRETECİ v2.0 🔐          ║
    ║                                                              ║
    ║     Gelişmiş Kriptografik Anahtar Üretim Sistemi            ║
    ║     Bilgi Sistemleri Güvenliği - Özel Proje                 ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)

def print_progress_bar(progress, total, bar_length=40):
    """Terminal'de progress bar gösterir."""
    percent = float(progress) * 100 / total
    filled = int(percent/100 * bar_length)
    bar = '█' * filled
    spaces = ' ' * (bar_length - filled)
    sys.stdout.write(f'\r{CYAN}[{bar}{spaces}] {percent:.1f}%{RESET}')
    sys.stdout.flush()

def main():
    """
    Programın ana giriş noktası. 
    Gelişmiş kullanıcı etkileşimi ve detaylı analiz raporu üretimi.
    """
    print_banner()
    
    try:
        # Kullanıcıdan bit uzunluğunu al
        print(f"{YELLOW}📊 Desteklenen uzunluklar: 128, 256, 512, 1024 bit{RESET}\n")
        user_input = input(f"{CYAN}[?] Üretilecek anahtar uzunluğunu girin: {RESET}")
        
        if not user_input.strip():
            length = 256  # Varsayılan değer
            print(f"{YELLOW}[!] Giriş yapılmadı, varsayılan değer kullanılıyor: {length}{RESET}")
        else:
            length = int(user_input)
            
        if length <= 0 or length % 2 != 0:
            print(f"{RED}[HATA] Uzunluk pozitif ve çift sayı olmalıdır (Dengeleme için).{RESET}")
            sys.exit(1)
            
        # Analiz tipi seçimi
        print(f"\n{CYAN}[?] Detaylı analiz raporu oluşturulsun mu? (E/H): {RESET}", end='')
        detailed_analysis = input().strip().upper() in ['E', 'Y', 'YES', 'EVET', '']
        
        print(f"\n{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{GREEN}{BOLD}🚀 ANAHTAR ÜRETME SÜRECİ BAŞLATILIYOR...{RESET}")
        print(f"{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
        
        start_time = time.time()
        
        # 1. Anahtar Üretimi
        print(f"{CYAN}[1/3] Collatz-AES hibrit algoritması çalıştırılıyor...{RESET}")
        generator = CollatzAESGenerator()
        result = generator.generate_balanced_key(length)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 2. Sonuçları Ekrana Yazdır
        print(f"{GREEN}✓ Tamamlandı ({duration:.4f} saniye){RESET}\n")
        
        print(f"{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{GREEN}{BOLD}📊 ÜRETIM SONUÇLARI{RESET}")
        print(f"{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
        
        # Hex Anahtar (Formatlanmış)
        print(f"{BLUE}{BOLD}🔑 HEX ANAHTAR:{RESET}")
        hex_key = result['hex']
        # Her 64 karakterde bir satır kır
        for i in range(0, len(hex_key), 64):
            chunk = hex_key[i:i+64]
            # Her 8 karakterde bir boşluk ekle (okunabilirlik)
            formatted = ' '.join([chunk[j:j+8] for j in range(0, len(chunk), 8)])
            print(f"   {GREEN}{formatted}{RESET}")
        
        print(f"\n{BLUE}{BOLD}⚙️  BINARY ANAHTAR (Örnek - İlk 128 bit):{RESET}")
        binary_sample = result['binary'][:128]
        # Her 32 bit'te bir satır
        for i in range(0, len(binary_sample), 32):
            chunk = binary_sample[i:i+32]
            # Her 8 bit'te bir boşluk
            formatted = ' '.join([chunk[j:j+8] for j in range(0, len(chunk), 8)])
            print(f"   {CYAN}{formatted}{RESET}")
        print(f"   {YELLOW}... ({length - 128} bit daha var){RESET}")
        
        # 3. İstatistiksel Kanıt
        stats = result['stats']
        print(f"\n{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{GREEN}{BOLD}📈 DETAYLI İSTATİSTİKSEL ANALİZ{RESET}")
        print(f"{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
        
        # Bit Dengesi
        print(f"{MAGENTA}{BOLD}▸ Bit Dağılımı:{RESET}")
        print(f"   Toplam Uzunluk : {stats['total_len']} bit")
        print(f"   0 Bitleri      : {stats['0_count']} ({stats['0_count']/stats['total_len']*100:.2f}%)")
        print(f"   1 Bitleri      : {stats['1_count']} ({stats['1_count']/stats['total_len']*100:.2f}%)")
        
        if stats['0_count'] == stats['1_count']:
            print(f"   {GREEN}{BOLD}✓ Mükemmel Denge Sağlandı!{RESET}")
        else:
            print(f"   {RED}{BOLD}✗ Denge Hatası!{RESET}")
        
        # Entropi
        print(f"\n{MAGENTA}{BOLD}▸ Kriptografik Kalite Metrikleri:{RESET}")
        entropy = stats['entropy']
        entropy_quality = "Mükemmel" if entropy > 0.99 else "İyi" if entropy > 0.95 else "Orta"
        entropy_color = GREEN if entropy > 0.99 else YELLOW if entropy > 0.95 else RED
        print(f"   Shannon Entropisi  : {entropy_color}{entropy:.6f}{RESET} ({entropy_quality})")
        print(f"   İterasyon Sayısı   : {stats['iterations']}")
        print(f"   Dengeleme İşlemi   : {stats['flipped_bits']} bit çevrildi")
        
        # Run Analysis
        print(f"\n{MAGENTA}{BOLD}▸ Run Length Analizi:{RESET}")
        runs = stats['runs']
        print(f"   Toplam Run Sayısı  : {runs['run_count']}")
        print(f"   Ortalama Run       : {runs['avg_run_length']:.2f}")
        print(f"   Maksimum Run       : {runs['max_run_length']}")
        
        run_quality = "İyi" if runs['max_run_length'] < 10 else "Orta" if runs['max_run_length'] < 15 else "Düşük"
        run_color = GREEN if runs['max_run_length'] < 10 else YELLOW if runs['max_run_length'] < 15 else RED
        print(f"   Kalite Değ.        : {run_color}{run_quality}{RESET}")
        
        # 4. Görselleştirme
        if detailed_analysis:
            print(f"\n{CYAN}[2/3] Kapsamlı analiz raporu oluşturuluyor...{RESET}")
            create_comprehensive_analysis(result)
            print(f"{GREEN}✓ Tamamlandı{RESET}\n")
        else:
            print(f"\n{CYAN}[2/3] Basit görselleştirme atlandı.{RESET}\n")
        
        # 5. Özet
        print(f"{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{GREEN}{BOLD}✅ İŞLEM BAŞARIYLA TAMAMLANDI{RESET}")
        print(f"{GREEN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
        
        print(f"{YELLOW}📁 Çıktı Dosyaları:{RESET}")
        if detailed_analysis:
            print(f"   • output/comprehensive_analysis.png (Ana rapor)")
            print(f"   • output/bit_histogram.png")
            print(f"   • output/run_analysis.png")
        print(f"\n{CYAN}💡 İpucu: PNG dosyalarını açarak detaylı analizi görebilirsiniz.{RESET}\n")
        
    except ValueError:
        print(f"\n{RED}[HATA] Lütfen geçerli bir tam sayı giriniz.{RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] İşlem kullanıcı tarafından iptal edildi.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[HATA] Beklenmedik bir sorun oluştu: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

