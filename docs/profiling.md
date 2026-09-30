# Hasil Profiling — Gate Fase 0 & Audit Pipeline

> **Status**: Selesai (Gate Fase 0 Terverifikasi & Diaudit pada 30 September 2026)
> **Dataset**: Indonesia E-Commerce Dataset: Tokopedia Listings (Kaggle)
> **Scope**: Lintas kategori (20.976 listing bersih)

---

## Gate Checks

| Gate | Target | Hasil | Status |
|---|---|---|---|
| Total baris setelah deduplikasi & cleaning | ≥ 20.000 | 20.976 | PASS |
| Jumlah listing berdiskon (diskon > 5%) | ≥ 5.000 | 6.853 | PASS |
| Akurasi parser `Terjual` | 100% baris ter-parse | 20.976 (100%) | PASS |
| Kategori teridentifikasi dari nama produk | ≥ 75% baris | 78,99% (16.568 baris) | PASS |
| Variasi rating cukup untuk H3 | Std dev rating > 0,1 | 0,24 | PASS |

---

## Funnel Pembersihan Data (Raw ke Mart)

| Tahap Pembersihan | Baris | % Raw | Catatan Kualitas Data |
|---|---:|---:|---|
| **Raw CSV** | **29.519** | **100%** | Dataset scrape mentah |
| − Duplikat (URL + nama produk) | −513 | 1,7% | Dideduplikasi di model staging |
| − Placeholder halaman search/kategori & 'Tokopedia Seller' | −7.976 | 27,0% | Listing non-produk/dummy teridentifikasi |
| − Harga ≤ 0 | −31 | 0,1% | Data anomali harga nol/negatif |
| − Parse error & lain-lain | −23 | 0,1% | URL/karakter rusak |
| **Mart Akhir `fct_listing`** | **20.976** | **71,1%** | Siap untuk pemodelan analitik |

---

## Temuan Profiling Terverifikasi

| Temuan | Nilai dari Data Card | Nilai Terverifikasi | Dampak & Catatan Audit |
|---|---|---|---|
| Total baris raw | 29.519 | 29.519 | Baseline awal |
| Baris duplikat (URL+nama) | Tidak diketahui | 513 | Dideduplikasi di staging |
| Placeholder dibuang | ~4% | 7.976 (27,0%) | Mart akhir merepresentasikan 71,1% listing raw |
| Listing diskon = 0% | ~69% | 61,6% | Analisis diskon pada 38,4% listing |
| Rating std dev | — | 0,24 | Variasi cukup untuk uji statistik |
| Rating 4.75–5.0 | ~83% | 89,3% | Sangat terkompresi; uji H3 wajib kontrol ulasan ≥ 30 |
| is_imputed (ulasan==terjual) | Beberapa | 25,2% | Di-flag untuk kontrol sensitivitas |
| is_official_store | — | 23,3% | Diturunkan dari nama toko (seller-level heuristic) |
| Lokasi 'Indonesia' | ~10% | 9,6% raw / 7,4% mart | Dieksklusikan dari analisis regional |
| DKI Jakarta dominan | — | 47,5% | Populasi data miring ke wilayah Jabodetabek |

---

## Distribusi Kategori (dari dbt mart fct_listing)

| Kategori | Jumlah Listing | % dari Total | Status |
|---|---|---|---|
| lainnya | 4.408 | 21,0% | Sisa baseline |
| rumah_tangga | 3.657 | 17,4% | Dominan |
| sepatu_aksesori | 2.472 | 11,8% | Teridentifikasi |
| elektronik | 2.054 | 9,8% | Teridentifikasi |
| kecantikan | 2.053 | 9,8% | Teridentifikasi |
| fashion_umum | 1.365 | 6,5% | Teridentifikasi |
| otomotif_perkakas | 1.247 | 5,9% | Teridentifikasi |
| makanan_minuman | 865 | 4,1% | Teridentifikasi |
| atk_kemasan | 714 | 3,4% | Teridentifikasi |
| fashion_wanita | 648 | 3,1% | Teridentifikasi |
| mainan_hobi | 634 | 3,0% | Teridentifikasi |
| fashion_pria | 452 | 2,2% | Teridentifikasi |
| olahraga | 259 | 1,2% | Teridentifikasi |
| kesehatan_bayi | 90 | 0,4% | Teridentifikasi |
| hewan_peliharaan | 58 | 0,3% | Teridentifikasi |
| **Total** | **20.976** | **100,0%** | **Coverage: 78,99%** |

---

## Keputusan Gate

- [x] **Scope**: Lanjut lintas kategori
- [x] **Deduplication**: 513 baris duplikat di-handle di staging
- [x] **Stack**: DuckDB + dbt-duckdb 1.9.4 confirmed working
- [x] **dbt build**: 3 model + 11 test PASS
- [x] **Kategori coverage**: 78,99% (target ≥ 75% tercapai)
- [x] **Asumsi A1–A5**: Draft tersedia di `assumptions.md`

## Aksi Lanjutan (Fase 4 & 5)

1. Eksekusi pengujian hipotesis H1–H6 di notebook / script analisis
2. Bangun margin simulator & dashboard interaktif (Streamlit)
3. Evaluasi sensitivitas `is_imputed` (25.2%) pada analisis regresi / H1-H6

---

## Catatan Parser `Terjual`

Format yang harus ditangani:
```
"1rb+ terjual"   → 1000
"4 rb+ Terjual"  → 4000
"3.5rb terjual"  → 3500
"4.95rb+ terjual"→ 4950
"terjual 200"    → 200
```

Regex yang direkomendasikan: `(\d+\.?\d*)\s*rb` → kali 1000; handle spasi, huruf besar/kecil, desimal, tanda `+`.
