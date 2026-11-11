/* ═══════════════════════════════════════════════════════════════════
   BLOOMFREE TERMINAL — app.js
   Full data simulation, charts, live updates, portfolio & all panels
═══════════════════════════════════════════════════════════════════ */

'use strict';

// ─────────────────────────────────────────────────────────────────
// MASTER DATA STORE
// ─────────────────────────────────────────────────────────────────
const STOCKS = {
    AAPL: { name: 'Apple Inc.', price: 175.40, prev: 172.80, pe: 29.1, mcap: '2.71T', sector: 'Tech' },
    MSFT: { name: 'Microsoft Corp.', price: 415.60, prev: 412.10, pe: 36.4, mcap: '3.09T', sector: 'Tech' },
    NVDA: { name: 'NVIDIA Corp.', price: 875.30, prev: 858.50, pe: 65.2, mcap: '2.16T', sector: 'Tech' },
    GOOGL: { name: 'Alphabet Inc.', price: 165.80, prev: 163.20, pe: 24.8, mcap: '2.04T', sector: 'Tech' },
    AMZN: { name: 'Amazon.com Inc.', price: 185.30, prev: 182.70, pe: 58.3, mcap: '1.94T', sector: 'Retail' },
    META: { name: 'Meta Platforms', price: 540.70, prev: 533.90, pe: 25.6, mcap: '1.36T', sector: 'Tech' },
    TSLA: { name: 'Tesla Inc.', price: 172.40, prev: 168.60, pe: 45.1, mcap: '0.55T', sector: 'Auto' },
    JPM: { name: 'JPMorgan Chase', price: 198.50, prev: 195.80, pe: 11.4, mcap: '0.57T', sector: 'Finance' },
    V: { name: 'Visa Inc.', price: 282.30, prev: 280.10, pe: 30.2, mcap: '0.58T', sector: 'Finance' },
    JNJ: { name: 'Johnson & Johnson', price: 152.70, prev: 151.20, pe: 22.8, mcap: '0.37T', sector: 'Health' },
    WMT: { name: 'Walmart Inc.', price: 62.40, prev: 61.80, pe: 27.3, mcap: '0.50T', sector: 'Retail' },
    BAC: { name: 'Bank of America', price: 37.60, prev: 36.90, pe: 12.1, mcap: '0.29T', sector: 'Finance' },
};

const INDICES = {
    'idx-spx': { name: 'S&P 500', base: 5248.49, vol: 0.0008 },
    'idx-ndx': { name: 'NASDAQ', base: 18386.22, vol: 0.001 },
    'idx-dow': { name: 'DOW JONES', base: 39127.80, vol: 0.0007 },
    'idx-nifty': { name: 'NIFTY 50', base: 22643.40, vol: 0.0009 },
    'idx-sensex': { name: 'SENSEX', base: 74820.30, vol: 0.0009 },
    'idx-vix': { name: 'VIX', base: 13.86, vol: 0.015 },
    'idx-btc': { name: 'BTC/USD', base: 67840.5, vol: 0.002 },
    'idx-gold': { name: 'GOLD', base: 2318.70, vol: 0.0006 },
    'idx-oil': { name: 'CRUDE OIL', base: 81.42, vol: 0.001 },
    'idx-usdinr': { name: 'USD/INR', base: 83.42, vol: 0.0004 },
};

// ── INDIA INDICES (F6 strip) ──
const INDIA_INDICES = {
    'iidx-nifty50': { name: 'NIFTY 50', base: 22643.40, vol: 0.001 },
    'iidx-sensex': { name: 'SENSEX', base: 74820.30, vol: 0.001 },
    'iidx-banknifty': { name: 'NIFTY BANK', base: 47840.20, vol: 0.0012 },
    'iidx-niftyit': { name: 'NIFTY IT', base: 38640.80, vol: 0.0014 },
    'iidx-niftymid': { name: 'NIFTY MIDCAP', base: 50210.60, vol: 0.0011 },
    'iidx-niftyauto': { name: 'NIFTY AUTO', base: 22180.40, vol: 0.0013 },
    'iidx-niftypharma': { name: 'NIFTY PHARMA', base: 19842.70, vol: 0.001 },
    'iidx-india-vix': { name: 'INDIA VIX', base: 14.28, vol: 0.018 },
};
let indiaIdxPrices = {};

// ── INDIA STOCKS ──
const INDIA_STOCKS = {
    RELIANCE: { name: 'Reliance Industries', price: 2943.50, prev: 2910.20, mcap: '19.9L Cr', sector: 'Energy' },
    TCS: { name: 'Tata Consultancy Svc', price: 3842.10, prev: 3798.60, mcap: '13.9L Cr', sector: 'IT' },
    INFY: { name: 'Infosys Ltd.', price: 1628.40, prev: 1612.80, mcap: '6.8L Cr', sector: 'IT' },
    HDFCBANK: { name: 'HDFC Bank Ltd.', price: 1542.30, prev: 1528.70, mcap: '11.7L Cr', sector: 'Finance' },
    ICICIBANK: { name: 'ICICI Bank Ltd.', price: 1248.60, prev: 1236.40, mcap: '8.8L Cr', sector: 'Finance' },
    WIPRO: { name: 'Wipro Ltd.', price: 468.20, prev: 462.80, mcap: '2.4L Cr', sector: 'IT' },
    HINDUNILVR: { name: 'HUL', price: 2386.40, prev: 2372.10, mcap: '5.6L Cr', sector: 'FMCG' },
    BAJFINANCE: { name: 'Bajaj Finance', price: 6842.30, prev: 6780.50, mcap: '4.1L Cr', sector: 'Finance' },
    TATAMOTORS: { name: 'Tata Motors Ltd.', price: 842.60, prev: 834.20, mcap: '3.1L Cr', sector: 'Auto' },
    MARUTI: { name: 'Maruti Suzuki', price: 12480.30, prev: 12340.60, mcap: '3.8L Cr', sector: 'Auto' },
    SUNPHARMA: { name: 'Sun Pharmaceutical', price: 1628.40, prev: 1610.20, mcap: '3.9L Cr', sector: 'Pharma' },
    DRREDDY: { name: 'Dr. Reddy\'s Labs', price: 6248.30, prev: 6180.40, mcap: '1.0L Cr', sector: 'Pharma' },
    ONGC: { name: 'Oil & Natural Gas', price: 248.60, prev: 246.20, mcap: '3.1L Cr', sector: 'Energy' },
    SBIN: { name: 'State Bank of India', price: 748.40, prev: 742.60, mcap: '6.7L Cr', sector: 'Finance' },
    LT: { name: 'Larsen & Toubro', price: 3648.20, prev: 3612.80, mcap: '5.0L Cr', sector: 'Infra' },
    ADANIPORTS: { name: 'Adani Ports & SEZ', price: 1248.30, prev: 1236.80, mcap: '2.6L Cr', sector: 'Infra' },
};
let indiaCurrentSymbol = 'RELIANCE';
let indiaTimeframe = '1D';
let indiaChart_ = null;
let currentIndiaMoverTab = 'gainers';

const INDIA_MOVERS = {
    gainers: [
        { sym: 'TATAMOTORS', price: 842.60, pct: +3.82 },
        { sym: 'SUNPHARMA', price: 1628.40, pct: +4.21 },
        { sym: 'BAJFINANCE', price: 6842.30, pct: +2.94 },
        { sym: 'MARUTI', price: 12480.30, pct: +1.85 },
        { sym: 'SBIN', price: 748.40, pct: +3.47 },
        { sym: 'LT', price: 3648.20, pct: +2.12 },
        { sym: 'ADANIPORTS', price: 1248.30, pct: +5.10 },
    ],
    losers: [
        { sym: 'INFY', price: 1628.40, pct: -2.34 },
        { sym: 'WIPRO', price: 468.20, pct: -1.88 },
        { sym: 'TCS', price: 3842.10, pct: -0.92 },
        { sym: 'DRREDDY', price: 6248.30, pct: -1.42 },
        { sym: 'ONGC', price: 248.60, pct: -0.88 },
        { sym: 'HINDUNILVR', price: 2386.40, pct: -0.72 },
        { sym: 'HDFCBANK', price: 1542.30, pct: -0.64 },
    ],
};

