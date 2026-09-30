"""
generate_seed.py
Buat data sintetik 500 baris untuk test dbt pipeline.
Jalankan dari root repo: python scripts/generate_seed.py
"""
import pandas as pd
import numpy as np
import os, random, re

random.seed(42)
np.random.seed(42)

# ── Konfigurasi ────────────────────────────────────────────────────────────────
N = 500

PRODUK_TEMPLATES = [
    # (nama_template, kategori_hint)
    ("Kaos Polos Cotton Combed 30s {color} Pria Wanita", "fashion_umum"),
    ("Kemeja Pria Lengan Panjang {color} Formal Casual", "fashion_pria"),
    ("Dress Wanita {adj} Cantik Elegan Bahan {material}", "fashion_wanita"),
    ("Gamis Syari {adj} Bahan Maxmara Premium", "fashion_wanita"),
    ("Hijab Pashmina {material} Polos Lembut {color}", "fashion_wanita"),
    ("Celana Jeans Pria Skinny Slim Fit Denim {color}", "fashion_pria"),
    ("Sepatu Sneakers {color} Casual Pria Wanita", "sepatu_aksesori"),
    ("Tas Wanita {adj} Import Kulit PU Tote Bag", "sepatu_aksesori"),
    ("Smartphone Android {adj} RAM 8GB 128GB", "elektronik"),
    ("Charger USB Type C Fast Charging {watt}W Original", "elektronik"),
    ("Earphone Bluetooth Wireless TWS {adj} Bass Stereo", "elektronik"),
    ("Skincare Serum Vitamin C {adj} Brightening 30ml", "kecantikan"),
    ("Sunscreen SPF {spf} PA+++ {adj} Daily Moisturizer", "kecantikan"),
    ("Body Lotion {adj} Glowing Whitening 250ml", "kecantikan"),
    ("Panci Teflon Anti Lengket {size}cm Frypan {adj}", "rumah_tangga"),
    ("Bantal Guling Set {adj} Dakron Premium Hypoallergenic", "rumah_tangga"),
    ("Rice Cooker Magic Com 1.8L {adj} Stainless Inner", "rumah_tangga"),
    ("Makanan Kucing Whiskas {adj} 480gr Dry Food Salmon", "hewan_peliharaan"),
    ("Pasir Kucing {adj} Clumping 5L Deodorizing", "hewan_peliharaan"),
    ("Dumbbell Barbel Set {weight}kg {adj} Rubber Gym", "olahraga"),
    ("Sepatu Olahraga Running {adj} {color} Ringan", "olahraga"),
    ("Snack Keripik {adj} Pedas Level {level} 200gr", "makanan_minuman"),
    ("Kopi Arabika {adj} Bubuk 250gr Single Origin", "makanan_minuman"),
]

COLORS = ["Hitam","Putih","Navy","Abu-abu","Merah","Biru","Hijau","Kuning","Pink","Cokelat"]
MATERIALS = ["Katun","Cotton","Polyester","Rayon","Linen","Sifon","Fleece","Denim","Wool","Kanvas"]
ADJS = ["Premium","Original","Import","Berkualitas","Terbaik","Murah","Branded","Eksklusif","Stylish","Modern"]
CITIES = [
    ("Jakarta Pusat","DKI Jakarta"), ("Jakarta Selatan","DKI Jakarta"),
    ("Bandung","Jawa Barat"), ("Bekasi","Jawa Barat"), ("Depok","Jawa Barat"),
    ("Surabaya","Jawa Timur"), ("Malang","Jawa Timur"),
    ("Semarang","Jawa Tengah"), ("Solo","Jawa Tengah"),
    ("Yogyakarta","DI Yogyakarta"),
    ("Medan","Sumatera Utara"), ("Palembang","Sumatera Selatan"),
    ("Makassar","Sulawesi Selatan"), ("Denpasar","Bali"),
    ("Indonesia","N/A"),
]
STORES = (
    ["Tokopedia Seller"] * 20 +           # placeholder ~4%
    [f"Toko {r}" for r in ["Maju","Jaya","Berkah","Sukses","Makmur","Indah","Laris","Bagus"]] * 40 +
    [f"{r} Official Store" for r in ["FashionID","TechWorld","BeautyHub","SportZone"]] * 10
)

rows = []
for i in range(N):
    tmpl_name, _ = random.choice(PRODUK_TEMPLATES)
    nama = tmpl_name.format(
        color=random.choice(COLORS),
        material=random.choice(MATERIALS),
        adj=random.choice(ADJS),
        watt=random.choice([18,25,33,45,65]),
        spf=random.choice([30,50]),
        size=random.choice([20,24,28,30]),
        weight=random.choice([2,5,10,20]),
        level=random.choice([1,2,3,4,5]),
    )

    harga_diskon = random.choice([
        random.randint(15_000, 100_000),   # fashion murah
        random.randint(50_000, 300_000),   # fashion menengah
        random.randint(200_000, 1_500_000),# elektronik/fashion premium
        random.randint(5_000, 50_000),     # fmcg
    ])
    diskon = random.choices([0]*69 + list(range(5, 81)), k=1)[0]  # ~69% no discount
    harga = int(harga_diskon * (1 - diskon/100)) if diskon > 0 else harga_diskon

    # Terjual dalam format asli dataset
    t = random.choices(
        [0, random.randint(1,999), random.randint(1000,9999), random.randint(10000,99999)],
        weights=[10, 40, 35, 15], k=1
    )[0]
    if t == 0:
        terjual_str = "0 terjual"
    elif t < 1000:
        terjual_str = f"{t} terjual"
    elif t < 10000:
        rb = t / 1000
        rb_str = f"{rb:.1f}".rstrip('0').rstrip('.')
        terjual_str = random.choice([f"{rb_str}rb+ terjual", f"{rb_str} rb+ Terjual", f"Terjual {rb_str}rb+"])
    else:
        rb = t / 1000
        rb_str = f"{rb:.1f}".rstrip('0').rstrip('.')
        terjual_str = f"{rb_str}rb+ terjual"

    # Ulasan
    ulasan_raw = max(0, int(t * random.uniform(0.05, 0.3)))
    # Kadang imputasi: ulasan == terjual
    if random.random() < 0.03:
        ulasan_raw = t
    if ulasan_raw >= 1000:
        u_rb = ulasan_raw / 1000
        ulasan_str = f"{u_rb:.1f}rb ulasan".rstrip('0').rstrip('.')
    else:
        ulasan_str = str(ulasan_raw)

    rating = 0.0 if ulasan_raw == 0 else round(random.gauss(4.85, 0.12), 1)
    rating = max(1.0, min(5.0, rating)) if ulasan_raw > 0 else 0.0

    city, _ = random.choice(CITIES)
    store = random.choice(STORES)
    is_placeholder_store = "Tokopedia Seller" in store
    url = f"https://tokopedia.com/search?q=dummy" if is_placeholder_store else f"https://tokopedia.com/{store.lower().replace(' ','-')}/product-{i}"

    rows.append({
        "Nama Produk": nama,
        "Nama Toko": store,
        "Lokasi Toko": city,
        "Terjual": terjual_str,
        "Jumlah Ulasan": ulasan_str,
        "Rating": rating,
        "Harga (IDR)": harga,
        "Diskon (%)": diskon if diskon > 0 else "",
        "Produk URL": url,
    })

df = pd.DataFrame(rows)
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/tokopedia_listings.csv", index=False)
print(f"✅ Generated {len(df)} rows → data/raw/tokopedia_listings.csv")
print(df.dtypes)
print(df.head(3).to_string())
