# Requirements Document

> **Proyek**: Tokopedia E-Commerce Pricing & Promo Analytics
> **Scope**: Lintas kategori — 29.519 listing Tokopedia
> **Versi**: v2 (pivot dari fashion-only ke cross-category)

---

## Stakeholder & Pertanyaan Keputusan

| Stakeholder | Pertanyaan | Keputusan yang Didukung |
|---|---|---|
| Performance Marketing Lead | Di tingkat diskon berapa penjualan berhenti naik, per kategori? | Menetapkan batas diskon campaign per kategori |
| Commercial Director | Jika diskon dipangkas X%, berapa margin yang diselamatkan dan berapa volume yang hilang? | Persetujuan perubahan strategi diskon |
| Head of Merchandising | Di mana fokus GMV — kategori dan tier harga mana yang paling berkontribusi? | Prioritas assortment dan promosi |

---

## Hipotesis (ringkas — detail di `hypotheses.md`)

H1 · H2 · H3 · H4 · H5 · H6 — lihat [`hypotheses.md`](hypotheses.md)

---

## Metrik & Definisi

| Metrik | Definisi | Catatan |
|---|---|---|
| GMV proxy | `harga × terjual` | Terjual kumulatif dan dibulatkan — gunakan sebagai proksi, bukan nilai pasti |
| Harga normal | `harga / (1 − diskon/100)` jika diskon > 0, else `harga` | Tidak ada kolom harga coret di dataset |
| Margin per unit | `harga_normal × (1 − HPP%) − fee − ongkos` | Bergantung asumsi A1–A3 |
| Margin total | `margin_per_unit × terjual` | Terjual adalah proxy |
| Bucket diskon | 0%, 1–10%, 11–20%, 21–30%, 31–50%, >50% | |
| Tier harga | Q33 bawah, Q33–Q66 menengah, >Q66 atas | Per kategori |
| Wilayah | Normalisasi kota → wilayah (Jawa Barat, DKI Jakarta, dll.) | Exclude "Indonesia" |

---

## Dashboard — Acceptance Criteria

### Halaman 1: Diskon & Penjualan
- [ ] Dapat difilter per kategori
- [ ] Menampilkan median terjual per bucket diskon
- [ ] Titik jenuh ditandai
- [ ] Jumlah listing per bucket tampil
- [ ] Hasil sama jika difilter berbeda (tidak ada data silang)

### Halaman 2: Peta Harga & GMV
- [ ] Dapat difilter wilayah dan kategori
- [ ] Tabel panas GMV proxy per kategori × tier harga
- [ ] Lifetime GMV dan jumlah listing tampil per sel
- [ ] Dapat difilter ke level wilayah

### Halaman 3: Profil Kategori
- [ ] Minimal 3 chart berbeda per kategori dalam satu view
- [ ] Distribusi harga, diskon, rating

---

## Simulator Margin — Acceptance Criteria

- [ ] Input: kategori, diskon sekarang, diskon baru, HPP %, fee %, biaya lain
- [ ] Output: margin per unit sebelum/sesudah, perkiraan perubahan volume (sebagai rentang)
- [ ] Semua asumsi tampil dengan nilai default & sumbernya
- [ ] Hasil sama dengan perhitungan manual untuk 3 kasus uji

---

## User Stories

1. **Performance Marketing Lead** — Saat memilih satu kategori, saya melihat median terjual per bucket diskon dan titik jenuh yang ditandai beserta jumlah listing per bucket.

2. **Commercial Director** — Saat saya mengubah HPP atau fee, margin per unit dan margin total langsung berubah, dan asumsi yang dipakai tampil di layar.

3. **Head of Merchandising** — Saya bisa menyaring berdasarkan wilayah dan melihat nilai GMV proxy serta jumlah listing per sel kategori × tier harga.