const INDIA_NEWS = [
    { time: '10:45', source: 'ET Markets', title: 'Nifty 50 hits fresh 52-week high; Sensex surges 800 points on FII buying', tag: 'bullish' },
    { time: '10:22', source: 'Moneycontrol', title: 'RBI holds repo rate at 6.5%; Governor signals accommodative stance ahead', tag: 'bullish' },
    { time: '09:58', source: 'Mint', title: 'Tata Motors Q3 profit surges 138% YoY on strong JLR and domestic EV demand', tag: 'bullish' },
    { time: '09:40', source: 'ET Markets', title: 'Adani Ports wins ₹8,400 Cr port contract; stock jumps 5% at open', tag: 'bullish' },
    { time: '09:18', source: 'BSE India', title: 'FIIs buy ₹4,200 Cr in Indian equities; DIIs also remain net buyers for 5th session', tag: 'bullish' },
    { time: '08:55', source: 'Moneycontrol', title: 'IT sector under pressure: Infosys, Wipro fall on weak US demand outlook warning', tag: 'bearish' },
    { time: '08:32', source: 'Mint', title: 'India GDP growth projected at 7.2% for FY25: World Bank raises forecast', tag: 'bullish' },
    { time: '08:10', source: 'ET Markets', title: 'SEBI tightens F&O rules; new margin norms for index options from April', tag: 'neutral' },
];

const SECTOR_DATA = {
    us: [
        { name: 'TECH', pct: +2.34, chg: '+$142B' },
        { name: 'FINANCIALS', pct: +0.82, chg: '+$38B' },
        { name: 'HEALTHCARE', pct: -0.44, chg: '-$18B' },
        { name: 'ENERGY', pct: -1.12, chg: '-$24B' },
        { name: 'CONSUMER', pct: +1.08, chg: '+$52B' },
        { name: 'REAL ESTATE', pct: -0.68, chg: '-$12B' },
        { name: 'UTILITIES', pct: +0.22, chg: '+$4B' },
        { name: 'MATERIALS', pct: +0.56, chg: '+$9B' },
        { name: 'INDUSTRIAL', pct: +0.34, chg: '+$14B' },
        { name: 'COMM SVC', pct: +1.62, chg: '+$76B' },
    ],
    india: [
        { name: 'IT', pct: -1.34, chg: '-₹8,400 Cr' },
        { name: 'BANKING', pct: +1.82, chg: '+₹12,600 Cr' },
        { name: 'AUTO', pct: +3.12, chg: '+₹9,800 Cr' },
        { name: 'PHARMA', pct: +1.48, chg: '+₹4,200 Cr' },
        { name: 'ENERGY', pct: -0.62, chg: '-₹3,100 Cr' },
        { name: 'FMCG', pct: -0.28, chg: '-₹1,200 Cr' },
        { name: 'INFRA', pct: +2.44, chg: '+₹7,600 Cr' },
        { name: 'METALS', pct: +0.88, chg: '+₹2,400 Cr' },
        { name: 'REALTY', pct: +1.22, chg: '+₹1,800 Cr' },
        { name: 'MEDIA', pct: -1.06, chg: '-₹480 Cr' },
    ],
};

const CRYPTOS = [
    { sym: 'BTC', name: 'Bitcoin', price: 67840, mcap: '1.33T', vol24: '48.2B', dom: 52.4 },
    { sym: 'ETH', name: 'Ethereum', price: 3542, mcap: '424.8B', vol24: '22.1B', dom: 16.8 },
    { sym: 'SOL', name: 'Solana', price: 172.3, mcap: '80.2B', vol24: '6.4B', dom: 3.1 },
    { sym: 'BNB', name: 'BNB', price: 578.4, mcap: '86.1B', vol24: '2.8B', dom: 3.4 },
    { sym: 'XRP', name: 'Ripple', price: 0.612, mcap: '34.8B', vol24: '1.6B', dom: 1.4 },
    { sym: 'DOGE', name: 'Dogecoin', price: 0.162, mcap: '23.3B', vol24: '1.2B', dom: 0.9 },
    { sym: 'ADA', name: 'Cardano', price: 0.454, mcap: '16.1B', vol24: '0.8B', dom: 0.6 },
    { sym: 'AVAX', name: 'Avalanche', price: 36.8, mcap: '15.2B', vol24: '0.7B', dom: 0.6 },
];

const FX_PAIRS = [
    { pair: 'EUR/USD', rate: 1.0842, base: 1.0842 },
    { pair: 'GBP/USD', rate: 1.2644, base: 1.2644 },
    { pair: 'USD/JPY', rate: 149.82, base: 149.82 },
    { pair: 'USD/CHF', rate: 0.8834, base: 0.8834 },
    { pair: 'AUD/USD', rate: 0.6514, base: 0.6514 },
    { pair: 'NZD/USD', rate: 0.5982, base: 0.5982 },
    { pair: 'USD/CAD', rate: 1.3568, base: 1.3568 },
    { pair: 'USD/CNY', rate: 7.2340, base: 7.2340 },
    { pair: 'USD/INR', rate: 83.42, base: 83.42 },
    { pair: 'USD/SGD', rate: 1.3452, base: 1.3452 },
    { pair: 'USD/HKD', rate: 7.8240, base: 7.8240 },
    { pair: 'EUR/GBP', rate: 0.8574, base: 0.8574 },
];

const PORTFOLIO = [
    { sym: 'AAPL', shares: 50, avgCost: 145.20 },
    { sym: 'MSFT', shares: 20, avgCost: 380.50 },
    { sym: 'NVDA', shares: 10, avgCost: 620.00 },
    { sym: 'GOOGL', shares: 30, avgCost: 140.80 },
    { sym: 'TSLA', shares: 40, avgCost: 195.00 },
    { sym: 'JPM', shares: 25, avgCost: 185.30 },
    { sym: 'V', shares: 35, avgCost: 255.60 },
];

const MOVERS = {
    gainers: [
        { sym: 'SMCI', price: 928.4, pct: +14.82 },
        { sym: 'NVDA', price: 875.3, pct: +3.47 },
        { sym: 'MSTR', price: 1642.0, pct: +8.21 },
        { sym: 'ARM', price: 128.6, pct: +5.93 },
        { sym: 'PLTR', price: 28.4, pct: +4.12 },
        { sym: 'COIN', price: 236.8, pct: +6.74 },
        { sym: 'RIVN', price: 11.2, pct: +3.88 },
    ],
    losers: [
        { sym: 'INTC', price: 31.20, pct: -5.42 },
        { sym: 'BA', price: 178.60, pct: -3.87 },
        { sym: 'PFE', price: 26.80, pct: -2.91 },
        { sym: 'CVS', price: 54.30, pct: -4.23 },
        { sym: 'WBA', price: 14.60, pct: -6.81 },
        { sym: 'VFC', price: 13.20, pct: -3.44 },
        { sym: 'MU', price: 117.40, pct: -2.18 },
    ],
};

