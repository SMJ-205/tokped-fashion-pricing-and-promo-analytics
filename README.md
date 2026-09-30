# Tokopedia E-Commerce Pricing & Promo Analytics

> **Status proyek**: 🚧 In Progress — Fase 0 (Profiling)

Analisis pricing dan promo pada 29.519 listing Tokopedia lintas kategori (fashion, elektronik, rumah tangga, kecantikan, hewan peliharaan, dan lainnya).

---

## Pertanyaan Bisnis

1. **Di diskon berapa penjualan berhenti naik?** — dan apakah titik jenuhnya berbeda per kategori?
2. **Berapa margin yang bisa diselamatkan** jika diskon dipangkas — dengan asumsi yang bisa disesuaikan sendiri?
3. **Di mana fokus GMV?** — kategori dan tier harga mana yang paling berkontribusi?

> ⚠️ Jawaban akan diisi setelah analisis selesai (Fase 4). Dokumen ini akan diperbarui dengan 3 temuan utama beserta angkanya.

---

## Rekomendasi

> Akan diisi setelah hipotesis H1–H6 diuji. Format: rekomendasi → hipotesis pendukung → tingkat keyakinan → cara validasi di dunia nyata.

---

## Links

| Artifact | Link |
|---|---|
| Dashboard | *(Tableau Public / Looker Studio — coming soon)* |
| Margin Simulator | *(Streamlit — coming soon)* |
| Deck | *(PDF — coming soon)* |

---

## Keterbatasan Data

- Data adalah **snapshot** tanpa tanggal pengambilan — bukan data time-series
- `Terjual` adalah nilai **kumulatif dan dibulatkan** (mis. "1rb+" = ≥ 1.000, bukan tepat 1.000)
- **Tanpa kategori resmi** — kategori diturunkan dari nama produk via keyword matching
- **Tanpa HPP** — margin dihitung berdasarkan asumsi yang bisa diubah pengguna
- **Tanpa data iklan** — tidak bisa membedakan penjualan organik vs. berbayar
- ~4% baris kemungkinan **placeholder** (di-exclude dari analisis)
- ~83% listing memiliki rating 4.75–5.0 — variasi rating sangat kecil

---

## Arsitektur & Cara Menjalankan Ulang

```
CSV (Kaggle)
    ↓ read_csv_auto
DuckDB (lokal)
    ↓ dbt build
  stg_listings → int_clean_listings → fct_listing
    ↓ export CSV
Tableau Public / Looker Studio    Streamlit Simulator
```

### Setup

```bash
# 1. Install dependencies
pip install dbt-duckdb duckdb pandas numpy matplotlib seaborn streamlit

# 2. Download dataset ke data/raw/tokopedia_listings.csv
#    https://www.kaggle.com/datasets/kanchana1990/indonesia-ecommerce-dataset-tokopedia-listings

# 3. Run profiling
cd notebooks && python 00_profiling.py

# 4. Run dbt
cd dbt && dbt build --profiles-dir . --project-dir .

# 5. Run simulator
cd app && streamlit run streamlit_app.py
```

### Stack (semua free tier)

| Kebutuhan | Tool |
|---|---|
| Warehouse | DuckDB (lokal) |
| Transformasi & test | dbt Core + dbt-duckdb |
| Notebook | Jupyter / Google Colab |
| Dashboard | Tableau Public (utama), Looker Studio (cadangan) |
| Simulator | Streamlit Community Cloud |
| Repo & CI | GitHub + GitHub Actions |

---

## Struktur Repo

```
├── docs/                    # requirements, hypotheses, assumptions, profiling
├── data/raw/                # CSV Kaggle (gitignored)
├── dbt/                     # staging → intermediate → mart + tests
├── notebooks/               # profiling & analisis H1–H6
├── app/                     # margin simulator (Streamlit)
├── reports/                 # laporan 1 halaman + deck PDF
└── .github/workflows/       # dbt build otomatis
```
