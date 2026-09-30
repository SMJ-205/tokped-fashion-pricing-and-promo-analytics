# Hasil Profiling — Gate Fase 0

> **Status**: ⏳ Belum dijalankan — isi setelah notebook `00_profiling.ipynb` selesai
> **Dataset**: Indonesia E-Commerce Dataset: Tokopedia Listings (Kaggle)
> **Scope**: Lintas kategori (pivot dari fashion-only)

---

## Gate Checks

| Gate | Target | Hasil | Status |
|---|---|---|---|
| Total baris setelah exclude placeholder | ≥ 28.000 | — | ⏳ |
| Jumlah listing berdiskon (diskon > 5%) | ≥ 5.000 | — | ⏳ |
| Akurasi parser `Terjual` | 100% baris ter-parse | — | ⏳ |
| Kategori teridentifikasi dari nama produk | ≥ 90% baris | — | ⏳ |
| Variasi rating cukup untuk H3 | Std dev rating > 0.1 | — | ⏳ |

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

## Distribusi Kategori (dari dbt mart)

| Kategori | Jumlah Listing | % dari Total | Status |
|---|---|---|---|
| lainnya | 10.246 | 48.8% | ⚠️ Perlu perbaikan keyword |
| sepatu_aksesori | 2.698 | 12.9% | ✅ |
| elektronik | 1.793 | 8.5% | ✅ |
| rumah_tangga | 1.719 | 8.2% | ✅ |
| fashion_umum | 1.285 | 6.1% | ✅ |
| kecantikan | 1.213 | 5.8% | ✅ |
| fashion_wanita | 689 | 3.3% | ✅ |
| fashion_pria | 498 | 2.4% | ✅ |
| makanan_minuman | 488 | 2.3% | ✅ |
| olahraga | 285 | 1.4% | ✅ |
| hewan_peliharaan | 62 | 0.3% | ✅ (sedikit) |
| **Total** | **20.976** | **100%** | |

---

## Keputusan Gate

- [x] **Scope**: Lanjut lintas kategori ✅
- [x] **Deduplication**: 510 baris duplikat di-handle di staging ✅
- [x] **Stack**: DuckDB + dbt-duckdb 1.10.1 confirmed working ✅
- [x] **dbt build**: 14/14 PASS ✅
- [ ] **Kategori coverage**: 51.2% — target ≥ 75% setelah tuning keyword di Fase 3
- [x] **Asumsi A1–A3**: Draft tersedia di `assumptions.md`

## Aksi Lanjutan (Fase 3)

1. Ekspansi keyword list — terutama untuk `lainnya` (10.246 baris) — target coverage ≥ 75%
2. Sample 200 listing dari `lainnya` untuk inspeksi manual kategori mana yang dominan
3. Flag sensitifitas `is_imputed` (25.2%!) — jalankan semua analisis dengan dan tanpa baris ini
4. Pertimbangkan apakah hewan_peliharaan (62 baris) cukup untuk analisis tersendiri atau gabung ke kategori lain

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
