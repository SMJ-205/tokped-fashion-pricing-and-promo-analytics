# Hipotesis & Status Hasil Uji Empiris

> Scope: **Lintas kategori** (20.976 listing bersih Tokopedia di DuckDB mart `fct_listing`)
> Tanggal Uji: 30 September 2026
> Metode: OLS Multivariat, Kruskal-Wallis Test, Mann-Whitney U Test, Non-parametric Group Analysis.

---

## Ringkasan Status Hipotesis

| ID | Hipotesis | Metode Uji | Status | Temuan Kunci |
|----|-----------|------------|--------|--------------|
| **H1** | Titik jenuh diskon (Discount Saturation Point) | Median/Mean per bucket diskon & OLS kuadrat diskon | ✅ **Didukung** | Penjualan jenuh di rentang diskon 20–30%. Di atas 30%, median flat di 100 unit dan mean turun dari 5.799 ke 3.840 unit. |
| **H2** | Responsivitas Diskon: Utilitarian vs Fashion | Regresi OLS interaksi (`diskon_pct * kategori`) | ✅ **Didukung** | Utilitarian dan Fashion sama-sama merespons diskon (p < 0.001), dengan elastisitas harga utilitarian sedikit lebih sensitif pada diskon rendah. |
| **H3** | Price Tier vs Rating Produk | Kruskal-Wallis & Mann-Whitney U (filter ulasan ≥ 30) | ✅ **Didukung** | Tier bawah rata-rata rating 4.86 vs tier atas 4.90 (p = 1.62e-22). Perbedaan signifikan meski skala rating sangat terkompresi. |
| **H4** | Regional Pricing (Sentra Produksi) | Median harga fashion per wilayah & Kruskal-Wallis | ✅ **Didukung** | Jawa Barat (Bandung/sentra konveksi) memasang median harga fashion Rp 105.000 vs DKI Jakarta Rp 129.000 (p = 1.20e-6). |
| **H5** | Spesifikasi Produk di Awal Judul | Mann-Whitney U harga & unit terjual | ⚠️ **Didukung Sebagian** | Spesifikasi di awal judul menaikkan volume penjualan (+80%, median 90 vs 50 unit), namun harganya lebih rendah (Rp 68rb vs 105rb) karena didominasi produk komoditas/fast-moving. |
| **H6** | Efek Toko Official (Official Store) | Mann-Whitney U harga, diskon, volume terjual | ✅ **Didukung Sebagian** | Official store menjual lebih banyak (+125%, median 90 vs 40 unit) dan harga premium (+55%, Rp 147rb vs 95rb), namun diskon rata-rata justru lebih aktif (13.9% vs 12.1%). |

---

## Detail Hasil Pengujian Hipotesis

### H1 — Discount Saturation Point

- **Status**: ✅ **Didukung**
- **Temuan**:
  - Listing tanpa diskon (0%) memiliki median terjual 26 unit (mean: 1.064 unit).
  - Pemberian diskon awal (1–10% dan 11–20%) melipatgandakan median terjual ke 100 unit.
  - Namun kurva volume mengalami **titik jenuh (saturation)** di level **20–30%**:
    - Bucket 21–30%: mean terjual memuncak di **5.799 unit**.
    - Bucket 31–50%: mean terjual turun ke **4.121 unit**.
    - Bucket >50%: mean terjual turun ke **3.840 unit**, dengan median tetap stagnan di 100 unit.
  - Model OLS kuadratik mengonfirmasi koefisien negatif pada tingkat diskon ekstrem, membuktikan *diminishing returns* terhadap volume penjualan.
- **Keterbatasan**: Data listing bersifat cross-sectional (bukan panel time-series), sehingga merefleksikan portofolio penjual aktif.
- **Implikasi untuk Simulator Margin**:
  - Penurunan diskon dari >30% ke 20–25% mempertahankan volume penjualan tinggi tanpa mengorbankan margin kotor.

---

### H2 — Responsivitas Diskon: Utilitarian vs Fesyen

- **Status**: ✅ **Didukung**
- **Temuan**:
  - Kedua kelompok kategori memiliki koefisien diskon positif signifikan terhadap log-penjualan ($p < 0.001$).
  - Kategori Utilitarian (Rumah Tangga, Elektronik, Perkakas) memiliki adopsi diskon yang lebih terstandardisasi, sedangkan kategori Fashion memiliki variasi harga dan diskon yang lebih lebar.
  - Kontrol jumlah ulasan membuktikan bahwa reputasi toko tetap menjadi determinan terbesar ($t = 76.3, p < 0.001$).
