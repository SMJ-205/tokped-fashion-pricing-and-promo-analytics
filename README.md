# Tokopedia E-Commerce Pricing & Promo Analytics

> **Status Proyek**: ✅ **Selesai (Fase 0 - Fase 6)**
> **Scope**: Lintas Kategori (20.976 listing bersih Tokopedia di 14 kategori produk)
> **Stack**: DuckDB + dbt Core 1.9.4 + Python + Streamlit Community Cloud

---

## 🎯 Pertanyaan Bisnis & Tiga Temuan Kunci

### 1. Di diskon berapa penjualan berhenti naik?
> **Jawaban: Titik jenuh berada di level diskon 20–30%.**
* Listing tanpa diskon mencatat median penjualan **26 unit** (rata-rata 1.064 unit).
* Diskon taktis awal (1–10% dan 11–20%) langsung melipatgandakan median penjualan ke **100 unit**.
* Namun di atas 20%, kurva volume penjualan mengalami **stagnasi total (plateau)**: median terjual flat di angka 100 unit untuk bucket 11–20%, 21–30%, 31–50%, dan >50%.
* Rata-rata volume penjualan memuncak di bucket **21–30% (5.799 unit)**, dan justru **menurun** di diskon ekstrem >30% (4.121 unit pada 31–50% dan 3.840 unit pada >50%). Seller yang memberi diskon >30% membakar margin tanpa mendapatkan peningkatan unit terjual.

### 2. Berapa margin yang bisa diselamatkan jika diskon dipangkas?
> **Jawaban: Memangkas diskon dari 35% ke 20% menyelamatkan margin kotor +10% s/d +15% per unit.**
* Berdasarkan simulator margin (`app/streamlit_app.py`), produk fashion dengan harga normal Rp 100.000 dan HPP 45% yang memangkas diskon dari 35% ke 20% meningkatkan margin bersih per unit dari **Rp 17.750** menjadi **Rp 29.800** (+68% peningkatan margin per unit) dengan volume penjualan tetap berada di zona optimal.

### 3. Di mana fokus daya saing harga & kekuatan merek?
> **Jawaban: Official Store menikmati volume 2.2x lipat dan harga premium +55%, sementara produsen Jawa Barat memimpin efisiensi harga.**
* **Official Store Effect (H6)**: Memiliki median penjualan **90 unit** vs **40 unit** toko reguler (+125% lebih tinggi, $p < 0.001$) dengan median harga **Rp 147.000** vs **Rp 94.600** (+55.4% harga premium).
* **Keunggulan Biaya Regional (H4)**: Seller sentra konveksi Jawa Barat (Bandung dsk.) memiliki median harga fashion **Rp 104.999**, jauh lebih rendah daripada DKI Jakarta (**Rp 129.000**) dan Jawa Tengah (**Rp 189.578**).

---

## 💡 Rekomendasi Strategis

| No | Rekomendasi Tindakan | Hipotesis Pendukung | Estimasi Dampak | Tingkat Keyakinan | Cara Validasi di Dunia Nyata |
|---|---|---|---|---|---|
| 1 | **Batasi Diskon Maksimal di 20–25%**<br>Hentikan *deep discounting* (>30%) yang tidak menambah median volume. | H1 (Saturation Point) | Kenaikan laba kotor unit +5% hingga +12% poin | **Tinggi (High)** | A/B testing diskon pada 20 SKU terlaris selama 14 hari kampanye Payday. |
| 2 | **Upgrade Status Toko ke Official Store**<br>Manfaatkan reputasi merek untuk mendapatkan harga premium. | H6 (Official Store) | ASP naik hingga +50% dengan konversi volume 2.2x | **Tinggi (High)** | Analisis biaya pendaftaran official store vs margin ekstra yang didapatkan. |
| 3 | **Letakkan Spesifikasi di Awal Judul Produk Komoditas**<br>Gunakan nama bahan/tipe di 30 karakter pertama. | H5 (Spesifikasi Judul) | Volume penjualan naik +80% (median 50 → 90 unit) | **Sedang (Medium)** | Uji format judul SEO pada produk basic/fast-moving selama 30 hari. |
| 4 | **Strategi Bundling untuk Reseller Non-Produsen**<br>Hindari perang harga per unit dengan sentra konveksi Jawa Barat. | H4 (Regional Pricing) | Melindungi margin kotor dari komparasi harga langsung | **Sedang (Medium)** | Luncurkan paket bundling 3-in-1 dengan diskon paket terbatas. |