const NEWS_ITEMS = [
    { time: '09:32', source: 'Reuters', title: 'Fed signals potential rate cuts as inflation eases toward 2% target', tag: 'bullish', sym: 'SPX' },
    { time: '09:18', source: 'Bloomberg', title: 'NVIDIA surpasses $2 trillion market cap as AI demand drives record revenue', tag: 'bullish', sym: 'NVDA' },
    { time: '08:55', source: 'FT', title: 'Apple Vision Pro secures new enterprise deals with Fortune 500 companies', tag: 'bullish', sym: 'AAPL' },
    { time: '08:44', source: 'CNBC', title: 'Oil rises on Middle East supply concerns and lower US crude inventories', tag: 'bearish', sym: 'OIL' },
    { time: '08:30', source: 'Barrons', title: 'Tesla recalls 125,000 vehicles over software issue in autopilot system', tag: 'bearish', sym: 'TSLA' },
    { time: '08:15', source: 'WSJ', title: 'Bitcoin ETF inflows hit record $1.2B in a single day, crypto market rallies', tag: 'bullish', sym: 'BTC' },
    { time: '07:58', source: 'FT', title: 'JPMorgan raises S&P 500 year-end target to 5,800 on strong earnings outlook', tag: 'bullish', sym: 'SPX' },
    { time: '07:40', source: 'Reuters', title: 'China economic data disappoints, exports fall for third consecutive month', tag: 'bearish', sym: 'DXY' },
    { time: '07:22', source: 'CNBC', title: 'Microsoft Azure cloud revenue surges 31%, beats analyst estimates', tag: 'bullish', sym: 'MSFT' },
    { time: '07:05', source: 'Bloomberg', title: 'European Central Bank holds rates, hints at summer cut amid cooling CPI', tag: 'neutral', sym: 'EUR' },
    { time: '06:48', source: 'Barrons', title: 'Amazon Web Services secures $10B government cloud infrastructure deal', tag: 'bullish', sym: 'AMZN' },
    { time: '06:30', source: 'Reuters', title: 'Gold hits record high amid dollar weakness and central bank buying', tag: 'bullish', sym: 'GOLD' },
];

const ECON_CALENDAR = [
    { time: '08:30', event: 'Non-Farm Payrolls (Mar)', impact: 'high', prev: '275K', est: '230K' },
    { time: '08:30', event: 'Unemployment Rate', impact: 'high', prev: '3.7%', est: '3.7%' },
    { time: '10:00', event: 'ISM Manufacturing PMI', impact: 'medium', prev: '47.8', est: '48.4' },
    { time: '10:00', event: 'Consumer Confidence', impact: 'medium', prev: '106.7', est: '107.2' },
    { time: '14:00', event: 'FOMC Meeting Minutes', impact: 'high', prev: '—', est: '—' },
    { time: '14:30', event: 'Crude Oil Inventories', impact: 'medium', prev: '-2.1M', est: '-1.8M' },
    { time: '15:00', event: 'Fed Chair Speech (Powell)', impact: 'high', prev: '—', est: '—' },
];

const TICKER_ITEMS = [
    'S&P 500 +0.42% ▲ 5,248  |  ',
    'NASDAQ +0.61% ▲ 18,386  |  ',
    'AAPL $175.40 +1.53% ▲  |  ',
    'NVDA $875.30 +3.47% ▲  |  ',
    'BTC/USD $67,840 +2.12% ▲  |  ',
    'ETH/USD $3,542 +1.84% ▲  |  ',
    'GOLD $2,318/oz +0.31% ▲  |  ',
    'EUR/USD 1.0842 -0.12% ▼  |  ',
    'TSLA $172.40 +2.26% ▲  |  ',
    'DOW +0.28% ▲ 39,127  |  ',
    '10Y YIELD 4.312% ▲  |  ',
    'VIX 13.86 -1.42% ▼  |  ',
    'CRUDE OIL $81.42 -0.68% ▼  |  ',
    '⚡ FED RATE HOLD: 5.25-5.50% | NEXT MEETING: MAY 1 | ',
];

// ─────────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────────
let currentSymbol = 'AAPL';
let currentTimeframe = '1D';
let currentChartType = 'line';
let currentView = 'dashboard';
let mainChart = null;
let fullChart_ = null;
let allocationChart_ = null;
let fearGreedChart_ = null;
let dominanceChart_ = null;
let updateCount = 0;
let indexCurrentPrices = {};

// ─────────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────────
function rand(min, max) { return Math.random() * (max - min) + min; }
function fmtNum(n, decimals = 2) {
    if (n >= 1e12) return (n / 1e12).toFixed(2) + 'T';
    if (n >= 1e9) return (n / 1e9).toFixed(1) + 'B';
    if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
    return n.toFixed(decimals);
}
function fmtPrice(p) {
    if (p >= 1000) return p.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (p >= 10) return p.toFixed(2);
    if (p >= 1) return p.toFixed(4);
    return p.toFixed(5);
}
function pctStr(pct) {
    return (pct >= 0 ? '▲ +' : '▼ ') + Math.abs(pct).toFixed(2) + '%';
}
function flashRow(el, up) {
    el.classList.remove('flash-up', 'flash-down');
    void el.offsetWidth;
    el.classList.add(up ? 'flash-up' : 'flash-down');
}

