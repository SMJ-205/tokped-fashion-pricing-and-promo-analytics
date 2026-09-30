-- int_clean_listings.sql
-- Intermediate: exclude placeholder & baris harga=0; normalisasi lokasi → wilayah.

{{ config(materialized='view') }}

with source as (

    select * from {{ ref('stg_listings') }}

),

clean as (

    select * from source
    where
        is_placeholder = false
        and harga > 0
        and terjual >= 0

),

with_region as (

    select
        *,

        -- Normalisasi kota → wilayah (null untuk 'Indonesia' — exclude dari analisis wilayah)
        case
            when lower(lokasi_raw) = 'indonesia'            then null
            when lower(lokasi_raw) like '%jakarta%'         then 'DKI Jakarta'
            when lower(lokasi_raw) like '%bandung%'         then 'Jawa Barat'
            when lower(lokasi_raw) like '%bekasi%'          then 'Jawa Barat'
            when lower(lokasi_raw) like '%depok%'           then 'Jawa Barat'
            when lower(lokasi_raw) like '%bogor%'           then 'Jawa Barat'
            when lower(lokasi_raw) like '%karawang%'        then 'Jawa Barat'
            when lower(lokasi_raw) like '%tangerang%'       then 'Banten'
            when lower(lokasi_raw) like '%serang%'          then 'Banten'
            when lower(lokasi_raw) like '%surabaya%'        then 'Jawa Timur'
            when lower(lokasi_raw) like '%malang%'          then 'Jawa Timur'
            when lower(lokasi_raw) like '%sidoarjo%'        then 'Jawa Timur'
            when lower(lokasi_raw) like '%gresik%'          then 'Jawa Timur'
            when lower(lokasi_raw) like '%semarang%'        then 'Jawa Tengah'
            when lower(lokasi_raw) like '%solo%'            then 'Jawa Tengah'
            when lower(lokasi_raw) like '%surakarta%'       then 'Jawa Tengah'
            when lower(lokasi_raw) like '%purwokerto%'      then 'Jawa Tengah'
            when lower(lokasi_raw) like '%yogyakarta%'
              or lower(lokasi_raw) like '%jogja%'           then 'DI Yogyakarta'
            when lower(lokasi_raw) like '%medan%'           then 'Sumatera Utara'
            when lower(lokasi_raw) like '%palembang%'       then 'Sumatera Selatan'
            when lower(lokasi_raw) like '%pekanbaru%'       then 'Riau'
            when lower(lokasi_raw) like '%batam%'           then 'Kepulauan Riau'
            when lower(lokasi_raw) like '%makassar%'        then 'Sulawesi Selatan'
            when lower(lokasi_raw) like '%denpasar%'
              or lower(lokasi_raw) like '%bali%'            then 'Bali'
            when lower(lokasi_raw) like '%balikpapan%'
              or lower(lokasi_raw) like '%samarinda%'       then 'Kalimantan Timur'
            when lower(lokasi_raw) like '%banjarmasin%'     then 'Kalimantan Selatan'
            when lower(lokasi_raw) like '%pontianak%'       then 'Kalimantan Barat'
            else 'Lainnya'
        end                                                 as wilayah

    from clean

)

select * from with_region
