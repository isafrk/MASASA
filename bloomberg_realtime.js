/* ═══════════════════════════════════════════════════════════════════
   BLOOMFREE TERMINAL — realtime.js
   Live data from:
     • Finnhub (stocks, news, forex)   — api key provided
     • CoinGecko (crypto)              — free, no key
     • Frankfurter (FX rates)          — free, no key
═══════════════════════════════════════════════════════════════════ */

'use strict';

const FINNHUB_KEY = 'd6lcqo9r01qrq6i27k8gd6lcqo9r01qrq6i27k90';
const FINNHUB_BASE = 'https://finnhub.io/api/v1';
const COINGECKO_BASE = 'https://api.coingecko.com/api/v3';
const FRANKFURTER_BASE = 'https://api.frankfurter.app';

// ── Throttle helper: prevent hammering APIs ──────────────────────
const _apiCache = {};
async function cachedFetch(url, ttlMs = 15000) {
    const now = Date.now();
    if (_apiCache[url] && now - _apiCache[url].ts < ttlMs) {
        return _apiCache[url].data;
    }
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        _apiCache[url] = { data, ts: now };
        return data;
    } catch (e) {
        console.warn('[RT] fetch failed:', url, e.message);
        return null;
    }
}

// ─────────────────────────────────────────────────────────────────
// FINNHUB — STOCK QUOTES
// Updates the STOCKS object in app.js with real prices
// ─────────────────────────────────────────────────────────────────
const US_SYMBOLS = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'JPM', 'V', 'JNJ', 'WMT', 'BAC'];

async function fetchFinnhubQuote(symbol) {
    const url = `${FINNHUB_BASE}/quote?symbol=${symbol}&token=${FINNHUB_KEY}`;
    return cachedFetch(url, 20000); // cache 20 sec
}

async function refreshUSStocks() {
    for (const sym of US_SYMBOLS) {
        const q = await fetchFinnhubQuote(sym);
        if (!q || !q.c || q.c === 0) continue;

        if (typeof STOCKS !== 'undefined' && STOCKS[sym]) {
            const prev = STOCKS[sym].price;
            STOCKS[sym].price = q.c;
            STOCKS[sym].prev = q.pc || STOCKS[sym].prev;

            // Update watchlist row directly
            const priceEl = document.getElementById(`wl-${sym}-price`);
            const chgEl = document.getElementById(`wl-${sym}-chg`);
            const pctEl = document.getElementById(`wl-${sym}-pct`);
            const row = document.getElementById(`wl-${sym}`);

            if (priceEl) {
                const up = q.c >= prev;
                const pct = ((q.c - q.pc) / q.pc) * 100;
                const diff = q.c - q.pc;

                priceEl.textContent = '$' + fmtPrice(q.c);
                if (chgEl) {
                    chgEl.textContent = (diff >= 0 ? '+' : '-') + '$' + Math.abs(diff).toFixed(2);
                    chgEl.className = diff >= 0 ? 'positive' : 'negative';
                }
                if (pctEl) {
                    pctEl.textContent = pctStr(pct);
                    pctEl.className = pct >= 0 ? 'positive' : 'negative';
                }
                if (row) flashRow(row, up);
                drawSpark(`spark-${sym}`, generateSparkData(STOCKS[sym]));
            }
        }
        await sleep(120); // gentle spacing to avoid rate limit
    }
    console.info('[RT] US stocks refreshed');
}

// ─────────────────────────────────────────────────────────────────
// FINNHUB — US INDICES (via ETF proxies / index quotes)
// ─────────────────────────────────────────────────────────────────
// Finnhub free tier supports US stocks. We use index symbols.
const INDEX_SYMBOL_MAP = {
    'idx-spx': '^GSPC',
    'idx-ndx': '^IXIC',
    'idx-dow': '^DJI',
    'idx-vix': '^VIX',
};