// ─────────────────────────────────────────────────────────────────
// CLOCK
// ─────────────────────────────────────────────────────────────────
function updateClock() {
    const now = new Date();
    const hm = (h, m) => `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
    // Local
    document.getElementById('clockTime').textContent =
        String(now.getHours()).padStart(2, '0') + ':' +
        String(now.getMinutes()).padStart(2, '0') + ':' +
        String(now.getSeconds()).padStart(2, '0');
    document.getElementById('clockDate').textContent =
        now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: '2-digit', year: 'numeric' });
    // NY = UTC-5 (EST) or UTC-4 (EDT)
    const nyOff = -5;
    const nyH = (now.getUTCHours() + nyOff + 24) % 24;
    const lonH = (now.getUTCHours() + 0 + 24) % 24;
    const tkyH = (now.getUTCHours() + 9) % 24;
    const istH = (now.getUTCHours() + 5) % 24;
    const istM = now.getUTCMinutes() + 30;
    const istHfin = istM >= 60 ? (istH + 1) % 24 : istH;
    const istMfin = istM % 60;
    document.getElementById('clockNY').textContent = hm(nyH, now.getUTCMinutes());
    document.getElementById('clockLON').textContent = hm(lonH, now.getUTCMinutes());
    document.getElementById('clockTKY').textContent = hm(tkyH, now.getUTCMinutes());
    document.getElementById('clockIST').textContent = hm(istHfin, istMfin);
    // NSE market hours: 9:15–15:30 IST
    const nseMin = istHfin * 60 + istMfin;
    const nseOpen = nseMin >= 555 && nseMin < 930;
    // Market status (NYSE)
    const nyMin = nyH * 60 + now.getUTCMinutes();
    const open = nyMin >= 570 && nyMin < 960; // 9:30–16:00
    document.getElementById('marketStatusDot').className = 'status-dot' + (open ? '' : ' closed');
    document.getElementById('marketStatusText').textContent = open ? 'MARKET OPEN' : 'MARKET CLOSED';
}

// ─────────────────────────────────────────────────────────────────
// NEWS TICKER
// ─────────────────────────────────────────────────────────────────
function initTicker() {
    const el = document.getElementById('tickerContent');
    el.textContent = TICKER_ITEMS.join('  ');
}

// ─────────────────────────────────────────────────────────────────
// GENERATE CHART DATA
// ─────────────────────────────────────────────────────────────────
function generatePriceData(symbol, timeframe) {
    const stock = STOCKS[symbol] || STOCKS['AAPL'];
    const base = stock.price;
    const configs = {
        '1D': { points: 78, vol: 0.002, fmt: i => { const h = Math.floor((9.5 + i * 6.5 / 78)); const m = Math.floor((i * 6.5 * 60 / 78) % 60); return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`; } },
        '1W': { points: 35, vol: 0.008, fmt: i => { const d = new Date(Date.now() - (34 - i) * 86400000); return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit' }); } },
        '1M': { points: 30, vol: 0.015, fmt: i => { const d = new Date(Date.now() - (29 - i) * 86400000); return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit' }); } },
        '3M': { points: 90, vol: 0.012, fmt: i => { const d = new Date(Date.now() - (89 - i) * 86400000); return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit' }); } },
    };
    const cfg = configs[timeframe] || configs['1D'];
    let price = base * rand(0.92, 0.97);
    const labels = [], prices = [], opens = [], highs = [], lows = [], closes = [];

    for (let i = 0; i <= cfg.points; i++) {
        labels.push(cfg.fmt(i));
        const change = price * rand(-cfg.vol, cfg.vol) * (Math.random() > 0.52 ? 1.1 : 0.9);
        const o = price;
        price += change;
        price = Math.max(price, base * 0.7);
        const h = Math.max(o, price) * rand(1.0001, 1.003);
        const l = Math.min(o, price) * rand(0.997, 0.9999);
        opens.push(o); highs.push(h); lows.push(l); closes.push(price);
        prices.push(price);
    }
    return { labels, prices, opens, highs, lows, closes, base };
}

function generateSparkData(stock) {
    let p = stock.prev;
    const pts = [];
    for (let i = 0; i < 20; i++) {
        p += p * rand(-0.003, 0.003);
        pts.push(p);
    }
    return pts;
}

// ─────────────────────────────────────────────────────────────────
// INIT CHART
// ─────────────────────────────────────────────────────────────────
function buildChart(canvasId, symbol, timeframe, type = 'line') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    const data = generatePriceData(symbol, timeframe);

    const isUp = data.closes[data.closes.length - 1] >= data.closes[0];
    const lineColor = isUp ? '#00e676' : '#ff3d3d';
    const fillColor = isUp ? 'rgba(0,230,118,0.07)' : 'rgba(255,61,61,0.07)';
    const borderColor = isUp ? 'rgba(0,230,118,0.4)' : 'rgba(255,61,61,0.4)';

    const chartData = {
        labels: data.labels,
        datasets: [{
            label: symbol,
            data: type === 'bar'
                ? data.closes.map((c, i) => ({ x: data.labels[i], o: data.opens[i], h: data.highs[i], l: data.lows[i], c }))
                : data.closes,
            borderColor: lineColor,
            backgroundColor: type === 'bar'
                ? function (ctx) { const v = ctx.raw; return v && v.o > v.c ? 'rgba(255,61,61,0.8)' : 'rgba(0,230,118,0.8)'; }
                : fillColor,
            borderWidth: 1.5,
            fill: type === 'line',
            tension: 0.3,
            pointRadius: 0,
            pointHoverRadius: 4,
            pointHoverBackgroundColor: lineColor,
        }],
    };

    const chartType = type === 'bar' ? 'bar' : 'line';

    const chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            animation: { duration: 400, easing: 'easeInOutQuart' },
            scales: {
                x: {
                    ticks: { color: '#555', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8, maxRotation: 0 },
                    grid: { color: '#111', drawTicks: false },
                    border: { color: '#222' },
                },
                y: {
                    position: 'right',
                    ticks: {
                        color: '#888', font: { family: 'JetBrains Mono', size: 9 },
                        callback: v => '$' + fmtPrice(v),
                    },
                    grid: { color: '#111' },
                    border: { color: '#222' },
                },
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0d0d0d',
                    borderColor: '#f5a623',
                    borderWidth: 1,
                    titleColor: '#f5a623',
                    bodyColor: '#e8e8e8',
                    titleFont: { family: 'JetBrains Mono', size: 10 },
                    bodyFont: { family: 'JetBrains Mono', size: 10 },
                    callbacks: {
                        label: ctx => ` $${fmtPrice(typeof ctx.raw === 'object' ? ctx.raw.c : ctx.raw)}`
                    },
                },
            },
        },
    });

    // Update stats bar
    const prices = data.closes;
    const last = prices[prices.length - 1];
    const high = Math.max(...data.highs);
    const low = Math.min(...data.lows);
    const open = data.opens[0];
    const stock = STOCKS[symbol] || STOCKS['AAPL'];
    document.getElementById('cs-open') && (document.getElementById('cs-open').textContent = '$' + fmtPrice(open));
    document.getElementById('cs-high') && (document.getElementById('cs-high').textContent = '$' + fmtPrice(high));
    document.getElementById('cs-low') && (document.getElementById('cs-low').textContent = '$' + fmtPrice(low));
    document.getElementById('cs-prev') && (document.getElementById('cs-prev').textContent = '$' + fmtPrice(stock.prev));
    document.getElementById('cs-mcap') && (document.getElementById('cs-mcap').textContent = stock.mcap);
    document.getElementById('cs-pe') && (document.getElementById('cs-pe').textContent = stock.pe);

    return chart;
}

// ─────────────────────────────────────────────────────────────────
// LIVE CHART AUTO-UPDATE (replace last point for 1D)
// ─────────────────────────────────────────────────────────────────
function liveUpdateChart() {
    if (!mainChart || currentTimeframe !== '1D') return;
    const ds = mainChart.data.datasets[0];
    const labels = mainChart.data.labels;
    const last = ds.data[ds.data.length - 1];
    const lastVal = typeof last === 'object' ? last.c : last;
    const newPrice = lastVal * (1 + rand(-0.001, 0.001));
    const now = new Date();
    const label = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    labels.push(label);
    ds.data.push(newPrice);
    if (labels.length > 100) { labels.shift(); ds.data.shift(); }
    mainChart.update('none');
}

// ─────────────────────────────────────────────────────────────────
// WATCHLIST
// ─────────────────────────────────────────────────────────────────
function initWatchlist() {
    const tbody = document.getElementById('watchlistBody');
    tbody.innerHTML = '';
    Object.entries(STOCKS).forEach(([sym, s]) => {
        const pct = ((s.price - s.prev) / s.prev * 100);
        const up = pct >= 0;
        const row = document.createElement('tr');
        row.id = `wl-${sym}`;
        row.onclick = () => { currentSymbol = sym; updateChartSymbol(sym); };
        row.innerHTML = `
      <td>${sym}</td>
      <td id="wl-${sym}-price">$${fmtPrice(s.price)}</td>
      <td class="${up ? 'positive' : 'negative'}" id="wl-${sym}-chg">${up ? '+' : '-'}$${Math.abs(s.price - s.prev).toFixed(2)}</td>
      <td class="${up ? 'positive' : 'negative'}" id="wl-${sym}-pct">${pctStr(pct)}</td>
      <td id="wl-${sym}-vol">${fmtNum(Math.round(rand(1e6, 80e6)))}M</td>
      <td><canvas class="spark" id="spark-${sym}"></canvas></td>
    `;
        tbody.appendChild(row);
    });
    // draw sparklines
    Object.entries(STOCKS).forEach(([sym, s]) => {
        drawSpark(`spark-${sym}`, generateSparkData(s));
    });
}

