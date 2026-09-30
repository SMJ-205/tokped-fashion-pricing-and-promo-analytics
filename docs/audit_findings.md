# Audit Kualitas Data & Hasil Analisis — Referensi Update Dokumentasi

> **Tanggal audit**: 30 September 2026
> **Objek audit**: `data/fct_listing.csv` (20.976 baris), `data/raw/produk_tokopedia.csv` (29.519 baris), model dbt, `reports/tokopedia_business_analytics_reference.docx`, README & docs.
> **Metode**: Hitung ulang independen dengan pandas / SciPy / statsmodels langsung dari CSV mart & raw, lalu dibandingkan dengan klaim di dokumentasi.
> **Deck hasil audit**: [Google Slides — Portofolio Deck](https://docs.google.com/presentation/d/1lcLq4jXliQDnPkvw5Pw7YGvxTehndD68pJepx7kA5r4/edit)

---

## 1. Ringkasan

| # | Temuan | Dampak | Prioritas |
|---|---|---|---|
| 1 | Placeholder yang dibuang **27,0%** (7.976 baris), bukan ~4% | Sampel akhir hanya 71% dari raw | Tinggi |
| 2 | "14/14 tests PASS" = **3 model + 11 test** | Klaim coverage test berlebihan | Sedang |
| 3 | Mapping wilayah di kode hanya kota besar → **1.672 baris "Lainnya"** (termasuk Garut, Cimahi, Tasikmalaya, Sleman) | H4 berubah kesimpulan | Tinggi |
| 4 | H4: setelah mapping diperbaiki & pakaian dipisah dari sepatu/aksesori, **Jabar bukan termurah** | Rekomendasi #4 (bundling vs Jabar) tidak didukung | Tinggi |
| 5 | H2: interaksi `diskon × utilitarian` **negatif** (−0,003; p = 0,012) dan tidak robust tanpa kontrol ulasan (p = 0,27) | Arah klaim berbalik | Tinggi |
| 6 | H1: "mean turun di atas 30%" hilang setelah top 1% (≥50rb terjual) dikeluarkan; median "flat 100" adalah artefak bin `100+ terjual` | Narasi H1 perlu dikualifikasi | Tinggi |
| 7 | H6: premium +55,4% sebagian besar **efek bauran kategori**; 7 dari 12 kategori premiumnya < +55% | Rekomendasi #2 perlu per kategori | Sedang |
| 8 | Simulator 35% → 20%: dokumen Rp17.750 → Rp29.800 tidak cocok dengan rumus/default app (Rp12.775 → Rp26.800) | Angka headline salah | Tinggi |
| 9 | 27 listing ≥ Rp100 juta (mobil) = **60% GMV proxy**; top 1% listing = 85% GMV | GMV total tidak layak dipakai mentah | Sedang |
| 10 | 237 `product_url` duplikat di mart (URL terpotong ke homepage), bukan ~73 | Deskripsi schema.yml salah | Rendah |
| 11 | Lokasi "Indonesia" = 9,6% raw / 7,4% mart, bukan 5,7% | Angka keterbatasan salah | Rendah |

Klaim yang **terverifikasi benar** (tidak perlu diubah): 20.976 baris mart, 6.853 listing diskon > 5%, coverage kategori 78,99%, is_imputed 25,2%, official 23,3%, rating 4,75–5,0 = 89,3% (dari listing yang punya rating), H3 mean per tier (4,863 / 4,881 / 4,902), H5 median 90 vs 50 unit & Rp68rb vs Rp104,9rb, H6 median 90 vs 40 unit & Rp147rb vs Rp94,6rb & diskon 13,9% vs 12,1%.

---

## 2. Angka Pengganti (single source of truth)

### Funnel cleaning (raw → mart)

| Tahap | Baris | % raw |
|---|---:|---:|
| Raw CSV | 29.519 | 100% |
| − Duplikat (URL + nama) | −513 | 1,7% |
| − Placeholder (URL search/kategori, `Tokopedia Seller`) | −7.976 | 27,0% |
| − Harga ≤ 0 | −31 | 0,1% |
| − Lain-lain (parse) | −23 | 0,1% |
| **Mart `fct_listing`** | **20.976** | **71,1%** |

### H1 — per bucket diskon

| Bucket | n | Median terjual | % listing ≥ 1rb | Mean (semua) | Mean (tanpa top 1%) |
|---|---:|---:|---:|---:|---:|
| 0% | 12.918 | 26 | 11,6% | 1.064 | 557 |
| 1–10% | 1.936 | 100 | 22,8% | 2.093 | 979 |
| 11–20% | 1.155 | 100 | 25,8% | 2.566 | 1.287 |
| 21–30% | 971 | 100 | 29,6% | 5.799 | 1.426 |
| 31–50% | 2.055 | 100 | 27,5% | 4.122 | 1.244 |
| >50% | 1.941 | 100 | 31,6% | 3.840 | 1.503 |

- 10–13% listing di setiap bucket bernilai tepat 100 (bin `100+ terjual`); ~40% seluruh nilai `terjual` adalah bin platform.
- Spearman ρ diskon vs terjual (hanya listing berdiskon) = **0,08**.
- **Kalimat baru**: *"Diskon 1–10% menggandakan porsi listing laris (11,6% → 22,8%). Di atas 20%, tambahannya hanya 2–6 poin; tidak ada bukti volume turun di diskon ekstrem, tetapi juga tidak ada kenaikan yang sepadan dengan margin yang dikorbankan."*

### H4 — median harga per wilayah (Rp ribu)

| Wilayah | Versi awal (fashion + sepatu/aksesori, mapping lama) | Audit (pakaian saja, mapping kabupaten) |
|---|---:|---:|
| Jawa Timur | 126,6 (n=286) | **95,5** (n=184) |
| DKI Jakarta | 129,0 (n=2.063) | **99,0** (n=945) |
| Jawa Barat | 105,0 (n=966) | **104,0** (n=648) |
| Jawa Tengah | 189,6 (n=60) | **107,0** (n=175) |
| Banten | 137,0 (n=426) | **126,0** (n=169) |

Kruskal-Wallis (pakaian, 5 wilayah): H = 11,94, **p = 0,018** (versi awal p = 1,2e-6). Tanpa Banten p = 0,048.

### H6 — premium median harga official vs reguler per kategori (kategori dengan ≥30 listing official)

ATK −20% · Kecantikan +4% · Fashion wanita +9% · Makanan +16% · Fashion pria +36% · Elektronik +50% · Fashion umum +53% · Sepatu & aksesori +56% · Rumah tangga +57% · Otomotif +74% · Olahraga +350% · Mainan & hobi +413%.
Volume official lebih tinggi di **11 dari 12** kategori (kecuali ATK & kemasan).

### H2 — OLS `log_terjual ~ diskon_pct * is_utilitarian + log_ulasan + C(tier_harga)`

| Koefisien | Estimasi | p |
|---|---:|---:|
| diskon_pct | +0,0221 | 1,3e-145 |
| diskon_pct : is_utilitarian | **−0,0034** | 0,012 |
| (tanpa `log_ulasan`) interaksi | −0,0018 | 0,27 |

### Simulator (default app: harga normal Rp100.000, HPP 45%, fee 6,5%, packing Rp3.000)

| | Diskon 35% | Diskon 20% |
|---|---:|---:|
| Harga jual | Rp65.000 | Rp80.000 |
| Fee marketplace | Rp4.225 | Rp5.200 |
| **Margin per unit** | **Rp12.775** | **Rp26.800** |
| Margin % | 19,7% | 33,5% |

Selisih +Rp14.025/unit (+110%). Volume impas: diskon 20% tetap lebih untung selama volume tidak turun lebih dari **52%**. Untuk 500 unit/bulan: +Rp7.012.500.

### Status hipotesis setelah audit

| ID | Awal | Setelah audit | Alasan singkat |
|---|---|---|---|
| H1 | ✅ Didukung | ⚠️ Didukung sebagian | Lonjakan di diskon awal nyata; penurunan >30% tidak robust |
| H2 | ✅ Didukung | ❌ Tidak didukung | Interaksi negatif & tidak robust |
| H3 | ✅ Didukung | ⚠️ Signifikan, efek kecil | Selisih 0,04 bintang; median semua tier 4,9 |
| H4 | ✅ Didukung | ❌ Tidak didukung | Jabar bukan termurah setelah mapping diperbaiki |
| H5 | ⚠️ Sebagian | ⚠️ Terkonfon kategori | 35% listing spec-di-awal adalah rumah tangga |
| H6 | ✅ Sebagian | ⚠️ Didukung sebagian | Volume unggul di 11/12 kategori; premium harga efek bauran |

---

## 3. Checklist Update per File

### `README.md`
- [ ] L16 — ganti narasi "mean memuncak di 21–30% lalu menurun" dengan kalimat baru H1 (bagian 2).
- [ ] L19–20 — ganti angka simulator: Rp12.775 → Rp26.800 (+Rp14.025/unit, +110%); hapus "+10% s/d +15%" dan "+68%".
- [ ] L23–25 — H6: tambah "premium bervariasi per kategori (−20% s.d. +413%)"; H4: ganti dengan tabel audit, hapus klaim "Jawa Barat memimpin efisiensi harga".
- [ ] L33 — rekomendasi #1: ubah batas "20–25%" menjadi "10–20%" untuk campaign reguler.
- [ ] L34 — rekomendasi #2: "Evaluasi ROI official store per kategori", hapus "ASP naik hingga +50%".
- [ ] L36 — rekomendasi #4 (bundling vs Jabar): hapus atau pindahkan ke "hipotesis lanjutan"; ganti dengan "Perbaiki pipeline (mapping kabupaten, flag outlier, test rentang)".
- [ ] L71 — `dbt build (14/14 tests PASS)` → `dbt build (3 model + 11 test PASS)`.
- [ ] Keterbatasan — tambah: sampel 71% dari raw; 40% nilai `terjual` adalah bin; GMV proxy didominasi 27 listing mobil; official store = proxy dari nama toko.

### `docs/hypotheses.md`
- [ ] L13–18 — update kolom Status sesuai tabel "Status hipotesis setelah audit".
- [ ] L26–37 (H1) — ganti bullet mean 5.799 / 4.121 / 3.840 dengan tabel H1 (termasuk kolom % ≥1rb & trimmed mean); tambah catatan bin `100+`.
- [ ] L43–50 (H2) — ganti temuan dengan koefisien interaksi negatif & uji robustness.
- [ ] L56+ (H3) — tambah interpretasi effect size (0,04 bintang).
- [ ] L72–79 (H4) — ganti dengan tabel H4 audit; L79 "5.7%" → "7,4% di mart (9,6% di raw)".
- [ ] L86+ (H5) — tambah catatan konfonding kategori (35% rumah tangga).
- [ ] L98+ (H6) — tambah daftar premium per kategori & keterbatasan deteksi official (IKEA Indonesia, AZKO ID tidak terdeteksi; `cigemoyofficial` ikut terhitung).

### `docs/profiling.md`
- [ ] L32 — "~5.7%" → "9,6% raw / 7,4% mart".
- [ ] L65 — "14/14 PASS" → "3 model + 11 test PASS".
- [ ] Tambah tabel funnel cleaning (bagian 2) dan baris "Placeholder dibuang: 7.976 (27,0%)".
- [ ] Status header masih "⏳ Belum dijalankan" — ubah ke selesai.

### `reports/executive_summary.md`
- [ ] L19 — narasi H1 (sama dengan README).
- [ ] L27 — H4: ganti p = 1,2e-6 & angka Jabar/Jakarta/Jateng dengan hasil audit.
- [ ] L35–38 — rekomendasi disamakan dengan README.
- [ ] L44 — "14/14 data tests" → "3 model + 11 test".

### `notebooks/generate_reference_doc.py` (sumber `.docx`) → lalu regenerate `reports/tokopedia_business_analytics_reference.docx`
- [ ] L338 — "Sekitar 4% … Tokopedia Seller" → "27,0% baris (7.976) adalah placeholder: URL halaman search/kategori dan akun 'Tokopedia Seller'".
- [ ] L339 — "5.7%" → "7,4% (mart)".
- [ ] L566–571 — tabel ringkasan hipotesis sesuai status audit; H2 "p = 0.018" → interaksi −0,0034 (p = 0,012), tidak robust.
- [ ] L585–597 — tabel & narasi H1; tambah kolom % ≥1rb.
- [ ] L604, L702 — tambah kualifikasi efek bauran kategori untuk H6.
- [ ] L613–614, L709 — angka H4 audit.
- [ ] L627–630, L729–730 — rekomendasi baru (bundling dihapus).
- [ ] L647, L723 — simulator Rp12.775 → Rp26.800 (+Rp14.025, +110%).
- [ ] L681 — "14 Data Tests PASS" → "3 model + 11 test PASS".
- [ ] **Cuplikan SQL di docx tidak sama dengan kode di repo** (docx: `hash(product_url)`, regex wilayah mencakup Garut/Cimahi; repo: `md5(url||nama)`, `LIKE` kota besar). Ambil cuplikan langsung dari file `.sql` saat generate, jangan ditulis ulang manual.

### Web dashboard — `index.html` (identik dengan `public/index.html` & `web/index.html`, update ketiganya atau hapus duplikat)
- [ ] L43–44 — KPI "20% - 30% / Diskon >30% Mengikis Margin" → mis. "1–10% / Diskon awal = 2× listing laris".
- [ ] L180 — "titik jenuh pada rentang diskon 20-30%" → narasi H1 baru.
- [ ] L223 — hapus klaim "Jawa Barat … signifikan lebih murah".
- [ ] L277 — tambah kualifikasi "bervariasi per kategori".
- [ ] `data/dashboard_data.json` (+ salinannya) — regenerate setelah perbaikan mapping wilayah.

### `app/streamlit_app.py`
- [ ] L247 — kualifikasi klaim ">30% mengikis margin" (volume tidak turun, tapi tidak naik sepadan).
- [ ] L302 — insight H4 diganti.
- [ ] L362 — tambah kualifikasi H6 per kategori.

### `dbt/models/schema.yml`
- [ ] L13 — "~73 baris" → "237 baris di mart (2.222 di raw)".

---

## 4. Perbaikan Pipeline (kode, bukan hanya dokumentasi)

1. **`int_clean_listings.sql` — mapping wilayah**: tambah kabupaten/kota Jawa Barat (Garut, Cimahi, Tasikmalaya, Cirebon, Sukabumi, Cianjur, Purwakarta, Subang, Sumedang, Kuningan, Majalengka, Indramayu, Ciamis, Kab. Bandung), DIY (Sleman, Bantul, Kulon Progo, Gunungkidul), Jawa Tengah (Jepara, Pekalongan, Klaten, Cilacap, Sukoharjo, Banyumas, Kudus, Tegal, Magelang, dll.), Jawa Timur (Mojokerto, Kediri, Pasuruan, Jember, Banyuwangi, dll.). Hasil uji: "Lainnya" turun dari 1.672 → 361. Lebih baik lagi: pindahkan mapping ke **seed CSV** (`seeds/lokasi_wilayah.csv`) dan `join`, bukan `CASE` panjang.
2. **Flag outlier** di `fct_listing`: `is_price_outlier = harga >= 100000000` dan `terjual_capped = least(terjual, p99)`; gunakan di semua agregasi GMV/mean.
3. **Kolom `is_terjual_binned`**: tandai nilai yang berasal dari format `+` (100+, 1rb+) agar analisis bisa membedakan nilai pasti vs batas bawah.
4. **Tambah test dbt**:
   - `accepted_values` untuk `kategori`, `bucket_diskon`, `wilayah`
   - `dbt_utils.accepted_range`: `rating` 1–5 (atau null), `diskon_pct` 0–99, `harga` > 0, `terjual` ≥ 0
   - `expression_is_true`: `harga_normal >= harga`, `gmv_proxy = harga * terjual`
   - test custom: jumlah baris placeholder yang dibuang dilog / di-warn jika > 30%
   - `relationships` / `not_null` pada `wilayah` dengan `severity: warn`
5. **Hapus artefak test basi** di `dbt/target/` (`unique_fct_listing_product_url` masih ada di compiled walau test sudah dihapus dari schema) — tambahkan `dbt/target/` ke `.gitignore`.
6. **Official store**: ganti deteksi berbasis nama toko dengan badge resmi (scrape) atau minimal whitelist brand official yang dikenal (IKEA Indonesia, AZKO ID, dll.).
7. **Notebook audit**: simpan script audit ini sebagai `notebooks/01_audit_robustness.py` agar angka di bagian 2 bisa direproduksi.