async function refreshUSIndices() {
    for (const [id, sym] of Object.entries(INDEX_SYMBOL_MAP)) {
        const url = `${FINNHUB_BASE}/quote?symbol=${sym}&token=${FINNHUB_KEY}`;
        const q = await cachedFetch(url, 30000);
        if (!q || !q.c || q.c === 0) continue;

        const base = INDICES[id]?.base || q.pc || q.c;
        const pct = ((q.c - base) / base) * 100;
        const up = pct >= 0;

        if (typeof indexCurrentPrices !== 'undefined') {
            indexCurrentPrices[id] = q.c;
            INDICES[id].base = q.pc || base; // use prev close as baseline
        }

        const card = document.getElementById(id);
        if (!card) continue;

        card.querySelector('.idx-price').textContent =
            q.c >= 1000
                ? q.c.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                : fmtPrice(q.c);
        const chgEl = card.querySelector('.idx-change');
        chgEl.textContent = pctStr(pct);
        chgEl.className = 'idx-change ' + (up ? 'positive' : 'negative');

        await sleep(150);
    }
    console.info('[RT] US indices refreshed');
}

// ─────────────────────────────────────────────────────────────────
// COINGECKO — CRYPTO PRICES
// ─────────────────────────────────────────────────────────────────
const CG_IDS = {
    BTC: 'bitcoin',
    ETH: 'ethereum',
    SOL: 'solana',
    BNB: 'binancecoin',
    XRP: 'ripple',
    DOGE: 'dogecoin',
    ADA: 'cardano',
    AVAX: 'avalanche-2',
};

async function refreshCrypto() {
    const ids = Object.values(CG_IDS).join(',');
    const url = `${COINGECKO_BASE}/simple/price?ids=${ids}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true`;
    const data = await cachedFetch(url, 60000); // CoinGecko: cache 60 sec (rate limiting)
    if (!data) return;

    // Update CRYPTOS array
    if (typeof CRYPTOS !== 'undefined') {
        CRYPTOS.forEach((c, i) => {
            const cgId = CG_IDS[c.sym];
            if (!cgId || !data[cgId]) return;
            const d = data[cgId];
            CRYPTOS[i].price = d.usd || c.price;
            CRYPTOS[i].change = d.usd_24h_change || 0;
            CRYPTOS[i].mcap = d.usd_market_cap
                ? fmtNum(d.usd_market_cap)
                : c.mcap;
            CRYPTOS[i].vol24 = d.usd_24h_vol
                ? fmtNum(d.usd_24h_vol)
                : c.vol24;
        });
    }

    // Also update BTC index card on dashboard
    const btcData = data['bitcoin'];
    if (btcData) {
        const bPrice = btcData.usd;
        const bPct = btcData.usd_24h_change || 0;
        const up = bPct >= 0;
        const card = document.getElementById('idx-btc');
        if (card) {
            card.querySelector('.idx-price').textContent =
                bPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            const chgEl = card.querySelector('.idx-change');
            chgEl.textContent = pctStr(bPct);
            chgEl.className = 'idx-change ' + (up ? 'positive' : 'negative');
        }
    }

    // Re-render crypto table if on that view
    if (typeof currentView !== 'undefined' && currentView === 'crypto') {
        renderCryptoTable();
    }

    console.info('[RT] Crypto refreshed');
}

// Override renderCryptoTable to use real 24h change
const _origRenderCrypto = typeof renderCryptoTable === 'function' ? renderCryptoTable : null;
function renderCryptoTableReal() {
    const tbody = document.getElementById('cryptoBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    CRYPTOS.forEach((c) => {
        const pct = c.change !== undefined ? c.change : rand(-2, 2);
        const up = pct >= 0;
        const tr = document.createElement('tr');
        tr.innerHTML = `
      <td>${c.sym} <span style="color:#555;font-size:9px">${c.name}</span></td>
      <td>$${fmtPrice(c.price)}</td>
      <td class="${up ? 'positive' : 'negative'}">${pctStr(pct)}</td>
      <td>${c.vol24}</td>
      <td>${c.mcap}</td>
      <td>${c.dom}%</td>
    `;
        tbody.appendChild(tr);
    });
}

