# Hipotesis & Status Hasil Uji Empiris

> Scope: **Lintas kategori** (20.976 listing bersih Tokopedia di DuckDB mart `fct_listing`)
> Tanggal Uji: 30 September 2026
> Metode: OLS Multivariat, Kruskal-Wallis Test, Mann-Whitney U Test, Non-parametric Group Analysis.

---

## Ringkasan Status Hipotesis

| ID | Hipotesis | Metode Uji | Status Awal | Status Setelah Audit | Temuan & Evaluasi Audit |
|----|-----------|------------|-------------|----------------------|-------------------------|
| **H1** | Titik jenuh diskon (Discount Saturation Point) | Median/Mean per bucket diskon & trimmed outlier | Didukung | ⚠️ **Didukung Sebagian** | Lonjakan volume nyata di diskon awal (1–10% menggandakan listing laris dari 11,6% ke 22,8%). Penurunan mean di atas 30% hilang setelah top 1% (≥50rb terjual) dikeluarkan; median flat 100 adalah artefak bin platform. |
| **H2** | Responsivitas Diskon: Utilitarian vs Fashion | Regresi OLS interaksi (`diskon_pct * is_utilitarian`) | Didukung | ❌ **Tidak Didukung** | Interaksi diskon × utilitarian negatif (−0,0034; p = 0,012) dan tidak robust tanpa kontrol ulasan (p = 0,27). Arah klaim berbalik. |
| **H3** | Price Tier vs Rating Produk | Kruskal-Wallis & Mann-Whitney U (ulasan ≥ 30) | Didukung | ⚠️ **Signifikan, Efek Sangat Kecil** | Secara statistik signifikan (p < 0,001), namun selisih mean antar tier hanya 0,04 bintang (4,863 vs 4,902) dan median seluruh tier identik di 4,90. |
| **H4** | Regional Pricing (Sentra Produksi) | Median harga fashion per wilayah & Kruskal-Wallis | Didukung | ❌ **Tidak Didukung** | Setelah mapping wilayah diperbaiki ke kabupaten dan pakaian dipisahkan dari sepatu/aksesori, Jawa Barat bukan termurah (Jatim Rp 95,5rb & DKI Rp 99,0rb < Jabar Rp 104,0rb). |
| **H5** | Spesifikasi Produk di Awal Judul | Mann-Whitney U harga & unit terjual | Didukung Sebagian | ⚠️ **Terkonfon Kategori** | Volume lebih tinggi (median 90 vs 50 unit), namun 35% listing dengan spesifikasi di awal adalah produk kebutuhan pokok/rumah tangga berharga murah. |
| **H6** | Efek Toko Official (Official Store) | Mann-Whitney U harga, diskon, volume terjual | Didukung Sebagian | ⚠️ **Didukung Sebagian** | Official store unggul volume penjualan di 11 dari 12 kategori (+125%). Namun, harga premium agregat (+55,4%) sebagian besar merupakan efek bauran kategori (7 dari 12 kategori memiliki premium < +55%). |

---

## Detail Hasil Pengujian Hipotesis (Re-Audited Single Source of Truth)

### H1 — Discount Saturation Point

- **Status Setelah Audit**: ⚠️ **Didukung Sebagian**
- **Distribusi Penjualan per Bucket Diskon**:

| Bucket Diskon | n Listing | Median Terjual | % Listing ≥ 1.000 Terjual | Mean Terjual (Semua) | Mean Terjual (Tanpa Top 1%) |
|---|---:|---:|---:|---:|---:|
| 0% | 12.918 | 26 unit | 11,6% | 1.064 | 557 |
| 1–10% | 1.936 | 100 unit | 22,8% | 2.093 | 979 |
| 11–20% | 1.155 | 100 unit | 25,8% | 2.566 | 1.287 |
| 21–30% | 971 | 100 unit | 29,6% | 5.799 | 1.426 |
| 31–50% | 2.055 | 100 unit | 27,5% | 4.122 | 1.244 |
| >50% | 1.941 | 100 unit | 31,6% | 3.840 | 1.503 |

- **Evaluasi Audit**:
  - Diskon taktis awal 1–10% menggandakan porsi listing laris (11,6% → 22,8%).
  - Di atas 20%, tambahan porsi listing laris melambat (hanya +2 hingga +6 poin persentase).
  - Median flat di angka 100 unit untuk semua bucket diskon > 0% adalah artefak pembulatan platform (`100+ terjual`), di mana 10–13% listing di setiap bucket bernilai tepat 100 unit (~40% seluruh nilai penjualan adalah bin platform).
  - Korelasi Spearman diskon vs terjual pada listing berdiskon hanya **0,08**.
  - Penurunan mean di diskon >30% pada data mentah didorong oleh outlier top 1% (≥50.000 terjual). Setelah di-trim, tidak ada bukti volume turun di diskon ekstrem, namun ketiadaan kenaikan yang sepadan membuktikan bahwa *deep discounting* (>30%) membakar margin tanpa hasil konversi berarti.

---

### H2 — Responsivitas Diskon: Utilitarian vs Fashion

- **Status Setelah Audit**: ❌ **Tidak Didukung**
- **Model Regresi OLS**: `log_terjual ~ diskon_pct * is_utilitarian + log_ulasan + C(tier_harga)`

| Variabel Independen | Koefisien | p-value |
|---|---:|---:|
| `diskon_pct` | +0,0221 | 1,3e-145 |
| `diskon_pct : is_utilitarian` | **−0,0034** | 0,012 |
| *(tanpa kontrol `log_ulasan`)* interaksi | −0,0018 | 0,27 |

