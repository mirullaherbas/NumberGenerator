"""
Gelişmiş Analiz ve Görselleştirme Modülü

Bu modül, üretilen anahtarların kriptografik kalitesini ve rastgelelik özelliklerini
çeşitli istatistiksel testler ve görselleştirmelerle analiz eder.

Görselleştirmeler:
1. Bit Dağılım Pasta Grafiği (Balance Verification)
2. Bit Pattern Histogram (Frequency Analysis)
3. Run Length Distribution (Consecutive Bits Analysis)
4. Autocorrelation Plot (Sequence Independence)
5. Collatz Path Visualization (Chaos Theory)
6. Entropy Analysis (Information Theory)
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
from collections import Counter

# Matplotlib stil ayarları
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def create_comprehensive_analysis(result, output_dir='output'):
    """
    Tüm analizleri içeren kapsamlı bir görselleştirme raporu oluşturur.
    
    Args:
        result (dict): generate_balanced_key fonksiyonundan dönen sonuç sözlüğü.
        output_dir (str): Çıktıların kaydedileceği klasör.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    stats = result['stats']
    bits = result['raw_bits']
    binary_str = result['binary']
    
    # Ana figure oluştur (2x3 grid)
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('COLLATZ-AES HİBRİT ANAHTAR ÜRETECİ - KAPSAMLI ANALİZ RAPORU', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # ==================== 1. BIT DAĞILIM PASTA GRAFİĞİ ====================
    ax1 = fig.add_subplot(gs[0, 0])
    create_balance_pie_chart(ax1, stats)
    
    # ==================== 2. BIT PATTERN HISTOGRAM ====================
    ax2 = fig.add_subplot(gs[0, 1])
    create_bit_pattern_histogram(ax2, binary_str)
    
    # ==================== 3. RUN LENGTH DISTRIBUTION ====================
    ax3 = fig.add_subplot(gs[0, 2])
    create_run_length_chart(ax3, stats['runs'])
    
    # ==================== 4. ENTROPY GAUGE ====================
    ax4 = fig.add_subplot(gs[1, 0])
    create_entropy_gauge(ax4, stats['entropy'])
    
    # ==================== 5. AUTOCORRELATION PLOT ====================
    ax5 = fig.add_subplot(gs[1, 1])
    create_autocorrelation_plot(ax5, bits)
    
    # ==================== 6. BIT SEQUENCE VISUALIZATION ====================
    ax6 = fig.add_subplot(gs[1, 2])
    create_bit_sequence_visual(ax6, bits)
    
    # ==================== 7. COLLATZ PATH VISUALIZATION ====================
    ax7 = fig.add_subplot(gs[2, :2])
    create_collatz_path_plot(ax7, result.get('collatz_path', []))
    
    # ==================== 8. STATISTICS TABLE ====================
    ax8 = fig.add_subplot(gs[2, 2])
    create_statistics_table(ax8, stats)
    
    # Kaydet
    filepath = os.path.join(output_dir, 'comprehensive_analysis.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n[ANALİZ] Kapsamlı analiz raporu kaydedildi: {filepath}")
    
    # Ek olarak tekil grafikler de oluştur
    create_individual_charts(result, output_dir)

def create_balance_pie_chart(ax, stats):
    """Bit dağılımı pasta grafiği."""
    labels = ['0 Bitleri', '1 Bitleri']
    sizes = [stats['0_count'], stats['1_count']]
    colors = ['#ff6b6b', '#4ecdc4']
    explode = (0.05, 0.05)
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%',
                                        startangle=90, explode=explode, shadow=True)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax.set_title('Bit Dağılım Dengesi\n(Hedef: 50%-50%)', fontweight='bold', fontsize=12)

def create_bit_pattern_histogram(ax, binary_str):
    """8-bitlik pattern frekans analizi."""
    # İlk 256 biti 8'erli gruplara ayır
    patterns = []
    sample_size = min(256, len(binary_str))
    for i in range(0, sample_size - 7, 8):
        pattern = binary_str[i:i+8]
        patterns.append(int(pattern, 2))
    
    ax.hist(patterns, bins=30, color='#95e1d3', edgecolor='#38ada9', alpha=0.8)
    ax.set_xlabel('8-bit Pattern Değeri', fontweight='bold')
    ax.set_ylabel('Frekans', fontweight='bold')
    ax.set_title('8-bit Pattern Dağılımı\n(Uniform Olmalı)', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)

def create_run_length_chart(ax, runs_data):
    """Run length dağılımı (ardışık aynı bitler)."""
    run_dist = runs_data['run_distribution'][:30]  # İlk 30 run
    
    colors = ['#e74c3c' if x > 5 else '#3498db' for x in run_dist]
    ax.bar(range(len(run_dist)), run_dist, color=colors, alpha=0.8, edgecolor='black')
    ax.axhline(y=runs_data['avg_run_length'], color='green', linestyle='--', 
               linewidth=2, label=f"Ortalama: {runs_data['avg_run_length']:.2f}")
    ax.set_xlabel('Run İndeksi', fontweight='bold')
    ax.set_ylabel('Run Uzunluğu', fontweight='bold')
    ax.set_title(f'Run Length Analizi\n(Max: {runs_data["max_run_length"]})', 
                 fontweight='bold', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

def create_entropy_gauge(ax, entropy):
    """Shannon entropisi göstergesi (gauge chart)."""
    # Yarım daire gauge
    theta = np.linspace(0, np.pi, 100)
    r = 1
    
    # Arka plan renkli bölgeler
    ax.fill_between(theta[:33], 0, r, color='#e74c3c', alpha=0.3, label='Düşük')
    ax.fill_between(theta[33:66], 0, r, color='#f39c12', alpha=0.3, label='Orta')
    ax.fill_between(theta[66:], 0, r, color='#27ae60', alpha=0.3, label='Yüksek')
    
    # İbre (needle)
    needle_angle = entropy * np.pi  # entropy 0-1 arası, pi ile çarparak 0-180 derece
    ax.plot([0, r * np.cos(needle_angle)], [0, r * np.sin(needle_angle)], 
            color='black', linewidth=3)
    ax.plot(0, 0, 'ko', markersize=10)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0, -0.1, f'Entropi: {entropy:.4f}', ha='center', fontsize=14, fontweight='bold')
    ax.set_title('Shannon Entropisi\n(Maks: 1.0)', fontweight='bold', fontsize=12)
    ax.legend(loc='upper right', fontsize=8)

def create_autocorrelation_plot(ax, bits):
    """Otokorelasyon grafiği (bağımsızlık testi)."""
    # İlk 500 bit için autocorrelation hesapla
    sample = bits[:min(500, len(bits))]
    n = len(sample)
    
    # Mean-centered data
    mean_val = np.mean(sample)
    centered = np.array(sample) - mean_val
    
    # Autocorrelation için 50 lag hesapla
    max_lag = min(50, n // 2)
    autocorr = []
    
    for lag in range(max_lag):
        if lag == 0:
            autocorr.append(1.0)
        else:
            c = np.correlate(centered[:-lag], centered[lag:], mode='valid')[0]
            c0 = np.correlate(centered, centered, mode='valid')[0]
            autocorr.append(c / c0 if c0 != 0 else 0)
    
    ax.stem(range(max_lag), autocorr, basefmt=' ', linefmt='#2980b9', markerfmt='o')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.axhline(y=0.2, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Eşik')
    ax.axhline(y=-0.2, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Lag', fontweight='bold')
    ax.set_ylabel('Korelasyon', fontweight='bold')
    ax.set_title('Otokorelasyon Fonksiyonu\n(Sıfıra Yakın Olmalı)', fontweight='bold', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

def create_bit_sequence_visual(ax, bits):
    """İlk 400 biti görsel olarak göster (matrix formatında)."""
    sample = bits[:min(400, len(bits))]
    
    # 20x20 matrix oluştur
    matrix_size = int(np.sqrt(len(sample)))
    sample = sample[:matrix_size**2]
    matrix = np.array(sample).reshape((matrix_size, matrix_size))
    
    cmap = plt.cm.colors.ListedColormap(['#2c3e50', '#ecf0f1'])
    im = ax.imshow(matrix, cmap=cmap, interpolation='nearest')
    ax.set_title(f'Bit Sekans Görselleştirme\n({matrix_size}x{matrix_size} matrix)', 
                 fontweight='bold', fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Colorbar ekle
    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1], fraction=0.046, pad=0.04)
    cbar.ax.set_yticklabels(['0', '1'])

def create_collatz_path_plot(ax, collatz_path):
    """Collatz yörüngesinin ilk N adımını göster."""
    if not collatz_path or len(collatz_path) < 2:
        ax.text(0.5, 0.5, 'Collatz Yörüngesi Verisi Yok', 
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return
    
    # Log scale kullan (değerler çok büyük olabiliyor)
    path_sample = collatz_path[:min(200, len(collatz_path))]
    log_path = np.log10(np.array(path_sample) + 1)  # +1 to avoid log(0)
    
    ax.plot(log_path, color='#8e44ad', linewidth=1.5, alpha=0.8)
    ax.fill_between(range(len(log_path)), log_path, alpha=0.3, color='#9b59b6')
    ax.set_xlabel('İterasyon', fontweight='bold')
    ax.set_ylabel('log₁₀(değer)', fontweight='bold')
    ax.set_title(f'Collatz Yörünge Grafiği (İlk {len(path_sample)} adım)\nKaotik Davranış Göstergesi', 
                 fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)

def create_statistics_table(ax, stats):
    """İstatistik tablosu oluştur."""
    ax.axis('off')
    
    # Veriyi hazırla
    table_data = [
        ['Metrik', 'Değer'],
        ['─' * 20, '─' * 15],
        ['Toplam Bit', f"{stats['total_len']}"],
        ['0 Sayısı', f"{stats['0_count']}"],
        ['1 Sayısı', f"{stats['1_count']}"],
        ['Denge', f"{stats['0_count'] / stats['total_len'] * 100:.2f}% / {stats['1_count'] / stats['total_len'] * 100:.2f}%"],
        ['─' * 20, '─' * 15],
        ['Entropi', f"{stats['entropy']:.6f}"],
        ['Run Sayısı', f"{stats['runs']['run_count']}"],
        ['Ort. Run', f"{stats['runs']['avg_run_length']:.2f}"],
        ['Maks Run', f"{stats['runs']['max_run_length']}"],
        ['─' * 20, '─' * 15],
        ['İterasyon', f"{stats['iterations']}"],
        ['Dengeleme', f"{stats['flipped_bits']} bit"],
    ]
    
    table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                     colWidths=[0.6, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Başlık satırını vurgula
    for i in range(2):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax.set_title('İstatistiksel Özet', fontweight='bold', fontsize=12, pad=20)

def create_individual_charts(result, output_dir):
    """Her bir grafiği ayrı dosya olarak kaydet (yüksek çözünürlük)."""
    stats = result['stats']
    bits = result['raw_bits']
    
    # 1. Detaylı Bit Histogram
    fig, ax = plt.subplots(figsize=(12, 6))
    create_detailed_bit_histogram(ax, bits)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bit_histogram.png'), dpi=300)
    plt.close()
    
    # 2. Detaylı Run Analysis
    fig, ax = plt.subplots(figsize=(12, 6))
    create_detailed_run_analysis(ax, stats['runs'])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'run_analysis.png'), dpi=300)
    plt.close()
    
    print(f"[ANALİZ] Tekil grafikler kaydedildi: {output_dir}/")

def create_detailed_bit_histogram(ax, bits):
    """Detaylı bit histogram (sliding window analizi)."""
    # 16-bit sliding window
    window_size = 16
    window_values = []
    
    for i in range(len(bits) - window_size + 1):
        window = bits[i:i+window_size]
        val = sum([b * (2 ** (window_size - 1 - j)) for j, b in enumerate(window)])
        window_values.append(val)
    
    ax.hist(window_values, bins=100, color='#3498db', edgecolor='black', alpha=0.7)
    ax.set_xlabel('16-bit Window Değeri', fontweight='bold', fontsize=12)
    ax.set_ylabel('Frekans', fontweight='bold', fontsize=12)
    ax.set_title('16-bit Sliding Window Histogram\n(Uniform Dağılım Beklenir)', 
                 fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.3)

def create_detailed_run_analysis(ax, runs_data):
    """Detaylı run length frekans dağılımı."""
    run_lengths = runs_data['run_distribution']
    
    # Run length frekanslarını say
    counter = Counter(run_lengths)
    lengths = sorted(counter.keys())
    frequencies = [counter[l] for l in lengths]
    
    ax.bar(lengths, frequencies, color='#e74c3c', edgecolor='black', alpha=0.8)
    ax.set_xlabel('Run Uzunluğu', fontweight='bold', fontsize=12)
    ax.set_ylabel('Frekans', fontweight='bold', fontsize=12)
    ax.set_title('Run Length Frekans Dağılımı\n(Kısa run\'lar baskın olmalı)', 
                 fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')

def visualize_key_balance(stats):
    """
    Basit pasta grafiği (geriye dönük uyumluluk için).
    Artık create_comprehensive_analysis kullanılması önerilir.
    """
    labels = ['0 Bitleri', '1 Bitleri']
    sizes = [stats['0_count'], stats['1_count']]
    colors = ['#ff9999', '#66b3ff']
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.title(f"Anahtar Bit Dağılım Analizi\n(Toplam Uzunluk: {stats['total_len']} bit)", 
              fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, 'balance_chart.png')
    plt.savefig(file_path, dpi=300)
    plt.close()
    
    print(f"\n[ANALİZ] Basit görselleştirme grafiği kaydedildi: {file_path}")