// ─────────────────────────────────────────────────────────────────
// FRANKFURTER — FX RATES (free, no key)
// ─────────────────────────────────────────────────────────────────
async function refreshFX() {
    // Frankfurter gives latest rates with USD as base
    const url = `${FRANKFURTER_BASE}/latest?from=USD`;
    const data = await cachedFetch(url, 300000); // cache 5 min (FX updates slowly)
    if (!data || !data.rates) return;

    const r = data.rates;

    const currencyMap = {
        'EUR/USD': 1 / r.EUR,
        'GBP/USD': 1 / r.GBP,
        'USD/JPY': r.JPY,
        'USD/CHF': r.CHF,
        'AUD/USD': 1 / r.AUD,
        'NZD/USD': 1 / r.NZD,
        'USD/CAD': r.CAD,
        'USD/CNY': r.CNY,
        'USD/INR': r.INR,
        'USD/SGD': r.SGD,
        'USD/HKD': r.HKD,
        'EUR/GBP': r.GBP / r.EUR,
    };

    if (typeof FX_PAIRS !== 'undefined') {
        FX_PAIRS.forEach(fx => {
            if (currencyMap[fx.pair] !== undefined) {
                const newRate = currencyMap[fx.pair];
                fx.base = fx.rate || newRate; // lock baseline to first real value
                fx.rate = newRate;
            }
        });
    }

    // Also update USD/INR index card
    if (r.INR) {
        const card = document.getElementById('idx-usdinr');
        if (card) {
            const rate = r.INR;
            card.querySelector('.idx-price').textContent = rate.toFixed(2);
            const chgEl = card.querySelector('.idx-change');
            chgEl.textContent = '—';
            chgEl.className = 'idx-change';
        }
    }

    // Re-render FX if on that view
    if (typeof currentView !== 'undefined' && currentView === 'fx') {
        updateFX();
    }

    console.info('[RT] FX refreshed from Frankfurter');
}

// ─────────────────────────────────────────────────────────────────
// COINGECKO — GOLD & CRUDE OIL (via commodity proxies)
// ─────────────────────────────────────────────────────────────────
async function refreshCommodities() {
    // Gold via CoinGecko (XAU/USD isn't there, but we can use Finnhub)
    const goldUrl = `${FINNHUB_BASE}/quote?symbol=OANDA:XAU_USD&token=${FINNHUB_KEY}`;
    const oilUrl = `${FINNHUB_BASE}/quote?symbol=OANDA:USOIL_USD&token=${FINNHUB_KEY}`;

    const [goldData, oilData] = await Promise.all([
        cachedFetch(goldUrl, 60000),
        cachedFetch(oilUrl, 60000),
    ]);

    if (goldData && goldData.c && goldData.c > 0) {
        const card = document.getElementById('idx-gold');
        if (card) {
            const pct = ((goldData.c - goldData.pc) / goldData.pc) * 100;
            const up = pct >= 0;
            card.querySelector('.idx-price').textContent =
                goldData.c.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            const chgEl = card.querySelector('.idx-change');
            chgEl.textContent = pctStr(pct);
            chgEl.className = 'idx-change ' + (up ? 'positive' : 'negative');
        }
    }

    if (oilData && oilData.c && oilData.c > 0) {
        const card = document.getElementById('idx-oil');
        if (card) {
            const pct = ((oilData.c - oilData.pc) / oilData.pc) * 100;
            const up = pct >= 0;
            card.querySelector('.idx-price').textContent = fmtPrice(oilData.c);
            const chgEl = card.querySelector('.idx-change');
            chgEl.textContent = pctStr(pct);
            chgEl.className = 'idx-change ' + (up ? 'positive' : 'negative');
        }
    }

    console.info('[RT] Commodities refreshed');
}

// ─────────────────────────────────────────────────────────────────
// FINNHUB — REAL NEWS
// ─────────────────────────────────────────────────────────────────
async function refreshNews() {
    const today = new Date().toISOString().slice(0, 10);
    const url = `${FINNHUB_BASE}/news?category=general&token=${FINNHUB_KEY}`;
    const data = await cachedFetch(url, 600000); // cache 10 min
    if (!data || !Array.isArray(data) || data.length === 0) return;

    const feed = document.getElementById('newsFeed');
    if (!feed) return;
    feed.innerHTML = '';

    const items = data.slice(0, 12);
    items.forEach(n => {
        const div = document.createElement('div');
        div.className = 'news-item';
        const ts = new Date(n.datetime * 1000);
        const hm = `${String(ts.getHours()).padStart(2, '0')}:${String(ts.getMinutes()).padStart(2, '0')}`;
        const src = n.source || 'News';
        const headline = n.headline || n.summary || '';
        const newsSummary = n.summary || n.headline || '';
        const origUrl = n.url || '';
        const readerUrl = `/news/reader.html?title=${encodeURIComponent(headline)}&source=${encodeURIComponent(src)}&category=${encodeURIComponent(n.category || 'MARKETS')}&time=${encodeURIComponent(hm + ' UTC')}&summary=${encodeURIComponent(newsSummary)}&url=${encodeURIComponent(origUrl)}`;

        div.innerHTML = `
      <div style="display:flex;justify-content:space-between">
        <span class="news-time">TODAY ${hm}</span>
        <span class="news-source">${src}</span>
      </div>
      <div class="news-title">${headline.length > 120 ? headline.slice(0, 120) + '...' : headline}</div>
      <span class="news-tag">${(n.category || 'general').toUpperCase()}</span>
    `;
        div.style.cursor = 'pointer';
        div.onclick = () => window.location.href = readerUrl;
        feed.appendChild(div);
    });

    console.info('[RT] News refreshed');
}

