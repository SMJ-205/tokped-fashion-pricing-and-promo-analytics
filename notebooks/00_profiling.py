"""
Profiling notebook: 00_profiling.ipynb
Jalankan cell per cell; isi docs/profiling.md dengan hasil gate checks.
"""

# ── 0. Install & import ──────────────────────────────────────────────────────
# pip install duckdb pandas numpy matplotlib seaborn

import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")

DATA_PATH = "../data/raw/tokopedia_listings.csv"

# ── 1. Load raw ───────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"Shape: {df.shape}")
print(df.dtypes)
df.head(3)

# ── 2. Basic counts ───────────────────────────────────────────────────────────
print("=== Missing values ===")
print(df.isnull().sum())
print("\n=== Unique values per column ===")
print(df.nunique())

# ── 3. Parser: Terjual ────────────────────────────────────────────────────────
def parse_terjual(val):
    """
    Handles: '1rb+ terjual', '4 rb+ Terjual', '3.5rb terjual',
             '4.95rb+ terjual', 'terjual 200', '500', None
    Returns: int or np.nan
    """
    if pd.isna(val):
        return np.nan
    s = str(val).lower().replace(" ", "").replace("+", "")
    # Match: number (with optional decimal) followed by 'rb'
    m = re.search(r"(\d+\.?\d*)rb", s)
    if m:
        return int(float(m.group(1)) * 1000)
    # Plain number
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1))
    return np.nan

# Detect the correct column name (may vary)
terjual_col = [c for c in df.columns if "terjual" in c.lower() or "sold" in c.lower()][0]
print(f"Terjual column: {terjual_col}")

df["terjual_parsed"] = df[terjual_col].apply(parse_terjual)
print(f"Parse success rate: {df['terjual_parsed'].notna().mean():.1%}")
print(df["terjual_parsed"].describe())

# ── 4. Parser: Jumlah Ulasan ─────────────────────────────────────────────────
def parse_ulasan(val):
    if pd.isna(val):
        return np.nan
    s = str(val).lower().replace(" ", "").replace("+", "")
    m = re.search(r"(\d+\.?\d*)rb", s)
    if m:
        return int(float(m.group(1)) * 1000)
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1))
    return np.nan

ulasan_col = [c for c in df.columns if "ulasan" in c.lower() or "review" in c.lower()][0]
df["ulasan_parsed"] = df[ulasan_col].apply(parse_ulasan)
print(f"Ulasan parse success: {df['ulasan_parsed'].notna().mean():.1%}")

# ── 5. Flags: Placeholder & Imputasi ─────────────────────────────────────────
toko_col = [c for c in df.columns if "toko" in c.lower() or "store" in c.lower() or "shop" in c.lower()][0]
url_col  = [c for c in df.columns if "url" in c.lower()][0]

df["is_placeholder"] = (
    df[toko_col].str.lower().str.contains("tokopedia seller", na=False) |
    df[url_col].str.contains(r"search|kategori|q=", case=False, na=False)
)
print(f"\nPlaceholder rows: {df['is_placeholder'].sum()} ({df['is_placeholder'].mean():.1%})")

df["is_imputed"] = (
    df["ulasan_parsed"].notna() &
    df["terjual_parsed"].notna() &
    (df["ulasan_parsed"] == df["terjual_parsed"])
)
print(f"Suspected imputed rows: {df['is_imputed'].sum()} ({df['is_imputed'].mean():.1%})")

# ── 6. Price & Discount ───────────────────────────────────────────────────────
harga_col  = [c for c in df.columns if "harga" in c.lower() or "price" in c.lower()][0]
diskon_col = [c for c in df.columns if "diskon" in c.lower() or "discount" in c.lower()][0]

df["harga_num"]  = pd.to_numeric(df[harga_col],  errors="coerce")
df["diskon_num"] = pd.to_numeric(df[diskon_col], errors="coerce").fillna(0)
df["harga_normal"] = np.where(
    df["diskon_num"] > 0,
    df["harga_num"] / (1 - df["diskon_num"] / 100),
    df["harga_num"]
)

print(f"\nHarga describe:\n{df['harga_num'].describe()}")
print(f"\nDiskon (%) distribution:")
print(pd.cut(df["diskon_num"],
             bins=[-1, 0, 5, 10, 20, 30, 50, 100],
             labels=["0%","1-5%","6-10%","11-20%","21-30%","31-50%",">50%"]
             ).value_counts(normalize=True).sort_index())

# ── 7. GATE CHECK: Listing berdiskon ─────────────────────────────────────────
n_discounted = (df["diskon_num"] > 5).sum()
print(f"\n🔒 GATE — Listing diskon > 5%: {n_discounted} (target ≥ 5.000)")
print("✅ LOLOS" if n_discounted >= 5000 else "❌ GAGAL")

# ── 8. Rating distribution ────────────────────────────────────────────────────
rating_col = [c for c in df.columns if "rating" in c.lower()][0]
df["rating_num"] = pd.to_numeric(df[rating_col], errors="coerce")
# Rating 0 → NaN jika ulasan = 0
df.loc[(df["rating_num"] == 0) & (df["ulasan_parsed"] == 0), "rating_num"] = np.nan

