/**
 * app.js - Tokopedia E-Commerce Pricing & Promo Analytics
 * Client-side reactive logic for Vercel deployment with smooth transitions
 */

let appData = null;
let chartMedian = null;
let chartMean = null;
let chartRegional = null;

// Currency Formatter
function formatRupiah(num) {
  if (num === null || num === undefined || isNaN(num)) return '-';
  return 'Rp ' + Math.round(num).toLocaleString('id-ID');
}

function formatNumber(num) {
  if (num === null || num === undefined || isNaN(num)) return '-';
  return Math.round(num).toLocaleString('id-ID');
}

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  await loadDashboardData();
  setupSimulator();
  setupDiscountAnalytics();
  setupRegionalAnalytics();
  setupStoreAnalytics();
  setupDataExplorer();
});

// Tab Navigation with Smooth Transition
function setupTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-tab');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
      }

      // Smoothly resize charts on newly visible tab
      setTimeout(() => {
        if (chartMedian) chartMedian.resize();
        if (chartMean) chartMean.resize();
        if (chartRegional) chartRegional.resize();
      }, 50);
    });
  });
}

// Load Precomputed JSON Data
async function loadDashboardData() {
  try {
    const res = await fetch('data/dashboard_data.json');
    appData = await res.json();
  } catch (err) {
    console.error('Gagal membaca data/dashboard_data.json:', err);
  }
}

// Setup Simulator Logic
function setupSimulator() {
  if (!appData) return;

  const categorySelect = document.getElementById('sim-category');
  const normalPriceInput = document.getElementById('sim-normal-price');
  const oldDiscountSlider = document.getElementById('sim-old-discount');
  const newDiscountSlider = document.getElementById('sim-new-discount');
  const valOldDiscount = document.getElementById('val-old-discount');
  const valNewDiscount = document.getElementById('val-new-discount');
  const hppInput = document.getElementById('sim-hpp-pct');
  const feeInput = document.getElementById('sim-fee-pct');
  const packingInput = document.getElementById('sim-packing');
  const volumeInput = document.getElementById('sim-base-vol');

  // Populate categories
  const nonLainnyaCats = appData.categories.filter(c => c.kategori !== 'lainnya');
  nonLainnyaCats.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c.kategori;
    opt.textContent = c.kategori;
    if (c.kategori === 'fashion_wanita') opt.selected = true;
    categorySelect.appendChild(opt);
  });

  function updateCategoryPrice() {
    const selected = categorySelect.value;
    const catObj = appData.categories.find(c => c.kategori === selected);
    if (catObj && catObj.median_harga_normal) {
      normalPriceInput.value = catObj.median_harga_normal;
    }
    calculateSimulation();
  }

  categorySelect.addEventListener('change', updateCategoryPrice);

  oldDiscountSlider.addEventListener('input', (e) => {
    valOldDiscount.textContent = e.target.value + '%';
    calculateSimulation();
  });

  newDiscountSlider.addEventListener('input', (e) => {
    valNewDiscount.textContent = e.target.value + '%';
    calculateSimulation();
  });

  [normalPriceInput, hppInput, feeInput, packingInput, volumeInput].forEach(input => {
    input.addEventListener('input', calculateSimulation);
  });

  calculateSimulation();
}