// ─────────────────────────────────────────────────────────────────
// LIVE TICKER — Update with real prices
// ─────────────────────────────────────────────────────────────────
function updateLiveTicker() {
    if (typeof STOCKS === 'undefined') return;
    const parts = [];
    const syms = ['AAPL', 'NVDA', 'MSFT', 'TSLA', 'GOOGL'];
    syms.forEach(sym => {
        const s = STOCKS[sym];
        if (!s) return;
        const pct = ((s.price - s.prev) / s.prev * 100);
        const up = pct >= 0;
        parts.push(`${sym} $${fmtPrice(s.price)} ${up ? '▲' : '▼'} ${pct >= 0 ? '+' : ''}${pct.toFixed(2)}%  |  `);
    });

    // BTC from CRYPTOS
    if (typeof CRYPTOS !== 'undefined' && CRYPTOS[0]) {
        const btc = CRYPTOS[0];
        const pct = btc.change || 0;
        parts.push(`BTC/USD $${btc.price.toLocaleString('en-US', { maximumFractionDigits: 0 })} ${pct >= 0 ? '▲' : '▼'} ${pct >= 0 ? '+' : ''}${pct.toFixed(2)}%  |  `);
    }

    // Gold
    const goldCard = document.getElementById('idx-gold');
    if (goldCard) {
        const price = goldCard.querySelector('.idx-price')?.textContent;
        if (price) parts.push(`GOLD $${price}/oz  |  `);
    }

    const el = document.getElementById('tickerContent');
    if (el && parts.length > 0) el.textContent = parts.join('  ');
}

// ─────────────────────────────────────────────────────────────────
// UTILITY
// ─────────────────────────────────────────────────────────────────
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ─────────────────────────────────────────────────────────────────
// MASTER REFRESH SCHEDULER
// ─────────────────────────────────────────────────────────────────
async function rtRefreshAll() {
    console.info('[RT] Starting full data refresh...');
    await refreshUSStocks();
    await sleep(500);
    await refreshUSIndices();
    await sleep(500);
    await refreshCrypto();
    await sleep(300);
    await refreshFX();
    await sleep(300);
    await refreshCommodities();
    updateLiveTicker();

    // Override crypto renderer with real version
    window.renderCryptoTable = renderCryptoTableReal;
}

// ─────────────────────────────────────────────────────────────────
// BOOT
// ─────────────────────────────────────────────────────────────────
// Wait for app.js to fully init, then start fetching real data
window.addEventListener('load', () => {
    // First refresh after 1.5s (let app.js render first so UI exists)
    setTimeout(async () => {
        await refreshNews();  // news first (fast, cached)
        await rtRefreshAll(); // then prices
    }, 1500);

    // Refresh stocks every 30 seconds
    setInterval(refreshUSStocks, 30000);

    // Refresh indices every 45 seconds
    setInterval(refreshUSIndices, 45000);

    // Refresh crypto every 60 seconds (CoinGecko rate limit)
    setInterval(refreshCrypto, 60000);

    // Refresh FX every 5 minutes (FX doesn't change fast)
    setInterval(refreshFX, 5 * 60 * 1000);

    // Refresh commodities every 60 seconds
    setInterval(refreshCommodities, 60000);

    // Refresh news every 10 minutes
    setInterval(refreshNews, 10 * 60 * 1000);

    // Update ticker every 15 seconds
    setInterval(updateLiveTicker, 15000);

    console.info('[RT] BloomFree real-time engine started ✔');
});
