# Log Asumsi (untuk Simulator Margin)

> Scope: **Lintas kategori** — nilai default diisi per kategori di Fase 0.
> Semua asumsi bisa diubah pengguna di simulator; nilai default dan sumbernya selalu ditampilkan.

---

| ID | Asumsi | Nilai Default | Sumber / Catatan |
|----|--------|---------------|------------------|
| A1 | HPP sebagai persen dari harga normal | Diisi di Fase 0 per kategori | Estimasi dari artikel industri atau wawancara seller; bisa diubah pengguna |
| A2 | Fee marketplace (admin + program Tokopedia) | Diisi di Fase 0 | Halaman resmi Tokopedia Seller Center / Seller Education — **catat tanggal akses**; berbeda per kategori dan tipe toko |
| A3 | Ongkos tambahan per order (kemasan, dll.) | Diisi di Fase 0 | Estimasi; bisa diubah pengguna |
| A4 | Penurunan volume jika diskon dipangkas | Diambil dari hasil H1 per kategori | Asosiasi, bukan kausal; ditampilkan sebagai rentang (bukan angka tunggal) |
| A5 | Data mewakili kondisi pada tahun pengambilan dataset | Tahun dataset (tidak dicantumkan di sumber) | Kondisi fee dan pasar sekarang bisa berbeda — tuliskan keterbatasan ini di laporan |

---

## Cara Mengisi A1–A3 di Fase 0

1. **A2 (Fee Tokopedia)** — paling penting dan paling bisa diverifikasi:
   - Buka: https://seller.tokopedia.com/edu/biaya-layanan/ (catat tanggal akses)
   - Fee biasanya berbeda: toko biasa vs. toko official, per kategori
   - Contoh struktur: biaya admin % + biaya program (flash sale, dll.)

2. **A1 (HPP %)** — estimasi per kategori:
   - Fashion: ~30–50% dari harga jual (gross margin 50–70%)
   - Elektronik: ~70–80% dari harga jual (margin lebih tipis)
   - Rumah tangga: ~40–60%
   - Sumber: artikel industri e-commerce Indonesia; catat URL dan tanggal

3. **A3 (Ongkos kemasan)** — estimasi flat:
   - Rp 2.000–5.000 per order untuk kategori ringan
   - Rp 5.000–15.000 untuk kategori berat/fragile