function drawSpark(canvasId, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width = 60;
    const H = canvas.height = 24;
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;
    const up = data[data.length - 1] >= data[0];
    const color = up ? '#00e676' : '#ff3d3d';
    ctx.clearRect(0, 0, W, H);
    ctx.beginPath();
    data.forEach((v, i) => {
        const x = (i / (data.length - 1)) * W;
        const y = H - ((v - min) / range) * (H - 2) - 1;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.stroke();
}

// ─────────────────────────────────────────────────────────────────
// INDICES
// ─────────────────────────────────────────────────────────────────
function initIndices() {
    Object.entries(INDICES).forEach(([id, idx]) => {
        indexCurrentPrices[id] = idx.base;
    });
    Object.entries(INDIA_INDICES).forEach(([id, idx]) => {
        indiaIdxPrices[id] = idx.base;
    });
}

function updateIndices() {
    Object.entries(INDICES).forEach(([id, idx]) => {
        const old = indexCurrentPrices[id];
        const change = old * rand(-idx.vol, idx.vol);
        const newPrice = old + change;
        indexCurrentPrices[id] = newPrice;
        const pct = (newPrice - idx.base) / idx.base * 100;
        const up = pct >= 0;
        const card = document.getElementById(id);
        if (!card) return;
        card.querySelector('.idx-price').textContent = newPrice >= 1000
            ? newPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
            : fmtPrice(newPrice);
        const chgEl = card.querySelector('.idx-change');
        chgEl.textContent = pctStr(pct);
        chgEl.className = 'idx-change ' + (up ? 'positive' : 'negative');
    });
}

// ─────────────────────────────────────────────────────────────────
// LIVE STOCK PRICES
// ─────────────────────────────────────────────────────────────────
function updateStockPrices() {
    Object.entries(STOCKS).forEach(([sym, s]) => {
        const old = s.price;
        const change = old * rand(-0.002, 0.002);
        s.price += change;
        s.price = Math.max(s.price, s.prev * 0.7);
        const pct = (s.price - s.prev) / s.prev * 100;
        const up = s.price >= old;

        const row = document.getElementById(`wl-${sym}`);
        if (row) { flashRow(row, up); }

        const priceEl = document.getElementById(`wl-${sym}-price`);
        const chgEl = document.getElementById(`wl-${sym}-chg`);
        const pctEl = document.getElementById(`wl-${sym}-pct`);

        if (priceEl) priceEl.textContent = '$' + fmtPrice(s.price);
        if (chgEl) {
            const diff = s.price - s.prev;
            chgEl.textContent = (diff >= 0 ? '+' : '-') + '$' + Math.abs(diff).toFixed(2);
            chgEl.className = up ? 'positive' : 'negative';
        }
        if (pctEl) {
            pctEl.textContent = pctStr(pct);
            pctEl.className = up ? 'positive' : 'negative';
        }
        // redraw spark
        drawSpark(`spark-${sym}`, generateSparkData(s));
    });
}

// ─────────────────────────────────────────────────────────────────
// MOVERS
// ─────────────────────────────────────────────────────────────────
let currentMoverTab = 'gainers';
function initMovers() { renderMovers('gainers'); }

function switchMovers(type, btn) {
    currentMoverTab = type;
    document.querySelectorAll('.mtab').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderMovers(type);
}

function renderMovers(type) {
    const container = document.getElementById('moversContainer');
    container.innerHTML = '';
    const items = MOVERS[type];
    items.forEach((m, i) => {
        const up = m.pct >= 0;
        const div = document.createElement('div');
        div.className = 'mover-row';
        div.onclick = () => { currentSymbol = m.sym; };
        div.innerHTML = `
      <div class="mover-rank">#${i + 1}</div>
      <div class="mover-sym">${m.sym}</div>
      <div class="mover-price">$${fmtPrice(m.price)}</div>
      <div class="mover-pct ${up ? 'positive' : 'negative'}">${pctStr(m.pct)}</div>
    `;
        container.appendChild(div);
    });
}

function updateMovers() {
    MOVERS.gainers.forEach(m => {
        m.price += m.price * rand(-0.001, 0.003);
        m.pct += rand(-0.05, 0.1);
    });
    MOVERS.losers.forEach(m => {
        m.price += m.price * rand(-0.003, 0.001);
        m.pct += rand(-0.1, 0.05);
    });
    renderMovers(currentMoverTab);
}

// ─────────────────────────────────────────────────────────────────
// OPTIONS CHAIN
// ─────────────────────────────────────────────────────────────────
function initOptions() {
    const stock = STOCKS['AAPL'];
    const price = stock.price;
    const strikes = [-15, -10, -5, 0, 5, 10, 15].map(d => Math.round((price + d) / 5) * 5);

    const callsBody = document.getElementById('callsBody');
    const putsBody = document.getElementById('putsBody');
    callsBody.innerHTML = ''; putsBody.innerHTML = '';

    strikes.forEach(k => {
        const intrinsic = Math.max(price - k, 0);
        const itm = price > k;
        const iv = rand(0.22, 0.45).toFixed(2);
        const bid = (intrinsic + rand(0.5, 3)).toFixed(2);
        const ask = (parseFloat(bid) + rand(0.05, 0.4)).toFixed(2);
        const oi = Math.round(rand(100, 5000));
        const tr = `<tr class="${itm ? 'positive' : ''}">
      <td>$${k}</td><td>$${bid}</td><td>$${ask}</td><td>${iv}</td><td>${fmtNum(oi, 0)}</td>
    </tr>`;
        callsBody.insertAdjacentHTML('beforeend', tr);

        const pIntrinsic = Math.max(k - price, 0);
        const pItm = price < k;
        const pBid = (pIntrinsic + rand(0.5, 3)).toFixed(2);
        const pAsk = (parseFloat(pBid) + rand(0.05, 0.4)).toFixed(2);
        const pOi = Math.round(rand(100, 5000));
        const ptr = `<tr class="${pItm ? 'negative' : ''}">
      <td>$${k}</td><td>$${pBid}</td><td>$${pAsk}</td><td>${iv}</td><td>${fmtNum(pOi, 0)}</td>
    </tr>`;
        putsBody.insertAdjacentHTML('beforeend', ptr);
    });

    document.getElementById('optCurrentPrice').textContent = `$${fmtPrice(price)}`;
}

// ─────────────────────────────────────────────────────────────────
// ECONOMIC CALENDAR
// ─────────────────────────────────────────────────────────────────
function initCalendar() {
    const list = document.getElementById('calendarList');
    list.innerHTML = '';
    ECON_CALENDAR.forEach(e => {
        const div = document.createElement('div');
        div.className = 'cal-row';
        div.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span class="cal-time">${e.time} ET</span>
        <span class="cal-impact ${e.impact}">${e.impact.toUpperCase()}</span>
      </div>
      <div class="cal-event">${e.event}</div>
      <div style="font-size:9px;color:#555;margin-top:2px">PREV: ${e.prev} &nbsp; EST: ${e.est}</div>
    `;
        list.appendChild(div);
    });
}

// ─────────────────────────────────────────────────────────────────
// NEWS FEED
// ─────────────────────────────────────────────────────────────────
function initNewsFeed() {
    const feed = document.getElementById('newsFeed');
    feed.innerHTML = '';
    NEWS_ITEMS.forEach(n => {
        const div = document.createElement('div');
        div.className = 'news-item';
        const tagClass = n.tag === 'bullish' ? 'bullish' : n.tag === 'bearish' ? 'bearish' : '';
        const readerUrl = `/news/reader.html?title=${encodeURIComponent(n.title)}&source=${encodeURIComponent(n.source)}&category=${encodeURIComponent(n.tag || 'MARKETS')}&time=${encodeURIComponent(n.time + ' UTC')}&summary=${encodeURIComponent(n.title)}&url=#`;
        div.innerHTML = `
      <div style="display:flex;justify-content:space-between">
        <span class="news-time">TODAY ${n.time}</span>
        <span class="news-source">${n.source}</span>
      </div>
      <div class="news-title">${n.title}</div>
      <span class="news-tag ${tagClass}">${(n.tag || 'neutral').toUpperCase()}</span>
      <span class="news-tag" style="margin-left:4px">${n.sym}</span>
    `;
        div.style.cursor = 'pointer';
        div.onclick = () => window.location.href = readerUrl;
        feed.appendChild(div);
    });
}

// ─────────────────────────────────────────────────────────────────
// PORTFOLIO
// ─────────────────────────────────────────────────────────────────
function initPortfolio() {
    renderHoldings();
    initAllocationChart();
}

function renderHoldings() {
    const tbody = document.getElementById('holdingsBody');
    tbody.innerHTML = '';
    let totalValue = 0, totalCost = 0;
    const values = [];

    PORTFOLIO.forEach(h => {
        const s = STOCKS[h.sym];
        const current = s ? s.price : h.avgCost;
        const mktVal = current * h.shares;
        const cost = h.avgCost * h.shares;
        const pl = mktVal - cost;
        const plPct = ((current - h.avgCost) / h.avgCost) * 100;
        totalValue += mktVal;
        totalCost += cost;
        values.push({ sym: h.sym, val: mktVal });
        const tr = document.createElement('tr');
        tr.innerHTML = `
      <td>${h.sym}</td>
      <td>${h.shares}</td>
      <td>$${fmtPrice(h.avgCost)}</td>
      <td>$${fmtPrice(current)}</td>
      <td>$${fmtNum(mktVal)}</td>
      <td class="${pl >= 0 ? 'positive' : 'negative'}">${pl >= 0 ? '+' : ''}}$${fmtNum(Math.abs(pl))}</td>
      <td class="${plPct >= 0 ? 'positive' : 'negative'}">${pctStr(plPct)}</td>
      <td>—</td>
    `;
        tbody.appendChild(tr);
    });

    // weights
    const rows = tbody.querySelectorAll('tr');
    values.forEach((v, i) => {
        const w = (v.val / totalValue * 100).toFixed(1) + '%';
        if (rows[i]) rows[i].cells[7].textContent = w;
    });

    // summary
    const totalPL = totalValue - totalCost;
    const dayPL = totalValue * rand(-0.004, 0.008);
    document.getElementById('portTotal').textContent = '$' + fmtNum(totalValue);
    document.getElementById('portDayPL').textContent = (dayPL >= 0 ? '+$' : '-$') + fmtNum(Math.abs(dayPL));
    document.getElementById('portDayPL').className = 'port-stat-value ' + (dayPL >= 0 ? 'positive' : 'negative');
    document.getElementById('portTotalPL').textContent = (totalPL >= 0 ? '+$' : '-$') + fmtNum(Math.abs(totalPL));
    document.getElementById('portTotalPL').className = 'port-stat-value ' + (totalPL >= 0 ? 'positive' : 'negative');
}

function initAllocationChart() {
    const canvas = document.getElementById('allocationChart');
    if (!canvas || allocationChart_) return;
    const labels = PORTFOLIO.map(h => h.sym);
    const data = PORTFOLIO.map(h => {
        const s = STOCKS[h.sym];
        return (s ? s.price : h.avgCost) * h.shares;
    });
    const COLORS = ['#f5a623', '#00e676', '#ff3d3d', '#4fc3f7', '#ce93d8', '#a5d6a7', '#ef9a9a'];
    allocationChart_ = new Chart(canvas, {
        type: 'doughnut',
        data: { labels, datasets: [{ data, backgroundColor: COLORS, borderWidth: 0 }] },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right', labels: { color: '#888', font: { family: 'JetBrains Mono', size: 10 } } },
                tooltip: { callbacks: { label: ctx => ` ${ctx.label}: $${fmtNum(ctx.raw)}` } },
            },
        },
    });
}