function calculateSimulation() {
  const normalPrice = parseFloat(document.getElementById('sim-normal-price').value) || 100000;
  const oldDisc = parseFloat(document.getElementById('sim-old-discount').value) || 0;
  const newDisc = parseFloat(document.getElementById('sim-new-discount').value) || 0;
  const hppPct = parseFloat(document.getElementById('sim-hpp-pct').value) || 45;
  const feePct = parseFloat(document.getElementById('sim-fee-pct').value) || 6.5;
  const packing = parseFloat(document.getElementById('sim-packing').value) || 3000;
  const volumeBasis = parseFloat(document.getElementById('sim-base-vol').value) || 500;

  const hppRp = normalPrice * (hppPct / 100);

  // Status Lama
  const oldPrice = normalPrice * (1 - oldDisc / 100);
  const oldFee = oldPrice * (feePct / 100);
  const oldMarginRp = oldPrice - hppRp - oldFee - packing;
  const oldMarginPct = oldPrice > 0 ? (oldMarginRp / oldPrice * 100) : 0;
  const oldTotalProfit = oldMarginRp * volumeBasis;

  // Empirical Saturation Multiplier (H1)
  function getScore(d) {
    if (d === 0) return 1.0;
    if (d <= 10) return 2.0;
    if (d <= 20) return 2.6;
    if (d <= 30) return 3.2; // Peak
    if (d <= 50) return 3.1; // Plateau
    return 3.0; // Diminishing return
  }

  const volMult = getScore(newDisc) / getScore(oldDisc);
  const newVolumeEst = Math.round(volumeBasis * volMult);

  // Status Baru
  const newPrice = normalPrice * (1 - newDisc / 100);
  const newFee = newPrice * (feePct / 100);
  const newMarginRp = newPrice - hppRp - newFee - packing;
  const newMarginPct = newPrice > 0 ? (newMarginRp / newPrice * 100) : 0;
  const newTotalProfit = newMarginRp * newVolumeEst;

  const diffProfit = newTotalProfit - oldTotalProfit;
  const diffMarginRp = newMarginRp - oldMarginRp;
  const diffMarginPct = newMarginPct - oldMarginPct;

  // Update Mini Metrics with Smooth Pulse Animation
  const resPriceEl = document.getElementById('res-price');
  const resMarginEl = document.getElementById('res-margin');
  const resProfitEl = document.getElementById('res-profit');
  const deltaMarginEl = document.getElementById('delta-margin');
  const deltaProfitEl = document.getElementById('delta-profit');

  resPriceEl.textContent = formatRupiah(newPrice);
  document.getElementById('delta-price').textContent = (newPrice >= oldPrice ? '+' : '') + formatRupiah(newPrice - oldPrice);

  resMarginEl.textContent = formatRupiah(newMarginRp);
  deltaMarginEl.textContent = (diffMarginPct >= 0 ? '+' : '') + diffMarginPct.toFixed(1) + '% margin';
  deltaMarginEl.className = 'mini-delta ' + (diffMarginPct >= 0 ? 'positive' : 'negative');

  resProfitEl.textContent = formatRupiah(newTotalProfit);
  deltaProfitEl.textContent = (diffProfit >= 0 ? '+' : '') + formatRupiah(diffProfit) + ' / bln';
  deltaProfitEl.className = 'mini-delta ' + (diffProfit >= 0 ? 'positive' : 'negative');

  // Trigger subtle tactile pulse
  [resPriceEl, resMarginEl, resProfitEl].forEach(el => {
    el.classList.remove('pulse-change');
    void el.offsetWidth;
    el.classList.add('pulse-change');
  });

  // Recommendation Box
  const alertBox = document.getElementById('sim-alert');
  const alertTitle = document.getElementById('alert-title');
  const alertDesc = document.getElementById('alert-desc');

  if (oldDisc > 30 && newDisc <= 30 && diffProfit > 0) {
    alertBox.className = 'alert-box alert-success';
    alertTitle.textContent = 'Rekomendasi Strategis: Pangkas Diskon ke ' + newDisc + '%';
    alertDesc.textContent = 'Memangkas diskon dari ' + oldDisc + '% ke ' + newDisc + '% mengembalikan margin per unit sebesar ' +
      formatRupiah(diffMarginRp) + ' (+' + diffMarginPct.toFixed(1) + '% poin) tanpa menjatuhkan volume ke luar area optimal. Potensi kenaikan laba kotor: +' + formatRupiah(diffProfit) + ' per bulan.';
  } else if (diffProfit >= 0) {
    alertBox.className = 'alert-box alert-success';
    alertTitle.textContent = 'Dampak Positif terhadap Margin Kotor';
    alertDesc.textContent = 'Simulasi diskon baru ini diperkirakan meningkatkan laba kotor bulanan sebesar +' + formatRupiah(diffProfit) + '.';
  } else {
    alertBox.className = 'alert-box alert-warning';
    alertTitle.textContent = 'Perhatian: Trade-off Penurunan Laba Kotor';
    alertDesc.textContent = 'Perubahan parameter ini diperkirakan menurunkan laba kotor bulanan sebesar ' + formatRupiah(diffProfit) + '. Evaluasi kembali elastisitas volume.';
  }

  // Populate Table Comparison
  const tbody = document.getElementById('comparison-tbody');
  const rows = [
    { label: 'Harga Coret (Normal)', oldVal: formatRupiah(normalPrice), newVal: formatRupiah(normalPrice) },
    { label: 'Tingkat Diskon Diterapkan', oldVal: oldDisc + '%', newVal: newDisc + '%' },
    { label: 'Harga Jual Bersih Efektif', oldVal: formatRupiah(oldPrice), newVal: formatRupiah(newPrice) },
    { label: 'HPP Pokok Barang', oldVal: formatRupiah(hppRp), newVal: formatRupiah(hppRp) },
    { label: 'Biaya Admin Marketplace', oldVal: formatRupiah(oldFee), newVal: formatRupiah(newFee) },
    { label: 'Biaya Packing & Operasional', oldVal: formatRupiah(packing), newVal: formatRupiah(packing) },
    { label: 'Margin Bersih per Unit (Rp)', oldVal: formatRupiah(oldMarginRp), newVal: formatRupiah(newMarginRp) },
    { label: 'Margin Bersih per Unit (%)', oldVal: oldMarginPct.toFixed(1) + '%', newVal: newMarginPct.toFixed(1) + '%' },
    { label: 'Proyeksi Volume Penjualan', oldVal: formatNumber(volumeBasis) + ' unit', newVal: formatNumber(newVolumeEst) + ' unit' },
    { label: 'Estimasi Total Laba Kotor', oldVal: formatRupiah(oldTotalProfit), newVal: formatRupiah(newTotalProfit) }
  ];

  tbody.innerHTML = rows.map(r => `
    <tr>
      <td><strong>${r.label}</strong></td>
      <td>${r.oldVal}</td>
      <td><span class="badge badge-info">${r.newVal}</span></td>
    </tr>
  `).join('');
}

