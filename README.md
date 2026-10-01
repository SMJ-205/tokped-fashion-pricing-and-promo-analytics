# Tokopedia E-Commerce Pricing & Promo Analytics

> **Status Proyek**: **Selesai (Fase 0 - Fase 6)**
> **Scope**: Lintas Kategori (20.976 listing bersih Tokopedia di 14 kategori produk)
> **Stack**: DuckDB + dbt Core 1.9.4 + Python + Streamlit Community Cloud

---

## Pertanyaan Bisnis & Tiga Temuan Kunci

### 1. Di diskon berapa penjualan berhenti naik?
> **Jawaban: Diskon 1–10% memberikan dorongan volume terbesar; di atas 20%, tambahan volume tidak sepadan dengan margin yang dikorbankan.**
* Listing tanpa diskon (0%) mencatat median penjualan **26 unit** (11,6% listing mencapai ≥1.000 terjual).
* Diskon 1–10% menggandakan porsi listing laris menjadi **22,8%** dengan median terjual melonjak ke **100 unit**.
* Di atas 20%, pertambahan porsi listing laris melambat tajam (21–30%: 29,6%; 31–50%: 27,5%; >50%: 31,6%), sementara median bertahan flat di angka 100 unit akibat batas bawah bin platform (`100+ terjual`).
* Penurunan rata-rata volume di atas 30% yang semula teramati hilang setelah outlier top 1% (≥50.000 terjual) dikeluarkan (mean trimmed: 1.426 unit pada 21–30% vs 1.244 unit pada 31–50% dan 1.503 unit pada >50%). Tidak ada bukti volume turun di diskon ekstrem, namun ketiadaan kenaikan yang substansial membuktikan pemborosan margin. Korelasi Spearman diskon vs terjual pada listing berdiskon hanya **0,08**.

### 2. Berapa margin yang bisa diselamatkan jika diskon dipangkas?
> **Jawaban: Memangkas diskon dari 35% ke 20% melipatgandakan margin bersih per unit (+110%).**
* Berdasarkan unit economics simulator pada produk dengan harga normal Rp 100.000, HPP 45% (Rp 45.000), admin fee marketplace 6,5%, dan biaya packing Rp 3.000:
  * **Diskon 35%**: Harga jual Rp 65.000, fee Rp 4.225, menghasilkan margin bersih **Rp 12.775 per unit** (margin 19,7%).
  * **Diskon 20%**: Harga jual Rp 80.000, fee Rp 5.200, menghasilkan margin bersih **Rp 26.800 per unit** (margin 33,5%).
* Penghematan margin mencapai **+Rp 14.025 per unit (+109,8%)**. Pada volume 500 unit/bulan, diskon 20% menghasilkan tambahan laba kotor **+Rp 7.012.500**. Diskon 20% tetap lebih menguntungkan selama penurunan volume penjualan tidak melebihi **52%**.

### 3. Di mana fokus daya saing harga & kekuatan merek?
> **Jawaban: Official Store unggul volume di 11 dari 12 kategori dengan premium bervariasi; disparitas harga regional dipengaruhi bauran subkategori.**
* **Official Store Effect (H6)**: Memiliki median penjualan **90 unit** vs **40 unit** toko reguler (+125% lebih tinggi, $p < 0.001$). Namun, harga premium agregat (+55,4%, Rp 147.000 vs Rp 94.600) sebagian besar merupakan efek bauran kategori: premium harga bervariasi luas mulai dari −20% (ATK) hingga +413% (Mainan & Hobi), dengan 7 dari 12 kategori memiliki premium di bawah +55%.
* **Analisis Regional Pakaian (H4)**: Setelah mapping wilayah diperbaiki ke tingkat kabupaten dan subkategori pakaian dipisahkan dari sepatu/aksesori, Jawa Barat **bukan** wilayah termurah. Median harga pakaian: Jawa Timur (**Rp 95.500**), DKI Jakarta (**Rp 99.000**), Jawa Barat (**Rp 104.000**), Jawa Tengah (**Rp 107.000**), dan Banten (**Rp 126.000**) (Kruskal-Wallis $p = 0,018$).

---

## Rekomendasi Strategis

| No | Rekomendasi Tindakan | Hipotesis Pendukung | Estimasi Dampak | Tingkat Keyakinan | Cara Validasi di Dunia Nyata |
|---|---|---|---|---|---|
| 1 | **Terapkan Diskon Taktis 10–20% untuk Kampanye Reguler**<br>Hindari *deep discounting* (>30%) yang tidak memberikan pertambahan volume sepadan. | H1 (Saturation Curve) | Margin bersih per unit naik hingga 2x lipat (+Rp 14.000/unit) | **Tinggi (High)** | A/B testing diskon pada 20 SKU terlaris selama 14 hari kampanye gajian. |
| 2 | **Evaluasi ROI Official Store per Kategori Produk**<br>Fokuskan investasi official store pada kategori dengan pricing power terbukti (aksesori, perlengkapan rumah, otomotif). | H6 (Official Store Effect) | Volume konversi 2,2x lebih tinggi dengan margin terjaga | **Tinggi (High)** | Analisis biaya pendaftaran official store vs tambahan volume & gross profit per kategori. |
| 3 | **Letakkan Spesifikasi di Awal Judul Produk Komoditas**<br>Gunakan nama bahan/tipe di 30 karakter pertama untuk produk kebutuhan pokok/fast-moving. | H5 (Spesifikasi Judul) | Volume penjualan median naik dari 50 ke 90 unit (+80%) | **Sedang (Medium)** | Uji format judul SEO pada produk basic selama 30 hari (perhatikan kontrol bauran kategori). |
| 4 | **Perbaiki Data Pipeline & Monitoring Anomali**<br>Terapkan mapping wilayah kabupaten, capping outlier harga/GMV, dan flag bin penjualan platform. | Audit Kualitas Data | Mencegah distorsi estimasi GMV dan kesalahan kesimpulan regional | **Tinggi (High)** | Tambahkan dbt data tests untuk accepted ranges, seed mapping kabupaten, dan flag outlier GMV. |