// ─────────────────────────────────────────────────────────────────
// CRYPTO VIEW
// ─────────────────────────────────────────────────────────────────
function initCrypto() {
    renderCryptoTable();
    initFearGreed();
    initDominanceChart();
}

let cryptoPrices = CRYPTOS.map(c => c.price);

function renderCryptoTable() {
    const tbody = document.getElementById('cryptoBody');
    tbody.innerHTML = '';
    CRYPTOS.forEach((c, i) => {
        const p = cryptoPrices[i];
        const pct = rand(-8, 8);
        const up = pct >= 0;
        const tr = document.createElement('tr');
        tr.innerHTML = `
      <td>${c.sym} <span style="color:#555;font-size:9px">${c.name}</span></td>
      <td>$${fmtPrice(p)}</td>
      <td class="${up ? 'positive' : 'negative'}">${pctStr(pct)}</td>
      <td>${c.vol24}</td>
      <td>${c.mcap}</td>
      <td>${c.dom}%</td>
    `;
        tbody.appendChild(tr);
    });
}

function initFearGreed() {
    const canvas = document.getElementById('fearGreedChart');
    if (!canvas) return;
    const value = 72;
    fearGreedChart_ = new Chart(canvas, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: ['#f5a623', '#1a1a1a'],
                borderWidth: 0, circumference: 180, rotation: 270,
            }],
        },
        options: {
            responsive: true, cutout: '75%',
            plugins: { legend: { display: false }, tooltip: { enabled: false } },
        },
    });
    document.getElementById('fgValue').textContent = value;
    document.getElementById('fgLabel').textContent = value >= 80 ? 'EXTREME GREED' : value >= 60 ? 'GREED' : value >= 40 ? 'NEUTRAL' : value >= 20 ? 'FEAR' : 'EXTREME FEAR';
}

function initDominanceChart() {
    const canvas = document.getElementById('dominanceChart');
    if (!canvas) return;
    const labels = CRYPTOS.map(c => c.sym);
    const data = CRYPTOS.map(c => c.dom);
    const COLORS = ['#f5a623', '#516beb', '#9945ff', '#f0a500', '#00a3ff', '#ba9a01', '#0033ad', '#e84142'];
    dominanceChart_ = new Chart(canvas, {
        type: 'bar',
        data: {
            labels,
            datasets: [{ data, backgroundColor: COLORS, borderWidth: 0 }],
        },
        options: {
            responsive: true, indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#555', font: { family: 'JetBrains Mono', size: 9 } }, grid: { color: '#111' } },
                y: { ticks: { color: '#888', font: { family: 'JetBrains Mono', size: 10 } }, grid: { display: false } },
            },
        },
    });
}

// ─────────────────────────────────────────────────────────────────
// FX VIEW
// ─────────────────────────────────────────────────────────────────
function initFX() {
    const grid = document.getElementById('fxGrid');
    grid.innerHTML = '';
    FX_PAIRS.forEach((fx, i) => {
        const div = document.createElement('div');
        div.className = 'fx-card';
        div.id = `fx-${i}`;
        grid.appendChild(div);
    });
    updateFX();
}

function updateFX() {
    FX_PAIRS.forEach((fx, i) => {
        fx.rate += fx.rate * rand(-0.0003, 0.0003);
        const pct = (fx.rate - fx.base) / fx.base * 100;
        const up = pct >= 0;
        const el = document.getElementById(`fx-${i}`);
        if (!el) return;
        const fillW = Math.min(Math.abs(pct) * 20, 100);
        el.innerHTML = `
      <div class="fx-pair">${fx.pair}</div>
      <div class="fx-rate">${fx.rate.toFixed(4)}</div>
      <div class="fx-chg ${up ? 'positive' : 'negative'}">${pctStr(pct)}</div>
      <div class="fx-bar"><div class="fx-bar-fill" style="width:${fillW}%;background:${up ? '#00e676' : '#ff3d3d'}"></div></div>
    `;
    });
}

// ─────────────────────────────────────────────────────────────────
// CHART SYMBOL UPDATE
// ─────────────────────────────────────────────────────────────────
function updateChartSymbol(sym) {
    const stock = STOCKS[sym] || STOCKS['AAPL'];
    const title = `◈ ${sym} — ${stock.name.toUpperCase()}`;
    document.getElementById('chartTitle').textContent = title;
    if (document.getElementById('chartTitle2')) document.getElementById('chartTitle2').textContent = '◈ FULL CHART — ' + sym;

    if (mainChart) { mainChart.destroy(); }
    mainChart = buildChart('mainChart', sym, currentTimeframe, currentChartType);
}

function setTimeframe(tf) {
    currentTimeframe = tf;
    document.querySelectorAll('.tframe').forEach(b => {
        if (['1D', '1W', '1M', '3M'].includes(b.textContent)) b.classList.remove('active');
    });
    document.querySelectorAll('.tframe').forEach(b => {
        if (b.textContent === tf) b.classList.add('active');
    });
    if (mainChart) { mainChart.destroy(); }
    mainChart = buildChart('mainChart', currentSymbol, currentTimeframe, currentChartType);
}

function setChartType(type) {
    currentChartType = type;
    if (mainChart) { mainChart.destroy(); }
    mainChart = buildChart('mainChart', currentSymbol, currentTimeframe, currentChartType);
}

// ─────────────────────────────────────────────────────────────────
// SEARCH
// ─────────────────────────────────────────────────────────────────
function searchSymbol() {
    const val = document.getElementById('symbolSearch').value.toUpperCase().trim();
    if (!val) return;
    if (STOCKS[val]) {
        currentSymbol = val;
        updateChartSymbol(val);
        switchView('dashboard');
    } else {
        const el = document.getElementById('symbolSearch');
        el.style.borderColor = '#ff3d3d';
        setTimeout(() => el.style.borderColor = '', 1000);
    }
    document.getElementById('symbolSearch').value = '';
}

