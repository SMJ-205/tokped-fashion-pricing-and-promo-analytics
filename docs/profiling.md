# Hasil Profiling — Gate Fase 0

> **Status**: ⏳ Belum dijalankan — isi setelah notebook `00_profiling.ipynb` selesai
> **Dataset**: Indonesia E-Commerce Dataset: Tokopedia Listings (Kaggle)
> **Scope**: Lintas kategori (pivot dari fashion-only)

---

## Gate Checks

| Gate | Target | Hasil | Status |
|---|---|---|---|
| Total baris setelah deduplikasi & cleaning | ≥ 20.000 | 20.976 | ✅ PASS |
| Jumlah listing berdiskon (diskon > 5%) | ≥ 5.000 | 6.853 | ✅ PASS |
| Akurasi parser `Terjual` | 100% baris ter-parse | 20.976 (100%) | ✅ PASS |
| Kategori teridentifikasi dari nama produk | ≥ 75% baris | 78.99% (16.568 baris) | ✅ PASS |
| Variasi rating cukup untuk H3 | Std dev rating > 0.1 | 0.24 | ✅ PASS |

---

## Temuan Awal (Diverifikasi dari Data Asli)

| Temuan | Nilai dari Data Card | Nilai Terverifikasi | Dampak |
|---|---|---|---|
| Total baris raw | 29.519 | 29.519 | — |
| Baris duplikat (URL+nama identik) | Tidak diketahui | 510 | Di-dedup di staging (ambil 1 per grup) |
| Listing diskon = 0% | ~69% | 61.6% | Analisis diskon pada 38.4% listing |
| Rating std dev | — | 0.24 | H3 bisa diuji ✅ |
| Rating 4.75–5.0 | ~83% | 89.3% | Sangat terkonsentrasi — H3 dengan kontrol ulasan |
| is_imputed (ulasan==terjual) | Beberapa | 25.2% | Tinggi — sensitifitas wajib |
| is_official_store | — | 23.3% | Untuk H6 ✅ |
| Lokasi 'Indonesia' | ~10% | ~5.7% | Exclude dari analisis wilayah |
| DKI Jakarta dominan | — | 47.5% | Analisis wilayah miring Jakarta |

---

## Distribusi Kategori (dari dbt mart fct_listing)

| Kategori | Jumlah Listing | % dari Total | Status |
|---|---|---|---|
| lainnya | 4.408 | 21.0% | Sisa baseline |
| rumah_tangga | 3.657 | 17.4% | ✅ Dominan |
| sepatu_aksesori | 2.472 | 11.8% | ✅ |
| elektronik | 2.054 | 9.8% | ✅ |
| kecantikan | 2.053 | 9.8% | ✅ |
| fashion_umum | 1.365 | 6.5% | ✅ |
| otomotif_perkakas | 1.247 | 5.9% | ✅ |
| makanan_minuman | 865 | 4.1% | ✅ |
| atk_kemasan | 714 | 3.4% | ✅ |
| fashion_wanita | 648 | 3.1% | ✅ |
| mainan_hobi | 634 | 3.0% | ✅ |
| fashion_pria | 452 | 2.2% | ✅ |
| olahraga | 259 | 1.2% | ✅ |
| kesehatan_bayi | 90 | 0.4% | ✅ |
| hewan_peliharaan | 58 | 0.3% | ✅ |
| **Total** | **20.976** | **100.0%** | **Coverage: 78.99%** |

---

## Keputusan Gate

- [x] **Scope**: Lanjut lintas kategori ✅
- [x] **Deduplication**: 510 baris duplikat di-handle di staging ✅
- [x] **Stack**: DuckDB + dbt-duckdb 1.10.1 confirmed working ✅
- [x] **dbt build**: 14/14 PASS ✅
- [x] **Kategori coverage**: 78.99% (target ≥ 75% tercapai) ✅
- [x] **Asumsi A1–A5**: Draft tersedia di `assumptions.md` ✅

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
