import json
from pathlib import Path

SITE_ROOT = Path(r"D:\PORTFOLIO_NEO_BRUTALISM")
ARTICLES_DIR = SITE_ROOT / "articles"
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = SITE_ROOT / "data" / "financial_articles.json"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"

with open(DB_FILE, "r", encoding="utf-8") as f:
    total_articles = json.load(f)

print(f"Loaded {len(total_articles)} articles with assigned images.")

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | MANTRA LABS FINANCIAL INTELLIGENCE</title>
  <meta name="description" content="{summary}">
  <meta name="author" content="Mantra Labs Macroeconomic Desk">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://mantralabs.web.id/articles/{slug}.html">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Mantra Labs Financial">
  <meta property="og:url" content="https://mantralabs.web.id/articles/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{summary}">
  <meta property="og:image" content="{image_url}">
  <meta property="article:published_time" content="{iso_date}">
  <meta property="article:section" content="{category}">

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
      --amber-soft: rgba(245, 166, 35, 0.1);
      --text: #e6e6e6;
      --text-muted: #888888;
      --positive: #00e676;
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
      line-height: 1.7;
      padding: 0;
      margin: 0;
    }}

    .top-nav {{
      border-bottom: 1px solid var(--border);
      background: #000000;
      padding: 14px 24px;
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .brand-link {{
      text-decoration: none;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-head);
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 0.5px;
    }}

    .brand-link:hover .back-tag {{
      background: var(--amber);
      color: #000;
    }}

    .back-tag {{
      background: #111;
      border: 1px solid var(--border-accent);
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 8px;
      letter-spacing: 1px;
      transition: all 0.2s;
    }}

    .cat-badge {{
      background: var(--amber-soft);
      border: 1px solid var(--amber);
      color: var(--amber);
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 8px;
      letter-spacing: 1px;
      font-weight: 600;
    }}

    .article-wrap {{
      max-width: 840px;
      margin: 40px auto 80px;
      padding: 0 20px;
    }}

    .article-header {{
      margin-bottom: 32px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }}

    .meta-line {{
      display: flex;
      gap: 16px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}

    .meta-line span b {{
      color: var(--amber);
    }}

    h1 {{
      font-family: var(--font-head);
      font-size: 32px;
      line-height: 1.25;
      color: #ffffff;
      margin-bottom: 20px;
      letter-spacing: -0.5px;
    }}

    .lead-summary {{
      font-size: 17px;
      line-height: 1.6;
      color: #d0d0d0;
      background: #0a0800;
      border-left: 3px solid var(--amber);
      padding: 16px 20px;
    }}

    .article-hero-img {{
      margin-top: 24px;
      border: 1px solid var(--border);
      overflow: hidden;
      max-height: 420px;
      background: #050505;
    }}

    .article-hero-img img {{
      width: 100%;
      height: 420px;
      object-fit: cover;
      display: block;
    }}

    .article-body {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 36px 32px;
    }}

    .article-body h2 {{
      font-family: var(--font-head);
      font-size: 20px;
      color: var(--amber);
      margin: 32px 0 14px;
      padding-bottom: 8px;
      border-bottom: 1px solid #161616;
    }}

    .article-body h2:first-child {{
      margin-top: 0;
    }}

    .article-body p {{
      margin-bottom: 18px;
      color: #cccccc;
      font-size: 16px;
      line-height: 1.75;
    }}

    .bottom-actions {{
      margin-top: 36px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .action-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #000;
      border: 1px solid var(--border-accent);
      color: var(--amber);
      padding: 10px 18px;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
    }}

    .action-btn:hover {{
      background: var(--amber);
      color: #000;
    }}

    footer {{
      border-top: 1px solid var(--border);
      padding: 24px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
      background: #000;
    }}

    @media (max-width: 640px) {{
      h1 {{ font-size: 24px; }}
      .article-body {{ padding: 24px 18px; }}
      .article-hero-img img {{ height: 240px; }}
    }}
  </style>
</head>
<body>

  <header class="top-nav">
    <a href="/" class="brand-link">
      <span class="back-tag">&larr; NEWS DESK</span>
      <span>MANTRA LABS // FINANCIAL</span>
    </a>
    <span class="cat-badge">{badge}</span>
  </header>

  <main class="article-wrap">
    <article class="article-header">
      <div class="meta-line">
        <span>SECTOR: <b>{category}</b></span>
        <span>DATE: <b>{date}</b></span>
        <span>READ: <b>{reading_time}</b></span>
      </div>
      <h1>{title}</h1>
      <p class="lead-summary">{summary}</p>
      <div class="article-hero-img">
        <img src="{image_url}" alt="{title}" loading="lazy">
      </div>
    </article>

    <div class="article-body">
      {body_html}

      <div class="bottom-actions">
        <a href="/" class="action-btn">&larr; BACK TO EDITORIAL HOMEPAGE</a>
        <a href="#top" class="action-btn">RETURN TO TOP &uarr;</a>
      </div>
    </div>
  </main>

  <footer>
    MANTRA LABS FINANCIAL DISPATCH &bull; QUANTITATIVE MACRO, COMMODITIES, DIGITAL ASSETS & STRATEGIC DIPLOMACY &bull; ALL RIGHTS RESERVED
  </footer>

</body>
</html>
"""

for art in total_articles:
    body_parts = []
    for blk in art["content_blocks"]:
        body_parts.append(f"<h2>{blk['subheading']}</h2>")
        for p in blk["paragraphs"]:
            body_parts.append(f"<p>{p}</p>")
    body_html = "\n      ".join(body_parts)
    
    page_html = ARTICLE_TEMPLATE.format(
        title=art["title"],
        summary=art["summary"],
        slug=art["slug"],
        iso_date=art["iso_date"],
        category=art["category"],
        badge=art["badge"],
        date=art["date"],
        reading_time=art["reading_time"],
        image_url=art["image_url"],
        body_html=body_html
    )
    out_file = ARTICLES_DIR / f"{art['slug']}.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)

print("Generated all standalone article pages with distinct images.")

# Render Homepage
lead_art = total_articles[0]
grid_arts = total_articles[1:]
grid_cards_html = []

for a in grid_arts:
    card = f"""
    <article class="news-card">
      <div class="card-thumb">
        <img src="{a['image_url']}" alt="{a['title']}" loading="lazy">
      </div>
      <div class="card-meta">
        <span class="card-cat">{a['category']}</span>
        <span class="card-date">{a['date']} &bull; {a['reading_time']}</span>
      </div>
      <h3 class="card-title">
        <a href="/articles/{a['slug']}.html">{a['title']}</a>
      </h3>
      <p class="card-summary">{a['summary']}</p>
      <div class="card-footer">
        <a href="/articles/{a['slug']}.html" class="read-link">READ FULL DISPATCH &rarr;</a>
      </div>
    </article>
    """
    grid_cards_html.append(card)

grid_cards_rendered = "\n".join(grid_cards_html)

HOME_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MANTRA LABS // Financial News, Equities, Crypto & Global Geopolitics</title>
  <meta name="description" content="Institutional financial intelligence covering equities, digital assets, energy supply chains, gold and oil wartime dynamics, and bilateral economic statecraft.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://mantralabs.web.id/">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mantra Labs Financial">
  <meta property="og:url" content="https://mantralabs.web.id/">
  <meta property="og:title" content="MANTRA LABS // Financial News & Global Macro Intelligence">
  <meta property="og:description" content="Deep-dive institutional analysis on capital markets, commodities, crypto, bilateral trade policies, and AI infrastructure.">
  <meta property="og:image" content="{lead_art['image_url']}">

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
      --text: #e6e6e6;
      --text-muted: #888888;
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

    .container {{
      max-width: 1200px;
      margin: 30px auto 60px;
      padding: 0 20px;
    }}

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

    .featured-hero-img {{
      border: 1px solid var(--border);
      overflow: hidden;
      max-height: 380px;
      margin: 4px 0 8px;
    }}

    .featured-hero-img img {{
      width: 100%;
      height: 380px;
      object-fit: cover;
      display: block;
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

    .card-thumb {{
      margin: -24px -24px 16px -24px;
      overflow: hidden;
      height: 175px;
      border-bottom: 1px solid var(--border);
      background: #050505;
    }}

    .card-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.3s;
    }}

    .news-card:hover .card-thumb img {{
      transform: scale(1.03);
    }}

    .card-meta {{
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 6px;
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
      .featured-hero-img img {{ height: 220px; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-brand">
        <span class="brand-logo">MANTRA<span>LABS</span></span>
        <span class="brand-tag">GLOBAL DISPATCH</span>
      </a>
      <nav class="main-nav">
        <a href="/" class="nav-link active">ALL DISPATCHES</a>
        <a href="/articles/gold-oil-middle-east-war-risk-transmission-macro-assets.html" class="nav-link">COMMODITIES & WAR</a>
        <a href="/articles/ai-hyperscaler-capex-supercycle-semiconductors-energy-limits.html" class="nav-link">AI & TECH</a>
        <a href="/articles/us-china-bilateral-dynamics-petrodollar-erosion-trade.html" class="nav-link">BILATERAL MACRO</a>
        <a href="/articles/federal-reserve-interest-rates-emerging-market-equity-valuations.html" class="nav-link">EQUITIES</a>
        <a href="/articles/bitcoin-etf-institutional-liquidity-supply-halving-dynamics.html" class="nav-link">DIGITAL ASSETS</a>
      </nav>
    </div>
  </header>

  <div class="ticker-bar">
    <div class="ticker-title">LIVE TELEMETRY</div>
    <div class="ticker-track">
      <div class="ticker-content">
        BRENT CRUDE $85.60/bbl ▲  &bull;  WTI CRUDE $81.42/bbl ▲  &bull;  GOLD SPOT $2,318.70/oz ▲  &bull;  NVDA $875.30 ▲  &bull;  AI CAPEX SPEND: $200B+ RUN-RATE ▲  &bull;  TSMC WAFER UTILIZATION: 98.4% ▲  &bull;  USD/IDR Rp16,145 ▲  &bull;  IHSG 7,285.40 ▲ +0.55%  &bull;  S&P 500 5,248.49 ▲  &bull;  NASDAQ 18,386.22 ▲  &bull;  BTC/USD $67,840 ▲  &bull;  ETH/USD $3,542 ▲  &bull;  US 10Y YIELD 4.312% ▲  &bull;  FED FUNDS RATE: 5.25-5.50% HOLD  &bull;  RMB OIL SHARE: 41% IN MIDDLE EAST-CHINA TRADE &bull; 
      </div>
    </div>
  </div>

  <main class="container">
    
    <section class="featured-section">
      <div class="featured-card">
        <div class="featured-badge-row">
          <span class="badge-label">{lead_art['badge']}</span>
          <span class="badge-cat">{lead_art['category']}</span>
        </div>
        <div class="featured-hero-img">
          <img src="{lead_art['image_url']}" alt="{lead_art['title']}" loading="lazy">
        </div>
        <h2 class="featured-title">
          <a href="/articles/{lead_art['slug']}.html">{lead_art['title']}</a>
        </h2>
        <p class="featured-summary">{lead_art['summary']}</p>
        <div class="featured-footer">
          <span>Published: {lead_art['date']} &bull; {lead_art['reading_time']}</span>
          <a href="/articles/{lead_art['slug']}.html" class="read-btn">READ COMPLETE ANALYSIS &rarr;</a>
        </div>
      </div>
    </section>

    <section>
      <div class="section-head">
        <h3 class="section-title">LATEST INTELLIGENCE DISPATCHES</h3>
        <span style="font-family:var(--font-mono);font-size:12px;color:var(--text-muted);">{len(total_articles)} RESEARCH DISPATCHES AVAILABLE</span>
      </div>

      <div class="articles-grid">
        {grid_cards_rendered}
      </div>
    </section>

  </main>

  <footer class="site-footer">
    MANTRA LABS FINANCIAL INTELLIGENCE &bull; INSTITUTIONAL MACRO, COMMODITIES, DIGITAL ASSETS & STRATEGIC DIPLOMACY &bull; 2026
  </footer>

</body>
</html>
"""

with open(SITE_ROOT / "index.html", "w", encoding="utf-8") as f:
    f.write(HOME_PAGE_HTML)

print("Rebuilt index.html with distinct card thumbnails!")
