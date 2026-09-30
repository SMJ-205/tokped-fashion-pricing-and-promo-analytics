-- stg_listings.sql
-- Staging layer: parse semua kolom raw, flag baris bermasalah.
-- Scope: SEMUA listing lintas kategori (tanpa filter kategori).
-- Kompatibel dengan dbt-duckdb 1.10.x

{{ config(materialized='view') }}

with raw as (

    select * from read_csv_auto(
        '{{ env_var("DBT_CSV_PATH", "../data/raw/tokopedia_listings.csv") }}',
        header = true,
        nullstr = ['', 'NULL', 'null', 'None']
    )

),

parsed as (

    select
        -- ── Identifiers ──────────────────────────────────────────────────────
        "Produk URL"                                                     as product_url,

        -- ── Text fields ──────────────────────────────────────────────────────
        "Nama Produk"                                                    as nama_produk,
        "Nama Toko"                                                      as nama_toko,
        "Lokasi Toko"                                                    as lokasi_raw,

        -- ── Diskon → float (kosong/null = 0) ─────────────────────────────────
        coalesce(try_cast("Diskon (%)" as double), 0.0)                  as diskon_pct,

        -- ── Harga (sudah integer dari CSV) ───────────────────────────────────
        try_cast("Harga (IDR)" as integer)                               as harga,

        -- ── Harga Normal (sebelum diskon) ────────────────────────────────────
        case
            when coalesce(try_cast("Diskon (%)" as double), 0) > 0
            then try_cast("Harga (IDR)" as integer)
                 / (1.0 - coalesce(try_cast("Diskon (%)" as double), 0) / 100.0)
            else try_cast("Harga (IDR)" as integer)
        end                                                              as harga_normal,

        -- ── Terjual: parse format 'Xrb+', '3.5rb', '200 terjual', dll ────────
        -- Step 1: lowercase & strip spaces/+
        -- Step 2: if contains 'rb' → extract number * 1000, else extract plain int
        case
            when regexp_extract(lower(regexp_replace("Terjual", '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) <> ''
            then cast(
                    cast(regexp_extract(lower(regexp_replace("Terjual", '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) as double)
                    * 1000 as integer
                 )
            when regexp_extract(coalesce("Terjual", ''), '(\d+)', 1) <> ''
            then cast(regexp_extract("Terjual", '(\d+)', 1) as integer)
            else 0
        end                                                              as terjual,

        -- ── Jumlah Ulasan: parse format serupa ───────────────────────────────
        case
            when regexp_extract(lower(regexp_replace(coalesce("Jumlah Ulasan", ''), '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) <> ''
            then cast(
                    cast(regexp_extract(lower(regexp_replace(coalesce("Jumlah Ulasan", ''), '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) as double)
                    * 1000 as integer
                 )
            when regexp_extract(coalesce("Jumlah Ulasan", '0'), '(\d+)', 1) <> ''
            then cast(regexp_extract(coalesce("Jumlah Ulasan", '0'), '(\d+)', 1) as integer)
            else 0
        end                                                              as jumlah_ulasan,

        -- ── Rating (0 → NULL jika ulasan = 0) ────────────────────────────────
        "Rating"                                                         as rating_raw

    from raw

),

with_flags as (

    select
        *,

        -- Rating: 0 → NULL jika tidak ada ulasan (bukan rating nyata)
        case
            when rating_raw = 0 and jumlah_ulasan = 0 then null
            else rating_raw
        end                                                              as rating,

        -- Harga Normal yang sudah di-round
        round(harga_normal)                                              as harga_normal_idr,

        -- ── Flag: Placeholder row ─────────────────────────────────────────────
        (
            lower(nama_toko) like '%tokopedia seller%'
            or lower(product_url) like '%/search%'
            or lower(product_url) like '%/kategori%'
            or product_url like '%q=%'
        )                                                                as is_placeholder,

        -- ── Flag: Official store ──────────────────────────────────────────────
        lower(nama_toko) like '%official store%'
        or lower(nama_toko) like '%official shop%'
        or lower(nama_toko) like '%official%'                           as is_official_store,

        -- ── Flag: Imputed (ulasan == terjual — suspicious) ───────────────────
        (jumlah_ulasan > 0 and jumlah_ulasan = terjual)                 as is_imputed

    from parsed

),

with_derived as (

    select
        product_url,
        nama_produk,
        nama_toko,
        lokasi_raw,
        harga,
        round(harga_normal_idr)::integer                                as harga_normal,
        diskon_pct,
        terjual,
        jumlah_ulasan,
        rating,
        is_placeholder,
        is_official_store,
        is_imputed,

        -- GMV proxy (BIGINT to avoid INT32 overflow on large harga*terjual)
        (cast(harga as bigint) * cast(terjual as bigint))              as gmv_proxy,

        -- Bucket diskon (label ordinal)
        case
            when diskon_pct = 0               then '0%'
            when diskon_pct <= 10             then '1-10%'
            when diskon_pct <= 20             then '11-20%'
            when diskon_pct <= 30             then '21-30%'
            when diskon_pct <= 50             then '31-50%'
            else '>50%'
        end                                                             as bucket_diskon,

        -- Order bucket untuk sorting
        case
            when diskon_pct = 0               then 1
            when diskon_pct <= 10             then 2
            when diskon_pct <= 20             then 3
            when diskon_pct <= 30             then 4
            when diskon_pct <= 50             then 5
            else 6
        end                                                             as bucket_diskon_order

    from with_flags

)

select * from with_derived