// Discount Analytics (H1 & H2) with Smooth Morphing Charts
function setupDiscountAnalytics() {
  if (!appData) return;

  const selectH1 = document.getElementById('filter-category-h1');
  const allOption = document.createElement('option');
  allOption.value = 'all';
  allOption.textContent = 'Semua Kategori';
  selectH1.appendChild(allOption);

  appData.categories.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c.kategori;
    opt.textContent = c.kategori;
    selectH1.appendChild(opt);
  });

  selectH1.addEventListener('change', renderDiscountCharts);
  renderDiscountCharts();
}

function renderDiscountCharts() {
  const filterCat = document.getElementById('filter-category-h1').value;
  let bucketData = [];

  if (filterCat === 'all') {
    bucketData = appData.overall_buckets;
  } else {
    bucketData = appData.category_buckets.filter(b => b.kategori === filterCat);
  }

  bucketData.sort((a, b) => a.bucket_diskon_order - b.bucket_diskon_order);

  const labels = bucketData.map(b => b.bucket_diskon);
  const medianSold = bucketData.map(b => b.median_terjual);
  const meanSold = bucketData.map(b => b.mean_terjual);

  // Render Table with smooth row animation
  const tbody = document.getElementById('bucket-tbody');
  tbody.innerHTML = bucketData.map(b => {
    let statusBadge = '<span class="badge badge-info">Optimal Margin</span>';
    if (b.bucket_diskon === '0%') statusBadge = '<span class="badge badge-warning">Baseline (26 unit)</span>';
    if (b.bucket_diskon === '1-10%') statusBadge = '<span class="badge badge-success">Lonjakan Utama (2x Laris)</span>';
    if (b.bucket_diskon === '11-20%') statusBadge = '<span class="badge badge-info">Optimal Margin</span>';
    if (b.bucket_diskon === '21-30%') statusBadge = '<span class="badge badge-warning">Plateau Volume</span>';
    if (b.bucket_diskon === '31-50%' || b.bucket_diskon === '>50%') statusBadge = '<span class="badge badge-danger">Margin Burn</span>';

    return `
      <tr>
        <td><strong>${b.bucket_diskon}</strong></td>
        <td>${formatNumber(b.total_listing)}</td>
        <td>${formatNumber(b.median_terjual)} unit</td>
        <td>${formatNumber(b.mean_terjual)} unit</td>
        <td>${formatRupiah(b.median_harga)}</td>
        <td>${statusBadge}</td>
      </tr>
    `;
  }).join('');

  // Smooth Chart 1: Median Sold
  if (chartMedian) {
    chartMedian.data.labels = labels;
    chartMedian.data.datasets[0].data = medianSold;
    chartMedian.update();
  } else {
    const ctxMedian = document.getElementById('chart-median-sold').getContext('2d');
    chartMedian = new Chart(ctxMedian, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Median Terjual (Unit)',
          data: medianSold,
          backgroundColor: '#4f46e5',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 450,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#94a3b8' }
          }
        }
      }
    });
  }

  // Smooth Chart 2: Mean Sold
  if (chartMean) {
    chartMean.data.labels = labels;
    chartMean.data.datasets[0].data = meanSold;
    chartMean.update();
  } else {
    const ctxMean = document.getElementById('chart-mean-sold').getContext('2d');
    chartMean = new Chart(ctxMean, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Rata-rata Terjual (Unit)',
          data: meanSold,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointBackgroundColor: '#ef4444',
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 450,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#94a3b8' }
          }
        }
      }
    });
  }
}

