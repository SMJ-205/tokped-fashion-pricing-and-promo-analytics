-- fct_listing.sql
-- Mart: feature engineering — tagging kategori, spesifikasi di judul,
--       tier harga per kategori (quantile), dan semua derived metrics.

{{ config(materialized='table') }}

with base as (

    select * from {{ ref('int_clean_listings') }}

),

with_category as (

    select
        *,

        -- ────────────────────────────────────────────────────────────────────
        -- Tagging Kategori (keyword-based, lintas kategori)
        -- Urutan penting: lebih spesifik dulu, lebih umum belakangan
        -- ────────────────────────────────────────────────────────────────────
        case
            -- Hewan Peliharaan (keyword spesifik, harus sebelum "makanan")
            when regexp_matches(lower(nama_produk),
                'makanan kucing|makanan anjing|cat food|dog food|kandang|akuarium|'
                'pasir kucing|mainan kucing|collar anjing|leash|pakan ikan|'
                'vitamin kucing|vitamin anjing|grooming kucing|pet carrier')
            then 'hewan_peliharaan'

            -- Fashion Wanita (spesifik wanita dulu)
            when regexp_matches(lower(nama_produk),
                '\bgamis\b|\bdress\b|\bhijab\b|pashmina|kebaya|blouse|'
                '\brok\b|legging|daster|abaya|tunik|mukena|kaftan')
            then 'fashion_wanita'

            -- Fashion Pria (spesifik pria dulu)
            when regexp_matches(lower(nama_produk),
                'kemeja pria|kaos pria|celana pria|batik pria|jaket pria|'
                'baju koko|sarung\b|boxer|brief pria|polo shirt pria')
            then 'fashion_pria'

            -- Fashion Umum (gender-neutral / tidak ada label pria/wanita)
            when regexp_matches(lower(nama_produk),
                '\bkaos\b|hoodie|sweater|\bjaket\b|t-shirt|tshirt|'
                '\bkemeja\b|\bjeans\b|\bcelana\b|shorts|\bbaju\b')
            then 'fashion_umum'

            -- Sepatu & Aksesori
            when regexp_matches(lower(nama_produk),
                '\bsepatu\b|\bsandal\b|\btas\b|\bdompet\b|\btopi\b|'
                'kacamata|jam tangan|ikat pinggang|\bgelang\b|\bkalung\b|'
                '\bcincin\b|anting|jepit rambut|scrunchie')
            then 'sepatu_aksesori'

            -- Elektronik
            when regexp_matches(lower(nama_produk),
                '\bhp\b|handphone|smartphone|\blaptop\b|\btablet\b|'
                '\bcharger\b|powerbank|earphone|headset|\bspeaker\b|'
                'keyboard|\bmouse\b|\bram\b|harddisk|\bssd\b|router|'
                '\bkamera\b|action cam|smartwatch|\btv\b|monitor')
            then 'elektronik'

            -- Kecantikan & Perawatan
            when regexp_matches(lower(nama_produk),
                'skincare|serum\b|moisturizer|sunscreen|\bspf\b|lipstik|'
                'maskara|foundation|concealer|sabun muka|\bshampoo\b|'
                'kondisioner|body lotion|\bparfum\b|deodorant|\btoner\b|'
                'essence|\bmicellar\b|sheet mask|sleeping mask|lip tint|'
                'BB cream|CC cream|setting spray|blush on|eyebrow')
            then 'kecantikan'

            -- Rumah Tangga
            when regexp_matches(lower(nama_produk),
                '\bpanci\b|\bwajan\b|spatula|\bgelas\b|\bpiring\b|mangkok|'
                '\bsapu\b|\bpel\b|\bember\b|taplak|\bbantal\b|selimut|\brak\b|'
                '\blemari\b|\bkursi\b|\bmeja\b|dispenser|blender|rice cooker|'
                '\bsetrika\b|vacuum cleaner|kipas angin|AC portable')
            then 'rumah_tangga'

            -- Olahraga
            when regexp_matches(lower(nama_produk),
                '\braket\b|\bbola\b|sepatu olahraga|dumbbell|matras\b|'
                '\bjersey\b|celana olahraga|tas gym|\bsepeda\b|treadmill|'
                '\bgym\b|resistance band|protein|whey|skipping|badminton')
            then 'olahraga'

            -- Makanan & Minuman
            when regexp_matches(lower(nama_produk),
                '\bsnack\b|\bkopi\b|\bteh\b|\bcokelat\b|\bmie\b|\bberas\b|'
                '\bbumbu\b|\bsaus\b|\bminuman\b|\bcemilan\b|\bkue\b|\broti\b|'
                'keripik|crackers|biskuit|granola|madu|susu\b|yogurt')
            then 'makanan_minuman'

            else 'lainnya'
        end                                                             as kategori,

        -- ────────────────────────────────────────────────────────────────────
        -- Tagging Spesifikasi/Material di Judul (untuk H5)
        -- Deteksi apakah kata kunci spesifikasi ada di seluruh judul
        -- ────────────────────────────────────────────────────────────────────
        regexp_matches(
            lower(nama_produk),
            'katun|cotton|polyester|rayon|linen|denim|sifon|wool|fleece|'
            'besi|aluminium|plastik|kayu|stainless|kulit|kanvas|nylon|'
            'spandex|viscose|bamboo fiber|microfiber'
        )                                                               as has_spec_keyword,

        -- Apakah spesifikasi ada di 3 kata PERTAMA (posisi awal judul = H5)
        regexp_matches(
            lower(
                split_part(nama_produk, ' ', 1) || ' ' ||
                split_part(nama_produk, ' ', 2) || ' ' ||
                split_part(nama_produk, ' ', 3)
            ),
            'katun|cotton|polyester|rayon|linen|denim|sifon|wool|fleece|'
            'besi|aluminium|plastik|kayu|stainless|kulit|kanvas|nylon|'
            'spandex|viscose|bamboo fiber|microfiber'
        )                                                               as has_spec_at_start

    from base

),

with_price_tier as (

    select
        *,

        -- Tier harga per kategori (quantile N-tile 3)
        -- Produk dengan harga_normal null → tier null
        case
            when harga_normal is null or harga_normal = 0 then null
            else ntile(3) over (
                    partition by kategori
                    order by harga_normal
                 )
        end                                                             as price_tier_num

    from with_category

),

final as (

    select
        -- ── Core ──────────────────────────────────────────────────────────────
        product_url,
        nama_produk,
        nama_toko,
        lokasi_raw,
        wilayah,

        -- ── Pricing ───────────────────────────────────────────────────────────
        harga,
        harga_normal,
        diskon_pct,
        bucket_diskon,
        bucket_diskon_order,

        -- Tier label
        case price_tier_num
            when 1 then 'bawah'
            when 2 then 'menengah'
            when 3 then 'atas'
            else null
        end                                                             as tier_harga,

        -- ── Volume & Engagement ───────────────────────────────────────────────
        terjual,
        jumlah_ulasan,
        rating,
        gmv_proxy,

        -- ── Tagging ───────────────────────────────────────────────────────────
        kategori,
        has_spec_keyword,
        has_spec_at_start,

        -- ── Flags ─────────────────────────────────────────────────────────────
        is_official_store,
        is_imputed

    from with_price_tier

)

select * from final
