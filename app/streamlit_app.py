"""
app/streamlit_app.py
====================
E-Commerce Pricing & Promo Analytics Dashboard + Margin Simulator
Berbasis DuckDB mart fct_listing (Tokopedia Analytics)
"""

import streamlit as st
import duckdb
import pandas as pd
import numpy as np
import altair as alt
import os

# Page config
st.set_page_config(
    page_title="Tokopedia Pricing & Promo Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive look
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tokped.duckdb')
    if not os.path.exists(db_path):
        db_path = 'data/tokped.duckdb'
    con = duckdb.connect(db_path, read_only=True)
    df = con.execute("SELECT * FROM fct_listing").df()
    con.close()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat database DuckDB: {e}")
    st.stop()

# Header
st.markdown('<div class="main-title">Tokopedia E-Commerce Pricing & Promo Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analisis empiris titik jenuh diskon, elastisitas kategori, dan simulator margin keuntungan seller</div>', unsafe_allow_html=True)

# Tabs
tab_sim, tab_discount, tab_region, tab_store, tab_data = st.tabs([
    "Simulator Margin Promosi",
    "Analisis Diskon & Titik Jenuh (H1/H2)",
    "Peta Harga Regional (H4)",
    "Official Store & Spesifikasi (H3/H5/H6)",
    "Data Explorer"
])

# ==============================================================================
# TAB 1: SIMULATOR MARGIN PROMOSI
# ==============================================================================
with tab_sim:
    st.subheader("Simulator Dampak Diskon & Margin Per Unit")
    st.markdown("""
    Gunakan simulator ini untuk menguji trade-off antara **besaran diskon** dan **margin keuntungan bersih**.
    Proyeksi volume penjualan didasarkan pada temuan empiris **H1 (Discount Saturation Point)** dari 20.976 listing Tokopedia.
    """)

    col_input, col_result = st.columns([1, 1.4], gap="large")

    with col_input:
        st.markdown("#### Parameter Produk & Biaya")

        kategori_list = sorted([k for k in df['kategori'].unique() if k != 'lainnya'])
        selected_cat = st.selectbox("Pilih Kategori Produk", kategori_list, index=kategori_list.index("fashion_wanita") if "fashion_wanita" in kategori_list else 0)

        # Baseline stats for category
        cat_df = df[df['kategori'] == selected_cat]
        default_price = int(cat_df['harga_normal'].median()) if not cat_df.empty else 100000

        harga_normal = st.number_input("Harga Normal / Coret (Rp)", min_value=1000, max_value=10000000, value=default_price, step=5000)

        c1, c2 = st.columns(2)
        with c1:
            diskon_lama = st.slider("Diskon Saat Ini (%)", min_value=0, max_value=70, value=35, step=5)
        with c2:
            diskon_baru = st.slider("Diskon Baru yang Diuji (%)", min_value=0, max_value=70, value=20, step=5)

        st.markdown("##### Struktur Biaya & Fee Marketplace")
        c3, c4 = st.columns(2)
        with c3:
            hpp_pct = st.number_input("HPP (% dari Harga Normal)", min_value=10.0, max_value=90.0, value=45.0, step=2.5)
        with c4:
            admin_fee_pct = st.number_input("Admin / Commission Fee (%)", min_value=0.0, max_value=20.0, value=6.5, step=0.5)

        biaya_packing = st.number_input("Biaya Packing & Operasional Lain (Rp/Unit)", min_value=0, max_value=50000, value=3000, step=500)
        volume_basis = st.number_input("Estimasi Penjualan Bulanan Saat Ini (Unit)", min_value=10, max_value=100000, value=500, step=50)

    # Calculations
    hpp_rp = harga_normal * (hpp_pct / 100.0)

    # Status Lama
    harga_jual_lama = harga_normal * (1 - diskon_lama / 100.0)
    fee_lama = harga_jual_lama * (admin_fee_pct / 100.0)
    margin_lama_rp = harga_jual_lama - hpp_rp - fee_lama - biaya_packing
    margin_lama_pct = (margin_lama_rp / harga_jual_lama * 100) if harga_jual_lama > 0 else 0
    profit_lama_total = margin_lama_rp * volume_basis

    def estimate_volume_multiplier(old_disc, new_disc):
        def disc_score(d):
            if d == 0: return 1.0
            elif d <= 10: return 2.0
            elif d <= 20: return 2.6
            elif d <= 30: return 3.2 # Peak
            elif d <= 50: return 3.1 # Plateau
            else: return 3.0 # Over-discounting
        score_old = disc_score(old_disc)
        score_new = disc_score(new_disc)
        return score_new / score_old

    vol_mult = estimate_volume_multiplier(diskon_lama, diskon_baru)
    volume_baru_est = int(round(volume_basis * vol_mult))

    # Status Baru
    harga_jual_baru = harga_normal * (1 - diskon_baru / 100.0)
    fee_baru = harga_jual_baru * (admin_fee_pct / 100.0)
    margin_baru_rp = harga_jual_baru - hpp_rp - fee_baru - biaya_packing
    margin_baru_pct = (margin_baru_rp / harga_jual_baru * 100) if harga_jual_baru > 0 else 0
    profit_baru_total = margin_baru_rp * volume_baru_est

    selisih_profit = profit_baru_total - profit_lama_total
    selisih_margin_rp = margin_baru_rp - margin_lama_rp

    with col_result:
        st.markdown("#### Hasil Simulasi & Rekomendasi")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(
                label="Harga Jual Efektif",
                value=f"Rp {int(harga_jual_baru):,}",
                delta=f"{int(harga_jual_baru - harga_jual_lama):,} Rp"
            )
        with m2:
            st.metric(
                label="Margin Bersih / Unit",
                value=f"Rp {int(margin_baru_rp):,}",
                delta=f"{margin_baru_pct - margin_lama_pct:+.1f}% margin",
                delta_color="normal"
            )
        with m3:
            st.metric(
                label="Total Laba Kotor",
                value=f"Rp {int(profit_baru_total):,}",
                delta=f"{int(selisih_profit):,} Rp",
                delta_color="normal" if selisih_profit >= 0 else "inverse"
            )

        # Recommendation alert box
        if diskon_lama > 30 and diskon_baru <= 30 and selisih_profit > 0:
            st.success(f"""
            **REKOMENDASI: OPTIMALISASI DISKON KE {diskon_baru}%**
            Memangkas diskon dari {diskon_lama}% ke {diskon_baru}% menaikkan margin per unit sebesar **Rp {int(selisih_margin_rp):,}** (+{margin_baru_pct - margin_lama_pct:.1f}% poin).
            Berdasarkan temuan H1, volume penjualan berada di area optimal (tidak turun drastis), menghasilkan potensi kenaikan laba kotor **+Rp {int(selisih_profit):,} per bulan**.
            """)
        elif selisih_profit > 0:
            st.info(f"Skema diskon baru diperkirakan meningkatkan laba kotor sebesar **Rp {int(selisih_profit):,} / bulan**.")
        else:
            st.warning(f"Perubahan diskon ini diperkirakan mengurangi laba kotor sebesar **Rp {int(abs(selisih_profit)):,} / bulan**.")

        st.markdown("##### Perbandingan Detail")
        comp_df = pd.DataFrame({
            "Metrik": [
                "Harga Coret (Normal)",
                "Diskon Diterapkan",
                "Harga Jual Bersih",
                "HPP Pokok",
                "Admin Fee Marketplace",
                "Biaya Packing/Lain",
                "Margin Bersih / Unit (Rp)",
                "Margin Bersih / Unit (%)",
                "Proyeksi Volume Penjualan",
                "Estimasi Total Profit Kotor"
            ],
            "Kondisi Saat Ini": [
                f"Rp {int(harga_normal):,}",
                f"{diskon_lama}%",
                f"Rp {int(harga_jual_lama):,}",
                f"Rp {int(hpp_rp):,}",
                f"Rp {int(fee_lama):,}",
                f"Rp {int(biaya_packing):,}",
                f"Rp {int(margin_lama_rp):,}",
                f"{margin_lama_pct:.1f}%",
                f"{volume_basis:,} unit",
                f"Rp {int(profit_lama_total):,}"
            ],
            "Simulasi Diskon Baru": [
                f"Rp {int(harga_normal):,}",
                f"{diskon_baru}%",
                f"Rp {int(harga_jual_baru):,}",
                f"Rp {int(hpp_rp):,}",
                f"Rp {int(fee_baru):,}",
                f"Rp {int(biaya_packing):,}",
                f"Rp {int(margin_baru_rp):,}",
                f"{margin_baru_pct:.1f}%",
                f"{volume_baru_est:,} unit",
                f"Rp {int(profit_baru_total):,}"
            ]
        })
        st.dataframe(comp_df, hide_index=True, width=700)

# ==============================================================================
# TAB 2: ANALISIS DISKON & TITIK JENUH (H1/H2)
# ==============================================================================
with tab_discount:
    st.subheader("Kurva Penjualan & Titik Jenuh Diskon (H1 & H2)")
    st.markdown("""
    **Insight Utama H1:** Diskon taktis awal (1–10%) menggandakan porsi listing laris (11,6% ke 22,8%). Namun di atas 20%, median bertahan flat di 100 unit (artefak pembulatan platform) dan tambahan volume penjualan tidak sepadan dengan margin yang dikorbankan.
    """)

    col_cat_filter, col_opt = st.columns([1, 2])
    with col_cat_filter:
        cat_filter = st.selectbox(
            "Filter Kategori",
            ["Semua Kategori"] + sorted(list(df['kategori'].unique())),
            key="cat_filter_h1"
        )

    filt_df = df if cat_filter == "Semua Kategori" else df[df['kategori'] == cat_filter]

    bucket_stats = filt_df.groupby(['bucket_diskon_order', 'bucket_diskon']).agg(
        total_listing=('listing_id', 'count'),
        median_terjual=('terjual', 'median'),
        mean_terjual=('terjual', 'mean'),
        median_harga=('harga', 'median')
    ).reset_index().sort_values('bucket_diskon_order')

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("##### Median Unit Terjual per Bucket Diskon")
        chart_med = alt.Chart(bucket_stats).mark_bar(color='#2563eb', cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('bucket_diskon:N', sort=None, title='Bucket Diskon'),
            y=alt.Y('median_terjual:Q', title='Median Unit Terjual'),
            tooltip=['bucket_diskon', 'total_listing', 'median_terjual', 'mean_terjual']
        ).properties(height=350)
        st.altair_chart(chart_med, width=450)

    with c2:
        st.markdown("##### Rata-rata Unit Terjual (Peak di 21-30%)")
        chart_mean = alt.Chart(bucket_stats).mark_line(color='#dc2626', point=True, strokeWidth=3).encode(
            x=alt.X('bucket_diskon:N', sort=None, title='Bucket Diskon'),
            y=alt.Y('mean_terjual:Q', title='Rata-rata Unit Terjual'),
            tooltip=['bucket_diskon', 'total_listing', 'mean_terjual']
        ).properties(height=350)
        st.altair_chart(chart_mean, width=450)

    st.markdown("##### Distribusi Listing per Bucket Diskon")
    st.dataframe(bucket_stats[['bucket_diskon', 'total_listing', 'median_terjual', 'mean_terjual', 'median_harga']].rename(columns={
        'bucket_diskon': 'Bucket Diskon',
        'total_listing': 'Jumlah Listing',
        'median_terjual': 'Median Terjual (Unit)',
        'mean_terjual': 'Rata-rata Terjual (Unit)',
        'median_harga': 'Median Harga (Rp)'
    }), hide_index=True, width=800)

# ==============================================================================
# TAB 3: PETA HARGA REGIONAL (H4)
# ==============================================================================
with tab_region:
    st.subheader("Analisis Penetapan Harga Berdasarkan Wilayah (H4)")
    st.markdown("""
    **Insight Utama H4:** Analisis pakaian (pakaian saja, mapping kabupaten): Jawa Timur (Rp 95,5rb) dan DKI Jakarta (Rp 99rb) mencatat median harga pakaian lebih terjangkau dibanding Jawa Barat (Rp 104rb) dan Jawa Tengah (Rp 107rb) (p = 0.018).
    """)

    valid_region_df = df[~df['wilayah'].isin(['Tidak Diketahui', 'Indonesia'])].copy()

    reg_summary = valid_region_df.groupby('wilayah').agg(
        listing_count=('listing_id', 'count'),
        median_harga=('harga', 'median'),
        median_terjual=('terjual', 'median'),
        gmv_proxy_total=('gmv_proxy', 'sum')
    ).reset_index().sort_values('listing_count', ascending=False)

    top_regions = reg_summary.head(8)

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown("##### Median Harga Produk per Wilayah Utama")
        chart_reg = alt.Chart(top_regions).mark_bar(color='#0d9488').encode(
            x=alt.X('median_harga:Q', title='Median Harga (Rp)'),
            y=alt.Y('wilayah:N', sort='-x', title='Wilayah'),
            tooltip=['wilayah', 'listing_count', 'median_harga', 'median_terjual']
        ).properties(height=380)
        st.altair_chart(chart_reg, width=500)

    with c2:
        st.markdown("##### Ringkasan Wilayah")
        st.dataframe(top_regions.rename(columns={
            'wilayah': 'Wilayah',
            'listing_count': 'Listing',
            'median_harga': 'Median Harga (Rp)',
            'median_terjual': 'Median Terjual',
            'gmv_proxy_total': 'Total GMV Proxy (Rp)'
        }), hide_index=True, width=500)

# ==============================================================================
# TAB 4: OFFICIAL STORE & SPESIFIKASI (H3, H5, H6)
# ==============================================================================
with tab_store:
    st.subheader("Pengaruh Official Store, Rating, & Format Judul")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### H6: Official Store vs Toko Reguler")
        os_summary = df.groupby('is_official_store').agg(
            listing_count=('listing_id', 'count'),
            median_harga=('harga', 'median'),
            median_terjual=('terjual', 'median'),
            mean_diskon=('diskon_pct', 'mean')
        ).reset_index()
        os_summary['Tipe Toko'] = os_summary['is_official_store'].map({True: 'Official Store', False: 'Reguler'})

        st.dataframe(os_summary[['Tipe Toko', 'listing_count', 'median_harga', 'median_terjual', 'mean_diskon']].rename(columns={
            'listing_count': 'Jumlah Listing',
            'median_harga': 'Median Harga (Rp)',
            'median_terjual': 'Median Terjual',
            'mean_diskon': 'Rata-rata Diskon (%)'
        }), hide_index=True, width=450)

        st.info("Official store memiliki median penjualan 2.25x lipat (+125%) dan unggul volume di 11 dari 12 kategori. Premium harga agregat +55.4% bervariasi luas per kategori (-20% hingga +413%) sebagian besar akibat efek bauran kategori.")

    with c2:
        st.markdown("#### H5: Spesifikasi Produk di Awal Judul")
        spec_summary = df.groupby('has_spec_at_start').agg(
            listing_count=('listing_id', 'count'),
            median_harga=('harga', 'median'),
            median_terjual=('terjual', 'median')
        ).reset_index()
        spec_summary['Format Judul'] = spec_summary['has_spec_at_start'].map({True: 'Spesifikasi di Awal', False: 'Format Biasa'})

        st.dataframe(spec_summary[['Format Judul', 'listing_count', 'median_harga', 'median_terjual']].rename(columns={
            'listing_count': 'Jumlah Listing',
            'median_harga': 'Median Harga (Rp)',
            'median_terjual': 'Median Terjual'
        }), hide_index=True, width=450)

        st.info("Pencantuman spesifikasi di awal judul menaikkan volume median dari 50 ke 90 unit (+80%) pada produk komoditas fast-moving.")

    st.markdown("---")
    st.markdown("#### H3: Rating vs Tier Harga (Hanya Ulasan >= 30)")
    h3_sub = df[(df['jumlah_ulasan'] >= 30) & df['rating'].notnull()]
    h3_table = h3_sub.groupby('tier_harga')['rating'].agg(
        listing_count=('count'),
        mean_rating=('mean'),
        median_rating=('median'),
        std_rating=('std')
    ).reindex(['bawah', 'menengah', 'atas']).reset_index()

    st.dataframe(h3_table.rename(columns={
        'tier_harga': 'Tier Harga',
        'listing_count': 'Jumlah Listing',
        'mean_rating': 'Rata-rata Rating',
        'median_rating': 'Median Rating',
        'std_rating': 'Std Dev Rating'
    }), hide_index=True, width=600)

# ==============================================================================
# TAB 5: DATA EXPLORER
# ==============================================================================
with tab_data:
    st.subheader("Eksplorasi Data Mart (fct_listing)")
    st.write(f"Total baris dalam database: {len(df):,} listing")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cat_choice = st.multiselect("Kategori", options=sorted(df['kategori'].unique()), default=[])
    with col_f2:
        tier_choice = st.multiselect("Tier Harga", options=['bawah', 'menengah', 'atas'], default=[])
    with col_f3:
        os_choice = st.selectbox("Status Toko", ["Semua", "Official Store Saja", "Reguler Saja"])

    filtered_view = df.copy()
    if cat_choice:
        filtered_view = filtered_view[filtered_view['kategori'].isin(cat_choice)]
    if tier_choice:
        filtered_view = filtered_view[filtered_view['tier_harga'].isin(tier_choice)]
    if os_choice == "Official Store Saja":
        filtered_view = filtered_view[filtered_view['is_official_store'] == True]
    elif os_choice == "Reguler Saja":
        filtered_view = filtered_view[filtered_view['is_official_store'] == False]

    st.write(f"Menampilkan {len(filtered_view):,} baris data hasil filter:")
    cols_to_show = ['nama_produk', 'kategori', 'nama_toko', 'wilayah', 'harga', 'diskon_pct', 'tier_harga', 'terjual', 'rating', 'is_official_store']
    st.dataframe(filtered_view[cols_to_show].head(100), width=900)
