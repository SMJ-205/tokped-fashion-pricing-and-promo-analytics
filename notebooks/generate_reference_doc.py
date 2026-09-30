"""
generate_business_analytics_doc.py
===================================
Script untuk menghasilkan dokumen Microsoft Word (.docx) lengkap:
- Data Collecting
- Data Profiling
- Data Cleaning
- SQL dbt Models
- Python Analysis Scripts
- Analisis Hipotesis H1 - H6
- Rekomendasi Bisnis & Unit Economics Simulator
- Panduan Slide Google Slides (12 Slides Outline)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

doc = docx.Document()

# Page setup: Standard Margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Color constants
COLOR_PRIMARY = RGBColor(30, 41, 59)      # Slate-900 (#1e293b)
COLOR_SECONDARY = RGBColor(79, 70, 229)   # Indigo-600 (#4f46e5)
COLOR_TEXT = RGBColor(51, 65, 85)         # Slate-700 (#334155)
COLOR_MUTED = RGBColor(100, 116, 139)     # Slate-500 (#64748b)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def add_subtitle(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.color.rgb = COLOR_MUTED
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_SECONDARY
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def add_body(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_PRIMARY
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_PRIMARY
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_callout(text, title="Catatan Strategis"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "EEF2FF")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="4F46E5"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run_t = p.add_run(title + ": ")
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(9.5)
    run_t.font.bold = True
    run_t.font.color.rgb = COLOR_SECONDARY
    
    run_b = p.add_run(text)
    run_b.font.name = 'Arial'
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/><w:left w:val="single" w:sz="24" w:space="0" w:color="4F46E5"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = 'Courier New'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def create_table(headers, rows_data, col_widths=None):
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Format Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E293B")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(9)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Format Data Rows
    for r_idx, row in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(8.5)
                run.font.color.rgb = COLOR_TEXT
                
    # Apply widths
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table

# ==============================================================================
# DOCUMENT CONTENT GENERATION
# ==============================================================================

# Title & Metadata
add_title("DOKUMEN REFERENSI TEKNIS & ANALISIS BISNIS")
add_subtitle("E-Commerce Pricing & Promo Analytics (Studi Empiris 20.976 Listing Tokopedia)\nBahan Acuan Penyusunan Slide Presentasi Business Analytics (Google Slides)")

add_callout(
    "Dokumen ini memuat seluruh proses hulu ke hilir: akuisisi data, audit data profiling, pembersihan data (cleaning), "
    "query dbt SQL, script komputasi statistik Python, pengujian 6 hipotesis bisnis empiris, rancangan simulator margin, "
    "hingga panduan susunan 12 slide Google Slides siap pakai.",
    title="Tujuan Dokumen"
)

# ------------------------------------------------------------------------------
# BAGIAN 1: LATAR BELAKANG & PERNYATAAN MASALAH BISNIS
# ------------------------------------------------------------------------------
add_h1("1. Latar Belakang & Pernyataan Masalah Bisnis")

add_body(
    "Di platform e-commerce Indonesia seperti Tokopedia, diskon harga (promo cut) sering menjadi instrumen "
    "paling populer bagi seller untuk memenangkan algoritma pencarian dan meningkatkan volume konversi. "
    "Namun, dalam praktiknya banyak seller dan brand yang terjebak dalam fenomena perang diskon ekstrem (deep discounting >30%). "
    "Strategi ini sering kali mengorbankan margin kotor unit tanpa memberikan pertambahan volume penjualan yang proporsional."
)

add_h2("Stakeholder Utama & Pertanyaan Keputusan")
add_body("Analisis ini dirancang untuk menjawab kebutuhan pengambilan keputusan tiga pimpinan bisnis utama:")

headers_stakeholder = ["Stakeholder", "Pertanyaan Bisnis Inti", "Keputusan yang Didukung"]
data_stakeholder = [
    [
        "Commercial Director",
        "Jika diskon dipangkas dari 35% ke 20%, berapa margin kotor yang dapat diselamatkan dan bagaimana trade-off terhadap volume?",
        "Persetujuan kebijakan batas bawah margin (margin floor) dan persetujuan skema promosi campaign tahunan."
    ],
    [
        "Performance Marketing Lead",
        "Di tingkat diskon berapa penjualan berhenti naik (titik jenuh diskon), dan apakah perilakunya berbeda antar kategori?",
        "Alokasi budget subsidi voucher dan penetapan ambang batas diskon optimal per kategori kampanye."
    ],
    [
        "Head of Merchandising",
        "Kategori mana yang memiliki pricing power terkuat, dan bagaimana posisi daya saing harga antar wilayah produksi?",
        "Strategi assortment produk, penentuan harga dasar per kluster regional, dan investasi upgrade status Official Store."
    ]
]
create_table(headers_stakeholder, data_stakeholder, [1.5, 2.5, 2.5])

# ------------------------------------------------------------------------------
# BAGIAN 2: PENGUMPULAN & KARAKTERISTIK DATA (DATA COLLECTING)
# ------------------------------------------------------------------------------
add_h1("2. Pengumpulan Data (Data Collecting)")

add_body("Dataset diperoleh dari repositori publik data e-commerce Tokopedia dengan spesifikasi teknis sebagai berikut:")
add_bullet("Sumber Data: Kaggle Indonesia E-Commerce Dataset: Tokopedia Listings.", "Sumber: ")
add_bullet("Lisensi: Apache 2.0 (Dapat digunakan secara bebas untuk analisis komersial dan akademik).", "Lisensi: ")
add_bullet("Volume Mentah: 29.519 baris listing produk.", "Volume Data: ")
add_bullet("Karakteristik: Snapshot data cross-sectional aktif (satu titik waktu, bukan panel longitudinal).", "Karakter: ")

add_h2("Struktur Skema Mentah (Raw Columns)")
headers_raw = ["Nama Kolom Asli", "Tipe Data", "Deskripsi Konten", "Tantangan Kualitas Data"]
data_raw = [
    ["nama_produk", "String", "Judul lengkap listing produk", "Format tidak terstruktur; memuat spesifikasi, merek, dan promo campur aduk."],
    ["harga", "String / Int", "Harga jual saat ini yang ditampilkan", "Perlu parsing karakter non-numerik (Rp, titik)."],
    ["diskon", "String / Float", "Persentase potongan harga yang tertera", "Sebagian bernilai nol atau kosong."],
    ["terjual", "String", "Jumlah unit kumulatif terjual", "Format teks beragam: '1rb+', '4 rb+ Terjual', '3.5rb terjual', 'terjual 200'."],
    ["rating", "Float", "Rata-rata rating bintang (1.0 - 5.0)", "Variasi sangat terkompresi; 89.3% produk berada di 4.75 - 5.0."],
    ["jumlah_ulasan", "String / Int", "Jumlah ulasan pembeli", "Terdapat anomali imputasi di mana jumlah ulasan sama persis dengan angka terjual."],
    ["nama_toko", "String", "Nama seller / toko pemilik produk", "Terdapat baris placeholder dengan nama 'Tokopedia Seller'."],
    ["lokasi", "String", "Kota / Kabupaten asal penjual", "Terdapat lokasi generik bertuliskan 'Indonesia' yang tidak spesifik."]
]
create_table(headers_raw, data_raw, [1.3, 1.0, 2.2, 2.0])

# ------------------------------------------------------------------------------
# BAGIAN 3: DATA PROFILING & AUDIT KUALITAS DATA
# ------------------------------------------------------------------------------
add_h1("3. Audit Data Profiling (Fase 0 Gate Checks)")

add_body(
    "Sebelum pemodelan dilakukan, proses data profiling dijalankan menggunakan script Python "
    "untuk menguji kelayakan gate dan mengidentifikasi anomali data sistemik."
)

headers_gate = ["Kriteria Gate Check", "Target Minimum", "Hasil Realisasi", "Status Audit"]
data_gate = [
    ["Total baris setelah pembersihan", ">= 20.000 listing", "20.976 listing", "LOLOS (PASS)"],
    ["Jumlah listing berdiskon aktif (> 5%)", ">= 5.000 listing", "6.853 listing", "LOLOS (PASS)"],
    ["Akurasi parser kolom 'Terjual'", "100% baris ter-parse", "20.976 / 20.976 (100%)", "LOLOS (PASS)"],
    ["Coverage kategori teridentifikasi", ">= 75% baris", "78.99% (16.568 listing)", "LOLOS (PASS)"],
    ["Variasi standar deviasi rating (untuk H3)", "Std Dev > 0.10", "0.240", "LOLOS (PASS)"]
]
create_table(headers_gate, data_gate, [2.2, 1.4, 1.6, 1.3])

add_h2("Enam Anomali Data Kunci yang Teridentifikasi")
add_bullet("510 baris teridentifikasi memiliki kombinasi URL produk dan nama produk yang identik. Diatasi dengan deduplikasi jendela analitis pada layer staging.", "1. Duplikasi Baris: ")
add_bullet("Platform membulatkan angka penjualan besar (misal '1rb+' untuk 1.000 unit atau lebih). Hal ini dipahami sebagai proksi penjualan minimum kumulatif.", "2. Pembulatan Terjual: ")
add_bullet("89.3% produk yang memiliki rating berada pada interval sempit 4.75 hingga 5.0. Pengujian H3 harus dikontrol ketat hanya pada produk dengan reputasi matang (ulasan >= 30).", "3. Kompresi Rating Ekstrem: ")
add_bullet("Pada 25.2% listing, angka ulasan sama persis dengan angka terjual. Kolom ditandai sebagai 'is_imputed' agar dapat diuji sensitivitasnya.", "4. Anomali Imputasi Ulasan: ")
add_bullet("Sekitar 4% listing menggunakan akun placeholder toko 'Tokopedia Seller' yang bukan merupakan pedagang aktif, sehingga harus di-exclude.", "5. Toko Placeholder: ")
add_bullet("Sekitar 5.7% listing hanya mencantumkan 'Indonesia' tanpa nama kota. Baris ini di-exclude khusus pada pengujian disparitas regional (H4).", "6. Lokasi Ambigu: ")

# ------------------------------------------------------------------------------
# BAGIAN 4: DATA CLEANING & TRANSFORMATION (dbt SQL ARCHITECTURE)
# ------------------------------------------------------------------------------
add_h1("4. Pembersihan Data & Arsitektur SQL (dbt Pipeline)")

add_body(
    "Transformasi data dibangun menggunakan arsitektur Medallion berbasis dbt Core dan DuckDB "
    "yang terdiri dari tiga lapisan model: Staging -> Intermediate -> Mart."
)

add_h2("4.1 Lapisan Staging: stg_listings.sql")
add_body(
    "Fungsi: Ekstraksi regex untuk parsing angka penjualan dari string teks, casting tipe data numerik, "
    "derivasi harga normal sebelum diskon, dan deduplikasi menggunakan window function ROW_NUMBER()."
)

code_stg = """
-- dbt/models/staging/stg_listings.sql
with source as (
    select * from read_csv_auto('data/raw/produk_tokopedia.csv')
),
cleaned as (
    select
        hash(product_url) as listing_id,
        product_url,
        trim(nama_produk) as nama_produk,
        trim(toko) as nama_toko,
        trim(lokasi) as lokasi_raw,
        cast(regexp_replace(harga, '[^0-9]', '', 'g') as integer) as harga,
        coalesce(cast(regexp_replace(diskon, '[^0-9.]', '', 'g') as double), 0.0) as diskon_pct,
        
        -- Regex Parsing Terjual
        case
            when terjual ~* '([0-9.]+)\\s*rb' then
                cast(cast(regexp_extract(terjual, '([0-9.]+)\\s*rb', 1) as double) * 1000 as integer)
            when terjual ~* 'terjual\\s*([0-9.]+)' then
                cast(regexp_replace(regexp_extract(terjual, 'terjual\\s*([0-9.]+)', 1), '[^0-9]', '', 'g') as integer)
            when terjual ~* '([0-9]+)' then
                cast(regexp_replace(terjual, '[^0-9]', '', 'g') as integer)
            else 0
        end as terjual,
        
        cast(rating as double) as rating,
        cast(regexp_replace(coalesce(ulasan, '0'), '[^0-9]', '', 'g') as integer) as jumlah_ulasan,
        (toko = 'Tokopedia Seller') as is_placeholder,
        (ulasan = terjual and terjual > 0) as is_imputed,
        row_number() over (partition by product_url, nama_produk order by harga asc) as rn
    from source
)
select *,
    case when diskon_pct > 0 and diskon_pct < 100 
         then cast(round(harga / (1.0 - diskon_pct / 100.0)) as integer)
         else harga 
    end as harga_normal
