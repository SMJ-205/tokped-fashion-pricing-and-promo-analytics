# Executive Summary: Tokopedia Pricing & Promo Analytics

**Analisis Empiris Titik Jenuh Diskon, Kekuatan Merek, dan Trade-Off Margin pada 20.976 Listing E-Commerce**

---

## 📌 Ringkasan Eksekutif

Proyek ini mengevaluasi dinamika penetapan harga (*pricing*) dan efektivitas promosi (*promo analytics*) pada platform Tokopedia dengan menganalisis **20.976 listing bersih** lintas 14 kategori produk menggunakan stack modern data stack (*DuckDB, dbt Core, Python, dan Streamlit*).

Fokus utama adalah membedah fenomena perang diskon (*deep discounting*): apakah diskon besar selalu mendongkrak volume penjualan, dan pada titik mana diskon justru merugikan margin kotor seller?

---

## 💡 Tiga Temuan Kunci (Empirical Insights)

### 1. Titik Jenuh Diskon (H1: Saturation Point di 20–30%)
* **Temuan**: Pemberian diskon awal (1–10%) meningkatkan median penjualan dari **26 unit** (tanpa diskon) ke **100 unit** (+284%). Namun, di atas diskon 20%, kurva volume penjualan mengalami **stagnasi total (plateau)** di mana median unit terjual flat di angka 100 unit untuk semua bucket (11–20%, 21–30%, 31–50%, >50%).
* **Puncak Penjualan**: Rata-rata volume penjualan memuncak di bucket **21–30% (5.799 unit)**, dan justru **menurun** di bucket 31–50% (4.121 unit) serta >50% (3.840 unit).
* **Implikasi**: Diskon di atas 30% adalah inefisiensi margin (*margin burn*) tanpa pertambahan volume penjualan proporsional.

### 2. Pricing Power Toko Official (H6: +55% Harga Premium, +125% Volume)
* **Temuan**: Listing Official Store (23.3% dari total) memiliki median penjualan **90 unit** vs **40 unit** pada toko reguler (+125% lebih tinggi, $p < 0.001$), sekaligus menikmati median harga **Rp 147.000** vs **Rp 94.600** (+55.4% harga premium).
* **Aktivitas Promo**: Official Store bukan menjual dengan diskon lebih rendah, melainkan menjalankan promosi lebih terstruktur (rata-rata diskon 13.9% vs 12.1% reguler) dengan harga dasar yang lebih terlindungi.

### 3. Keunggulan Biaya Sentra Konveksi (H4: Jawa Barat vs DKI Jakarta)
* **Temuan**: Kategori fesyen menunjukkan disparitas harga regional yang tajam ($p = 1.20 \times 10^{-6}$). Seller di sentra konveksi Jawa Barat (Bandung & sekitarnya) mencatat median harga **Rp 104.999** (966 listing), jauh lebih murah daripada reseller DKI Jakarta (**Rp 129.000**) dan Jawa Tengah (**Rp 189.578**).

---

## 🎯 Rekomendasi Strategis untuk Seller & Brand

| No | Rekomendasi Tindakan | Hipotesis Pendukung | Estimasi Dampak | Tingkat Keyakinan | Cara Validasi di Dunia Nyata |
|---|---|---|---|---|---|
| 1 | **Pangkas Diskon Maksimal ke 20–25%**<br>Hindari diskon di atas 30% yang tidak memberikan kenaikan median volume. | H1 (Titik Jenuh Diskon) | Peningkatan margin kotor +5% s/d +12% poin per unit | **Tinggi (High)** | A/B testing diskon pada 20 SKU terlaris selama 14 hari kampanye Payday. |
| 2 | **Investasi Upgrade ke Status Official Store**<br>Manfaatkan pricing power badge untuk menaikkan ASP. | H6 (Official Store Effect) | ASP naik hingga +50% dengan konversi volume naik 2.2x | **Tinggi (High)** | Analisis ROI pendaftaran official/pro store vs biaya admin tambahan Tokopedia. |
| 3 | **Format Judul: Spesifikasi di Awal untuk Produk Komoditas**<br>Gunakan nama bahan/ukuran di awal kata judul produk. | H5 (Spesifikasi Judul) | Volume penjualan naik +80% (median 50 → 90 unit) | **Sedang (Medium)** | Uji format judul (SEO kata kunci bahan di 30 karakter pertama) pada produk basic/fast-moving. |
| 4 | **Diferensiasi Non-Harga untuk Reseller Luar Jawa Barat**<br>Fokus pada bundling dan kecepatan pengiriman lokal. | H4 (Regional Pricing) | Melindungi margin dari perang harga produsen langsung | **Sedang (Medium)** | Buat paket bundling 3-in-1 untuk menghindari perbandingan harga langsung per SKU. |

---

## 🛠️ Stack & Reproducibility

- **Data Pipeline**: dbt Core 1.9.4 + DuckDB 1.10.1 (14/14 data tests passed).
- **Interactive Simulator**: Streamlit (`app/streamlit_app.py`).
- **Data Mart Export**: `data/fct_listing.csv` (20.976 listing siap dihubungkan ke BI tools).
