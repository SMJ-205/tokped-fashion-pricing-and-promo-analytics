# Hipotesis & Status

> Scope: **Lintas kategori** (semua 29.519 listing Tokopedia)
> Diperbarui: pivot dari fashion-only ke cross-category — semua hipotesis digeneralisasi.

---

## Daftar Hipotesis

| ID | Hipotesis | Metode Uji | Status |
|----|-----------|------------|--------|
| H1 | Di atas tingkat diskon tertentu, penjualan tidak lagi naik — dan titik jenuhnya berbeda per kategori | Median terjual per bucket diskon per kategori; regresi dengan kontrol tier harga, jumlah ulasan, lokasi | ⏳ Belum diuji |
| H2 | Kategori musiman (misal gamis, produk lebaran) kurang responsif terhadap diskon dibanding kategori utilitarian (misal kaos, perlengkapan rumah) | Bandingkan kemiringan hubungan diskon–penjualan antar kategori | ⏳ Belum diuji |
| H3 | Produk di tier harga terendah punya rating rata-rata lebih rendah — berlaku lintas kategori | Uji beda rating antar tier, hanya produk dengan ulasan ≥ 30 | ⏳ Belum diuji |
| H4 | Seller dari sentra produksi/konveksi (misal Bandung untuk fashion, Surabaya) memasang harga lebih rendah dibanding wilayah lain untuk kategori yang sama | Median harga per wilayah per kategori | ⏳ Belum diuji |
| H5 | Menyebut spesifikasi produk (bahan, ukuran, merek) di awal judul berasosiasi dengan harga dan penjualan lebih tinggi | Posisi keyword spesifikasi di judul vs. harga dan penjualan | ⏳ Belum diuji |
| H6 | Toko official memasang diskon lebih rendah namun menjual lebih banyak dibanding toko biasa — berlaku lintas kategori | Tandai toko official dari nama toko; bandingkan median diskon dan terjual per kategori | ⏳ Belum diuji |

---

## Template Hasil Uji (diisi Fase 4)

```
### H1 — Discount Saturation Point

- **Status**: [Didukung / Tidak Didukung / Tidak Bisa Diuji]
- **Temuan**: ...
- **Keterbatasan**: ...
- **Implikasi untuk simulator**: ...
```

---

## Catatan Metodologi

- Semua uji statistik menggunakan threshold p < 0.05, dengan koreksi Bonferroni jika multiple comparison
- Kontrol variabel: tier harga, jumlah ulasan, lokasi (untuk H1 & H2)
- H3 berisiko tidak bisa diuji jika variasi rating terlalu kecil (~83% listing di 4.75–5.0) → fallback: gunakan jumlah ulasan sebagai proksi engagement
- Baris placeholder (`Tokopedia Seller`) dan baris imputasi di-exclude dari semua analisis; analisis sensitifitas dijalankan dengan & tanpa baris tersebut