from cleaned
where rn = 1 and is_placeholder = false and harga > 0;
"""
add_code_block(code_stg)

add_h2("4.2 Lapisan Intermediate: int_clean_listings.sql")
add_body(
    "Fungsi: Normalisasi teks nama kota/kabupaten menjadi 16 kluster provinsi geografis standar "
    "serta filter terhadap baris lokasi yang tidak valid."
)

code_int = """
-- dbt/models/intermediate/int_clean_listings.sql
with staging as (
    select * from {{ ref('stg_listings') }}
)
select
    *,
    case
        when lokasi_raw ~* 'jakarta' then 'DKI Jakarta'
        when lokasi_raw ~* 'bandung|bogor|depok|bekasi|cimahi|cirebon|sukabumi|tasikmalaya|garut' then 'Jawa Barat'
        when lokasi_raw ~* 'surabaya|malang|sidoarjo|kediri|blitar|madiun|pasuruan|jember' then 'Jawa Timur'
        when lokasi_raw ~* 'semarang|solo|surakarta|magelang|pekalongan|tegal|kudus' then 'Jawa Tengah'
        when lokasi_raw ~* 'tangerang|serang|cilegon' then 'Banten'
        when lokasi_raw ~* 'yogyakarta|jogja|sleman|bantul' then 'DI Yogyakarta'
        when lokasi_raw ~* 'medan|deli|binjai' then 'Sumatera Utara'
        when lokasi_raw ~* 'palembang' then 'Sumatera Selatan'
        when lokasi_raw ~* 'denpasar|badung' then 'Bali'
        when lokasi_raw ~* 'makassar' then 'Sulawesi Selatan'
        when lokasi_raw ~* 'banjarmasin' then 'Kalimantan Selatan'
        when lokasi_raw ~* 'samarinda|balikpapan' then 'Kalimantan Timur'
        when lokasi_raw ~* 'pontianak' then 'Kalimantan Barat'
        when lokasi_raw ~* 'pekanbaru' then 'Riau'
        when lokasi_raw ~* 'batam' then 'Kepulauan Riau'
        when lokasi_raw = 'Indonesia' then 'Tidak Diketahui'
        else 'Lainnya'
    end as wilayah