---

## Live Simulator & Artifacts

| Artifact | Deskripsi | Lokasi / Link |
|---|---|---|
| **Slide Presentasi (Google Slides)** | Deck presentasi business analytics & portofolio eksekutif | [Google Slides Presentation](https://docs.google.com/presentation/d/1IlnnU1m7jjdqyjmsLOqFnLdQxVT99lUOQarIKMo6fO8/preview?slide=id.p12) |
| **Web Dashboard** | Interactive Web Dashboard (Vercel deployment) dengan unit economics simulator | `index.html`, `app.js`, `style.css` |
| **Margin Simulator App** | Interactive Streamlit Dashboard & Unit Economics Simulator | `app/streamlit_app.py` |
| **Data Mart Export** | Clean analytical dataset siap sambung ke BI tools (Tableau/Looker) | `data/fct_listing.csv` (6.0 MB, 20.976 baris) |
| **Audit Kualitas Data** | Hasil audit independen, single source of truth, dan evaluasi hipotesis | [`docs/audit_findings.md`](docs/audit_findings.md) |
| **Executive Summary** | Ringkasan analitis eksekutif 1 halaman | [`reports/executive_summary.md`](reports/executive_summary.md) |
| **Hypothesis Testing Docs** | Detail uji statistik H1–H6 (OLS, Kruskal-Wallis, Mann-Whitney U) | [`docs/hypotheses.md`](docs/hypotheses.md) |
| **Profiling Report** | Hasil gate check Fase 0, funnel cleaning data, dan perbaikan coverage | [`docs/profiling.md`](docs/profiling.md) |
| **Visualisasi Analisis** | Grafik kurva diskon, peta regional, dan official store | `reports/figures/` |

---

## Keterbatasan Data

1. **Funnel Pembersihan & Sampel**: Dari 29.519 baris raw, 7.976 baris (27,0%) adalah placeholder halaman pencarian/kategori dan akun `Tokopedia Seller` yang dibuang, sehingga mart akhir merepresentasikan 71,1% listing valid (20.976 baris).
2. **Artefak Bin Penjualan Platform**: Sekitar 40% nilai metrik `terjual` berupa format pembulatan platform (misal `100+ terjual`, `1rb+ terjual`), di mana 10–13% listing di setiap bucket diskon bernilai tepat 100.
3. **Konsentrasi Ekstrem GMV Proxy**: Sebanyak 27 listing bernilai ≥ Rp 100 juta (listing kendaraan bermotor/alat berat) menyumbang 60% total GMV proxy, dan top 1% listing menyumbang 85% GMV. Total GMV mentah tidak layak digunakan tanpa trimming/capping.
4. **Deteksi Official Store Berbasis Pola Nama**: Status official store diturunkan dari heuristik penamaan toko pada data scraping, bukan verifikasi lencana resmi platform Tokopedia secara real-time.
5. **Kategori Rule-Based**: Kategori diturunkan dari keyword matching judul produk dengan coverage **78,99%** (16.568 baris ter-tag di 14 kategori, sisanya 21,0% di kategori `lainnya`).
6. **Variasi Rating Terkompresi**: 89,3% produk ber-rating berada di rentang 4,75–5,0; pengujian H3 dilakukan dengan kontrol ketat hanya pada produk dengan `jumlah_ulasan ≥ 30`.
7. **Imputasi Ulasan**: 25,2% listing memiliki `jumlah_ulasan == terjual` (di-flag sebagai `is_imputed` untuk kontrol sensitivitas).
8. **Lokasi Umum**: Lokasi bertuliskan "Indonesia" mencakup 9,6% data raw (7,4% di data mart) dan dieksklusikan dari analisis regional.

---

## Arsitektur & Cara Menjalankan Ulang

```
Raw CSV (Kaggle Tokopedia Listings - 29.519 baris)
    │
    ▼ read_csv_auto
DuckDB (`data/tokped.duckdb`)
    │
    ▼ dbt build (3 model + 11 test PASS)
├── `stg_listings` (deduplikasi 513 baris, type casting, parser regex terjual)
├── `int_clean_listings` (filter 7.976 placeholder & harga <= 0, normalisasi lokasi)
└── `fct_listing` (tagging 14 kategori, quantile tier harga, bucket diskon, flag fitur)
    │
    ├──► Analisis Statistik H1–H6 (`notebooks/run_hypothesis_analysis.py`)
    ├──► Export CSV untuk Tableau/Looker (`data/fct_listing.csv`)
    ├──► Web Dashboard Vercel (`index.html`, `app.js`, `style.css`)
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
