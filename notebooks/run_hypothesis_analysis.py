"""
run_hypothesis_analysis.py
===========================
Fase 4: Pengujian Hipotesis H1 - H6
Menggunakan fct_listing dari data/tokped.duckdb
Menghasilkan uji statistik formal, metrik bisnis, dan visualisasi.
"""

import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os

# Setup style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, sans-serif'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
os.makedirs('reports/figures', exist_ok=True)

# 1. Load Data
con = duckdb.connect('data/tokped.duckdb')
df = con.execute("SELECT * FROM fct_listing").df()
con.close()

print(f"Loaded {len(df):,} listings from fct_listing.")
print(f"Categories: {df['kategori'].nunique()} | Regions: {df['wilayah'].nunique()}")
print("=" * 60)

# ==============================================================================
# H1: DISCOUNT SATURATION POINT
# Hipotesis: Di atas tingkat diskon tertentu, penjualan tidak lagi naik (titik jenuh).
# ==============================================================================
print("\n" + "="*20 + " H1: DISCOUNT SATURATION POINT " + "="*20)

# Median terjual per bucket diskon
h1_bucket = df.groupby(['bucket_diskon_order', 'bucket_diskon']).agg(
    count=('listing_id', 'count'),
    median_terjual=('terjual', 'median'),
    mean_terjual=('terjual', 'mean'),
    median_harga=('harga', 'median'),
    median_ulasan=('jumlah_ulasan', 'median')
).reset_index().sort_values('bucket_diskon_order')

print("\n--- Penjualan per Bucket Diskon (All Data) ---")
print(h1_bucket[['bucket_diskon', 'count', 'median_terjual', 'mean_terjual']])

# Cek per kategori utama (top 5 non-lainnya)
top_cats = df[df['kategori'] != 'lainnya']['kategori'].value_counts().head(5).index.tolist()
h1_cat_bucket = df[df['kategori'].isin(top_cats)].groupby(
    ['kategori', 'bucket_diskon_order', 'bucket_diskon']
)['terjual'].median().unstack(level='kategori')
print("\n--- Median Terjual per Kategori & Bucket Diskon ---")
print(h1_cat_bucket)

# OLS Regression dengan kontrol log(terjual + 1)
# Kontrol: diskon_pct, tier_harga, log(jumlah_ulasan + 1), wilayah, is_official_store
df['log_terjual'] = np.log1p(df['terjual'])
df['log_ulasan'] = np.log1p(df['jumlah_ulasan'])
df['diskon_sq'] = (df['diskon_pct'] / 100.0) ** 2  # Cek kurvatur / diminishing return

reg_data = df.dropna(subset=['log_terjual', 'diskon_pct', 'log_ulasan', 'tier_harga', 'wilayah'])
model_h1 = smf.ols('log_terjual ~ diskon_pct + diskon_sq + log_ulasan + C(tier_harga) + C(is_official_store)', data=reg_data).fit()

print("\n--- OLS Model H1 (Pengaruh Diskon & Kuadrat Diskon) ---")
print(model_h1.summary().tables[1])

# Visualisasi H1
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Median terjual per bucket
sns.barplot(data=h1_bucket, x='bucket_diskon', y='median_terjual', color='#2563eb', ax=ax1)
ax1.set_title('Median Terjual per Bucket Diskon', fontsize=12, fontweight='bold')
ax1.set_xlabel('Bucket Diskon')
ax1.set_ylabel('Median Unit Terjual')
for i, v in enumerate(h1_bucket['median_terjual']):
    ax1.text(i, v + 2, f"{int(v):,}", ha='center', fontweight='bold', fontsize=9)

# Plot 2: Kurva per Top Kategori
for cat in top_cats:
    cat_data = df[df['kategori'] == cat].groupby('bucket_diskon_order')['terjual'].median()
    labels = h1_bucket.set_index('bucket_diskon_order')['bucket_diskon'].to_dict()
    ax2.plot([labels.get(k) for k in cat_data.index], cat_data.values, marker='o', label=cat, linewidth=2)