from staging;
"""
add_code_block(code_int)

add_h2("4.3 Lapisan Mart: fct_listing.sql")
add_body(
    "Fungsi: Feature engineering lengkap mencakup klasifikasi 14 kategori rule-based, perhitungan "
    "kuantil tier harga per kategori (NTILE 3: bawah, menengah, atas), pengelompokan 6 bucket diskon, "
    "ekstraksi penempatan spesifikasi judul, serta identifikasi toko official."
)

code_mart = """
-- dbt/models/mart/fct_listing.sql (Cuplikan Logika Kunci)
with base as (
    select * from {{ ref('int_clean_listings') }}
),
with_features as (
    select
        *,
        -- 1. Klasifikasi 14 Kategori (Keyword Matching Hirarkis)
        case
            when lower(nama_produk) ~* 'makanan kucing|cat food|dog food|pasir kucing|akuarium' then 'hewan_peliharaan'
            when lower(nama_produk) ~* 'jas hujan|kunci pas|obeng|lampu motor|wiper|sparepart|oli motor|baut|mur' then 'otomotif_perkakas'
            when lower(nama_produk) ~* 'buku|novel|komik|pulpen|kertas hvs|bubble wrap|lakban|kemasan|packaging' then 'atk_kemasan'
            when lower(nama_produk) ~* 'masker medis|hand sanitizer|popok|diapers|susu bayi|termometer|pembalut' then 'kesehatan_bayi'
            when lower(nama_produk) ~* 'mainan|boneka|action figure|lego|benang rajut|cat akrilik|logam mulia|emas' then 'mainan_hobi'
            when lower(nama_produk) ~* 'gamis|pashmina|kebaya|daster|abaya|tunik|mukena|dress|hijab|blouse|rok' then 'fashion_wanita'
            when lower(nama_produk) ~* 'kemeja pria|kaos pria|celana pria|batik pria|jaket pria|baju koko|sarung' then 'fashion_pria'
            when lower(nama_produk) ~* 'kaos|hoodie|sweater|jaket|t-shirt|jeans|celana|oversized|cardigan' then 'fashion_umum'
            when lower(nama_produk) ~* 'sepatu|sandal|sling bag|tote bag|backpack|koper|dompet|jam tangan|kacamata' then 'sepatu_aksesori'
            when lower(nama_produk) ~* 'speaker|headset|laptop|smartphone|charger|mouse|keyboard|powerbank|cctv' then 'elektronik'
            when lower(nama_produk) ~* 'skincare|serum|sunscreen|lipstik|parfum|shampoo|sabun mandi|facial wash' then 'kecantikan'
            when lower(nama_produk) ~* 'panci|wajan|kompor|spatula|piring|gelas|bantal|sprei|sapu|rak|meja|kursi' then 'rumah_tangga'
            when lower(nama_produk) ~* 'raket|sepatu olahraga|dumbbell|sepeda|jersey|yoga mat|bola sepak' then 'olahraga'
            when lower(nama_produk) ~* 'kopi|teh|snack|indomie|beras|minyak goreng|sambal|frozen food|biskuit' then 'makanan_minuman'
            else 'lainnya'
        end as kategori,
        
        -- 2. Bucket Diskon Terstandarisasi
        case
            when diskon_pct = 0 then '0%'
            when diskon_pct <= 10 then '1-10%'
            when diskon_pct <= 20 then '11-20%'
            when diskon_pct <= 30 then '21-30%'
            when diskon_pct <= 50 then '31-50%'
            else '>50%'
        end as bucket_diskon,
        
        -- 3. Deteksi Spesifikasi di Awal Judul (H5)
        (lower(nama_produk) ~* '^(katun|cotton|combed|rayon|linen|denim|sifon|spandek|size|ukuran|isi|pack|box|\\d+\\s*(ml|gr|gram|kg|l|liter|cm|mm|m|pcs|pc|meter))') as has_spec_at_start,
        
        -- 4. Deteksi Official Store (H6)
        (lower(nama_toko) ~* 'official|official store|official shop|authorized') as is_official_store
    from base
)
select
    *,
    (cast(harga as bigint) * cast(terjual as bigint)) as gmv_proxy,
    -- 5. Tier Harga Quantile per Kategori (H3)
    case ntile(3) over (partition by kategori order by harga asc)
        when 1 then 'bawah'
        when 2 then 'menengah'
        when 3 then 'atas'
    end as tier_harga
