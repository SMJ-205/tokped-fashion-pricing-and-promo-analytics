-- stg_listings.sql
-- Staging layer: parse semua kolom raw, flag baris bermasalah.
-- Scope: SEMUA listing lintas kategori (tanpa filter kategori).
-- Kompatibel dengan dbt-duckdb 1.10.x

{{ config(materialized='view') }}

with raw as (

    select * from read_csv_auto(
        '{{ env_var("DBT_CSV_PATH", "../data/raw/produk_tokopedia.csv") }}',
        header = true,
        nullstr = ['', 'NULL', 'null', 'None']
    )

),

-- Deduplicate: data asli memiliki baris identik (URL + nama sama persis)
-- Ambil baris pertama per (URL, nama); baris duplikat di-drop
deduped as (

    select *
    from (
        select *,
            row_number() over (
                partition by "Produk URL", "Nama Produk"
                order by "Harga (IDR)" desc
            ) as _row_num
        from raw
    )
    where _row_num = 1

),

parsed as (

    select
        -- ── Surrogate key (md5 URL+nama — handle truncated URLs di data asli) ──
        md5(coalesce("Produk URL", '') || '|' || coalesce("Nama Produk", ''))  as listing_id,

        -- ── Identifiers ──────────────────────────────────────────────────────
        "Produk URL"                                                    as product_url,

        -- ── Text fields ──────────────────────────────────────────────────────
        "Nama Produk"                                                   as nama_produk,
        "Nama Toko"                                                     as nama_toko,
        "Lokasi Toko"                                                   as lokasi_raw,

        -- ── Diskon → float (kosong/null = 0) ──────────────────────────────
        coalesce(try_cast("Diskon (%)" as double), 0.0)                 as diskon_pct,

        -- ── Harga ──────────────────────────────────────────────────────────
        try_cast("Harga (IDR)" as integer)                              as harga,

        -- ── Terjual: parse 'Xrb+', '3.5rb', '200 terjual', dll ────────────
        case
            when regexp_extract(lower(regexp_replace("Terjual", '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) <> ''
            then cast(
                    cast(regexp_extract(lower(regexp_replace("Terjual", '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) as double)
                    * 1000 as integer
                 )
            when regexp_extract(coalesce("Terjual", ''), '(\d+)', 1) <> ''
            then cast(regexp_extract("Terjual", '(\d+)', 1) as integer)
            else 0
        end                                                             as terjual,

        -- ── Jumlah Ulasan: parse format serupa ───────────────────────────
        case
            when regexp_extract(lower(regexp_replace(coalesce("Jumlah Ulasan", ''), '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) <> ''
            then cast(
                    cast(regexp_extract(lower(regexp_replace(coalesce("Jumlah Ulasan", ''), '\s+', '', 'g')), '(\d+\.?\d*)rb', 1) as double)
                    * 1000 as integer
                 )
            when regexp_extract(coalesce("Jumlah Ulasan", '0'), '(\d+)', 1) <> ''
            then cast(regexp_extract(coalesce("Jumlah Ulasan", '0'), '(\d+)', 1) as integer)
            else 0
        end                                                             as jumlah_ulasan,

        -- ── Rating raw (null-handling di with_flags) ──────────────────────
        "Rating"                                                        as rating_raw

    from deduped

),

with_flags as (

    select
        *,

        -- Rating: 0 → NULL jika tidak ada ulasan (bukan rating nyata)
        case
            when rating_raw = 0 and jumlah_ulasan = 0 then null
            else rating_raw
        end                                                             as rating,

        -- Harga Normal (sebelum diskon), di-round ke integer
        round(
            case
                when diskon_pct > 0
                then harga / (1.0 - diskon_pct / 100.0)
                else harga
            end
        )::integer                                                      as harga_normal,

        -- ── Flag: Placeholder row ─────────────────────────────────────────
        (
            lower(nama_toko) like '%tokopedia seller%'
            or lower(product_url) like '%/search%'
            or lower(product_url) like '%/kategori%'
            or product_url like '%q=%'
        )                                                               as is_placeholder,

        -- ── Flag: Truncated URL (share URL toko, bukan URL produk spesifik)
        (
            length(product_url) < 45
            or product_url not like '%//%/%/%'
        )                                                               as is_truncated_url,

        -- ── Flag: Official store ──────────────────────────────────────────
        (
            lower(nama_toko) like '%official store%'
            or lower(nama_toko) like '%official shop%'
            or lower(nama_toko) like '%official%'
        )                                                               as is_official_store,

        -- ── Flag: Imputed (ulasan == terjual — suspicious) ───────────────
        (jumlah_ulasan > 0 and jumlah_ulasan = terjual)                as is_imputed

    from parsed

),

with_derived as (

    select
        listing_id,
        product_url,
        nama_produk,
        nama_toko,
        lokasi_raw,
        harga,
        harga_normal,
        diskon_pct,
        terjual,
        jumlah_ulasan,
        rating,
        is_placeholder,
        is_truncated_url,
        is_official_store,
        is_imputed,

        -- GMV proxy (BIGINT to avoid INT32 overflow)
        (cast(harga as bigint) * cast(terjual as bigint))              as gmv_proxy,

        -- Bucket diskon (label)
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
