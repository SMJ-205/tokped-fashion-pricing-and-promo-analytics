-- fct_listing.sql
-- Mart: feature engineering — tagging kategori, spesifikasi di judul,
--       tier harga per kategori (quantile), dan semua derived metrics.
-- v2: 14 kategori (dari 10). Keyword rules diperluas dari analisis 10.246 baris 'lainnya'.
-- Note: DuckDB RE2 syntax — gunakan ' keyword ' (space-padded) bukan \b word boundary.

{{ config(materialized='table') }}

with base as (

    select * from {{ ref('int_clean_listings') }}

),

with_category as (

    select
        *,

        -- ────────────────────────────────────────────────────────────────────
        -- Tagging Kategori (keyword-based, lintas kategori)
        -- Urutan: paling spesifik → paling umum. 'lainnya' = fallback.
        -- ────────────────────────────────────────────────────────────────────
        case

            -- ── Hewan Peliharaan ──────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'makanan kucing|makanan anjing|cat food|dog food|pasir kucing|'
                'mainan kucing|collar anjing|pakan ikan|vitamin kucing|vitamin anjing|'
                'grooming kucing|pet carrier|cat litter|dog treat|obat kutu|vaksin hewan|'
                'tempat minum kucing|tempat makan kucing|kandang hamster|akuarium')
            then 'hewan_peliharaan'

            -- ── Otomotif & Perkakas ───────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'jas hujan|raincoat|mantel hujan|body protector|knee protector|'
                'sarung tangan motor|jaket motor|'
                'kunci |gembok|baut |mur |palu |gerinda|bor |perkakas|'
                'oli motor|oli mobil|minyak rem|kampas rem|helm |spion |knalpot|ban motor|ban mobil|pentil |onderdil|variasi motor|aksesoris motor|karburator|aki motor|aki mobil|'
                'kunci pas|tang |obeng|mata bor|mata gergaji|hacksaw|'
                'meteran|waterpass|skun |sekring|fuse |'
                'kabel aki|lampu motor|lampu mobil|wiper|karpet mobil|'
                'dongkrak|kompresor|velg |sparepart|spare part|'
                'vinyl lantai|list plafon| pipa |instalasi|keran |stop kontak|'
                'saklar |kabel listrik| mcb |kabel roll|fitting lampu|'
                'cat tembok|cat dinding|kunci pintu| engsel |semen ')
            then 'otomotif_perkakas'

            -- ── ATK, Kemasan & Perlengkapan Kantor ───────────────────────────
            when regexp_matches(lower(nama_produk),
                'buku |novel|komik|al-qur|alquran|majalah|'
                'buku tulis|buku notes| atk |pulpen|pensil|spidol|stabilo|'
                'penggaris|penghapus|tip-x|correction pen|kertas hvs|'
                'kertas label|stiker thermal|barcode|label stiker|'
                'id card|name tag|cetak pin|pin peniti|'
                'kantong plastik|plastik kresek|plastik hd|'
                'kotak kardus|bubble wrap|lakban coklat|lakban bening|'
                'paper bag|lunch box paper|bento mika|tray bento|'
                'box nasi|kotak nasi kemasan|food grade|kemasan|packaging')
            then 'atk_kemasan'

            -- ── Kesehatan & Bayi ──────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'masker medis|masker kesehatan|hazmat|sarung tangan medis|'
                'hand sanitizer|antiseptik|betadine|rivanol|plester luka|'
                'popok|diapers|pampers|tisu bayi|baby wipes|'
                'susu formula|susu bayi|mpasi|biskuit bayi|'
                'dot bayi|botol susu|empeng|teether|stroller|gendongan|'
                'obat batuk|obat flu|obat demam|suplemen kesehatan|'
                'alat tensi|termometer|oximeter|nebulizer|'
                'pembalut|softex|pantyliner|pembalut wanita')
            then 'kesehatan_bayi'

            -- ── Mainan, Hobi & Perhiasan ──────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'mainan |mobil mainan|mobil-mobilan|motor mainan|playset|building block|'
                'boneka|action figure|puzzle |lego|'
                'benang rajut|benang wool|benang wol|jarum rajut|'
                'cat akrilik|cat minyak| kuas |kanvas lukis|'
                'emas batangan|logam mulia|antam|lm antam|'
                'liontin emas|cincin emas|kalung emas|gelang emas|anting emas|'
                'perhiasan|gelang perak|cincin perak| bros |'
                'aksesoris rambut|jepit rambut mutiara')
            then 'mainan_hobi'

            -- ── Fashion Wanita ─────────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'gamis|pashmina|pasmina|kebaya|daster|abaya|tunik|mukena|kaftan|'
                'satin skirt|midi skirt|maxi skirt|corset|bustier|crop top|'
                'pakaian wanita|baju wanita|atasan wanita|longsleeve wanita|'
                'dress |hijab |blouse | rok |legging|longsleeve loose')
            then 'fashion_wanita'

            -- ── Fashion Pria ───────────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'kemeja pria|kaos pria|celana pria|batik pria|jaket pria|'
                'baju koko|sarung |boxer pria|brief pria|polo shirt pria|'
                'pakaian pria|baju pria|atasan pria')
            then 'fashion_pria'

            -- ── Fashion Umum ───────────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'kaos |hoodie|sweater|jaket |t-shirt|tshirt|kemeja |jeans |'
                'celana |shorts|baju |longsleeve |oversized|streetwear|ootd|'
                'cardigan| vest |polo |henley|flannel|bahan katun|bahan cotton')
            then 'fashion_umum'

            -- ── Sepatu & Aksesori Fashion ──────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'jepit rambut|sisir|hair clip|jedai|wig |'
                'sepatu |sandal |sling bag|slingbag|tote bag|backpack|ransel |koper|travel bag|selempang|'
                'dompet |topi |kacamata|jam tangan|ikat pinggang|'
                'gelang |kalung |cincin |anting |scrunchie|headband|'
                'ikat rambut|bando |bandana|scarf |payung ')
            then 'sepatu_aksesori'

            -- ── Elektronik & Gadget ───────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'speaker|soundbar|subwoofer|amplifier|microphone|mic wireless|'
                'handphone|smartphone|laptop|tablet|charger|powerbank|earphone|headset|'
                'keyboard|harddisk|router|kamera|smartwatch|monitor|'
                'flashdisk|flash disk|kabel data|kabel lightning|kabel type c|'
                'kabel lan|rj45|cat6 |mousepad|led strip|cctv|'
                'baterai |battery|adaptor|converter|galaxy buds|airpods|tws|'
                'iphone|samsung galaxy|xiaomi|oppo |vivo |realme|'
                'hair dryer|pengering rambut|speaker bluetooth|speaker aktif|'
                ' hp |headphone|gaming mouse|gaming keyboard|'
                'mouse wireless|mouse logitech|mouse bluetooth|wireless mouse|'
                'logitech|razer |corsair|mechanical keyboard|gaming headset|'
                'sandisk|seagate|western digital|wd external|toshiba external')
            then 'elektronik'

            -- ── Kecantikan & Perawatan ────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'skincare|serum |moisturizer|sunscreen| spf |lipstik|'
                'maskara|foundation|concealer|sabun muka|shampoo|'
                'kondisioner|body lotion|parfum|deodorant|toner |'
                'essence|micellar|sheet mask|sleeping mask|lip tint|'
                'bb cream|cc cream|setting spray|blush on|eyebrow|'
                'lip cream|lip balm|lip gloss|lip stain|lipstick|'
                'mascara|eyeliner|eyeshadow|eye shadow|highlighter|'
                'bronzer|primer |cushion |'
                'pasta gigi|sikat gigi|mouthwash|obat kumur|'
                'sabun mandi|body wash|shower gel|lulur |'
                'deodoran|antiperspirant|'
                'vitamin rambut|hair mask|hair serum|hair tonic|'
                'hair oil|minyak rambut|keratin treatment|'
                'eau de toilette|body mist|body fragrance|perfume|'
                'gunting kuku|pembersih telinga|masker organik|'
                'gluta soap|sabun pencerah|sabun pemutih|'
                'clay mask|masker wajah|facial wash|face wash|'
                'micellar water|make up|makeup| bpom |'
                'pelembab bibir|tinted lip|lip care|pelembab wajah|'
                'face serum|niacinamide|hyaluronic|retinol|ceramide|'
                'hmns |innisfree|skintific|wardah|maybelline|revlon|pixy|'
                'madame gie|mineral botanica|ms glow|emina |nacific|'
                'tinted moisturizer|loose powder|compact powder|no sebum|'
                'setting powder|translucent powder|face powder')
            then 'kecantikan'

            -- ── Rumah Tangga ──────────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'kompor|regulator gas|tabung gas|tungku|pemantik api|'
                'tanaman|pot bunga|pot tanaman|pupuk|bibit tanaman|'
                'kayu jati|pintu kayu|jendela|gantungan kunci|'
                'panci |wajan |spatula|gelas |piring |mangkok|'
                'sapu |ember |taplak|bantal |selimut|rak |'
                'lemari |kursi |meja |dispenser|blender|rice cooker|'
                'setrika|vacuum cleaner|kipas angin|ac portable|'
                'lampu |led bulb|downlight|bohlam|fitting |'
                'karpet |gordyn|tirai |gorden|'
                'cermin |jam dinding|wall decor|kaligrafi|'
                'tissue |tisu |tempat tisu|tempat sabun|'
                'tumbler|botol minum|termos |'
                'kotak makan|lunch box|tempat makan|food container|'
                'sendok garpu|pisau dapur|talenan|toples |'
                'handuk |sabun cuci|deterjen|pewangi pakaian|'
                'rak sepatu|gantungan baju|clothes hanger|'
                'sofa |furniture|lemari pakaian|meja makan|'
                'springbed|kasur |guling |bed cover|sprei|'
                'sikat toilet|sikat wc|pel lantai|sapu lantai|'
                'ranjang|dipan |nakas |meja rias|meja belajar|'
                'kursi lipat|tangga lipat|rak dinding|'
                'dekorasi rumah|hiasan rumah|wallpaper sticker|'
                'tempat tidur|lampu tidur|lampu kamar|'
                'tong sampah|tempat sampah|sikat lantai|'
                'celemek|apron |keset |lap tangan|lap piring|'
                'alat masak|perlengkapan masak|peralatan dapur|'
                'wajan anti lengket|kompor listrik|rice box|'
                'rak dapur|organizer dapur|tempat bumbu|'
                'spons cuci|scotch brite|sabun piring|'
                'sarung bantal|sarung guling|bed sheet|'
                'keramik |lemari es mini|kulkas mini')
            then 'rumah_tangga'

            -- ── Olahraga & Fitness ────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'raket |sepatu olahraga|dumbbell|matras |jersey |'
                'celana olahraga|tas gym|sepeda |treadmill|gym |'
                'resistance band|protein |whey |skipping|badminton|'
                'headband tennis|sepatu lari|sepatu futsal|bola basket|'
                'bola sepak|bola voli|renang|kacamata renang|'
                'yoga mat|foam roller|jump rope|pull up bar|'
                'jersey bola|jersey futsal|glove tinju|samsak')
            then 'olahraga'

            -- ── Makanan & Minuman ──────────────────────────────────────────────
            when regexp_matches(lower(nama_produk),
                'snack |kopi |teh |cokelat|indomie|mie goreng|mie sedap|mie instant|'
                'gula pasir|gula merah|tepung |minyak goreng|'
                'kecap |saus sambal|sambal|royco|masako|penyedap|'
                'basreng|cireng|siomay|dimsum |keripik|crackers|biskuit|'
                'daging sapi|daging ayam|sei sapi|iga sapi|tulang iga|'
                'alpukat|buah |jeruk |timun |labu |kentang |'
                'frozen food|bakso |nugget|sosis |beras |'
                'jamu |herbal |madu hutan|suplemen makanan|'
                'jelly candy|dodol|rumput laut|'
                'sayuran|benih |bibit |daging paha|fillet|sukiyaki|'
                'alpukat frozen|buah beku|minuman |cemilan |kue |roti |'
                'granola|yogurt|susu |madu |snack')
            then 'makanan_minuman'

            else 'lainnya'

        end                                                             as kategori,

        -- ────────────────────────────────────────────────────────────────────
        -- Tagging Spesifikasi/Material di Judul (untuk H5)
        -- ────────────────────────────────────────────────────────────────────
        regexp_matches(
            lower(nama_produk),
            'katun|cotton|polyester|rayon|linen|denim|sifon|wool|fleece|'
            'besi|aluminium|plastik|kayu|stainless|kulit|kanvas|nylon|'
            'spandex|viscose|bamboo fiber|microfiber'
        )                                                               as has_spec_keyword,

        -- Spesifikasi di 3 kata PERTAMA (H5: posisi keyword di judul)
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
        listing_id,
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