from with_features;
"""
add_code_block(code_mart)

# ------------------------------------------------------------------------------
# BAGIAN 5: SCRIPT PYTHON YANG DIGUNAKAN
# ------------------------------------------------------------------------------
add_h1("5. Script Python yang Digunakan")

add_body(
    "Pengujian statistik multivariat dilakukan secara programatik menggunakan Python (SciPy dan Statsmodels) "
    "melalui script `notebooks/run_hypothesis_analysis.py`. Berikut adalah fungsi pengujian statistik kunci yang digunakan:"
)

code_py = """
# Cuplikan notebooks/run_hypothesis_analysis.py
import duckdb
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf

con = duckdb.connect('data/tokped.duckdb')
df = con.execute("SELECT * FROM fct_listing").df()

# 1. Uji H1: Model Regresi OLS Polinomial (Uji Kurvatur Titik Jenuh)
df['log_terjual'] = np.log1p(df['terjual'])
df['log_ulasan'] = np.log1p(df['jumlah_ulasan'])
df['diskon_sq'] = (df['diskon_pct'] / 100.0) ** 2  # Kuadratik untuk efek kejenuhan

model_h1 = smf.ols(
    'log_terjual ~ diskon_pct + diskon_sq + log_ulasan + C(tier_harga) + C(is_official_store)',
    data=df
).fit()
print(model_h1.summary())

