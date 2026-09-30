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

## Temuan Awal (dari Data Card Kaggle — diverifikasi ulang di notebook)

| Temuan | Nilai dari Data Card | Nilai Terverifikasi | Dampak |
|---|---|---|---|
| Total baris | 29.519 | — | — |
| Kolom | 9 | — | — |
| Listing diskon < 5% | ~69% | — | Analisis diskon hanya ~31% listing |
| Rating 4.75–5.0 | ~83% | — | H3 berisiko; fallback: pakai ulasan |
| Lokasi "Indonesia" | ~10% | — | Exclude dari analisis wilayah |
| Placeholder `Tokopedia Seller` | ~4% | — | Flag & exclude |
| Baris imputasi (ulasan == terjual) | Beberapa | — | Flag & uji sensitifitas |

---

## Distribusi Kategori (diisi di Fase 0)

| Kategori | Jumlah Listing | % dari Total | Cukup untuk analisis? |
|---|---|---|---|
| Fashion Wanita | — | — | — |
| Fashion Pria | — | — | — |
| Elektronik | — | — | — |
| Rumah Tangga | — | — | — |
| Hewan Peliharaan | — | — | — |
| Lainnya | — | — | — |

---

## Keputusan Gate

- [ ] **Scope**: Lanjut lintas kategori ✅ (sudah diputuskan — pivot dari fashion-only)
- [ ] **Stack**: Konfirmasi free tier tools masih available
- [ ] **Asumsi A1–A3**: Nilai default sudah diisi di `assumptions.md`

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