- **Evaluasi Audit**:
  - Interaksi diskon dengan produk utilitarian ternyata bernilai **negatif** (−0,0034; p = 0,012) ketika dikontrol ulasan, dan tidak signifikan (p = 0,27) tanpa kontrol ulasan.
  - Arah hipotesis awal yang menyatakan utilitarian lebih responsif terhadap diskon daripada fashion berbalik dan tidak robust secara statistik.

---

### H3 — Price Tier vs Rating

- **Status Setelah Audit**: ⚠️ **Signifikan, Efek Sangat Kecil**
- **Evaluasi Statistik (pada listing dengan `jumlah_ulasan ≥ 30`)**:
  - Tier Bawah: Mean 4,863 (Std 0,197), Median 4,90
  - Tier Menengah: Mean 4,881 (Std 0,143), Median 4,90
  - Tier Atas: Mean 4,902 (Std 0,195), Median 4,90
  - Uji Kruskal-Wallis: $H = 100,35, p = 1,62 \times 10^{-22}$.
- **Evaluasi Praktis**:
  - Meskipun signifikansi statistik sangat tinggi akibat sampel besar ($N = 7.526$), ukuran efek (*effect size*) di dunia nyata sangat kecil: selisih rating rata-rata antara tier bawah dan atas hanya **0,04 bintang** (skala 1–5), dan nilai median di ketiga tier identik di angka 4,90.

---

### H4 — Regional Pricing (Sentra Produksi)

- **Status Setelah Audit**: ❌ **Tidak Didukung**
- **Perbandingan Analisis Sebelum vs Sesudah Audit**:

| Wilayah | Versi Awal (Fashion + Sepatu/Aksesori, Mapping Lama) | Hasil Audit (Pakaian Saja, Mapping Kabupaten) |
|---|---:|---:|
| Jawa Timur | Rp 126.650 (n = 286) | **Rp 95.500** (n = 184) |
| DKI Jakarta | Rp 129.000 (n = 2.063) | **Rp 99.000** (n = 945) |
| Jawa Barat | Rp 105.000 (n = 966) | **Rp 104.000** (n = 648) |
| Jawa Tengah | Rp 189.578 (n = 60) | **Rp 107.000** (n = 175) |
| Banten | Rp 137.000 (n = 426) | **Rp 126.000** (n = 169) |

- **Evaluasi Audit**:
  - Kruskal-Wallis (pakaian, 5 wilayah): $H = 11,94, p = 0,018$ (tanpa Banten $p = 0,048$).
  - Mapping wilayah awal menyisakan 1.672 baris di kategori "Lainnya" (termasuk sentra konveksi Garut, Cimahi, Tasikmalaya, Sleman).
  - Setelah mapping kabupaten diperbaiki dan pakaian dipisahkan dari alas kaki/aksesori, Jawa Barat **bukan** wilayah termurah. Rekomendasi bundling anti-perang harga Jawa Barat tidak lagi didukung oleh data. Lokasi generik "Indonesia" mencakup 7,4% di data mart (9,6% di raw).

---

### H5 — Spesifikasi Produk di Awal Judul

- **Status Setelah Audit**: ⚠️ **Terkonfon Kategori**
- **Evaluasi Temuan**:
  - Listing dengan spesifikasi di awal judul (`has_spec_at_start = True`, 581 listing):
    - Median terjual: **90 unit** vs **50 unit** non-spesifik ($p < 0,001$).
    - Median harga: **Rp 68.000** vs **Rp 104.900** non-spesifik ($p < 0,001$).
  - **Efek Konfonding**: 35% listing dengan spesifikasi di awal judul terkonsentrasi pada kategori produk rumah tangga dan kebutuhan pokok murah (bukan busana fashion branded). Kenaikan volume lebih mencerminkan karakteristik kategori komoditas daripada trik judul semata.

---

### H6 — Efek Toko Official (Official Store)

- **Status Setelah Audit**: ⚠️ **Didukung Sebagian**
- **Evaluasi Temuan**:
  - Official Store mencakup **23,3%** data mart (4.885 listing).
  - **Keunggulan Volume**: Official Store mencatat median terjual **90 unit** vs **40 unit** toko reguler (+125% lebih tinggi, $p < 0,001$). Keunggulan volume ini konsisten di **11 dari 12 kategori** produk (selain ATK & kemasan).
  - **Bauran Harga Premium**: Angka agregat premium harga +55,4% (Rp 147.000 vs Rp 94.600) sebagian besar didorong oleh perbedaan bauran kategori. Premium harga median per kategori (dengan ≥30 listing official):
    - ATK: −20%
    - Kecantikan: +4%
    - Fashion Wanita: +9%
    - Makanan & Minuman: +16%
    - Fashion Pria: +36%
    - Elektronik: +50%
    - Fashion Umum: +53%
    - Sepatu & Aksesori: +56%
    - Rumah Tangga: +57%
    - Otomotif: +74%
    - Olahraga: +350%
    - Mainan & Hobi: +413%
  - Tujuh dari 12 kategori mencatat premium harga di bawah +55%. Selain itu, deteksi official store berbasis string toko memiliki keterbatasan (toko seperti IKEA Indonesia dan AZKO ID tidak terdeteksi, sedangkan `cigemoyofficial` ikut terhitung).
  - **Aktivitas Diskon**: Diskon rata-rata official store adalah 13,9% vs 12,1% reguler ($p < 0,001$).