ax2.set_title('Kurva Diskon vs. Penjualan per Kategori', fontsize=12, fontweight='bold')
ax2.set_xlabel('Bucket Diskon')
ax2.set_ylabel('Median Unit Terjual')
ax2.legend(fontsize=8)
plt.tight_layout()
plt.savefig('reports/figures/h1_discount_saturation.png', dpi=300)
plt.close()
print("Saved: reports/figures/h1_discount_saturation.png")


# ==============================================================================
# H2: MUSIMAN VS UTILITARIAN RESPONSIVENESS
# Hipotesis: Kategori utilitarian lebih elastis terhadap diskon dibanding kategori fesyen/musiman.
# ==============================================================================
print("\n" + "="*20 + " H2: ELASTISITAS KATEGORI " + "="*20)

# Klasifikasi sederhana:
# Utilitarian: rumah_tangga, elektronik, otomotif_perkakas, atk_kemasan
# Fesyen/Musiman: fashion_wanita, fashion_pria, fashion_umum, sepatu_aksesori
util_cats = ['rumah_tangga', 'elektronik', 'otomotif_perkakas', 'atk_kemasan']
fash_cats = ['fashion_wanita', 'fashion_pria', 'fashion_umum', 'sepatu_aksesori']

df_h2 = df[df['kategori'].isin(util_cats + fash_cats)].copy()
df_h2['group_kategori'] = df_h2['kategori'].apply(lambda x: 'Utilitarian' if x in util_cats else 'Fashion')

model_h2 = smf.ols('log_terjual ~ diskon_pct * C(group_kategori) + log_ulasan + C(tier_harga)', data=df_h2).fit()
print("\n--- OLS Interaction: Diskon * Group Kategori ---")
print(model_h2.summary().tables[1])

# Visualisasi H2
fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(data=df_h2[df_h2['group_kategori'] == 'Utilitarian'], x='diskon_pct', y='log_terjual',
            scatter_kws={'alpha': 0.1, 'color': '#0284c7'}, line_kws={'color': '#0284c7', 'label': 'Utilitarian (Rumah Tangga/Elektronik)'}, ax=ax)
sns.regplot(data=df_h2[df_h2['group_kategori'] == 'Fashion'], x='diskon_pct', y='log_terjual',
            scatter_kws={'alpha': 0.1, 'color': '#e11d48'}, line_kws={'color': '#e11d48', 'label': 'Fashion (Pakaian/Sepatu/Aksesori)'}, ax=ax)
ax.set_title('Responsivitas Diskon: Utilitarian vs Fashion', fontsize=12, fontweight='bold')
ax.set_xlabel('Diskon (%)')
ax.set_ylabel('Log(Terjual + 1)')
ax.legend()
plt.tight_layout()
plt.savefig('reports/figures/h2_category_responsiveness.png', dpi=300)
plt.close()
print("Saved: reports/figures/h2_category_responsiveness.png")


# ==============================================================================
# H3: PRICE TIER VS RATING
# Hipotesis: Tier harga bawah memiliki rating lebih rendah (filter ulasan >= 30)
# ==============================================================================
print("\n" + "="*20 + " H3: PRICE TIER VS RATING " + "="*20)

h3_df = df[(df['jumlah_ulasan'] >= 30) & (df['rating'].notnull())].copy()
print(f"Sample dengan ulasan >= 30: {len(h3_df):,} baris")

h3_stats = h3_df.groupby('tier_harga')['rating'].agg(['count', 'mean', 'median', 'std']).reindex(['bawah', 'menengah', 'atas'])
print("\n--- Rating per Tier Harga (Ulasan >= 30) ---")
print(h3_stats)

# Kruskal-Wallis test (karena rating non-normal & skewed ke 5.0)
groups_h3 = [group['rating'].values for _, group in h3_df.groupby('tier_harga')]
kw_stat, kw_p = stats.kruskal(*groups_h3)
print(f"\nKruskal-Wallis Test: H-stat = {kw_stat:.4f}, p-value = {kw_p:.4e}")