// Regional Analytics (H4)
function setupRegionalAnalytics() {
  if (!appData || !appData.regions) return;

  const topRegions = appData.regions.slice(0, 8);
  const labels = topRegions.map(r => r.wilayah);
  const prices = topRegions.map(r => r.median_harga);

  const tbody = document.getElementById('region-tbody');
  tbody.innerHTML = topRegions.map(r => `
    <tr>
      <td><strong>${r.wilayah}</strong></td>
      <td>${formatNumber(r.listing_count)}</td>
      <td>${formatRupiah(r.median_harga)}</td>
      <td>${formatRupiah(r.gmv_total)}</td>
    </tr>
  `).join('');

  if (chartRegional) {
    chartRegional.data.labels = labels;
    chartRegional.data.datasets[0].data = prices;
    chartRegional.update();
  } else {
    const ctx = document.getElementById('chart-regional-price').getContext('2d');
    chartRegional = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Median Harga (Rp)',
          data: prices,
          backgroundColor: '#0d9488',
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 450,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              color: '#94a3b8',
              callback: (v) => 'Rp ' + (v / 1000) + 'k'
            }
          },
          y: {
            grid: { display: false },
            ticks: { color: '#94a3b8' }
          }
        }
      }
    });
  }
}

// Store & Format Analytics (H3, H5, H6)
function setupStoreAnalytics() {
  if (!appData) return;

  // H6 Table: Official Store
  const tbodyOS = document.getElementById('official-store-tbody');
  tbodyOS.innerHTML = appData.official_store.map(s => {
    const isOS = s.is_official_store === true || s.is_official_store === 1;
    return `
      <tr>
        <td><strong>${isOS ? 'Official Store' : 'Toko Reguler'}</strong></td>
        <td>${formatNumber(s.listing_count)}</td>
        <td>${formatRupiah(s.median_harga)}</td>
        <td>${formatNumber(s.median_terjual)} unit</td>
        <td>${s.mean_diskon}%</td>
      </tr>
    `;
  }).join('');

  // H5 Table: Spec in Title
  const tbodySpec = document.getElementById('spec-tbody');
  tbodySpec.innerHTML = appData.spec_title.map(s => {
    const hasSpec = s.has_spec_at_start === true || s.has_spec_at_start === 1;
    return `
      <tr>
        <td><strong>${hasSpec ? 'Spesifikasi di Awal Judul' : 'Format Judul Standar'}</strong></td>
        <td>${formatNumber(s.listing_count)}</td>
        <td>${formatRupiah(s.median_harga)}</td>
        <td>${formatNumber(s.median_terjual)} unit</td>
      </tr>
    `;
  }).join('');

  // H3 Table: Price Tier vs Rating
  const tbodyTier = document.getElementById('tier-tbody');
  tbodyTier.innerHTML = appData.price_tiers.map(t => `
    <tr>
      <td><strong>Tier ${t.tier_harga}</strong></td>
      <td>${formatNumber(t.listing_count)}</td>
      <td>${t.mean_rating.toFixed(3)}</td>
      <td>${t.median_rating.toFixed(2)}</td>
      <td>${t.std_rating.toFixed(3)}</td>
    </tr>
  `).join('');
}

// Data Explorer with Live Search
function setupDataExplorer() {
  if (!appData || !appData.sample_listings) return;

  const searchInput = document.getElementById('explorer-search');
  const tbody = document.getElementById('explorer-tbody');

  function renderTable(listings) {
    tbody.innerHTML = listings.slice(0, 50).map(l => {
      const isOS = l.is_official_store === true || l.is_official_store === 1;
      return `
        <tr>
          <td title="${l.nama_produk}">${l.nama_produk.length > 40 ? l.nama_produk.slice(0, 40) + '...' : l.nama_produk}</td>
          <td><span class="badge badge-info">${l.kategori}</span></td>
          <td>${l.nama_toko}</td>
          <td>${l.wilayah}</td>
          <td>${formatRupiah(l.harga)}</td>
          <td>${l.diskon_pct > 0 ? l.diskon_pct + '%' : '-'}</td>
          <td>${formatNumber(l.terjual)}</td>
          <td>${l.rating ? l.rating.toFixed(1) : '-'}</td>
          <td>${isOS ? '<span class="badge badge-success">Official</span>' : 'Reguler'}</td>
        </tr>
      `;
    }).join('');
  }

  renderTable(appData.sample_listings);

  searchInput.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = appData.sample_listings.filter(l => 
      l.nama_produk.toLowerCase().includes(q) || l.nama_toko.toLowerCase().includes(q)
    );
    renderTable(filtered);
  });
}