document.getElementById('symbolSearch').addEventListener('keydown', e => {
    if (e.key === 'Enter') searchSymbol();
});

// ─────────────────────────────────────────────────────────────────
// VIEW SWITCHING
// ─────────────────────────────────────────────────────────────────
function switchView(view) {
    currentView = view;
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(`view-${view}`)?.classList.add('active');
    document.querySelectorAll('.fkey').forEach(b => {
        b.classList.toggle('active', b.dataset.view === view);
    });

    // lazy init
    if (view === 'portfolio') { renderHoldings(); initAllocationChart(); }
    if (view === 'crypto') { renderCryptoTable(); }
    if (view === 'fx') { updateFX(); }
    if (view === 'india') { initIndiaWatchlist(); renderIndiaMovers('gainers'); buildIndiaChart(indiaCurrentSymbol, indiaTimeframe); renderSectorHeatmap('indiaSectorHeatmap', SECTOR_DATA['india']); initIndiaNews(); updateIndiaIndices(); }
    if (view === 'charts') {
        if (!fullChart_) {
            fullChart_ = buildChart('fullChart', currentSymbol, currentTimeframe);
        }
    }
}

// keyboard shortcuts F1-F6
document.addEventListener('keydown', e => {
    const views = ['dashboard', 'charts', 'portfolio', 'crypto', 'fx', 'india'];
    if (e.key >= 'F1' && e.key <= 'F6') {
        e.preventDefault();
        switchView(views[parseInt(e.key.slice(1)) - 1]);
    }
});

// ─────────────────────────────────────────────────────────────────
// INDIA INDICES STRIP
// ─────────────────────────────────────────────────────────────────
function updateIndiaIndices() {
    Object.entries(INDIA_INDICES).forEach(([id, idx]) => {
        const old = indiaIdxPrices[id];
        const newP = old + old * rand(-idx.vol, idx.vol);
        indiaIdxPrices[id] = newP;
        const pct = (newP - idx.base) / idx.base * 100;
        const up = pct >= 0;
        const card = document.getElementById(id);
        if (!card) return;
        card.querySelector('.iidx-price').textContent =
            newP >= 1000 ? newP.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : fmtPrice(newP);
        const chgEl = card.querySelector('.iidx-chg');
        chgEl.textContent = pctStr(pct);
        chgEl.className = 'iidx-chg ' + (up ? 'positive' : 'negative');
    });
    // update dashboard strip NIFTY/SENSEX cards too
    ['idx-nifty', 'idx-sensex'].forEach(id => {
        const mapped = id === 'idx-nifty' ? 'iidx-nifty50' : 'iidx-sensex';
        const newP = indiaIdxPrices[mapped];
        if (!newP) return;
        const base = INDIA_INDICES[mapped].base;
        const pct = (newP - base) / base * 100;
        const up = pct >= 0;
        const card = document.getElementById(id);
        if (!card) return;
        card.querySelector('.idx-price').textContent = newP.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const chgEl = card.querySelector('.idx-change');
        chgEl.textContent = pctStr(pct);
        chgEl.className = 'idx-change ' + (up ? 'positive' : 'negative');
    });
}

// ─────────────────────────────────────────────────────────────────
// INDIA WATCHLIST
// ─────────────────────────────────────────────────────────────────
function initIndiaWatchlist() {
    const tbody = document.getElementById('indiaWLBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    Object.entries(INDIA_STOCKS).forEach(([sym, s]) => {
        const pct = (s.price - s.prev) / s.prev * 100;
        const up = pct >= 0;
        const row = document.createElement('tr');
        row.id = `iwl-${sym}`;
        row.onclick = () => { indiaCurrentSymbol = sym; updateIndiaChart(sym); };
        row.innerHTML = `
          <td>${sym}</td>
          <td id="iwl-${sym}-price">₹${fmtPrice(s.price)}</td>
          <td class="${up ? 'positive' : 'negative'}" id="iwl-${sym}-chg">${up ? '+' : '-'}₹${Math.abs(s.price - s.prev).toFixed(2)}</td>
          <td class="${up ? 'positive' : 'negative'}" id="iwl-${sym}-pct">${pctStr(pct)}</td>
          <td>${fmtNum(Math.round(rand(1e5, 5e6)))}K</td>
          <td><canvas class="spark" id="ispark-${sym}"></canvas></td>
        `;
        tbody.appendChild(row);
    });
    Object.entries(INDIA_STOCKS).forEach(([sym, s]) => {
        drawSpark(`ispark-${sym}`, generateSparkData(s));
    });
}

function updateIndiaStockPrices() {
    Object.entries(INDIA_STOCKS).forEach(([sym, s]) => {
        const old = s.price;
        s.price += old * rand(-0.0025, 0.0025);
        s.price = Math.max(s.price, s.prev * 0.7);
        const pct = (s.price - s.prev) / s.prev * 100;
        const up = s.price >= old;
        const row = document.getElementById(`iwl-${sym}`);
        if (row) flashRow(row, up);
        const priceEl = document.getElementById(`iwl-${sym}-price`);
        const chgEl = document.getElementById(`iwl-${sym}-chg`);
        const pctEl = document.getElementById(`iwl-${sym}-pct`);
        if (priceEl) priceEl.textContent = '₹' + fmtPrice(s.price);
        if (chgEl) {
            const diff = s.price - s.prev;
            chgEl.textContent = (diff >= 0 ? '+' : '-') + '₹' + Math.abs(diff).toFixed(2);
            chgEl.className = up ? 'positive' : 'negative';
        }
        if (pctEl) { pctEl.textContent = pctStr(pct); pctEl.className = up ? 'positive' : 'negative'; }
        drawSpark(`ispark-${sym}`, generateSparkData(s));
    });
}