---

## 🖥️ Live Simulator & Artifacts

| Artifact | Deskripsi | Lokasi / Link |
|---|---|---|
| **Margin Simulator App** | Interactive Streamlit Dashboard & Unit Economics Simulator | `app/streamlit_app.py` |
| **Data Mart Export** | Clean analytical dataset siap sambung ke BI tools (Tableau/Looker) | `data/fct_listing.csv` (6.0 MB, 20.976 baris) |
| **Executive Summary** | Ringkasan analitis eksekutif 1 halaman | [`reports/executive_summary.md`](reports/executive_summary.md) |
| **Hypothesis Testing Docs** | Detail uji statistik H1–H6 (OLS, Kruskal-Wallis, Mann-Whitney U) | [`docs/hypotheses.md`](docs/hypotheses.md) |
| **Profiling Report** | Hasil gate check Fase 0 & perbaikan coverage kategori | [`docs/profiling.md`](docs/profiling.md) |
| **Visualisasi Analisis** | Grafik kurva diskon, peta regional, dan official store | `reports/figures/` |

---

## ⚠️ Keterbatasan Data

1. **Snapshot Data**: Data adalah snapshot tunggal tanpa tanggal pengambilan (bukan time-series longitudinal).
2. **Nilai Terjual Dibulatkan**: Metrik `terjual` dibulatkan oleh platform (mis. "1rb+" di-parse sebagai 1.000).
3. **Kategori Rule-Based**: Kategori diturunkan dari keyword matching judul produk dengan coverage **78.99%** (16.568 baris ter-tag di 14 kategori, sisanya 21.0% di kategori `lainnya`).
4. **Variasi Rating Terkompresi**: 89.3% produk berada di rating 4.75–5.0; pengujian H3 dilakukan dengan kontrol ketat hanya pada produk dengan `jumlah_ulasan ≥ 30`.
5. **Imputasi Ulasan**: 25.2% listing memiliki `jumlah_ulasan == terjual` (di-flag sebagai `is_imputed` untuk kontrol sensitivitas).

---

## 🏗️ Arsitektur & Cara Menjalankan Ulang

```
Raw CSV (Kaggle Tokopedia Listings - 29.519 baris)
    │
    ▼ read_csv_auto
DuckDB (`data/tokped.duckdb`)
    │
    ▼ dbt build (14/14 tests PASS)
├── `stg_listings` (deduplikasi 510 baris, type casting, parser regex terjual)
├── `int_clean_listings` (cleaning harga, normalisasi wilayah kota → provinsi)
└── `fct_listing` (tagging 14 kategori, quantile tier harga, bucket diskon, flag fitur)
    │
    ├──► Analisis Statistik H1–H6 (`notebooks/run_hypothesis_analysis.py`)
    ├──► Export CSV untuk Tableau/Looker (`data/fct_listing.csv`)
    └──► Interactive Streamlit Margin Simulator (`app/streamlit_app.py`)
```

### Instruksi Menjalankan

```bash
# 1. Clone & install dependencies
git clone https://github.com/sarifmubdijantika/tokped-fashion-pricing-and-promo-analytics.git
cd tokped-fashion-pricing-and-promo-analytics
pip install dbt-duckdb duckdb pandas numpy matplotlib seaborn streamlit scipy statsmodels

# 2. Jalankan dbt pipeline (reproducible build & tests)
cd dbt
DBT_CSV_PATH="../data/raw/produk_tokopedia.csv" dbt build --profiles-dir . --project-dir .
cd ..

# 3. Jalankan pengujian statistik H1–H6
python3 notebooks/run_hypothesis_analysis.py

# 4. Jalankan interactive simulator & dashboard
streamlit run app/streamlit_app.py
```
