# Executive Summary: Tokopedia Pricing & Promo Analytics

**Analisis Empiris Titik Jenuh Diskon, Kekuatan Merek, dan Trade-Off Margin pada 20.976 Listing E-Commerce**

---

## 📌 Ringkasan Eksekutif

Proyek ini mengevaluasi dinamika penetapan harga (*pricing*) dan efektivitas promosi (*promo analytics*) pada platform Tokopedia dengan menganalisis **20.976 listing bersih** lintas 14 kategori produk menggunakan stack modern data stack (*DuckDB, dbt Core, Python, dan Streamlit*).

Fokus utama adalah membedah fenomena perang diskon (*deep discounting*): apakah diskon besar selalu mendongkrak volume penjualan, dan pada titik mana diskon justru merugikan margin kotor seller?

---

## 💡 Tiga Temuan Kunci (Empirical Insights)

### 1. Pertumbuhan Terbesar di Diskon Awal (H1: Diskon 1–10% Gandakan Listing Laris)
* **Temuan**: Pemberian diskon taktis 1–10% menggandakan porsi listing laris (≥1.000 terjual) dari **11,6%** ke **22,8%** dengan median terjual melonjak dari 26 ke 100 unit. Namun, di atas diskon 20%, kurva volume penjualan mengalami plateau di mana median terjual bertahan flat di angka 100 unit (artefak bin platform `100+ terjual`) dan tambahan porsi listing laris melambat (hanya +2 hingga +6 poin persentase).
* **Evaluasi Trimmed Outlier**: Penurunan rata-rata volume di atas 30% yang tampak pada data mentah hilang setelah top 1% (≥50.000 unit) dikeluarkan (mean trimmed: 1.426 unit pada 21–30% vs 1.244 unit pada 31–50% dan 1.503 unit pada >50%). Korelasi Spearman diskon vs volume hanya **0,08**.
* **Implikasi Finansial**: Seller yang memberi diskon >30% mengorbankan margin tanpa mendapatkan kenaikan volume yang sepadan. Memangkas diskon dari 35% ke 20% menaikkan margin bersih per unit dari **Rp 12.775** ke **Rp 26.800** (+110%).

### 2. Efek Volume Official Store (H6: 2.25x Volume di 11 dari 12 Kategori)
* **Temuan**: Listing Official Store (23,3% dari total) memiliki median penjualan **90 unit** vs **40 unit** pada toko reguler (+125% lebih tinggi, $p < 0,001$) dan unggul di **11 dari 12 kategori produk**.
* **Harga Premium Bauran Kategori**: Angka agregat harga premium +55,4% (Rp 147.000 vs Rp 94.600) sebagian besar merupakan efek bauran kategori (premium bervariasi dari −20% di ATK hingga +413% di mainan/hobi; 7 dari 12 kategori memiliki premium di bawah +55%).

### 3. Realitas Disparitas Regional (H4: Jawa Timur dan DKI Jakarta Lebih Terjangkau pada Pakaian)
* **Temuan**: Setelah mapping wilayah diperbaiki ke tingkat kabupaten dan subkategori pakaian dipisahkan dari sepatu/aksesori, Jawa Barat **bukan** wilayah termurah. Median harga pakaian: Jawa Timur (**Rp 95.500**), DKI Jakarta (**Rp 99.000**), Jawa Barat (**Rp 104.000**), Jawa Tengah (**Rp 107.000**), dan Banten (**Rp 126.000**) (Kruskal-Wallis $p = 0,018$).

---

## 🎯 Rekomendasi Strategis untuk Seller & Brand

| No | Rekomendasi Tindakan | Hipotesis Pendukung | Estimasi Dampak | Tingkat Keyakinan | Cara Validasi di Dunia Nyata |
|---|---|---|---|---|---|
| 1 | **Terapkan Diskon Taktis 10–20% untuk Kampanye Reguler**<br>Hindari diskon di atas 30% yang tidak memberikan pertambahan volume sepadan. | H1 (Saturation Curve) | Margin bersih per unit naik hingga 2x lipat (+Rp 14.000/unit) | **Tinggi (High)** | A/B testing diskon pada 20 SKU terlaris selama 14 hari kampanye gajian. |
| 2 | **Evaluasi ROI Official Store per Kategori Produk**<br>Fokuskan investasi official store pada kategori dengan pricing power terbukti. | H6 (Official Store Effect) | Volume konversi 2,2x lebih tinggi dengan margin terjaga | **Tinggi (High)** | Analisis biaya pendaftaran official store vs tambahan volume & gross profit per kategori. |
| 3 | **Format Judul: Spesifikasi di Awal untuk Produk Komoditas**<br>Gunakan nama bahan/tipe di awal kata judul produk untuk produk kebutuhan pokok/fast-moving. | H5 (Spesifikasi Judul) | Volume penjualan naik +80% (median 50 → 90 unit) | **Sedang (Medium)** | Uji format judul SEO kata kunci bahan di 30 karakter pertama selama 30 hari. |
| 4 | **Perbaiki Pipeline Data & Pengendalian Anomali**<br>Terapkan mapping wilayah kabupaten, capping outlier GMV, dan kontrol bin penjualan platform. | Audit Kualitas Data | Mencegah distorsi estimasi GMV dan bias analisis regional | **Tinggi (High)** | Implementasikan dbt tests untuk rentang nilai wajar, seed mapping kabupaten, dan flag outlier GMV. |

---

## 🛠️ Stack & Reproducibility

- **Data Pipeline**: dbt Core 1.9.4 + DuckDB (3 model + 11 test PASS).
- **Web Dashboard**: Modern Static Web Dashboard Vercel.
- **Interactive Simulator**: Streamlit (`app/streamlit_app.py`).
- **Data Mart Export**: `data/fct_listing.csv` (20.976 listing bersih).