- **Keterbatasan**: Kategori didasarkan pada rule-based tagging judul produk dengan coverage 78.99%.
- **Implikasi untuk Simulator**:
  - Seller produk utilitarian dapat menggunakan diskon taktis kecil (5–15%) untuk memenangkan konversi algoritma pencarian.

---

### H3 — Price Tier vs Rating

- **Status**: ✅ **Didukung**
- **Temuan**:
  - Pengujian dibatasi pada produk dengan `jumlah_ulasan ≥ 30` (7.526 listing) untuk menghilangkan bias listing baru.
  - Distribusi rating:
    - Tier Bawah: Mean 4.863, Std 0.197
    - Tier Menengah: Mean 4.881, Std 0.143
    - Tier Atas: Mean 4.902, Std 0.195
  - Uji Kruskal-Wallis: $H = 100.35, p = 1.62 \times 10^{-22}$.
  - Uji Mann-Whitney U (Bawah vs Atas): $p = 5.91 \times 10^{-23}$.
- **Keterbatasan**: Kompresi rating ekstrim di e-commerce Indonesia (89% produk berada di kisaran 4.75–5.0).
- **Implikasi**: Tier harga bawah menghadapi risiko rating sedikit lebih rendah akibat ekspektasi kualitas material pembeli.

---

### H4 — Regional Pricing (Sentra Produksi)

- **Status**: ✅ **Didukung**
- **Temuan**:
  - Analisis kategori Fesyen menunjukkan perbedaan harga signifikan antar wilayah ($H = 56.03, p = 1.20 \times 10^{-6}$).
  - Jawa Barat (pusat konveksi Bandung, Cimahi, dsb.): Median harga fashion **Rp 104.999** (966 listing).
  - Jawa Timur (Surabaya/Sidoarjo): Median harga fashion **Rp 126.650**.
  - DKI Jakarta (sentra distribusi/reseller utama): Median harga fashion **Rp 129.000** (2.063 listing).
  - Jawa Tengah: Median harga fashion **Rp 189.578**.
- **Keterbatasan**: 5.7% listing mencantumkan lokasi non-spesifik ("Indonesia") dan telah di-exclude.
- **Implikasi**: Reseller di Jakarta dan luar Jawa perlu mengantisipasi persaingan harga langsung dari produsen Jawa Barat.

---

### H5 — Spesifikasi Produk di Awal Judul

- **Status**: ⚠️ **Didukung Sebagian**
- **Temuan**:
  - Listing dengan spesifikasi/material di awal judul (`has_spec_at_start = True`, 581 listing):
    - Median terjual: **90 unit** vs **50 unit** non-spesifik ($p = 1.34 \times 10^{-5}$, Mann-Whitney U).
    - Median harga: **Rp 68.000** vs **Rp 104.900** non-spesifik ($p = 5.89 \times 10^{-13}$).
  - Hipotesis bahwa spesifikasi di awal menaikkan *harga* tidak terbukti; sebaliknya, seller menggunakannya untuk produk komoditas fast-moving volume tinggi (misal: *"Kaos Polos Cotton Combed 30s"*).
- **Keterbatasan**: Deteksi spesifikasi mengandalkan regex material dan ukuran di awal string judul.

---

### H6 — Efek Toko Official (Official Store)

- **Status**: ✅ **Didukung Sebagian**
- **Temuan**:
  - Official Store mencakup **23.3%** dari total listing (4.885 listing).
  - **Volume & Harga**:
    - Median terjual Official Store: **90 unit** vs Reguler **40 unit** (+125% lebih tinggi, $p = 8.30 \times 10^{-30}$).
    - Median harga Official Store: **Rp 147.000** vs Reguler **Rp 94.600** (+55.4% harga premium).
  - **Diskon**:
    - Rata-rata diskon Official Store: **13.9%** vs Reguler **12.1%** ($p = 1.06 \times 10^{-7}$).
    - Official Store ternyata *lebih rajin* memberikan diskon terstruktur (kampanye brand), bukan lebih rendah, tetapi mereka tetap mampu menjual dengan harga dasar yang jauh lebih tinggi.
- **Implikasi**: Status Official Store memberikan *pricing power* kuat yang menjustifikasi investasi branding seller.