// ─────────────────────────────────────────────────────────────────
// INDIA CHART
// ─────────────────────────────────────────────────────────────────
function buildIndiaChart(sym, tf) {
    const s = INDIA_STOCKS[sym] || INDIA_STOCKS['RELIANCE'];
    const ctx = document.getElementById('indiaChart');
    if (!ctx) return null;
    const configs = {
        '1D': { points: 78, vol: 0.002, fmt: i => { const h = Math.floor(9.25 + i * 6.25 / 78); const m = Math.floor((i * 6.25 * 60 / 78) % 60); return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`; } },
        '1W': { points: 35, vol: 0.01, fmt: i => { const d = new Date(Date.now() - (34 - i) * 86400000); return d.toLocaleDateString('en-IN', { month: 'short', day: '2-digit' }); } },
        '1M': { points: 30, vol: 0.018, fmt: i => { const d = new Date(Date.now() - (29 - i) * 86400000); return d.toLocaleDateString('en-IN', { month: 'short', day: '2-digit' }); } },
    };
    const cfg = configs[tf] || configs['1D'];
    let price = s.price * rand(0.93, 0.97);
    const labels = [], closes = [];
    for (let i = 0; i <= cfg.points; i++) {
        labels.push(cfg.fmt(i));
        price += price * rand(-cfg.vol, cfg.vol) * (Math.random() > 0.52 ? 1.1 : 0.9);
        price = Math.max(price, s.prev * 0.7);
        closes.push(price);
    }
    const isUp = closes[closes.length - 1] >= closes[0];
    const col = isUp ? '#00e676' : '#ff3d3d';
    if (indiaChart_) { indiaChart_.destroy(); indiaChart_ = null; }
    indiaChart_ = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets: [{ data: closes, borderColor: col, backgroundColor: isUp ? 'rgba(0,230,118,0.07)' : 'rgba(255,61,61,0.07)', borderWidth: 1.5, fill: true, tension: 0.3, pointRadius: 0, pointHoverRadius: 4 }] },
        options: {
            responsive: true, maintainAspectRatio: false, animation: { duration: 300 },
            scales: {
                x: { ticks: { color: '#555', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8, maxRotation: 0 }, grid: { color: '#111' }, border: { color: '#222' } },
                y: { position: 'right', ticks: { color: '#888', font: { family: 'JetBrains Mono', size: 9 }, callback: v => '₹' + fmtPrice(v) }, grid: { color: '#111' }, border: { color: '#222' } },
            },
            plugins: { legend: { display: false }, tooltip: { backgroundColor: '#0d0d0d', borderColor: '#ff9933', borderWidth: 1, titleColor: '#ff9933', bodyColor: '#e8e8e8', titleFont: { family: 'JetBrains Mono', size: 10 }, bodyFont: { family: 'JetBrains Mono', size: 10 }, callbacks: { label: ctx => ' ₹' + fmtPrice(ctx.raw) } } },
            interaction: { mode: 'index', intersect: false },
        },
    });
    // stats bar
    const hi = Math.max(...closes), lo = Math.min(...closes);
    const el = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
    el('ics-open', '₹' + fmtPrice(closes[0]));
    el('ics-high', '₹' + fmtPrice(hi));
    el('ics-low', '₹' + fmtPrice(lo));
    el('ics-52h', '₹' + fmtPrice(s.price * rand(1.08, 1.22)));
    el('ics-52l', '₹' + fmtPrice(s.price * rand(0.62, 0.82)));
    el('ics-mcap', s.mcap);
    document.getElementById('indiaChartTitle').textContent = `◈ ${sym} — ${s.name.toUpperCase()}`;
    return indiaChart_;
}

function updateIndiaChart(sym) {
    indiaCurrentSymbol = sym;
    buildIndiaChart(sym, indiaTimeframe);
}
function setIndiaTimeframe(tf) {
    indiaTimeframe = tf;
    document.querySelectorAll('.tframe').forEach(b => {
        if (['1D', '1W', '1M'].includes(b.textContent)) b.classList.remove('active');
    });
    document.querySelectorAll('.tframe').forEach(b => { if (b.textContent === tf) b.classList.add('active'); });
    buildIndiaChart(indiaCurrentSymbol, tf);
}

// ─────────────────────────────────────────────────────────────────
// INDIA MOVERS
// ─────────────────────────────────────────────────────────────────
function switchIndiaMovers(type, btn) {
    currentIndiaMoverTab = type;
    document.querySelectorAll('.imtab').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderIndiaMovers(type);
}
function renderIndiaMovers(type) {
    const c = document.getElementById('indiaMoversContainer');
    if (!c) return;
    c.innerHTML = '';
    INDIA_MOVERS[type].forEach((m, i) => {
        const up = m.pct >= 0;
        const div = document.createElement('div');
        div.className = 'mover-row';
        div.onclick = () => updateIndiaChart(m.sym);
        div.innerHTML = `<div class="mover-rank">#${i + 1}</div><div class="mover-sym">${m.sym}</div><div class="mover-price">₹${fmtPrice(m.price)}</div><div class="mover-pct ${up ? 'positive' : 'negative'}">${pctStr(m.pct)}</div>`;
        c.appendChild(div);
    });
}
function updateIndiaMovers() {
    INDIA_MOVERS.gainers.forEach(m => { m.price += m.price * rand(-0.001, 0.003); m.pct += rand(-0.05, 0.1); });
    INDIA_MOVERS.losers.forEach(m => { m.price += m.price * rand(-0.003, 0.001); m.pct += rand(-0.1, 0.05); });
    renderIndiaMovers(currentIndiaMoverTab);
}

// ─────────────────────────────────────────────────────────────────
// SECTOR HEATMAP
// ─────────────────────────────────────────────────────────────────
let currentSectorView = 'us';
function switchSectorView(view, btn) {
    currentSectorView = view;
    document.querySelectorAll('.stab').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderSectorHeatmap('sectorHeatmap', SECTOR_DATA[view]);
}
function renderSectorHeatmap(containerId, sectors) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = '';
    sectors.forEach(s => {
        const up = s.pct >= 0;
        const intensity = Math.min(Math.abs(s.pct) * 25, 80);
        const bg = up ? `rgba(0,${100 + intensity},${70 + intensity * 0.5},0.85)` : `rgba(${120 + intensity},${20},${20},0.85)`;
        const div = document.createElement('div');
        div.className = 'sector-tile';
        div.style.background = bg;
        div.innerHTML = `<div class="sector-tile-name">${s.name}</div><div class="sector-tile-pct">${up ? '+' : ''}${s.pct.toFixed(2)}%</div><div class="sector-tile-chg">${s.chg}</div>`;
        el.appendChild(div);
    });
}
function updateSectors() {
    ['us', 'india'].forEach(mkt => {
        SECTOR_DATA[mkt].forEach(s => { s.pct += rand(-0.08, 0.08); });
    });
    renderSectorHeatmap('sectorHeatmap', SECTOR_DATA[currentSectorView]);
    renderSectorHeatmap('indiaSectorHeatmap', SECTOR_DATA['india']);
}

// ─────────────────────────────────────────────────────────────────
// INDIA NEWS
// ─────────────────────────────────────────────────────────────────
function initIndiaNews() {
    const feed = document.getElementById('indiaNewsFeed');
    if (!feed) return;
    feed.innerHTML = '';
    INDIA_NEWS.forEach(n => {
        const div = document.createElement('div');
        div.className = 'news-item';
        const tagClass = n.tag === 'bullish' ? 'bullish' : n.tag === 'bearish' ? 'bearish' : '';
        div.innerHTML = `<div style="display:flex;justify-content:space-between"><span class="news-time">TODAY ${n.time} IST</span><span class="news-source">${n.source}</span></div><div class="news-title">${n.title}</div><span class="news-tag ${tagClass}">${(n.tag || 'neutral').toUpperCase()}</span>`;
        feed.appendChild(div);
    });
}

// ─────────────────────────────────────────────────────────────────
// INDIA VIEW INIT
// ─────────────────────────────────────────────────────────────────
let indiaInited = false;
function initIndiaView() {
    if (indiaInited) return;
    indiaInited = true;
    initIndiaWatchlist();
    renderIndiaMovers('gainers');
    buildIndiaChart('RELIANCE', '1D');
    renderSectorHeatmap('indiaSectorHeatmap', SECTOR_DATA['india']);
    initIndiaNews();
    updateIndiaIndices();
}

// ─────────────────────────────────────────────────────────────────
// FOOTER LATENCY SIMULATION
// ─────────────────────────────────────────────────────────────────
function updateFooter() {
    const lat = Math.round(rand(8, 25));
    const el = document.getElementById('footerLatency');
    if (el) el.innerHTML = `LATENCY: <span class="positive">${lat}ms</span>`;
    document.getElementById('updateCount').textContent = ++updateCount;
}

// ─────────────────────────────────────────────────────────────────
// INIT ALL
// ─────────────────────────────────────────────────────────────────
function init() {
    initTicker();
    initIndices();
    initWatchlist();
    mainChart = buildChart('mainChart', 'AAPL', '1D', 'line');
    initMovers();
    initOptions();
    initCalendar();
    initNewsFeed();
    initPortfolio();
    initCrypto();
    initFX();
    renderSectorHeatmap('sectorHeatmap', SECTOR_DATA['us']);
    updateClock();
}

// ─────────────────────────────────────────────────────────────────
// TICK LOOPS
// ─────────────────────────────────────────────────────────────────
init();
setInterval(updateClock, 1000);
setInterval(() => {
    updateStockPrices();
    updateIndices();
    updateFX();
    updateMovers();
    updateFooter();
    liveUpdateChart();
    updateIndiaIndices();
    updateSectors();
    if (currentView === 'india') { updateIndiaStockPrices(); updateIndiaMovers(); }
}, 2000);

setInterval(() => {
    if (currentView === 'portfolio') renderHoldings();
    if (currentView === 'crypto') renderCryptoTable();
}, 10000);