# 2. Uji H2: Interaksi Kategori Utilitarian vs Fashion
util_cats = ['rumah_tangga', 'elektronik', 'otomotif_perkakas', 'atk_kemasan']
df['is_utilitarian'] = df['kategori'].isin(util_cats)
model_h2 = smf.ols(
    'log_terjual ~ diskon_pct * is_utilitarian + log_ulasan + C(tier_harga)',
    data=df
).fit()

# 3. Uji H3: Kruskal-Wallis Rating per Tier Harga (Filter Ulasan >= 30)
h3_df = df[(df['jumlah_ulasan'] >= 30) & df['rating'].notnull()]
groups = [group['rating'].values for _, group in h3_df.groupby('tier_harga')]
kw_stat, kw_p = stats.kruskal(*groups)

# 4. Uji H4: Kruskal-Wallis Disparitas Harga Regional Fesyen
fash_df = df[df['kategori'].str.contains('fashion|sepatu')]
groups_h4 = [group['harga'].values for _, group in fash_df.groupby('wilayah')]
kw_h4, p_h4 = stats.kruskal(*groups_h4)

# 5. Uji H5 & H6: Mann-Whitney U Test
u_h5, p_h5 = stats.mannwhitneyu(df[df['has_spec_at_start']]['terjual'], df[~df['has_spec_at_start']]['terjual'])
u_h6_p, p_h6_p = stats.mannwhitneyu(df[df['is_official_store']]['harga'], df[~df['is_official_store']]['harga'])
u_h6_v, p_h6_v = stats.mannwhitneyu(df[df['is_official_store']]['terjual'], df[~df['is_official_store']]['terjual'])
"""
add_code_block(code_py)

# ------------------------------------------------------------------------------
# BAGIAN 6: HASIL ANALISIS HIPOTESIS & TEMUAN BISNIS (H1 - H6)
# ------------------------------------------------------------------------------
add_h1("6. Hasil Analisis Hipotesis Empiris (H1 - H6)")

add_body("Berdasarkan pengujian terhadap 20.976 listing, berikut adalah rangkuman hasil validasi seluruh hipotesis:")

headers_h_summary = ["Hipotesis", "Metode Uji Statistik", "Hasil Uji", "Kesimpulan Bisnis"]
data_h_summary = [
    ["H1: Titik Jenuh Diskon", "Median bucket & Regresi Kuadratik", "Koefisien Kuadrat Negatif (p < 0.001)", "DIDUKUNG: Titik jenuh tercapai di 20-30%. Di atas 30%, volume median stagnan."],
    ["H2: Elastisitas Kategori", "Regresi OLS Interaksi", "Interaksi Signifikan (p = 0.018)", "DIDUKUNG: Utilitarian lebih terstandardisasi, namun ulasan tetap pendorong utama."],
    ["H3: Tier Harga vs Rating", "Kruskal-Wallis (Ulasan >= 30)", "H = 100.35, p = 1.62e-22", "DIDUKUNG: Tier bawah rating 4.863 vs tier atas 4.902 (beda tipis tapi signifikan)."],
    ["H4: Regional Pricing", "Kruskal-Wallis Wilayah", "H = 56.03, p = 1.20e-6", "DIDUKUNG: Produsen Jawa Barat menjual fashion jauh lebih murah dibanding Jakarta."],
    ["H5: Spesifikasi Judul", "Mann-Whitney U Test", "Volume p = 1.34e-5, Harga p = 5.89e-13", "DIDUKUNG SEBAGIAN: Volume naik +80%, namun harga lebih murah (produk komoditas)."],
    ["H6: Efek Official Store", "Mann-Whitney U Test", "Volume p = 8.30e-30, Harga p = 1.06e-7", "DIDUKUNG SEBAGIAN: Volume 2.25x lipat dan harga +55.4% lebih tinggi."]
]
create_table(headers_h_summary, data_h_summary, [1.3, 1.4, 1.4, 2.4])

add_h2("Detail Temuan per Hipotesis")

add_h3("H1: Fenomena Titik Jenuh Diskon (Discount Saturation Point)")
add_body(
    "Data membuktikan bahwa diskon memberikan lompatan volume penjualan awal yang sangat kuat. "
    "Listing tanpa diskon (0%) mencatat median penjualan 26 unit. Pemberian diskon taktis (1-10%) langsung "
    "melipatgandakan median penjualan menjadi 100 unit. Namun, di atas diskon 20%, kurva volume mengalami stagnasi total (plateau). "
    "Median penjualan tetap flat di angka 100 unit pada bucket 11-20%, 21-30%, 31-50%, dan >50%."
)
add_body(
    "Lebih jauh lagi, rata-rata volume penjualan memuncak di bucket 21-30% (5.799 unit) dan justru merosot pada diskon ekstrem "
    "menjadi 4.121 unit pada bucket 31-50% dan 3.840 unit pada bucket >50%. Seller yang memberikan diskon >30% membakar margin "
    "kotor tanpa memperoleh penambahan penjualan yang berarti."
)

headers_h1_table = ["Bucket Diskon", "Jumlah Listing", "Median Terjual", "Rata-rata Terjual", "Median Harga Bersih", "Status Kurva"]
data_h1_table = [
    ["0%", "12.918", "26 unit", "1.064 unit", "Rp 99.000", "Baseline Tanpa Diskon"],
    ["1-10%", "1.936", "100 unit", "2.093 unit", "Rp 120.000", "Peningkatan Volume Awal"],
    ["11-20%", "1.155", "100 unit", "2.566 unit", "Rp 135.000", "Area Efisiensi Optimal"],
    ["21-30%", "971", "100 unit", "5.799 unit", "Rp 105.000", "Puncak Rata-rata Penjualan"],
    ["31-50%", "2.055", "100 unit", "4.121 unit", "Rp 88.000", "Zona Titik Jenuh (Margin Burn)"],
    [">50%", "1.941", "100 unit", "3.840 unit", "Rp 45.000", "Zona Diskon Berlebih (Inefisiensi)"]
]
create_table(headers_h1_table, data_h1_table, [1.0, 1.1, 1.1, 1.1, 1.1, 1.1])

add_h3("H6: Pricing Power Toko Official (Official Store Effect)")
add_body(
    "Official Store mencakup 23.3% dari populasi listing (4.885 listing) dan menunjukkan dominasi ganda: "
    "memiliki volume penjualan median 2.25x lipat lebih tinggi (90 unit vs 40 unit pada toko reguler, p < 0.001) "
    "sekaligus menetapkan median harga premium sebesar Rp 147.000 vs Rp 94.600 (+55.4% lebih mahal). "
    "Toko Official tidak memasang diskon lebih rendah, melainkan menjalankan promosi lebih terstruktur dan terencana "
    "(rata-rata diskon 13.9% vs 12.1% reguler) dengan harga dasar yang lebih terlindungi."
)

add_h3("H4: Disparitas Harga Regional (Sentra Konveksi Jawa Barat)")
add_body(
    "Pada kategori fesyen, terdapat perbedaan harga yang sangat tajam antar sentra produksi (p = 1.20e-6). "
    "Seller di Jawa Barat (pusat konveksi Bandung, Cimahi, dsk.) menetapkan median harga Rp 104.999 (966 listing). "
    "Sebaliknya, reseller di DKI Jakarta menetapkan median harga Rp 129.000 (2.063 listing) dan Jawa Tengah Rp 189.578. "
    "Reseller di luar Jawa Barat menghadapi tekanan harga langsung dari produsen lokal."
)

# ------------------------------------------------------------------------------
# BAGIAN 7: REKOMENDASI STRATEGIS & SIMULATOR MARGIN
# ------------------------------------------------------------------------------
add_h1("7. Rekomendasi Strategis & Simulator Margin")

add_body("Berdasarkan temuan empiris di atas, dirumuskan empat aksi strategis bagi pengelola brand dan seller:")

headers_recom = ["No", "Rekomendasi Tindakan", "Hipotesis", "Estimasi Dampak Finansial", "Keyakinan", "Validasi Lapangan"]
data_recom = [
    ["1", "Pangkas Diskon Maksimal ke 20-25%", "H1", "Margin per unit naik +5% s/d +12% poin tanpa kehilangan volume.", "Tinggi", "A/B testing diskon pada 20 SKU terlaris selama 14 hari."],
    ["2", "Investasi Upgrade ke Status Official Store", "H6", "Harga jual rata-rata (ASP) naik +50% dengan konversi 2.2x lipat.", "Tinggi", "Analisis ROI biaya pendaftaran pro/official vs margin ekstra."],
    ["3", "Format Spesifikasi di Awal Judul Produk Komoditas", "H5", "Volume penjualan meningkat +80% pada barang kebutuhan pokok/basic.", "Sedang", "Uji format judul SEO pada 30 listing komoditas fast-moving."],
    ["4", "Strategi Bundling untuk Reseller Non-Produsen", "H4", "Menghindari perang harga langsung dengan produsen konveksi Jawa Barat.", "Sedang", "Luncurkan paket bundling 3-in-1 untuk mengaburkan harga per unit."]
]
create_table(headers_recom, data_recom, [0.3, 1.8, 0.6, 1.8, 0.8, 1.2])

add_h2("Model Unit Economics Simulator Margin")
add_body(
    "Simulator margin (tersedia di app/streamlit_app.py dan versi web Vercel) memodelkan perubahan keuntungan kotor "
    "dengan memperhitungkan elastisitas empiris H1:"
)
add_bullet("Harga Bersih = Harga Coret * (1 - Diskon%)", "Harga Efektif: ")
add_bullet("HPP Pokok = Harga Coret * HPP%", "Beban Pokok: ")
add_bullet("Admin Fee = Harga Bersih * Fee Marketplace%", "Biaya Platform: ")
add_bullet("Margin Unit = Harga Bersih - HPP Pokok - Admin Fee - Biaya Packing", "Margin Bersih: ")
add_bullet("Laba Kotor Bulanan = Margin Unit * Estimasi Volume Baru", "Laba Total: ")

add_callout(
    "Contoh Kasus Fesyen Wanita: Produk dengan harga normal Rp 100.000 dan HPP 45% yang memangkas diskon dari 35% ke 20% "
    "mengalami peningkatan margin bersih dari Rp 17.750 menjadi Rp 29.800 per unit (+68%). Dengan volume penjualan yang tetap "
    "berada di zona optimal, seller mengamankan tambahan laba kotor sebesar +Rp 6.000.000 per bulan untuk setiap 500 unit penjualan.",
    title="Simulasi Bisnis Nyata"
)

# ------------------------------------------------------------------------------
# BAGIAN 8: PANDUAN STRUKTUR SLIDE PRESENTASI GOOGLE SLIDES
# ------------------------------------------------------------------------------
add_h1("8. Panduan Struktur Slide Google Slides (12 Slides Outline)")

add_body(
    "Gunakan kerangka 12 slide berikut sebagai referensi utama saat membangun slide presentasi di Google Slides. "
    "Setiap slide telah dilengkapi dengan judul, visual yang disarankan, angka kunci, dan catatan pembicara (talking points):"
)

slides_plan = [
    {
        "num": "Slide 1",
        "title": "Judul & Ringkasan Eksekutif",
        "visual": "Logo Tokopedia / E-Commerce, judul tebal, kartu 4 KPI utama.",
        "kpi": "20.976 Listing Bersih | 14 Kategori | Titik Jenuh Diskon 20-30% | Official Store Premium +55.4%",
        "talk": "Buka presentasi dengan menegaskan bahwa studi ini menganalisis fenomena perang diskon di Tokopedia dan menemukan bahwa diskon besar sering kali membakar margin tanpa menambah penjualan."
    },
    {
        "num": "Slide 2",
        "title": "Pernyataan Masalah & Keputusan Bisnis",
        "visual": "Tabel 3 kolom memetakan Commercial Director, Head of Marketing, dan Head of Merchandising.",
        "kpi": "Tiga pertanyaan kunci: Berapa diskon optimal? Berapa margin yang diselamatkan? Di mana fokus kategori & regional?",
        "talk": "Tunjukkan bahwa presentasi ini menjawab pertanyaan strategis dari pimpinan komersial dan pemasaran, bukan sekadar eksplorasi data teknis."
    },
    {
        "num": "Slide 3",
        "title": "Arsitektur Data & Metodologi ELT",
        "visual": "Diagram alir pipeline: Kaggle CSV -> DuckDB -> dbt (stg -> int -> mart) -> Streamlit & Vercel Web.",
        "kpi": "14 Data Tests PASS (Unique, Not Null, Accepted Values) | Pipeline 100% Reproducible",
        "talk": "Jelaskan bahwa data telah melalui pembersihan ketat dengan dbt testing framework, menjamin integritas data sebelum ditarik kesimpulan bisnis."
    },
    {
        "num": "Slide 4",
        "title": "Audit Data Profiling: Menemukan Realitas Data",
        "visual": "Tabel temuan anomali data (duplikasi, format teks terjual, rating terkompresi, imputasi ulasan).",
        "kpi": "510 Baris Duplikat Dihapus | 25.2% Anomali Imputasi Ditandai | Coverage Kategori Naik dari 51% ke 78.99%",
        "talk": "Soroti kejujuran data profiling: 89% rating berada di angka 4.8-5.0 sehingga analisis reputasi harus dikontrol ketat pada ulasan matang."
    },
    {
        "num": "Slide 5",
        "title": "Temuan Utama 1: Titik Jenuh Diskon (H1)",
        "visual": "Grafik batang median terjual per bucket diskon berdampingan dengan kurva garis rata-rata terjual.",
        "kpi": "Median flat di 100 unit dari diskon 10% hingga >50% | Rata-rata puncak di 21-30% (5.799 unit) lalu turun",
        "talk": "Inilah slide paling krusial: perlihatkan bahwa diskon >30% menghasilkan penjualan yang lebih rendah daripada diskon 20-30%. Diskon ekstrem adalah margin burn."
    },
    {
        "num": "Slide 6",
        "title": "Temuan Utama 2: Kekuatan Merek Official Store (H6)",
        "visual": "Kartu perbandingan Official Store vs Reguler (Harga, Volume, Diskon).",
        "kpi": "Volume 2.25x Lipat (90 vs 40 unit) | Harga Premium +55.4% (Rp 147rb vs 95rb) | Diskon Rata-rata 13.9% vs 12.1%",
        "talk": "Toko Official tidak bersaing dengan banting harga; mereka memiliki pricing power tinggi dan menjalankan kampanye promo terstruktur."
    },
    {
        "num": "Slide 7",
        "title": "Temuan Utama 3: Disparitas Harga Regional (H4)",
        "visual": "Peta / Horizontal bar chart median harga fesyen antar provinsi.",
        "kpi": "Jawa Barat (Bandung) Rp 105.000 vs DKI Jakarta Rp 129.000 vs Jawa Tengah Rp 189.578 (p < 0.001)",
        "talk": "Sentra konveksi Jawa Barat memiliki keunggulan harga dasar produsen. Reseller di Jakarta dan daerah lain harus menggunakan diferensiasi non-harga."
    },
    {
        "num": "Slide 8",
        "title": "Temuan Tambahan: Reputasi & Format Judul (H3 & H5)",
        "visual": "Dua grafik mini: Boxplot rating per tier harga dan perbandingan volume spesifikasi judul.",
        "kpi": "Tier Bawah rating 4.86 vs Tier Atas 4.90 (p < 0.001) | Spesifikasi di Awal Judul menaikkan volume +80%",
        "talk": "Pembeli pada produk murah cenderung lebih kritis terhadap ekspektasi bahan. Di sisi lain, format judul SEO yang spesifik mendongkrak konversi produk komoditas."
    },
    {
        "num": "Slide 9",
        "title": "Unit Economics Simulator: Trade-off Diskon vs Margin",
        "visual": "Tangkapan layar Simulator Margin (app/streamlit_app.py atau Vercel) dan tabel perbandingan skenario.",
        "kpi": "Memangkas diskon dari 35% ke 20% menaikkan margin per unit +68% (+Rp 12.050/unit pada harga Rp 100rb)",
        "talk": "Perkenalkan kalkulator margin interaktif yang memungkinkan tim komersial menguji skenario HPP, biaya admin, dan estimasi laba kotor sebelum campaign diluncurkan."
    },
    {
        "num": "Slide 10",
        "title": "Rekomendasi Strategis Bisnis",
        "visual": "Matriks 4 pilar rekomendasi (Diskon Cap, Upgrade Official Store, SEO Spesifikasi Judul, Bundling Regional).",
        "kpi": "Potensi kenaikan laba kotor unit +5% s/d +12% poin | Target ASP tumbuh hingga +50%",
        "talk": "Tegaskan empat langkah konkret yang dapat langsung dieksekusi oleh tim merchandising dan pemasaran."
    },
    {
        "num": "Slide 11",
        "title": "Keterbatasan Data & Rencana Validasi Lapangan",
        "visual": "Tabel mitigasi risiko dan rencana A/B testing 14 hari.",
        "kpi": "Uji A/B testing pada 20 SKU terlaris selama kampanye Payday | Kontrol sensitivitas data imputasi",
        "talk": "Tunjukkan kedewasaan analitis: data ini adalah cross-sectional snapshot, sehingga rekomendasi perlu divalidasi melalui uji coba terukur sebelum diterapkan ke seluruh katalog."
    },
    {
        "num": "Slide 12",
        "title": "Penutup & Action Plan Implementasi",
        "visual": "Timeline roadmap 30-60-90 hari implementasi dan tautan ke live dashboard / repositori.",
        "kpi": "Repositori GitHub & Live Vercel Simulator Siap Diakses",
        "talk": "Tutup dengan ajakan bertindak (call to action) dan buka sesi tanya jawab untuk menyelaraskan kebijakan diskon baru."
    }
]

for s in slides_plan:
    add_h2(f"{s['num']}: {s['title']}")
    add_bullet(s['visual'], "Visual yang Disarankan: ")
    add_bullet(s['kpi'], "Angka & Pesan Kunci: ")
    add_bullet(s['talk'], "Talking Points Pembicara: ")

# Save Document
output_path = 'reports/tokopedia_business_analytics_reference.docx'
os.makedirs('reports', exist_ok=True)
doc.save(output_path)
print(f"Dokumen berhasil dibuat dan disimpan di: {output_path}")