# Mann-Whitney U test bawah vs atas
bawah_ratings = h3_df[h3_df['tier_harga'] == 'bawah']['rating']
atas_ratings = h3_df[h3_df['tier_harga'] == 'atas']['rating']
u_stat, u_p = stats.mannwhitneyu(bawah_ratings, atas_ratings, alternative='two-sided')
print(f"Mann-Whitney U (Bawah vs Atas): U-stat = {u_stat:.1f}, p-value = {u_p:.4e}")

# Visualisasi H3
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
sns.boxplot(data=h3_df, x='tier_harga', y='rating', order=['bawah', 'menengah', 'atas'], palette='Blues', ax=ax1)
ax1.set_title('Distribusi Rating per Tier Harga (Ulasan ≥ 30)', fontsize=11, fontweight='bold')
ax1.set_ylim(4.0, 5.05)

sns.kdeplot(data=h3_df, x='rating', hue='tier_harga', common_norm=False, palette='Set2', ax=ax2)
ax2.set_title('Density Rating per Tier Harga', fontsize=11, fontweight='bold')
ax2.set_xlim(4.2, 5.05)
plt.tight_layout()
plt.savefig('reports/figures/h3_price_tier_rating.png', dpi=300)
plt.close()
print("Saved: reports/figures/h3_price_tier_rating.png")


# ==============================================================================
# H4: REGIONAL PRICING
# Hipotesis: Sentra produksi/konveksi memiliki harga lebih rendah untuk kategori yang sama.
# ==============================================================================
print("\n" + "="*20 + " H4: REGIONAL PRICING " + "="*20)

# Filter wilayah valid (exclude Tidak Diketahui)
h4_df = df[~df['wilayah'].isin(['Tidak Diketahui', 'Indonesia'])].copy()
h4_wilayah = h4_df.groupby('wilayah')['harga'].agg(['count', 'median', 'mean']).sort_values('median')
print("\n--- Median Harga per Wilayah (All Categories) ---")
print(h4_wilayah)

# Median harga per wilayah untuk fashion
fash_all = ['fashion_wanita', 'fashion_pria', 'fashion_umum', 'sepatu_aksesori']
h4_fash = h4_df[h4_df['kategori'].isin(fash_all)].groupby('wilayah')['harga'].agg(['count', 'median']).sort_values('median')
print("\n--- Median Harga Fashion per Wilayah ---")
print(h4_fash)

# Kruskal-Wallis across regions for fashion
groups_h4 = [group['harga'].values for _, group in h4_df[h4_df['kategori'].isin(fash_all)].groupby('wilayah')]
kw_h4, p_h4 = stats.kruskal(*groups_h4)
print(f"Kruskal-Wallis Fashion Price across Regions: H = {kw_h4:.2f}, p-value = {p_h4:.4e}")

# Visualisasi H4
fig, ax = plt.subplots(figsize=(10, 5))
top_wilayah = h4_df['wilayah'].value_counts().head(6).index
sns.boxplot(data=h4_df[(h4_df['wilayah'].isin(top_wilayah)) & (h4_df['kategori'].isin(fash_all))],
            x='wilayah', y='harga', showfliers=False, palette='mako', ax=ax)
ax.set_title('Distribusi Harga Fashion di Wilayah Utama (Tanpa Outliers)', fontsize=12, fontweight='bold')
ax.set_xlabel('Wilayah')
ax.set_ylabel('Harga (Rp)')
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('reports/figures/h4_regional_pricing.png', dpi=300)
plt.close()
print("Saved: reports/figures/h4_regional_pricing.png")


# ==============================================================================
# H5: MATERIAL / SPEC KEYWORD IN TITLE
# Hipotesis: Menyebut spesifikasi di awal judul diasosiasikan dengan harga & terjual lebih tinggi.
# ==============================================================================
print("\n" + "="*20 + " H5: SPESIFIKASI DI JUDUL " + "="*20)

h5_spec = df.groupby('has_spec_at_start').agg(
    count=('listing_id', 'count'),
    median_harga=('harga', 'median'),
    median_terjual=('terjual', 'median'),
    median_ulasan=('jumlah_ulasan', 'median')
)
print("\n--- Efek Spesifikasi di Awal Judul (has_spec_at_start) ---")
print(h5_spec)