print(f"\nRating describe:\n{df['rating_num'].describe()}")
print(f"Rating std dev: {df['rating_num'].std():.4f} (target > 0.1 for H3)")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df["rating_num"].hist(bins=20, ax=axes[0])
axes[0].set_title("Distribusi Rating")
(df["diskon_num"] > 0).value_counts().plot.bar(ax=axes[1])
axes[1].set_title("Ada Diskon vs. Tidak")
plt.tight_layout()
plt.savefig("../docs/profiling_charts.png", dpi=120)
plt.show()

# ── 9. Lokasi distribution ────────────────────────────────────────────────────
lokasi_col = [c for c in df.columns if "lokasi" in c.lower() or "location" in c.lower() or "city" in c.lower()][0]
print(f"\nLokasi 'Indonesia': {(df[lokasi_col].str.lower() == 'indonesia').sum()}")
print(f"Lokasi unique: {df[lokasi_col].nunique()}")
print(df[lokasi_col].value_counts().head(15))

# ── 10. Kategori tagging preview (cross-category) ────────────────────────────
nama_col = [c for c in df.columns if "nama" in c.lower() or "name" in c.lower() or "product" in c.lower()][0]

CATEGORY_KEYWORDS = {
    # Fashion Wanita
    "fashion_wanita": ["dress", "gamis", "hijab", "pashmina", "kebaya", "blouse",
                        "baju wanita", "rok", "legging", "daster"],
    # Fashion Pria
    "fashion_pria":   ["kemeja pria", "kaos pria", "celana pria", "polo", "batik pria",
                        "jaket pria", "baju koko", "sarung"],
    # Fashion Unisex / General
    "fashion_umum":   ["kaos", "celana", "jaket", "hoodie", "sweater", "t-shirt",
                        "tshirt", "baju", "kemeja", "jeans", "shorts"],
    # Sepatu & Aksesori
    "sepatu_tas":     ["sepatu", "sandal", "tas", "dompet", "topi", "kacamata",
                        "jam tangan", "ikat pinggang", "gelang", "kalung"],
    # Elektronik
    "elektronik":     ["hp", "handphone", "smartphone", "laptop", "tablet", "charger",
                        "kabel", "earphone", "headset", "speaker", "powerbank",
                        "keyboard", "mouse", "monitor"],
    # Rumah Tangga
    "rumah_tangga":   ["panci", "wajan", "spatula", "gelas", "piring", "mangkok",
                        "sapu", "pel", "ember", "taplak", "bantal", "selimut",
                        "rak", "lemari", "kursi", "meja"],
    # Kecantikan & Perawatan
    "kecantikan":     ["skincare", "serum", "moisturizer", "sunscreen", "lipstik",
                        "maskara", "foundation", "sabun muka", "shampoo", "kondisioner",
                        "body lotion", "parfum"],
    # Hewan Peliharaan
    "hewan_peliharaan": ["makanan kucing", "makanan anjing", "kandang", "akuarium",
                          "pasir kucing", "mainan kucing", "collar", "leash"],
    # Olahraga
    "olahraga":       ["raket", "bola", "sepatu olahraga", "gym", "dumbbell",
                        "matras", "jersey", "celana olahraga", "tas gym"],
    # Makanan & Minuman
    "makanan_minuman": ["snack", "kopi", "teh", "cokelat", "mie", "beras",
                         "bumbu", "saus", "minuman"],
}

def tag_category(nama):
    if pd.isna(nama):
        return "lainnya"
    nama_lower = str(nama).lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in nama_lower for kw in keywords):
            return cat
    return "lainnya"

df["kategori"] = df[nama_col].apply(tag_category)
cat_dist = df["kategori"].value_counts()
print(f"\n=== Distribusi Kategori ===")
print(cat_dist)
print(f"\nTagging coverage (non-'lainnya'): {(df['kategori'] != 'lainnya').mean():.1%}")

# ── 11. GATE: Coverage tagging ────────────────────────────────────────────────
coverage = (df["kategori"] != "lainnya").mean()
print(f"\n🔒 GATE — Kategori teridentifikasi: {coverage:.1%} (target ≥ 90%)")
print("✅ LOLOS" if coverage >= 0.90 else "⚠️  Di bawah target — perbaiki keyword list")

# ── 12. Summary untuk profiling.md ───────────────────────────────────────────
print("""
╔══════════════════════════════════════════════════════════╗
║  SUMMARY — salin ke docs/profiling.md                  ║
╠══════════════════════════════════════════════════════════╣
║  Total rows          : {total}                          ║
║  Placeholder rows    : {placeholder}                    ║
║  Imputed rows        : {imputed}                        ║
║  Listing diskon > 5% : {discounted}                     ║
║  Rating std dev      : {rating_std:.4f}                ║
║  Tagging coverage    : {coverage:.1%}                   ║
╚══════════════════════════════════════════════════════════╝
""".format(
    total=len(df),
    placeholder=df["is_placeholder"].sum(),
    imputed=df["is_imputed"].sum(),
    discounted=n_discounted,
    rating_std=df["rating_num"].std(),
    coverage=coverage,
))
