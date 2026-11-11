import json
from pathlib import Path

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
DB_FILE = SITE_ROOT / "data" / "financial_articles.json"
OUT_HTML = SITE_ROOT / "index.html"

with open(DB_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

lead_art = articles[0]
grid_arts = articles[1:]

grid_cards_html = []
for a in grid_arts:
    card = f"""
    <article class="news-card">
      <div class="card-meta">
        <span class="card-cat">{a['category']}</span>
        <span class="card-date">{a['date']} &bull; {a['reading_time']}</span>
      </div>
      <h3 class="card-title">
        <a href="/articles/{a['slug']}.html">{a['title']}</a>
      </h3>
      <p class="card-summary">{a['summary']}</p>
      <div class="card-footer">
        <a href="/articles/{a['slug']}.html" class="read-link">BACA ANALISIS LENGKAP &rarr;</a>
      </div>
    </article>
    """
    grid_cards_html.append(card)

grid_cards_rendered = "\n".join(grid_cards_html)

HOME_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MANTRA LABS // Jurnal Finansial, Saham, Crypto, dan Makro Geopolitik Global</title>
  <meta name="description" content="Portal berita dan riset mendalam seputar pasar saham, aset kripto, makroekonomi global, korelasi emas dan minyak perang, serta dinamika bilateral negara.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://mantralabs.web.id/">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mantra Labs Financial">
  <meta property="og:url" content="https://mantralabs.web.id/">
  <meta property="og:title" content="MANTRA LABS // Financial News & Macro Intelligence">
  <meta property="og:description" content="Riset mendalam pasar modal, kripto, makroekonomi global, hubungan bilateral negara, dan korelasi komoditas perang.">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg: #030303;
      --bg-card: #080808;
      --border: #1a1a1a;
      --border-accent: #2e2410;
      --amber: #f5a623;
      --amber-soft: rgba(245, 166, 35, 0.08);
      --text: #e6e6e6;
      --text-muted: #888888;
      --positive: #00e676;
      --negative: #ff3d3d;
      --font-body: 'DM Sans', -apple-system, sans-serif;
      --font-head: 'Space Grotesk', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: 15px;
      line-height: 1.6;
      padding: 0;
      margin: 0;
    }}

    /* HEADER */
    header.site-header {{
      background: #000;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .header-inner {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .site-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #fff;
    }}

    .brand-logo {{
      font-family: var(--font-head);
      font-weight: 700;
      font-size: 20px;
      letter-spacing: 1px;
    }}

    .brand-logo span {{
      color: var(--amber);
    }}

    .brand-tag {{
      background: #111;
      border: 1px solid var(--border-accent);
      color: var(--text-muted);
      font-family: var(--font-mono);
      font-size: 10px;
      padding: 2px 6px;
      letter-spacing: 1px;
    }}

    nav.main-nav {{
      display: flex;
      gap: 20px;
    }}

    .nav-link {{
      color: var(--text-muted);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 500;
      transition: color 0.2s;
    }}

    .nav-link:hover, .nav-link.active {{
      color: var(--amber);
    }}

    /* LIVE TICKER STRIP */
    .ticker-bar {{
      background: #060500;
      border-bottom: 1px solid var(--border);
      overflow: hidden;
      display: flex;
      height: 32px;
      align-items: center;
    }}

    .ticker-title {{
      background: #0f0a00;
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      padding: 0 12px;
      height: 100%;
      display: flex;
      align-items: center;
      border-right: 1px solid var(--border-accent);
      flex-shrink: 0;
      letter-spacing: 1px;
    }}

    .ticker-track {{
      overflow: hidden;
      white-space: nowrap;
      flex: 1;
    }}

    .ticker-content {{
      display: inline-block;
      white-space: nowrap;
      animation: tickerRun 90s linear infinite;
      font-family: var(--font-mono);
      font-size: 11px;
      color: #aaa;
      padding-left: 100%;
    }}

    .ticker-content:hover {{
      animation-play-state: paused;
    }}

    @keyframes tickerRun {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-100%); }}
    }}

    /* CONTAINER */
    .container {{
      max-width: 1200px;
      margin: 30px auto 60px;
      padding: 0 20px;
    }}

    /* HERO FEATURED ARTICLE */
    .featured-section {{
      margin-bottom: 40px;
    }}

    .featured-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 32px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: relative;
      transition: border-color 0.2s;
    }}

    .featured-card:hover {{
      border-color: var(--amber);
    }}

    .featured-badge-row {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .badge-label {{
      background: var(--amber);
      color: #000;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      letter-spacing: 1px;
    }}

    .badge-cat {{
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
    }}

    .featured-title {{
      font-family: var(--font-head);
      font-size: 28px;
      line-height: 1.3;
      color: #fff;
    }}

    .featured-title a {{
      color: inherit;
      text-decoration: none;
    }}

    .featured-title a:hover {{
      color: var(--amber);
    }}

    .featured-summary {{
      font-size: 16px;
      color: #bbb;
      line-height: 1.7;
      max-width: 900px;
    }}

    .featured-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid #141414;
      padding-top: 16px;
      margin-top: 8px;
    }}

    .read-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--amber);
      text-decoration: none;
      font-weight: 600;
    }}

    .read-btn:hover {{
      text-decoration: underline;
    }}

    /* GRID ARTICLES */
    .section-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }}

    .section-title {{
      font-family: var(--font-head);
      font-size: 20px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-title::before {{
      content: "";
      width: 4px;
      height: 18px;
      background: var(--amber);
      display: inline-block;
    }}

    .articles-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
    }}

    .news-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: border-color 0.2s;
    }}

    .news-card:hover {{
      border-color: var(--amber);
    }}

    .card-meta {{
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}

    .card-cat {{
      color: var(--amber);
      font-weight: 600;
    }}

    .card-title {{
      font-family: var(--font-head);
      font-size: 19px;
      line-height: 1.4;
      margin-bottom: 12px;
    }}

    .card-title a {{
      color: #fff;
      text-decoration: none;
      transition: color 0.15s;
    }}

    .card-title a:hover {{
      color: var(--amber);
    }}

    .card-summary {{
      font-size: 14px;
      color: #aaa;
      line-height: 1.6;
      margin-bottom: 20px;
      flex-grow: 1;
    }}

    .card-footer {{
      border-top: 1px solid #141414;
      padding-top: 14px;
    }}

    .read-link {{
      color: var(--amber);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}

    .read-link:hover {{
      text-decoration: underline;
    }}

    /* FOOTER */
    footer.site-footer {{
      background: #000;
      border-top: 1px solid var(--border);
      padding: 30px 20px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
    }}

    @media (max-width: 768px) {{
      nav.main-nav {{ display: none; }}
      .featured-title {{ font-size: 22px; }}
      .featured-card {{ padding: 20px; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-brand">
        <span class="brand-logo">MANTRA<span>LABS</span></span>
        <span class="brand-tag">FINANCIAL DISPATCH</span>
      </a>
      <nav class="main-nav">
        <a href="/" class="nav-link active">SEMUA TOPIK</a>
        <a href="/articles/korelasi-emas-dan-minyak-saat-eskalasi-perang-timur-tengah.html" class="nav-link">KOMODITAS & PERANG</a>
        <a href="/articles/dinamika-bilateral-as-china-dan-pergeseran-petrodollar.html" class="nav-link">BILATERAL NEGARA</a>
        <a href="/articles/proyeksi-kebijakan-suku-bunga-the-fed-dan-dampaknya-ke-ihsg.html" class="nav-link">SAHAM & MAKRO</a>
        <a href="/articles/likuiditas-kripto-etf-institusional-dan-siklus-halving-bitcoin.html" class="nav-link">KRIPTO</a>
      </nav>
    </div>
  </header>

  <div class="ticker-bar">
    <div class="ticker-title">LIVE TELEMETRY</div>
    <div class="ticker-track">
      <div class="ticker-content">
        BRENT CRUDE $85.60/bbl ▲  &bull;  WTI CRUDE $81.42/bbl ▲  &bull;  GOLD SPOT $2,318.70/oz ▲  &bull;  SILVER $27.42/oz ▲  &bull;  USD/IDR Rp16,145 ▲  &bull;  IHSG 7,285.40 ▲ +0.55%  &bull;  S&P 500 5,248.49 ▲  &bull;  NASDAQ 18,386.22 ▲  &bull;  BTC/USD $67,840 ▲  &bull;  ETH/USD $3,542 ▲  &bull;  US 10Y YIELD 4.312% ▲  &bull;  FED FUNDS RATE: 5.25-5.50% HOLD  &bull;  RMB OIL SHARE: 41% IN MIDDLE EAST-CHINA TRADE &bull; 
      </div>
    </div>
  </div>

  <main class="container">
    
    <!-- FEATURED ARTICLE -->
    <section class="featured-section">
      <div class="featured-card">
        <div class="featured-badge-row">
          <span class="badge-label">{lead_art['badge']}</span>
          <span class="badge-cat">{lead_art['category']}</span>
        </div>
        <h2 class="featured-title">
          <a href="/articles/{lead_art['slug']}.html">{lead_art['title']}</a>
        </h2>
        <p class="featured-summary">{lead_art['summary']}</p>
        <div class="featured-footer">
          <span>Diterbitkan: {lead_art['date']} &bull; {lead_art['reading_time']}</span>
          <a href="/articles/{lead_art['slug']}.html" class="read-btn">BACA ANALISIS LENGKAP &rarr;</a>
        </div>
      </div>
    </section>

    <!-- ARTICLES GRID -->
    <section>
      <div class="section-head">
        <h3 class="section-title">LAPORAN TERBARU &bull; RISET MAKRO & KEBIJAKAN EKONOMI</h3>
        <span style="font-family:var(--font-mono);font-size:12px;color:var(--text-muted);">{len(articles)} ARTIKEL RISET TERSEDIA</span>
      </div>

      <div class="articles-grid">
        {grid_cards_rendered}
      </div>
    </section>

  </main>

  <footer class="site-footer">
    MANTRA LABS FINANCIAL INTELLIGENCE &bull; JURNAL RISET PASAR MODAL, KOMODITAS, KRIPTO, DAN MAKROEKONOMI GLOBAL &bull; 2026
  </footer>

</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HOME_PAGE_HTML)

print(f"Written new financial news portal homepage to {OUT_HTML}!")