# Mann-Whitney U test untuk harga dan penjualan
p_harga = stats.mannwhitneyu(df[df['has_spec_at_start']]['harga'], df[~df['has_spec_at_start']]['harga']).pvalue
p_terjual = stats.mannwhitneyu(df[df['has_spec_at_start']]['terjual'], df[~df['has_spec_at_start']]['terjual']).pvalue
print(f"Mann-Whitney U Harga: p = {p_harga:.4e}")
print(f"Mann-Whitney U Terjual: p = {p_terjual:.4e}")

# Visualisasi H5
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
sns.barplot(data=df, x='has_spec_at_start', y='harga', estimator=np.median, palette='Blues', ax=ax1)
ax1.set_title('Median Harga (Rp) vs Spesifikasi di Awal Judul', fontsize=11, fontweight='bold')
ax1.set_xlabel('Spesifikasi di Awal Judul')
ax1.set_ylabel('Median Harga (Rp)')
ax1.set_xticklabels(['Tidak / Tengah', 'Ya (Di Awal)'])

sns.barplot(data=df, x='has_spec_at_start', y='terjual', estimator=np.median, palette='Greens', ax=ax2)
ax2.set_title('Median Unit Terjual vs Spesifikasi di Awal Judul', fontsize=11, fontweight='bold')
ax2.set_xlabel('Spesifikasi di Awal Judul')
ax2.set_ylabel('Median Terjual')
ax2.set_xticklabels(['Tidak / Tengah', 'Ya (Di Awal)'])
plt.tight_layout()
plt.savefig('reports/figures/h5_spec_keyword.png', dpi=300)
plt.close()
print("Saved: reports/figures/h5_spec_keyword.png")


# ==============================================================================
# H6: OFFICIAL STORE EFFECT
# Hipotesis: Toko official memasang diskon lebih rendah tapi menjual lebih banyak.
# ==============================================================================
print("\n" + "="*20 + " H6: OFFICIAL STORE EFFECT " + "="*20)

h6_stats = df.groupby('is_official_store').agg(
    count=('listing_id', 'count'),
    median_diskon=('diskon_pct', 'median'),
    mean_diskon=('diskon_pct', 'mean'),
    median_terjual=('terjual', 'median'),
    mean_terjual=('terjual', 'mean'),
    median_harga=('harga', 'median'),
    median_rating=('rating', 'median')
)
print("\n--- Perbandingan Official Store vs Reguler ---")
print(h6_stats)

u_diskon, p_diskon = stats.mannwhitneyu(df[df['is_official_store']]['diskon_pct'], df[~df['is_official_store']]['diskon_pct'])
u_terjual, p_terjual = stats.mannwhitneyu(df[df['is_official_store']]['terjual'], df[~df['is_official_store']]['terjual'])
print(f"Mann-Whitney U Diskon: p = {p_diskon:.4e}")
print(f"Mann-Whitney U Terjual: p = {p_terjual:.4e}")

# Visualisasi H6
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
sns.barplot(data=df, x='is_official_store', y='diskon_pct', estimator=np.mean, palette='Purples', ax=ax1)
ax1.set_title('Rata-rata Diskon (%): Official vs Reguler', fontsize=11, fontweight='bold')
ax1.set_xticklabels(['Reguler', 'Official Store'])
ax1.set_ylabel('Mean Diskon (%)')

sns.barplot(data=df, x='is_official_store', y='terjual', estimator=np.median, palette='Oranges', ax=ax2)
ax2.set_title('Median Terjual: Official vs Reguler', fontsize=11, fontweight='bold')
ax2.set_xticklabels(['Reguler', 'Official Store'])
ax2.set_ylabel('Median Terjual')
plt.tight_layout()
plt.savefig('reports/figures/h6_official_store.png', dpi=300)
plt.close()
print("Saved: reports/figures/h6_official_store.png")

print("\n" + "="*60)
print("ANALISIS H1 - H6 SELESAI LENGKAP!")
print("Semua visualisasi tersimpan di reports/figures/")
